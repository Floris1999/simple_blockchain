
import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

from flask import Flask, jsonify, request
from flask_cors import CORS

class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.wallet = []

        self.wallet.append({
            'name': "GOD",
            'address': "2cf5e4771cc449f52850a7ac7c7c04cd",
            'balance': 100
        })

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)
        
    def new_block(self, proof, previous_hash=None):
        # Creates a new Block and adds it to the chain
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block
    
    def new_user(self, name, address):
        self.wallet.append({
            'name': name,
            'address': address,
            'balance': 0,
        })
        return self.wallet
    
    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    def calculate_balance(self):
        for x in self.current_transactions:
            sender = x
            # print(sender['recipient'])
            reciever = next((item for item in self.wallet if item["address"] == sender['recipient']), None)

            if sender['sender'] == '0':
                return
            else:
                reciever["balance"] = reciever["balance"] + sender['amount']
                print(reciever["balance"])

    @staticmethod
    def hash(block):
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]
    
    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


    # def valid_chain(self, chain):
    #     """
    #     Determine if a given blockchain is valid
    #     :param chain: <list> A blockchain
    #     :return: <bool> True if valid, False if not
    #     """

    #     last_block = chain[0]
    #     current_index = 1

    #     while current_index < len(chain):
    #         block = chain[current_index]
    #         print(f'{last_block}')
    #         print(f'{block}')
    #         print("\n-----------\n")
    #         # Check that the hash of the block is correct
    #         if block['previous_hash'] != self.hash(last_block):
    #             return False

    #         # Check that the Proof of Work is correct
    #         if not self.valid_proof(last_block['proof'], block['proof']):
    #             return False

    #         last_block = block
    #         current_index += 1

    #     return True

    # def resolve_conflicts(self):

    #     neighbours = self.nodes
    #     new_chain = None

    #     # We're only looking for chains longer than ours
    #     max_length = len(self.chain)

    #     # Grab and verify the chains from all the nodes in our network
    #     for node in neighbours:
    #         response = requests.get(f'http://{node}/chain')

    #         if response.status_code == 200:
    #             length = response.json()['length']
    #             chain = response.json()['chain']

    #             # Check if the length is longer and the chain is valid
    #             if length > max_length and self.valid_chain(chain):
    #                 max_length = length
    #                 new_chain = chain

    #     # Replace our chain if we discovered a new, valid chain longer than ours
    #     if new_chain:
    #         self.chain = new_chain
    #         return True

    #     return False


app = Flask(__name__)
CORS(app)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.

    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    blockchain.calculate_balance()

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200  
    
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # # Check if sender has enough coins in the wallet
    # sender = values['sender']
    # for x in blockchain.wallet:
    #     if x['address'] == sender:
    #         if x['balance'] - values['amount'] < 0:
    #                 return 'Balance insufficient', 400
    #     else:
    #         return 'Sender address invalid', 400

    value = next((item for item in blockchain.wallet if item["address"] == values['sender']), None)
    if value == None:
        return 'Sender address non existent', 400
    else:
        if(value['balance'] - values['amount'] < 0):
            return 'Balance insufficient', 400
        value['balance'] = value['balance'] - values['amount']
        
    # Check if recipient address exists
    if next((item for item in blockchain.wallet if item["address"] == values['recipient']), True) == True:
        return "You are trying to send coins to a non existent addres", 400
    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/wallet/new', methods=['POST'])
def new_user():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['name', 'address']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # print(values['address'])
    # if values['address'] == "gbkufudlabhf":
    #     return 'Address already exists', 400
    print(blockchain.wallet)


    value = values['address']
    for x in blockchain.wallet:
        if x['address'] == value:
            return 'Address already exists', 400

    # Create a new Transaction
    index = blockchain.new_user(values['name'], values['address'])

    response = {'message': f'User will be added to wallet {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/transaction', methods=['GET'])
def full_transaction():
    response = {
        'chain': blockchain.transaction,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/wallet', methods=['GET'])
def full_wallet():
    response = {
        'wallet': blockchain.wallet,
        'length': len(blockchain.wallet),
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)