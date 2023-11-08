import uuid
import time

from backend.wallet.wallet import Wallet

class Transaction():
    """
    Document of an exchange in currence from a sender to one (or more) recipients.
    """
    def __init__(
        self, 
        senderWallet=None, 
        recipient=None, 
        amount=None, 
        id=None, 
        output=None, 
        input=None
    ):
        self.id = id or str(uuid.uuid4())[:8]
        self.output = output or self.createOutput(
            senderWallet,
            recipient,
            amount
        )
        self.input = input or self.createInput(senderWallet, self.output)

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

        self.input = self.createInput(senderWallet, self.output)

    def toJson(self):
        """
        Serialize the transaction
        """
        return self.__dict__

    @staticmethod
    def fromJson(transactionJson):
        """
        Deserialize the transaction json representation into a Transaction instance
        """
        # return Transaction(
        #     id=transactionJson['id'],
        #     output=transactionJson['output'],
        #     input=transactionJson['input']
        # )
        # Unpack the kwargs
        return Transaction(**transactionJson)


    @staticmethod
    def isValidTransaction(transaction):
        """
        Validate transaction, raise exception if invalid
        """
        outputTotal = sum(transaction.output.values())

        if transaction.input['amount'] != outputTotal:
            raise Exception("Invalid transaction output value")

        if not Wallet.verify(
            transaction.input['publicKey'],
            transaction.output, 
            transaction.input['signature']
        ):
            raise Exception("Invalid signature")

     
def main():
    transaction = Transaction(Wallet(), "recipient", 15)
    print(f'transaction.__dict__: {transaction.__dict__}')
    transactionJson = transaction.toJson()
    restoredTransaction = Transaction.fromJson(transactionJson)
    print(f'restoredTransaction.__dict__: {restoredTransaction.__dict__}')

if __name__ == "__main__":
    main()