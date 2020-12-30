from flask import Flask, request, send_file, abort
from datetime import datetime
from Blockchain import Blockchain
from Block import Block
import requests
import json
import pickle
import Crypto
#Initialize
app = Flask(__name__)
blockchain = Blockchain()
peers = set()
try:
    open('keys/secret.pem', 'rb').close()
except FileNotFoundError:
    print('Keys not found. Generating pub/priv keys...')
    Crypto.rsa_keygen()
    print('Keys generated')
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
    if not tx:
        return "Invalid input"
    for field in required:
        print(field)
        if not tx.get(field):
            return "Invalid format", 404
    tx['timestamp'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    tx['public_key'] = open('keys/public.pem', 'r').read()
    tx['signature'] = Crypto.rsa_sign(json.dumps(tx))
    for ip in peers:
        # make new method to process incoming transactions
        # requests.post('http://' + ip + '/new_transaction', json = tx)
        pass
    with open('tx_pool.json', 'a') as jfile:
        try:
            jfile.write(json.dumps(tx) + '\n')
        finally:
            jfile.close()
    return 'Success'

@app.route('/get_chain', methods=['GET'])
def get_chain():
    with open('pickled_chain.bin', 'wb') as f:
        try:
            pickle.dump(blockchain.chain, f)
        except FileNotFoundError:
            abort(404)
    return send_file('pickled_chain.bin',
    mimetype = 'bin',
    attachment_filename = 'pickled_chain.bin',
    as_attachment = True)

@app.route('/register_node', methods=['POST'])
def register_new_node():
    ip = request.get_json()['node_address']
    if not ip and not isinstance(ip, str):
        return 'Invalid address', 400
    ping = requests.get('http://' + ip + '/ping').content
    if ping.decode('utf-8') != 'True':
        return 'Invalid address', 400
    peers.add(ip)
    print(peers)
    return 'Success'

@app.route('/sync', methods=['GET'])
def sync():
    global blockchain
    ip = peers.pop()
    file = requests.get('http://' + ip + '/get_chain')
    blockchain = pickle.loads(file.content)
    return 'Success'

@app.route('/mine', methods=['GET'])
def mine():
    global blockchain
    t = blockchain.mine()
    if not t[0]:
        return "No transactions to mine"
    for ip in peers:
        print(requests.post('http://' + ip + '/add_block', json = t[1].block_data).content)
    return "Block {} is mined".format(t[0] - 1)

@app.route('/add_block', methods=['POST'])
def add_block():
    j = request.get_json()
    print(j)
    block = Block(j.get('index'), j.get('data'), j.get('timestamp'), j.get('previous_hash'), j.get('nonce'))
    added = blockchain.add_block(block, j.get('hash'))
    if not added:
        return 'Rejected by node'
    return 'Success'

@app.route('/ping', methods=['GET'])
def ping():
    return 'True'

app.run('localhost', 6000, threaded = True)
