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

    def replaceChain(self, incomingChain):
        """
        Replace the local chain with incoming if the following applies: 
        - The new chain is longer
        - The new chain is formatted properly
        """
        if len(incomingChain) <= len(self.chain):
            raise Exception("Cannot replace. The incoming chain must be longer.")
        try:
            Blockchain.isValidChain(incomingChain)
        except Exception as e:
            raise Exception(f'Cannot replace. The incoming chain is invalid: {e}')
        
        self.chain = incomingChain

    def toJson(self):
        """
        Serialize the blockchain into a list of blocks
        """
        # serializedChain = []
        # for block in self.chain:
        #     serializedChain.append(block.toJson())
        # return serializedChain

        return list(map(lambda block: block.toJson(), self.chain))

        
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