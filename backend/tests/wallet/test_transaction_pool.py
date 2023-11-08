from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet 

def testSetTransaction():
    transactionPool = TransactionPool()
    transaction = Transaction(Wallet(), 'recipient', 15)
    transactionPool.setTransaction(transaction)

    assert transactionPool.transactionMap[transaction.id] == transaction
