# module 1 - create a blockchain
import datetime
import hashlib
import json
from flask import Flask, jsonify

# Part 1 - Building a blockchian

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1, 
            'timestamp': str(datetime.datetime.now()), 
            'proof': proof,
            'previous_hash': previous_hash,
            'data': 'oogabooga'
        }
        hashed_block = self.add_hash_to_block(block)
        self.chain.append(hashed_block)
        return hashed_block
    
    def add_hash_to_block(self, block):
        block_hash = self.hash(block)
        block['hash'] = block_hash
        return block
        
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False: 
            # Can make more challenging
            hash_operation =  hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        block_without_hash = dict(block)
        if 'hash' in block_without_hash:
            del block_without_hash['hash']
        encoded_block = json.dumps(block_without_hash, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        block_index = 1
        prev_block = chain[0]
        while block_index < len(chain):
            current_block = chain[block_index]
            # Check if previous_hash is valid
            if current_block['previous_hash'] != self.hash(prev_block):
                return False
            # Check if proof of work is valid
            previous_proof = prev_block['proof']
            current_proof = current_block['proof']
            hash_operation =  hashlib.sha256(str(current_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            prev_block = chain[block_index]
            block_index += 1
        return True
    

# Part 2 - Mining our blockchain

# Creating a Web App
app = Flask(__name__)

# Creating a blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    prev_block = blockchain.get_previous_block()
    prev_proof = prev_block['proof']
    proof = blockchain.proof_of_work(prev_proof)
    block = blockchain.create_block(proof, blockchain.hash(prev_block))
    response = {
        'message': 'Congrats, you just mined a block.', 
        'index': block['index'], 
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'hash': block['hash']
    }
    return jsonify(response), 200

#  Getting the full blockchain

@app.route('/get_blockchain', methods=['GET'])
def get_blockchain():
    response = {'chain': blockchain.chain, 'chain_length': len(blockchain.chain)}
    return jsonify(response), 200

@app.route('/validate_blockchain', methods=['GET'])
def validate_blockchain():
    response = {'is_valid': blockchain.is_chain_valid(blockchain.chain)}
    return jsonify(response), 200

@app.route('/hack_chain', methods=['GET'])
def hack_chain():
    if len(blockchain.chain) > 2:
        block_to_hack = blockchain.chain[2]
        block_to_hack['data'] = 'hacked jaajaja'
        blockchain.chain[2] = block_to_hack
        response = {'message': 'block 2 hacked'}
        return jsonify(response), 200
    
        

# Run the app
app.run(host = '0.0.0.0', port = 5000)
    









































            
            