# Test blockchain project

## How to use environments 

To set up an environment:
``` 
python3 -m venv venv
source venv/bin/activate
```

To install the dependencies:
``` 
pip install -r requirements.txt
```

To run tests, activate venv and run: 

```
python3 -m pytest backend/tests
```

To run a Flask app:
```
python3 -m backend.app
```

## Specifying the right versions

If there are issues with packages, use the proven versions:
```
itsdangerous==1.1.0
Jinja2==2.10.1
MarkupSafe==1.1.1
Werkzeug==0.16.0
pubnub==4.1.6
```
You can add the safe versions to `requirements.txt`. 

To :
```shell
pip uninstall itsdangerous Jinja2 MarkupSafe Werkzeug
pip install itsdangerous==1.1.0
pip install Jinja2==2.10.1
pip install MarkupSafe==1.1.1
pip install Werkzeug==0.16.0
pip
```

## Chain replacement

Goal: set up a blockchain network where multiple nodes are contributing to the growth of the data as part of the eventual system.

Each node will need to  come to a unanimous agreement on the official set of blocks if there is ever a point where a node in the network receives a different set of blocks.

That is both a valid chain and a longer one than the node should replace its own chain with that incoming set of blocks.

## Running a peer 

You need 3 terminal instances:

* Main blockchain instance running on the default port
* Peer blockchain instance running on a custom port
* The instance sending a message

Start the app:  
```shell
python3 -m backend.app 
```
Instance 2. Export the `PEER` value (should run a peer on instance 2) : 
```shell
source venv/bin/activate
export PEER=True
python3 -m backend.app  
```

Instance 3:
```shell
source venv/bin/activate
python3 -m backend.pubsub
```

## What to do when block received

For a valid block: 
1. Validate
2. Add to the local chain
3. Broadcast

## Transaction example  

<details> 
<summary>Example transaction data (`transaction.__dict__`): </summary>
```js
{
    'id': 'ac880043', 
    'output': {
        'recipient': 15, 
        'dd8ef45e': 985
    }, 
    'input': {
        'timestamp': 1698072624465655842, 
        'amount': 1000, 
        'address': 'dd8ef45e', 
        'publicKey': '<cryptography.hazmat.backends.openssl.ec._EllipticCurvePublicKey object at 0x7fe865976760>', 
        'signature': b'0D\x02 d\xf6&\xce\xd6\x82\xff\xb7d\xf8\xb2Fx\x16\xa8\xdbs\x17\xb3\x1b\xb9V\xcf\xdb\xb8\x17\xbf>\x05\x0fg\x1e\x02 C\xcc\xfd\xc2\xca}\xbb\xe3&QMTG!\xea\xd7\x1d\x19 \xc2\xb3\x0e\xffj-\x06\x8eD\x1a\xfe>['
    }
}
```
</details>

## Transaction pool 

Collect the transactions data created by wallets. Functions:
* Collects a unique set of transactions
* Updates existing stored transactions
* Can rewrite multiple transactions: 
replace the collection altogether or
or can clear the pool of some transaction

How it works: 
Everynode has a node

