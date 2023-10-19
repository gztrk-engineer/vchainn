import time

from pubnub.pubnub import PubNub 
from pubnub.pnconfiguration import PNConfiguration 
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory

from backend.keys import PUBLISH_KEY, SUBSCRIBE_KEY 


pnconfig = PNConfiguration()
pnconfig.publish_key = PUBLISH_KEY
pnconfig.subscribe_key = SUBSCRIBE_KEY
pubnub = PubNub(pnconfig) 

TEST_CHANNEL = "TEST_CHANNEL"

pubnub.subscribe().channels([TEST_CHANNEL]).execute()

class Listener(SubscribeCallback):
    def message(self, pubnub, message_object):
        print(f'\n-- Channel: {message_object.channel} | Message: {message_object.message}')
        # print(f'\n-- Incoming message_object: {message_object}')

pubnub.add_listener(Listener())

def main():
    time.sleep(1)
    pubnub.publish().channel(TEST_CHANNEL).message({"foo": "bar"}).sync()

if __name__ == "__main__":
    main()