from flask import Flask
import requests
from data_process import add_transaction,add_block,get_blockchain
class webAgent:

    app = Flask('webAgent')
    ### node include the active ip address that run webAgent in network
    node = {}

    ### the method to send block to other people
    def send_block(block):
        for ip in node.keys():
            r = requests.post(ip, json=block,timeout = 5)

    ### the method to send transaction to other people
    def send_transaction(transaction):
         for ip in node.keys():
             r = requests.post(ip,json=transaction,timeout = 5)
    
    ### check all the active ip that run webAgent and add to node
    def __check_active(ip,pubKey):
        print(ip+':')
        ip += ':8080'
        content = {'pubKey':pubkey,'ip':get_My_ip()}
        try:
            r = requests.post(ip, json=content,timeout = 5)
            node[ip] = r.text
            print(ip+':'+node[ip])
        except:
            print('Not webAgent')
    ### deal with receive message 
    @app.route('./',methods = ['post'])
    def __receive_message():
        content = requests.json
        valid = True
        if 'pubKey' in content:
            if content['ip'] not in node.keys(): 
                node[content['ip']] = content['pubKey']
            return publicKey
        if content['type'] == 'Transaction':
            valid = add_transaction(content)
        if content['type'] == 'Block':
            valid = add_block(content)
        return valid
    
    ### send your blockchain
    @app.route('./',methods = ['get'])
    def __send_blockchain():
        return get_blockchain()
 
    ### the functin to start work
    def __init__(pubKey):
        publicKey = pubKey
        active_ip = list_all_ip()
        for i in active_ip:
            check_active()
        app.run(host = '0.0.0.0',port = 8080)
    
   
