from src.domain.enum.coin_tag_type import CoinTagType

coins_to_seed = [
    {
        'name': 'Tether',
        'symbol': 'USDT',
        'tags': [
            CoinTagType.STABLE,
        ],
    },
    {
        'name': 'Bitcoin',
        'symbol': 'BTC',
        'tags': [
            CoinTagType.POW,
        ]
    },
    {
        'name': 'Ethereum',
        'symbol': 'ETH',
        'tags': [
            CoinTagType.POW,
            CoinTagType.LAYER_1,
        ]
    },
    {
        'name': 'Ripple',
        'symbol': 'XRP',
        'tags': [
            CoinTagType.LAYER_1,
        ]
    },
    {
        'name': 'Solana',
        'symbol': 'SOL',
        'tags': [
            CoinTagType.SOLANA,
            CoinTagType.LAYER_1,
        ]
    },
    {
        'name': 'Pepe',
        'symbol': 'PEPE',
        'tags': [
            CoinTagType.MEME,
        ]
    },
    {
        'name': 'Standard Tokenization Protocol',
        'symbol': 'STPT',
        'tags': [],
    }
]