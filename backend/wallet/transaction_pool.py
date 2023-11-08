
class TransactionPool:
    def __init__(self):
        self.transactionMap = {}

    def setTransaction(self, transaction):
        """
        Set a transaction in a tr pool
        """
        self.transactionMap[transaction.id] = transaction