import pytest 

from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet

def testTransaction():
    senderWallet = Wallet()
    print("============")
    print("Sender wallet before transaction")
    print(senderWallet.__dict__)
    recipient = "recipient"
    amount = 50

    transaction = Transaction(senderWallet, recipient, amount)
    print("============")


    assert transaction.output[recipient] == amount
    assert transaction.output[senderWallet.address] == senderWallet.balance - amount
    assert 'timestamp' in transaction.input
    assert transaction.input['amount'] == senderWallet.balance
    assert transaction.input['address'] == senderWallet.address 

    assert Wallet.verify(
        transaction.input['publicKey'],
        transaction.output, 
        transaction.input['signature']
    )

def testTransactionExceedsBalance():
    with pytest.raises(Exception, match="The amount exceeds the balance"):

        senderWallet = Wallet()

        transaction = Transaction(senderWallet, 'recipient', 2000)

def testTransactionUpdateExceedsBalance():
    senderWallet = Wallet()
    transaction = Transaction(senderWallet, "recipient", 50)

    with pytest.raises(Exception, match="The amount exceeds the balance"):
        transaction.updateTransaction(senderWallet, 'new_recipient', 1500)
def testTransactionUpdate():
    senderWallet = Wallet()
    recipient1 = 'first_recipient'
    recipient2 = 'second_recipient'
    amount1 = 50
    amount2 = 75

    transaction = Transaction(senderWallet, recipient1, amount1)
    transaction.updateTransaction(senderWallet, recipient2, amount2)

    assert transaction.output[recipient2] == amount2
    assert transaction.output[senderWallet.address] == \
    senderWallet.balance - amount1 - amount2
    assert Wallet.verify(
        transaction.input['publicKey'],
        transaction.output, 
        transaction.input['signature']
    )

    toFirstAgainAmt = 25
    transaction.updateTransaction(senderWallet, recipient1, toFirstAgainAmt)
    assert transaction.output[recipient1] == amount1 + toFirstAgainAmt
    assert transaction.output[senderWallet.address] == \
        senderWallet.balance - amount1 - amount2 - toFirstAgainAmt
    assert Wallet.verify(
        transaction.input['publicKey'],
        transaction.output, 
        transaction.input['signature']
    )

    def testValidTransaction():
        Transaction.isValidTransaction(Transaction(), 'recipient', 50)

    def testValidTransactionWithInvalidOutputs():
        senderWallet = Wallet()
        transaction = Transaction(senderWallet, 'recipient', 50)
        transaction.output[senderWallet.address] = 1500

        with pytest.raises(Exception, match="Invalid transaction output value"):
            Transaction.isValidTransaction(transaction)

    def testValidTransactionWithInvalidSignature():
        senderWallet = Wallet()
        transaction = Transaction(senderWallet, 'recipient', 50)
        transaction.input['signature'] = Wallet().sign(transaction.output)

        with pytest.raises(Exception, match="Invalid signature"):
            Transaction.isValidTransaction(transaction)
