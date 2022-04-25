from flask import Flask,request
import requests
import json
import requests
import time
from blockchain import Blockchain
from block import Block

app = Flask(__name__)

blockchain = Blockchain()

peers = set()

@app.route("/new_transaction",methods = ["POST"])
def newTransaction():
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
def getChain():
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
    return str(blockchain.unconfirmed_transactions)

@app.route("/register_new_node",methods = ["POST"])
def registerNewNode():
    # Retrieving data
    data_recieved = request.get_json()
    minimum_fields = ["new_node_address"]
    # Getting keys
    keys = data_recieved.keys()
    if minimum_fields[0] in keys :
        # Adding the node
        peers.add(data_recieved["new_node_address"])
        return getChain()
    else:
        return "Invalid transaction",404

@app.route("/register_with_existing_node",methods = ["POST"])
def registerExistingNode():
    # Retrieving data
    data_recieved = request.get_json()
    node_address = data_recieved["node_address"]
    
    url = "http://127.0.0.1:6000/register_new_node"
    payload = json.dumps({
    "new_node_address": node_address
    })
    headers = {
    'Content-Type': 'application/json'
    }
    responseAPI = requests.request("POST", url, headers=headers, data=payload)
    responseAPI.json()
    # Creating the response
    response = dict()
    # Setting the length
    response["length"] = responseAPI["length"]
    # Setting the peers
    response["peers"] = responseAPI["peers"]
    chain_to_proccess = responseAPI["chain"]
    for block_dict in chain_to_proccess:
        block = Block(int(block_dict["index"]),block_dict["transactions"],float(block_dict["timestamp"]),block_dict["previous_hash"])
        block.nonce = int(block_dict["nonce"])
        block.current_hash = block_dict["current_hash"]
        blockchain.append_block(block,block_dict["current_hash"])
    a = 2

