import pytest
import time

from backend.blockchain.block import Block, GENESIS_DATA
from backend.config import MINE_RATE, SECONDS
from backend.util.hex2bin import hexToBinary

def testMineBlock():
    lastBlock = Block.genesis()
    data = 'test-data'
    block = Block.mineBlock(lastBlock, data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.lastHash == lastBlock.hash
    assert hexToBinary(block.hash)[0:block.difficulty] == '0' * block.difficulty

def testGenesis():
    genesis = Block.genesis()

    assert isinstance(genesis, Block)
    for key, value in GENESIS_DATA.items():
        getattr(genesis, key) == value

def testQuicklyMinedBlock():
    lastBlock = Block.mineBlock(Block.genesis(), 'foo')
    minedBlock = Block.mineBlock(lastBlock, 'bar')

    assert minedBlock.difficulty == lastBlock.difficulty + 1

def test_slowly_mined_block():
    last_block = Block.mineBlock(Block.genesis(), 'foo')
    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mineBlock(last_block, 'bar')

    assert mined_block.difficulty == last_block.difficulty - 1

def test_mined_block_difficulty_limits_at_1():
    last_block = Block(
        time.time_ns(),
        'test_last_hash',
        'test_hash',
        'test_data',
        1,
        0
    )

    time.sleep(MINE_RATE / SECONDS)
    minedBlock = Block.mineBlock(last_block, 'bar')

    assert minedBlock.difficulty == 1

@pytest.fixture
def lastBlock():
    return Block.genesis()

@pytest.fixture
def block(lastBlock):
    return Block.mineBlock(lastBlock, "test_data")

def test_is_valid_block(lastBlock, block):
    # lastBlock = Block.genesis()
    # block = Block.mineBlock(lastBlock, "test_data")
    # Implicit test 
    block.isValidBlock(lastBlock, block)

def test_is_valid_block_bad_last_hash(): 
    lastBlock = Block.genesis()
    block = Block.mineBlock(lastBlock, "test_data")
    block.lastHash = "evil_last_hash"
    # Anticipate the exception
    with pytest.raises(Exception, match="The block's last hash is incorrect!"): 
        block.isValidBlock(lastBlock, block)

def testIsValidBadProofOfWork(lastBlock, block):
    block.hash = "fff"
    with pytest.raises(Exception, match="The proof of work reqt not met."):
        Block.isValidBlock(lastBlock, block)

def testIsValidBlockJumpedDifficulty(lastBlock, block):
    jumpedDifficulty = 10
    block.difficulty = jumpedDifficulty
    block.hash = f'{"0" * jumpedDifficulty}111abc'

    with pytest.raises(Exception, match="Block diff can only be adjusted by 1."):
        Block.isValidBlock(lastBlock, block)

def testIsValidBlockBadBlockHash(lastBlock, block):
    block.hash = "000000000000bbbabc"
    with pytest.raises(Exception, match="The block hash is incorrect!"): 
        Block.isValidBlock(lastBlock, block)