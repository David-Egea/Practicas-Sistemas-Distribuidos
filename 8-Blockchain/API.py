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
    # Ensures the blockchain is up-to-date
    consensus()
    # Copies the unconfirmed transactions
    unconfirmed_transactions_copy = blockchain.unconfirmed_transactions
    # The blockchain is mined
    index = blockchain.mine()
    # Checks that the actual chain is longer than the rest 
    longer = consensus()
    if not longer:
        # Announces the update
        announce_new_block(block=blockchain.last_block,request=request)
        if index:
            return (f"Block #{index} was mined sucessfully",200)
        else:
            return ("No transactions pending",200)
    else:
        # Restores the unconfirmed transactions
        blockchain.unconfirmed_transactions = unconfirmed_transactions_copy
        return ("Block was discarted and new mining is required.",400)

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
        if data_recieved["new_node_address"] != request.host:
            peers.add(data_recieved["new_node_address"])
        return get_chain()
    else:
        return ("Invalid transaction",404)

@app.route("/register_with_existing_node",methods = ["POST"])
def register_existing_node():
    global peers, blockchain
    # Gets the node_address field from request
    node_address = request.get_json()["node_address"]
    if request.host != node_address:
        # Constructs a POST request to register_new_node endpoint
        url = f"http://{node_address}/register_new_node"
        payload = json.dumps({
        "new_node_address": request.host
        })
        headers = {
        'Content-Type': 'application/json'
        }
        # Sends the request and returns the answer
        response = requests.request("POST", url, headers=headers, data=payload)
        # Depending on the status code of response
        if response.status_code == 201:
            # Updates chain and peers
            chain_dumps = response.json()["chain"]
            peers_dumps = response.json()["peers"]
            # Setting the peers
            for block_dumps in chain_dumps:
                # If it the first block (genesis) then it is added automately
                block = Block(int(block_dumps["index"]),block_dumps["transactions"],float(block_dumps["timestamp"]),block_dumps["previous_hash"])
                block.nonce = int(block_dumps["nonce"])
                # Depending on whether it is the first block or not
                if not block_dumps["index"]:
                    # Creates a blockchain with the genesis block recieved
                    block.current_hash = block_dumps["current_hash"]
                    blockchain_dumps = Blockchain(genesis_block=block)
                else:
                    # Attemps to add the block tothe blockchain
                    was_added = blockchain_dumps.append_block(block,block_dumps["current_hash"])
                    if not was_added:
                        return (f"Validation of chain failed", 400) # The validation failed
            # The completition of new blockchain was succesful
            blockchain = blockchain_dumps
            # Sets the difficulty of the blockchain depending on the number of zeros of last block
            difficulty = 0
            char = block.current_hash[0]
            while char == '0':
                difficulty += 1
                char = block.current_hash[difficulty]   
            blockchain.difficulty = difficulty # Asigns the difficulty to the blockchain
            # Creates a new set of peers
            if request.host in peers_dumps: peers_dumps.remove(request.host)
            if node_address not in peers_dumps: peers_dumps.append(node_address)
            peers = set(peers_dumps)
            return ("Registration successful", 200)
        else:
            # The post request failed
            return response.content, response.status_code
    else:
        return ("Self node is already registered.", 200)

def consensus() -> bool :
    """ 
        Function that implements the consensus logic to replicate the blockchain in a node.
        The function looks for the longest chain in the network, and then the actual blockchain of the node is replace by this one found.
        Returns true if a consensus is reached, False otherwise. 
    """
    global blockchain
    longest_chain = None
    current_len = len(blockchain.chain)
    for node in peers:
        try:
            # A GET request to endpoint /chain is sent to the node direction
            url = f"http://{node}/chain"
            payload={}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code == 200:
                length = response.json()["length"]
                chain = response.json()["chain"]
                if length > current_len:
                    # The chain is longer than the current one
                    longest_chain = chain
                    current_len = length
        except ConnectionRefusedError:
            pass
    if longest_chain is not None:
        # The blockchain of node is now the longest found
        blockchain = longest_chain
        return True
    else:
        return False

@app.route("/add_block",methods = ["POST"])
def add_block():
    try:
        # Attempts to get the required fields
        index = request.get_json()["index"]
        transactions = request.get_json()["transactions"]
        timestamp = request.get_json()["timestamp"]
        previous_hash = request.get_json()["previous_hash"]
        nonce = request.get_json()["nonce"]
        current_hash = request.get_json()["current_hash"]
    except KeyError: 
        return ("Invalid data", 400)
    else:
        # Constructs a block
        block = Block(index,transactions,timestamp,previous_hash)
        block.nonce = nonce
        # Tries to append the block to the blockchain
        global blockchain
        added = blockchain.append_block(block,current_hash)
        if added:
            return ("Success", 200)
        else: 
            return ("The block could not be appended to the blockchain.",400)

def announce_new_block(block: Block, request: Flask.request_class):
    """ Announces a new block to the rest of nodes of the Blockchain network. Arguments:
        * block: Block object
        * request: Request object of Flask 
        The rest of the nodes only have to verify the PoW and add the string. 
    """
    # Iterates for each node in peers variable
    for node in peers:
        if node != request.host_url:
            try:
                # Sends a POST request to /add_block
                url = f"http://{node}/add_block"
                payload = json.dumps(block.__dict__,sort_keys=True)
                headers = {
                'Content-Type': 'application/json'
                }
                requests.request("POST", url, headers=headers, data=payload)
            except ConnectionRefusedError:
                # In case the node is not responding
                pass
