import os
import requests
import random

from flask import Flask, jsonify 
from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub

app = Flask(__name__)
blockchain = Blockchain()
pubsub = PubSub(blockchain)
# for i in range(3):
#     blockchain.addBlock(i+1)

@app.route("/")
def default():
    return "<h1>Welcome To Blockchain</h1>"

@app.route("/blockchain")
def routeBlockchain():
    # Need to return string, dict, tuple, Response instance or WSGI callable
    
    # return blockchain.__repr__()
    # Or jsonify(bch) -> server error (bch not serializable)
    return jsonify(blockchain.toJson()) 

@app.route("/blockchain/mine")
def routeBlockchainMine():
    transactionData = "stubbed_transaction_data"
    blockchain.addBlock(transactionData)
    block = blockchain.chain[-1]
    pubsub.broadcastBlock(block)
    return jsonify(block.toJson())

ROOT_PORT = 5000
PORT = ROOT_PORT

if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001, 6000)
    result = requests.get(f'http://localhost:{ROOT_PORT}/blockchain')
    print(f'Result JSON: {result.json()}')
    resultBlockchain = Blockchain.fromJson(result.json())
    try: 
        blockchain.replaceChain(resultBlockchain.chain)
        print('\n -- Successfully synced the local chain.')
    except Exception as e:
        print(f'\n -- Error syncing: {e}')

app.run(port=PORT)
