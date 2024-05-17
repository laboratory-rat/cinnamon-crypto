from enum import StrEnum, auto


class CoinTagType(StrEnum):
    """
    Coin tag type
    """
    STABLE = auto()
    POW = auto()
    MEME = auto()
    SOLANA = auto()
    LAYER_1 = auto()
    LAYER_2 = auto()


