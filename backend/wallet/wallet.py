import uuid

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec

class Wallet():
    def __init__(self):
        self.address = str(uuid.uuid4())[0:8]
        self.privateKey = ec.generate_private_key(
            ec.SECP256K1()
            # ec.SECP256K1(),
            # default_backend
        )
        self.publicKey = self.privateKey.public_key()

def main():
    wallet = Wallet()
    print(f'wallet.__dict__: {wallet.__dict__}')

if __name__ == "__main__":
    main()