import pytest 

from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA

def test_blockchain_instance():
    blockchain = Blockchain()

    assert blockchain.chain[0].hash == GENESIS_DATA['hash']

def testAddBlock():
    blockchain = Blockchain()
    data = 'test-data'
    blockchain.addBlock(data)

    assert blockchain.chain[-1].data == data

@pytest.fixture
def blockchain3Blocks():
    blockchain = Blockchain()
    for i in range(3):
        blockchain.addBlock(i)
    return blockchain


def testIsValidChain(blockchain3Blocks):
    # blockchain = Blockchain()
    # for i in range(3):
    #     blockchain.addBlock(i)
    # print(blockchain.chain[0])    
    # Blockchain.isValidChain(blockchain.chain)
    Blockchain.isValidChain(blockchain3Blocks.chain)

def testIsValidChainBadGenesis(blockchain3Blocks):
    blockchain3Blocks.chain[0].hash = "evil_hash"
    with pytest.raises(Exception, match="The genesis block must be valid!"):
        Blockchain.isValidChain(blockchain3Blocks.chain)

