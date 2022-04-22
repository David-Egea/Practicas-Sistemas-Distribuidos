from block import Block
from blockchain import Blockchain

class Practica():

    def do_section(self, section: str) -> None:
        getattr(self,section)()

        #TODO: SACAR GRAFICA TIEMPOS
    
    def section1_3(self) -> None:
        """ 1.3 - Proof of work definition. """
        # Creates a block chain
        blockchain = Blockchain(difficulty=1)
        # Getting the genesis block
        print(f"Last block : {blockchain.get_last_block.__dict__}")

    def section1_4(self) -> None:
        """ 1.4 - Block Mining. """
        # Creates a block chain
        blockchain = Blockchain(difficulty=1)
        # Getting the genesis block
        print(f"Last block : {blockchain.get_last_block.__dict__}")
        # A new transaction is created
        blockchain.add_new_transaction("Hola")
        # Mining the transaction
        blockchain.mine()
        # A new transaction is created
        blockchain.add_new_transaction("que")
        # Mining the transaction
        blockchain.mine()
        # A new transaction is created
        blockchain.add_new_transaction("tal")
        # Mining the transaction
        blockchain.mine()
        # Retrieving unconfirmed transactions
        print(blockchain.unconfirmed_transactions)
        # Getting the blockchain length
        print("The length of the blockchaing is: {}".format(len(blockchain.chain)))
        # Gets the information of the last block
        print(f"Last block : {blockchain.get_last_block.__dict__}")

    def section1_5(self) -> None:
        """1.5 - Block Mining. """
       

if __name__ == "__main__":
    # Creates a practica
    p = Practica()
    # Evaluates the section 1.4
    p.do_section("section1_4")

