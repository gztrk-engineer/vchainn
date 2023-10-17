from backend.util.crypto_hash import cryptoHash

def testCryptoHash():
    # It should create the same hash with arguments of differetn data types
    # in any order
    assert cryptoHash(1, [2], 'three') == cryptoHash('three', 1, [2])
    assert cryptoHash('foo') == 'b2213295d564916f89a6a42455567c87c3f480fcd7a1c15e220f17d7169a790b'