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
    print("Sender wallet after transaction")
    print(senderWallet.__dict__)
    print("============\n")


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

def testTransactionExceedBalance():
    with pytest.raises(Exception, match="The amount exceeds the balance"):

        senderWallet = Wallet()

        transaction = Transaction(senderWallet, 'recipient', 2000)