import argparse
import logging
import sys

from cardmarket_loader import CardmarketLoader, DataLoadError, ExpansionError, ProductError
from file_loader import FileLoader


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
    offers = {}
    load_errs = 0
    exp_errs = 0
    product_errs = 0
    for card in cards:
        print(f"[i] Loading offers for {card}...")
        try:
            card_offers = c_loader.load_offers_for_card(card)
            offers[card] = card_offers
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
            print(f"[x] Card '{card.name}' does not exist in '{card.expansion}")
            product_errs += 1
    total_offers = sum([len(x) for y, x in offers.items()])
    legal_cards = len(offers.keys())
    print(f"[✓] {total_offers} total offers collected for {legal_cards} cards")


if __name__ == '__main__':
    main()
