import argparse
import logging

from file_loader import FileLoader


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="CLI to get and group offers from cardmarket.com to get the lowest combined price")
    parser.add_argument("--file", "-f", type=str, required=True, help="File to load the card identifiers from")
    parser.add_argument("--verbose", "-v", action="store_true", help="Activates debug output")
    args = parser.parse_args()
    return args


def log_error(msg: str):
    print(f"[x] {msg}")


def main():
    args = parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    loader = FileLoader(args.file, log_error)
    print(f"[i] Loading Cards from {loader.file}")
    cards = loader.parse()
    print(f"[✓] {len(cards)} Cards loaded from File")


if __name__ == '__main__':
    main()
