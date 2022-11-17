from cardmarket_loader import CardmarketLoader
from search_settings import SearchSettings


def main():
    loader = CardmarketLoader(SearchSettings())
    while True:
        search_string = input("Enter Search String: ").strip().strip("\n").strip()
        result = loader.find_expansion(search_string)
        print(f"Expansion IDs for '{search_string}'")
        for expansion in result:
            print(f"    {expansion}")
        print()


if __name__ == "__main__":
    main()
