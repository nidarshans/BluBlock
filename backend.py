from flask import Flask, request
from datetime import datetime
from Blockchain import Blockchain
import requests
import json
import threading
#Initialize
app = Flask(__name__)
blockchain = Blockchain()
peers = set()
#Helper functions
def json_reader(filename):
    with open(filename) as f:
        for line in f:
            yield json.loads(line)

@app.route('/new_transaction', methods = ['POST'])
def new_transaction():
    tx = request.get_json()
    required = ('from', 'to', 'amount', 'signature')
    for fields in required:
        if not tx.get(field):
            return "Invalid format", 404
    tx['timestamp'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    with open('thread_pool.json', 'a') as jfile:
        jfile.write(json.dumps(tx) + '\n')
        jfile.close()
    return 'Success'
