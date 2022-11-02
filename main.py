import argparse
import logging
import sys
from typing import Dict

from card import Card
from cardmarket_loader import CardmarketLoader, DataLoadError, ExpansionError, ProductError
from file_loader import FileLoader
from offer import Offer
from order_finder import OrderFinder


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="CLI to get and group offers from cardmarket.com to get the lowest combined price")
    parser.add_argument("--file", "-f", type=str, required=True, help="File to load the card identifiers from")
    parser.add_argument("--verbose", "-v", action="store_true", help="Activates debug output")
    parser.add_argument("--non_interactive", action="store_true",
                        help="Always answers questions posed to the user with 'yes, continue'")
    args = parser.parse_args()
    return args


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

    c_loader = CardmarketLoader()
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

    OrderFinder.find_lowest_offer(all_offers)

    # cheapest_combination: Dict[Card, Offer] = {}
    # for _ in all_offers:
    #     for card, offers in all_offers:
    #         all_sellers = [x.seller for x in cheapest_combination.items()]
    #         lowest_offer: offers[0]


if __name__ == '__main__':
    # main()
    card1 = Card("test1", "testcard1")
    card2 = Card("test2", "testcard2")
    all_offers = {card1: [Offer(card1, "seller1", 3, 0.13),
                          Offer(card1, "seller2", 1, 0.20),
                          Offer(card1, "seller3", 1, 0.34)],
                  card2: [Offer(card2, "seller11", 2, 0.02),
                          Offer(card2, "seller12", 2, 0.05),
                          Offer(card2, "seller13", 4, 0.18),
                          Offer(card2, "seller2", 1, 0.26)]
                  }
    print({str(a): [str(x) for x in b] for a, b in all_offers.items()})
    lowest = OrderFinder(all_offers).find_lowest_offer()
    print(lowest)
    print(lowest.sum())
