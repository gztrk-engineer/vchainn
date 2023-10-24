import uuid
import time

from backend.wallet.wallet import Wallet

class Transaction():
    """
    Document of an exchange in currence from a sender to one (or more) recipients.
    """
    def __init__(self, senderWallet, recipient, amount):
        self.id = str(uuid.uuid4())[:8]
        self.output = self.createOutput(
            senderWallet,
            recipient,
            amount
        )
        self.input = self.createInput(senderWallet, self.output)

    def createOutput(self, senderWallet, recipient, amount):
        """
        Structure the output data for transaction
        """
        if amount > senderWallet.balance:
            raise Exception("The amount exceeds the balance.")
        output = {}
        output[recipient] = amount
        output[senderWallet.address] = senderWallet.balance - amount

        return output
    
    def createInput(self, senderWallet, output):
        """
        # Structure the input data for the transaction.
        # Sign the transaction and include the sender's public key and address
        """
        return {
            "timestamp": time.time_ns(),
            "amount": senderWallet.balance,
            "address": senderWallet.address,
            "publicKey": senderWallet.publicKey,
            "signature": senderWallet.sign(output)
        }
    def updateTransaction(self, senderWallet, recipient, amount):
        if amount > self.output[senderWallet.address]:
            raise Exception("The amount exceeds the balance.")

        if recipient in self.output:
            self.output[recipient] = self.output[recipient] + amount 
        else:
            self.output[recipient] = amount 

        self.output[senderWallet.address] = \
            self.output[senderWallet.address] - amount
     
def main():
    transaction = Transaction(Wallet(), "recipient", 15)
    print(f'transaction.__dict__: {transaction.__dict__}')

if __name__ == "__main__":
    main()