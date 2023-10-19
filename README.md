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
