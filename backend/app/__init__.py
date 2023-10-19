from flask import Flask 
from backend.blockchain.blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()
for i in range(3):
    blockchain.addBlock(i+1)

@app.route("/")
def default():
    return "<h1>Welcome To Blockchain</h1>"

@app.route("/blockchain")
def routeBlockchain():
    # Need to return string, dict, tuple, Response instance or WSGI callable
    return blockchain.__repr__()

app.run(port=5001)