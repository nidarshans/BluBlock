from flask import Flask, request, send_file, abort
from datetime import datetime
from Blockchain import Blockchain
import requests
import json
import pickle
import RSA
#Initialize
app = Flask(__name__)
blockchain = Blockchain()
peers = set()
#RSA.keygen()
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
    tx['signature'] = RSA.sign(json.dumps(tx))
    # send to peers
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
            pickle.dump(blockchain, f)
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
    print(ping)
    print(type(ping))
    if ping.decode('utf-8') != 'True':
        return 'Invalid address', 400
    peers.add(ip)
    print(peers)
    file = requests.get('http://' + ip + '/get_chain')
    blockchain = pickle.loads(file.content)
    return 'Success'

@app.route('/mine', methods=['GET'])
def mine():
    index = blockchain.mine()
    if not index:
        return "No transactions to mine"
    # send to peers
    return "Block {} is mined".format(index)

@app.route('/ping', methods=['GET'])
def ping():
    return 'True'

app.run('localhost', 6000, threaded = True)
