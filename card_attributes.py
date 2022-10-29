import enum


class CardCondition(enum.IntEnum):
    Mint = 1
    NearMint = 2
    Excellent = 3
    Good = 4
    LightlyPlayed = 5
    Played = 6
    Poor = 7


class SellerCountry(enum.IntEnum):
    Germany = 7


class SellerType(enum.IntEnum):
    Private = 0
    Commercial = 1
    PowerSeller = 2


class Language(enum.IntEnum):
    English = 1
    German = 3
