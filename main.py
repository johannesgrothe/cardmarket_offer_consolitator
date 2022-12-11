import argparse
import enum
import logging
import sys
from typing import Tuple

from cardmarket_loader import CardmarketLoader, DataLoadError, ExpansionError, ProductError
from file_loader import FileLoader
from offer import Offer
from order_finder import OrderFinder
from search_settings import SearchSettings
from settings_loader import SettingsLoader
from utils.animated_loading_indicator import AnimatedLoadingIndicator
from utils.updated_loading_indicator import UpdatedLoadingIndicator

_indicator_size = 4


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="CLI to get and group offers from cardmarket.com to get the lowest combined price")
    parser.add_argument("--file", "-f", type=str, required=True, help="File to load the card identifiers from")
    parser.add_argument("--config", "-c", type=str, help="File to configure the filter parameters")
    parser.add_argument("--verbose", "-v", action="store_true", help="Activates debug output")
    parser.add_argument("--non_interactive", action="store_true",
                        help="Always answers questions posed to the user with 'yes, continue'")
    args = parser.parse_args()
    return args


def format_amount(number: int) -> str:
    number_names = {
        3: "thousand",
        6: "million",
        9: "billion",
        12: "trillion",
        15: "quadrillion",
        18: "quintillion",
        21: "sextillion",
        24: "septillion",
        27: "octillion"
    }

    base_nr = ((len(str(number)) - 1) // 3) * 3
    if base_nr < 3:
        return str(base_nr)
    if base_nr > 27:
        return f"over 10^{base_nr}"
    buf_number = number // (10 ** base_nr)
    type_str = number_names.get(base_nr)
    if type_str is None:
        type_str = ""
    else:
        type_str = " " + type_str

    return f"{buf_number}{type_str} (10^{base_nr}) "


def ask_for_continue(message: str) -> bool:
    """Asks the user if he wishes to continue."""
    while True:
        print(f"{message} [y/n]")
        res = input().strip().lower()
        if res == "y":
            return True
        elif res == "n":
            return False
        print("Illegal Input, please try again.")


def log_error(msg: str):
    print(f"[x] {msg}")


def format_price(price: float):
    out = str(round(price, 2))
    if len(out.split(".")[1]) < 2:
        out += "0"
    return out


def format_list_out(data: list[enum.Enum]):
    return ', '.join([x.name for x in data])


def main():
    args = parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.CRITICAL)

    if not args.config:
        config = SearchSettings()
    else:
        with AnimatedLoadingIndicator(size=3, message=f"Loading Search Parameters from {args.config}"):
            config = SettingsLoader.load_settings(args.config)
        print(f"[✓] Config with {len(config)} Options loaded. Searching for offers with:")
        if config.language:
            print(f"    Language: {format_list_out(config.language)}")
        if config.min_condition:
            print(f"    Minimal Condition: {config.min_condition.name}")
        if config.seller_type:
            print(f"    Seller Type: {format_list_out(config.seller_type)}")
        if config.seller_country:
            print(f"    Seller Country: {format_list_out(config.seller_country)}")
        print()

    with AnimatedLoadingIndicator(size=3, message=f"Loading Cards from {args.file}"):
        loader = FileLoader(args.file, log_error)
        cards = loader.cards
    print(f"[✓] {len(cards)} different Cards loaded from File, {sum([x.amount for x in cards])} in total.")
    if loader.double_cards or loader.illegal_identifiers and not args.non_interactive:
        if not ask_for_continue(f"[!] The file contained {loader.illegal_identifiers} illegal identifiers "
                                f"and {loader.double_cards} double cards. Continue anyway?"):
            sys.exit(1)
    print()

    c_loader = CardmarketLoader(config)

    all_offers = {}
    load_errs = 0
    exp_errs = 0
    product_errs = 0
    for card in cards:
        try:
            with AnimatedLoadingIndicator(size=_indicator_size, message=f"Loading offers for {card.name}..."):
                card_offers = c_loader.load_offers_for_card(card)
                card_offers.sort()
            all_offers[card] = card_offers
            min_price = min([x.price for x in card_offers])
            max_price = max([x.price for x in card_offers])
            print(f"[✓] {len(card_offers)} offers fetched between {format_price(min_price)}€ and "
                  f"{format_price(max_price)}€ for {card.name}", " " * (10 + len(str(card.name))))
        except DataLoadError as err:
            print(f"[x] Data could not be loaded, server responded with code {err.code}")
            load_errs += 1
        except ExpansionError as err:
            print(f"[x] '{err.args[0]}' is no legal expansion")
            exp_errs += 1
        except ProductError as err:
            print(f"[x] Card '{card.name}' does not exist in '{err.args[0]}'")
            product_errs += 1
    total_offers = sum([len(x) for y, x in all_offers.items()])
    legal_cards = len(all_offers.keys())
    print(f"[i] {total_offers} total offers collected for {legal_cards} cards")

    print()
    order_finder = OrderFinder(all_offers)
    indicator = UpdatedLoadingIndicator(order_finder.total_checks, lambda: order_finder.performed_checks, precision=1,
                                        message="Searching for lowest combination of sellers...")
    with indicator:
        cheapest_combination = order_finder.find_lowest_offer()

    sellers = cheapest_combination.sellers
    sellers.sort()

    print(f"[i] {format_amount(order_finder.total_checks)} combinations have been checked.")
    print()
    print("Cheapest possible combination found:" + " " * 60)
    for seller in sellers:
        offers: list[Tuple[Offer, int]] = []
        for offer_set in cheapest_combination.offer_sets:
            for offer in offer_set.offers:
                if offer.seller == seller:
                    offers.append((offer, offer_set.get_amount_for_offer(offer)))
        total = format_price(seller.shipping + sum([offer.price * amount for offer, amount in offers]))
        print(f"{seller.name} ({format_price(seller.shipping)}€ Shipping, {total} total):")
        offers.sort()
        for offer, amount in offers:
            print(f"    {offer.expansion} // {offer.card.name} - {format_price(offer.price)}€ "
                  f"x {amount} ({offer.amount} available)")
        print()

    print(f"Total: {format_price(cheapest_combination.sum())}€")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("[i] Script terminated by user.")
