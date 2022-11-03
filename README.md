# CardmarketLoader

This project allows you, automatically search for the lowest combined offer for as many cards as you wish.

## How to use

### Card-File

The file containing the card identifiers is a plain text file, containing one card id per line.
This could look like this:

```
Theros-Beyond-Death-Extras/Goat-Token-White-01
Commander-Legends-Battle-for-Baldurs-Gate-Extras/Copy-Token
Amonkhet/Warrior-Token-White-11-Vigilance
```

If you want a boilerplate-file to copy, see `test_assets/test_cards.txt`

### Settings-File

The file containing the search parameters is encoded as JSON.
The structure is as follows:

```json
{
  "language": [
    1,
    3
  ],
  "seller_type": [
    0,
    2
  ],
  "seller_country": 7,
  "min_condition": 5
}
```

See `card_attributes.py` to find out, which numbers translate to which value.
If you want a boilerplate-file to copy, see `test_assets/test_settings.json`

### Starting the program

The script is executed using the following command:
`python main.py --file <path_to_card_file>`

You can also add `--config <path_to_config_file>` to load a config file and apply its settings.

To see all other arguments, use `-h` for help.