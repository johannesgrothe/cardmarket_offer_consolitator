import argparse
import logging
import sys
import json

from card_attributes import Language, CardCondition, SellerType, SellerCountry
from cardmarket_loader import CardmarketLoader, DataLoadError, ExpansionError, ProductError
from file_loader import FileLoader
from order_finder import OrderFinder


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="CLI to get and group offers from cardmarket.com to get the lowest combined price")
    parser.add_argument("--file", "-f", type=str, required=True, help="File to load the card identifiers from")
    parser.add_argument("--config", "-c", type=str, required=True, help="File to configure the filter parameters")
    parser.add_argument("--verbose", "-v", action="store_true", help="Activates debug output")
    parser.add_argument("--non_interactive", action="store_true",
                        help="Always answers questions posed to the user with 'yes, continue'")
    args = parser.parse_args()
    return args


def load_config(path: str) -> dict:
    with open(path, "r") as file_p:
        return json.load(file_p)


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


def main():
    args = parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.CRITICAL)
    print(f"[i] Loading Cards from {args.file}")
    loader = FileLoader(args.file, log_error)
    cards = loader.cards
    print(f"[✓] {len(cards)} Cards loaded from File")
    if loader.double_cards or loader.illegal_identifiers and not args.non_interactive:
        if not ask_for_continue(f"[!] The file contained {loader.illegal_identifiers} illegal identifiers "
                                f"and {loader.double_cards} double cards. Continue anyway?"):
            sys.exit(1)

    config = load_config(args.config)

    language = config["language"]
    if language is not None:
        language = Language(language)

    min_condition = config["min_condition"]
    if min_condition is not None:
        min_condition = CardCondition(language)

    seller_type = config["seller_type"]
    if seller_type is not None:
        seller_type = SellerType(seller_type)

    seller_country = config["seller_country"]
    if seller_country is not None:
        seller_country = SellerCountry(seller_country)

    c_loader = CardmarketLoader(language,
                                min_condition,
                                seller_country,
                                seller_type)

    print()
    print("Loading Cards with:")
    if language:
        print(f"    Language: {language.name}")
    if min_condition:
        print(f"    Minimal Condition: {min_condition.name}")
    if seller_type:
        print(f"    Seller Type: {seller_type.name}")
    if seller_country:
        print(f"    Seller Country: {seller_country.name}")
    print()

    all_offers = {}
    load_errs = 0
    exp_errs = 0
    product_errs = 0
    for card in cards:
        print(f"[i] Loading offers for {card}...")
        try:
            card_offers = c_loader.load_offers_for_card(card)
            card_offers.sort()
            all_offers[card] = card_offers
            min_price = min([x.price for x in card_offers])
            max_price = max([x.price for x in card_offers])
            print(f"[✓] {len(card_offers)} offers fetched between {min_price}€ and {max_price}€")
        except DataLoadError as err:
            print(f"[x] Data could not be loaded, server responded with code {err.code}")
            load_errs += 1
        except ExpansionError:
            print(f"[x] '{card.expansion}' is no legal expansion")
            exp_errs += 1
        except ProductError:
            print(f"[x] Card '{card.name}' does not exist in '{card.expansion}'")
            product_errs += 1
    total_offers = sum([len(x) for y, x in all_offers.items()])
    legal_cards = len(all_offers.keys())
    print(f"[✓] {total_offers} total offers collected for {legal_cards} cards")

    cheapest_combination = OrderFinder(all_offers).find_lowest_offer()

    sellers = cheapest_combination.sellers
    sellers.sort()

    print()
    for seller in sellers:
        print()
        print(f"{seller.name} ({seller.shipping}€ Shipping):")
        offers = [x for x in cheapest_combination.offers if x.seller == seller]
        offers.sort()
        for offer in offers:
            print(f"    {str(offer.card)} - {offer.price}€")
        print()

    print(f"Total: {cheapest_combination.sum()}€")


if __name__ == '__main__':
    main()
    # card1 = Card("test1", "testcard1")
    # card2 = Card("test2", "testcard2")
    # all_offers = {card1: [Offer(card1, Seller("seller1", 1.15), 3, 0.13),
    #                       Offer(card1, Seller("seller2", 1.15), 1, 0.20),
    #                       Offer(card1, Seller("seller3", 1.15), 1, 0.34)],
    #               card2: [Offer(card2, Seller("seller4", 1.15), 2, 0.02),
    #                       Offer(card2, Seller("seller2", 1.15), 2, 0.05),
    #                       Offer(card2, Seller("seller5", 1.15), 4, 0.18),
    #                       # Offer(card2, Seller("seller1", 1.15), 4, 0.18),
    #                       Offer(card2, Seller("seller6", 1.15), 1, 0.26)]
    #               }
    # print({str(a): [str(x) for x in b] for a, b in all_offers.items()})
    # lowest = OrderFinder(all_offers).find_lowest_offer()
    # print(lowest)
    # print(lowest.sum())
