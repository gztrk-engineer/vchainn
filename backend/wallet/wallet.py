import uuid
import json

# from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
from backend.config import STARTING_BALANCE

class Wallet():
    def __init__(self):
        self.address = str(uuid.uuid4())[0:8]
        self.balance = STARTING_BALANCE
        self.privateKey = ec.generate_private_key(
            ec.SECP256K1()
            # ec.SECP256K1(),
            # default_backend
        )
        self.publicKey = self.privateKey.public_key()

    def sign(self, data):
        """
        Generate a signature based on the data using the private jey
        """
        return self.privateKey.sign(
            # The function requires a bytes-like object
            json.dumps(data).encode('utf-8'), 
            ec.ECDSA(hashes.SHA256())
        )

    @staticmethod
    def verify(publicKey, data, signature):
        """
        Verify 
        """
        try:
            publicKey.verify(
                signature,
                json.dumps(data).encode('utf-8'), 
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            return False


def main():
    wallet = Wallet()
    print(f'wallet.__dict__: {wallet.__dict__}')
    data = { "foo": "bar" }
    signature = wallet.sign(data)
    print(f'Signature: {signature}')
    shouldBeValid = Wallet.verify(wallet.publicKey, data, signature)
    print(f'ShouldBeValid: {shouldBeValid}')
    shouldBeInvalid = Wallet.verify(Wallet().publicKey, data, signature)
    print(f'ShouldBeInvalid: {shouldBeInvalid}')

if __name__ == "__main__":
    main()