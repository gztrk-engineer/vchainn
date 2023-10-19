import time

from backend.util.crypto_hash import cryptoHash
from backend.util.hex2bin import hexToBinary
from backend.config import MINE_RATE

GENESIS_DATA = {
    'timestamp': 1,
    'lastHash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data': [],
    'difficulty': 3,
    'nonce': 'genesis_nonce'
}


class Block:
  """
    Block: a unit of storage.
    Store transactions in a blockchain that supports a cryptocurrency.
    """

  def __init__(self, timestamp, lastHash, hash, data, difficulty, nonce):
    self.timestamp = timestamp
    self.lastHash = lastHash
    self.hash = hash
    self.data = data
    self.difficulty = difficulty
    self.nonce = nonce

  def __repr__(self):
    return ('Block('
            f'timestamp: {self.timestamp}, '
            f'lastHash: {self.lastHash}, '
            f'hash: {self.hash}, '
            f'data: {self.data}, '
            f'difficulty: {self.difficulty}, '
            f'nonce: {self.nonce})')

  def __eq__(self, other):
    return self.__dict__ == other.__dict__
  
  def toJson(self):
    """
    Serialize a block into a dictionary of its attributes
    """
    print("*************")
    print("Self dict: ")
    print(self.__dict__)
    return self.__dict__

  @staticmethod
  def mineBlock(lastBlock, data):
    """
        Mine a block based on the given last_block and data, until a block hash
        is found that meets the leading 0's proof of work requirement.
        """
    timestamp = time.time_ns()
    lastHash = lastBlock.hash
    difficulty = Block.adjustDifficulty(lastBlock, timestamp)
    nonce = 0
    hash = cryptoHash(timestamp, lastHash, data, difficulty, nonce)

    while hexToBinary(hash)[0:difficulty] != '0' * difficulty:
      nonce += 1
      timestamp = time.time_ns()
      difficulty = Block.adjustDifficulty(lastBlock, timestamp)
      hash = cryptoHash(timestamp, lastHash, data, difficulty, nonce)

    return Block(timestamp, lastHash, hash, data, difficulty, nonce)

  @staticmethod
  def genesis():
    """
        Generate the genesis block.
        """
    return Block(**GENESIS_DATA)

  @staticmethod
  def adjustDifficulty(lastBlock, newTimestamp):
    """
        Calculate the adjusted difficulty according to the MINE_RATE.
        Increase the difficulty for slowly mined blocks.
        Decrease the difficulty for quickly mined blocks.
    """
    if (newTimestamp - lastBlock.timestamp) < MINE_RATE:
      return lastBlock.difficulty + 1

    if (lastBlock.difficulty - 1) > 0:
      return lastBlock.difficulty - 1

    return 1

  @staticmethod
  def isValidBlock(lastBlock, block):
    if block.lastHash != lastBlock.hash:
      raise Exception("The block's last hash is incorrect!")
    if hexToBinary(block.hash)[0:block.difficulty] != "0" * block.difficulty:
      raise Exception("The proof of work reqt not met.")
    if abs(lastBlock.difficulty - block.difficulty) > 1:
      raise Exception("Block diff can only be adjusted by 1.")

    reconstructedHash = cryptoHash(block.timestamp, block.lastHash,
                                    block.data, block.nonce, block.difficulty)

    if block.hash != reconstructedHash:
      raise Exception("The block hash is incorrect!")


def main():
  genesisBlock = Block.genesis()
  badBlock = Block.mineBlock(Block.genesis(), "foo")
  # badBlock.last_hash = "evil_data"

  try:
    Block.isValidBlock(genesisBlock, badBlock)
  except Exception as e:
    print(f"isValidBlock: {e}")


if __name__ == '__main__':
  main()
