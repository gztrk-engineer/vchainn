from flask import Flask, jsonify 
from backend.blockchain.blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()
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
    return jsonify(blockchain.chain[-1].toJson())

app.run()
# app.run(port=5001)