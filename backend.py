from flask import Flask, request, send_file, safe_join, abort
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
    required = ['msg'] # ('from', 'to', 'amount', 'signature')
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
    with open('chain.bin', 'wb') as f:
        try:
            pickle.dump(blockchain, f)
        except FileNotFoundError:
            abort(404)
    return send_file('chain.bin',
    mimetype = 'bin',
    attachment_filename= 'chain.bin',
    as_attachment = True)

@app.route('/register_node', methods=['POST'])
def register_new_node():
    ip = request.get_json()['node_address']
    if not ip:
        return 'Invalid address', 400
    peers.add(ip)
    return get_chain()

@app.route('/mine', methods=['GET'])
def mine():
    blockchain.load_unconfirmed_transaction()
    index = blockchain.mine()
    if not index:
        return "No transactions to mine"
    return "Block #{} is mined".format(index)

app.run('localhost', 6000)
