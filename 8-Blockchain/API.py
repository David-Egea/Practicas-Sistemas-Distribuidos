from flask import Flask,request
import requests
import json
import requests
import time
from blockchain import Blockchain
from block import Block

app = Flask(__name__)

blockchain = Blockchain(difficulty=3)

peers = set()

@app.route("/new_transaction",methods = ["POST"])
def new_transaction():
    # Retrieving data
    data_recieved = request.get_json()
    minimum_fields = ["author","content"]
    # Getting keys
    keys = data_recieved.keys()
    if minimum_fields[0] in keys and minimum_fields[1] in keys :
        # Setting the actual time
        data_recieved["timestamp"]= time.time()
        # Adding the transaction
        blockchain.add_new_transaction(data_recieved)
        return "Success",201
    else:
        return "Invalid transaction",404

@app.route("/chain",methods = ["GET"])
def get_chain():
    # Creating the response
    response = dict()
    # Setting the length
    response["length"] = len(blockchain.chain)
    #Creating the list to response
    list_blocks = [b.__dict__ for b in blockchain.chain]
    # Adding the list
    response["chain"] = list_blocks
    # Adding peers
    response["peers"] = list(peers)
    final_response = json.dumps(response)
    # Returns the chain
    return final_response,201

@app.route("/mine",methods = ["GET"])
def mine():
    # The blockchain is mined
    response = blockchain.mine()
    if response >0:
        return "The index of the mining is {}".format(response)
    else:
        return "There are no transactions pending"

@app.route("/pending_transactions",methods = ["GET"])
def get_pending_transactions():
    return (str(blockchain.unconfirmed_transactions),200)

@app.route("/register_new_node",methods = ["POST"])
def register_new_node():
    # Retrieving data
    data_recieved = request.get_json()
    minimum_fields = ["new_node_address"]
    # Getting keys
    keys = data_recieved.keys()
    if minimum_fields[0] in keys :
        # Adding the node
        peers.add(data_recieved["new_node_address"])
        return get_chain()
    else:
        return "Invalid transaction",404

@app.route("/register_with_existing_node",methods = ["POST"])
def register_existing_node():
    node_address = request.get_json()["node_address"]
    # Constructs a POST request to register_new_node endpoint
    url = f"{request.host_url}/register_new_node"
    payload = json.dumps({
    "new_node_address": node_address
    })
    headers = {
    'Content-Type': 'application/json'
    }
    # Sends the request and returns the answer
    response = requests.request("POST", url, headers=headers, data=payload)
    # Depending on the status code of response
    if response.status_code == 200:
        # Updates chain and peers
        chain_dumps = response.json()["chain"]
        peers_dumps = response.json()["peers"]
        # Instantiates a Blockchain obj based on chain received
        blockchain = Blockchain()
        # Setting the peers
        for block_dumps in chain_dumps:
            block = Block(int(block_dumps["index"]),block_dumps["transactions"],float(block_dumps["timestamp"]),block_dumps["previous_hash"])
            block.nonce = int(block_dumps["nonce"])
            block.current_hash = block_dumps["current_hash"]
            was_added = blockchain.append_block(block,block_dumps["current_hash"])
            if not was_added:
                # The validation failed
                return ("Validation  of chain failed", 400)
        # The completition of new bockchain was succesful
        peers = peers_dumps
        return ("Registration successful", 200)
    else:
        # The post request failed
        return response.content, response.status_code

