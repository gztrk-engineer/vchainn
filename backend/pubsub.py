import time

from pubnub.pubnub import PubNub 
from pubnub.pnconfiguration import PNConfiguration 
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory

from backend.keys import PUBLISH_KEY, SUBSCRIBE_KEY 
from backend.blockchain.block import Block


pnconfig = PNConfiguration()
pnconfig.publish_key = PUBLISH_KEY
pnconfig.subscribe_key = SUBSCRIBE_KEY

# TEST_CHANNEL = "TEST_CHANNEL"
# BLOCK_CHANNEL = "BLOCK_CHANNEL"

CHANNELS = {
    "TEST": "TEST",
    "BLOCK": "BLOCK"
}


class Listener(SubscribeCallback):

    def __init__(self, blockchain): 
        self.blockchain = blockchain

    def message(self, pubnub, messageObject):
        print(f'\n-- Channel: {messageObject.channel} | Message: {messageObject.message}')
        # print(f'\n-- Incoming message_object: {message_object}')
        if messageObject.channel == CHANNELS['BLOCK']:
            block = Block.fromJson(messageObject.message)
            potentialChain = self.blockchain.chain[:]
            potentialChain.append(block)

            try:
                self.blockchain.replaceChain(potentialChain)
                print(f'\n -- Successfully replaced the local chain.')
            except Exception as e:
                print(f'\n -- Did not replace chain: {e}')
            



class PubSub():
    """
    Handles the publish/subscribe layer of the application
    Provides comm between the nodes of the blockchain network. 
    """
    def __init__(self, blockchain):
        
        self.pubnub = PubNub(pnconfig) 
        # ...channels([ch1, ch2])
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain))

    def publish(self, channel, message):
        """
        Publish the message object to the channel
        """
        # Version 1 - involved redundant interaction
        # self.pubnub.publish().channel(channel).message(message).sync()
        # Version 2 - Avoid redundant interaction
        self.pubnub.unsubscribe().channels([channel]).execute()
        self.pubnub.publish().channel(channel).message(message).sync()
        self.pubnub.subscribe().channels([channel]).execute()

    def broadcastBlock(self, block):
        """
        Broadcast block to all blocks
        """
        self.publish(CHANNELS['BLOCK'], block.toJson())


def main():
    pubsub = PubSub()
    time.sleep(1)
    pubsub.publish(CHANNELS['TEST'], {"foo": "bar"})

if __name__ == "__main__":
    main()