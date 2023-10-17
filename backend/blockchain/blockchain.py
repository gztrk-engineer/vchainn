from backend.blockchain.block import Block

class Blockchain:
    """
    Blockchain: a public ledger of transactions.
    Implemented as a list of blocks - data sets of transactions
    """
    def __init__(self):
        self.chain = [Block.genesis()]

    def addBlock(self, data):
        self.chain.append(Block.mineBlock(self.chain[-1], data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'

    @staticmethod
    def isValidChain(chain):
        """
        Validate the incoming chain.
        Enforce the rules: 
        1. starts with genesis block
        2. block must be formatted correctly
        """
        if chain[0] != Block.genesis():
            raise Exception("The genesis block must be valid!")
        for i in range(1, len(chain)):
            block = chain[i]
            lastBlock = chain[i-1]
            Block.isValidBlock(lastBlock, block)

def main():
    blockchain = Blockchain()
    blockchain.addBlock('one')
    blockchain.addBlock('two')

    print(blockchain)
    print(f'blockchain.py ___name__: {__name__}')

if __name__ == '__main__':
    main()