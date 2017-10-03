import os

CLIENT_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'app')

# TODO duplicated default ports, adapt to elements (with CA),
# uncomment, clean up
AVAILABLE_CHAINS = {
    "bitcoin": "bitcoin:8532",
    "testnet3": "bitcoin:18532",
    "elementsregtest": "elements:7041",
    # "elements": "elements:9042",
}

ALLOWED_CALLS = [
    "getblockchaininfo",
    "getblock",
    "getblockhash",
    "getrawtransaction",
    "getblockstats",
    "getmempoolinfo",
    "getrawmempool",
    "getmempoolentry",
]

RESOURCES_FOR_GET_BY_ID = [
    'block',
    'tx',
    'blockstats',
]