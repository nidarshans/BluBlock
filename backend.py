from flask import Flask, request
from datetime import datetime
from Blockchain import Blockchain
import requests
import json
import pickle
#Initialize
app = Flask(__name__)
blockchain = Blockchain()
peers = set()
#Helper functions
def json_reader(filename):
    with open(filename) as f:
        for line in f:
            yield json.loads(line)

@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    tx = request.get_json()
    print(tx)
    print(type(tx))
    required = ['msg']#('from', 'to', 'amount', 'signature')
    for field in required:
        print(field)
        if not tx.get(field):
            return "Invalid format", 404
    tx['timestamp'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    with open('tx_pool.json', 'a') as jfile:
        try:
            jfile.write(json.dumps(tx) + '\n')
        finally:
            jfile.close()
    return 'Success'

@app.route('/get_chain', methods=['GET'])
def get_chain():
    return pickle.dumps(blockchain)

@app.route('/register_node', methods=['POST'])
def register_new_node():
    ip = request.get_json()['node_address']
    if not ip:
        return 'Invalid address', 400
    peers.add(ip)
    #return json.dumps({"length": len(blockchain.chain), "chain": })

@app.route('/mine', methods=['GET'])
def mine():
    index = blockchain.mine()
    if not index:
        return "No transactions to mine"
    return "Block #{} is mined".format(index)

app.run('localhost', 6000)
