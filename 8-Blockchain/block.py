import json
import hashlib
from typing import List

class Block():
    """ Blockchain element class."""
    
    def __init__(self, index: int, transactions: List[str], timestamp: float, previous_hash: str):
        """
        Constructor for a 'Block' class.
        * param index: The unique ID number if a block.
        * param transactions: List of transactions.
        * param timestamp: Block creation time.
        * param previous_hash: Contains the hash value of the preceding block in the chain.
        """
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0


    def compute_hash(self) -> str:
        """
        Converts the block obj into JSON string and then returns a hash value.
        """
        block_str = json.dumps(self.__dict__, sort_keys = True)
        hash = hashlib.sha256(block_str.encode()).hexdigest()
        return hash