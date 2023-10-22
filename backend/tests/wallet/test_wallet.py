
from backend.wallet.wallet import Wallet

def testVerifyValidSignature():
    data = { "foo": "test_data" }
    wallet = Wallet()
    signature = wallet.sign(data)

    assert Wallet.verify(wallet.publicKey, data, signature) 

def testVerifyInvalidSignature():
    data = { "foo": "test_data" }
    wallet = Wallet()
    signature = wallet.sign(data)

    assert not Wallet.verify(Wallet().publicKey, data, signature) 
