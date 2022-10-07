import datetime
import hashlib
import json
from flask import Flask, jsonify
 
hashes_verified = []
 
dado = float(input("Sensor Temperature: "))

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, timestamp=str(datetime.datetime.now()))
        
    def create_block(self, proof, timestamp):
        previous_block = self.get_previous_block()
        
        block = {
            "index": len(self.chain) + 1,
            "Sensor": dado,
            "timestamp": timestamp,
            "proof": proof,
            "previous_hash": self.hash(previous_block) if previous_block else 0,
        }
        return block
 
    def insert_block(self, block):
        self.chain.append(block)
 
    def get_previous_block(self):
        return self.chain[-1] if len(self.chain) > 0 else None
 
    def proof_of_work(self):
        new_proof = 1
        check_proof = False
        hashes_verified.clear()
        timestamp = str(datetime.datetime.now())
        while check_proof is False:
            block = self.create_block(new_proof, timestamp)
            hash_operation = self.hash(block)
            hashes_verified.append(hash_operation)
            if hash_operation[:5] == "00000":
                check_proof = True
                self.chain.append(block)
                return block
            else:
                new_proof += 1
 
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
 
    def is_chain(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block["previous_hash"] != self.hash(previous_block):
                return False
            hash_operation = self.hash(block)
            if hash_operation[:5] != "00000":
                return False
            previous_block = block
            block_index += 1
        return True
 
 
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
 
blockchain = Blockchain()
 
 
@app.route("/mine_block", methods=["GET"])
def mine_block():
    block = blockchain.proof_of_work()
    return jsonify(block), 200
 
 
@app.route("/get_chain", methods=["GET"])
def get_chain():
    response = {"chain": blockchain.chain,"length": len(blockchain.chain)}
    return jsonify(response), 200
 
 
@app.route("/is_valid", methods=["GET"])
def is_valid():
    response = blockchain.is_chain(blockchain.chain)
    return jsonify({"is_valid": response}), 200
 
 
app.run(host="0.0.0.0", port=5000)
