import time
from block import Block

class Blockchain():
    """ Blockchain class."""
    
    def __init__(self, difficulty: int = 2) -> None:
        # transacciones que no se han do todavía
        self.unconfirmed_transactions = []
        self.chain = []
        # Se crea el primer bloque
        self.create_genesisBlock()
        # Se asigna la dificultad
        self.difficulty = difficulty

    def create_genesisBlock(self):
        # Se crea el objeto génesis
        genesis_block = Block(0,[],time.time(),"0")
        # Se le asigna el hash
        genesis_block.current_hash = genesis_block.compute_hash()
        # Se añade a la cadena
        self.chain.append(genesis_block)
    
    @property
    def last_block(self) -> Block:
        # Returns the last block
        return self.chain[-1]

    def proof_of_work(self, block: Block) -> str:
        """ 
            Algoritm that calculates the hash of the given block and increases the nonce block attribute until the pow condition is met. 
            The target hash must start with as many consecutive zeros as the difficulty value indicates. Keeps iterating intal a valid hash is found.
        """
        # Calculates the initial hash
        calculated_hash  = block.compute_hash()
        # A loop is forced until the condition is met
        while not calculated_hash[:self.difficulty].count("0") == self.difficulty:
            # Increases the nonce value of block
            block.nonce = block.nonce + 1
            # Computes the hash of the block with the nonce value updated
            calculated_hash = block.compute_hash()
        return calculated_hash

    def is_valid_proof(self, block: Block, hash: str) -> bool:
        """ Checks whether the given hash mets the conditions and is eq."""
        return block.compute_hash() == hash and hash[:self.difficulty].count("0") == self.difficulty

    def append_block(self, block: Block, hash: str) -> bool:
        """ Tries to append the given block to the blockchain, checks whether the valid proof is valid and """
        # Gets the Blockchain's last block
        last_block = self.last_block
        # Checks if the hash of the new block coincides with the last block's hash AND the block hash is valid
        if last_block.current_hash == block.previous_hash and self.is_valid_proof(block,hash):
            # Only if all requirements are met, the block is added
            block.current_hash = hash
            # Appends the block to the blockchain
            self.chain.append(block)
            return True
        else:
            return False

    def add_new_transaction(self,transaction) -> None:
        """"Adds a new transaction to the unconfirmed transactions list."""
        # Adds the new transaction
        self.unconfirmed_transactions.append(transaction)
        
    def mine(self) -> int:
        """Function in charge of mining the unconfirmed transactions."""
        if len(self.unconfirmed_transactions):
            # Gets the Blockchain's last block
            last_block = self.last_block
            # Gets the index of the last block
            last_index = last_block.index
            # Gets the last hash of the last block
            previous_hash = last_block.current_hash
            # Calculates the new index
            new_index = last_index + 1
            # The block with the transactions is created
            block = Block(new_index,self.unconfirmed_transactions,time.time(),previous_hash)
            # Calculates the hash of the block
            calculated_hash = self.proof_of_work(block)
            # The block is appended
            self.append_block(block,calculated_hash)
            
            self.unconfirmed_transactions = []
            return new_index
        else:
            return 0
