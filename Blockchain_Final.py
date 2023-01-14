
# Importing modules

import datetime      # To keep track of time, as each block has its own timestamp (exact date and time at which the block is created)
import json         # For encoding the blocks before hashing them
import hashlib      # For finding hashes for the blocks
from flask import Flask, jsonify      # For creating a web application interface

# Building the blockchain architecture

class Blockchain:

    def __init__(self):
        self.chain = []
        
        self.createblock(proof = 1, previous_hash="0"*64, grievant="Pranav", stamp=str(datetime.datetime.now()), complaint= None)

    def createblock(self, proof, previous_hash, grievant, stamp, complaint):
        
        # Defining the structure of our block
        block = {'number': len(self.chain) + 1,
                 'time': str(datetime.datetime.now()),
                 'prevhash': previous_hash,
                 'timestamp': stamp,
                 'grievant': grievant,
                 'proof': proof,
                 'grievance' : complaint
                 }

        # Establishing a cryptographic link
        self.chain.append(block)
        return block

    def getprevblock(self):
        return self.chain[-1]
    
    def proofofwork(self, prevproof):
        newproof = 1
        checkproof = False

        # Defining crypto puzzle for the miners and iterating until able to mine it 
        while checkproof is False:
            op = hashlib.sha256(str(newproof**2 - prevproof**5).encode()).hexdigest()
            
            if op[:5] == "00000":
                checkproof = True
            else:
                newproof += 1
        
        return newproof

    def hash(self, block):
        encodedblock = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encodedblock).hexdigest()

    def ischainvalid(self, chain):
        prevblock = chain[0]   # Initilized to Genesis block
        blockindex = 1         # Initilized to Next block

        while blockindex < len(chain):

            # First Check : For each block check if the previous hash field is equal to the hash of the previous block
            #               i.e. to verify the cryptographic link
            
            currentblock = chain[blockindex]
            if currentblock['prevhash'] != self.hash(prevblock):
                return False

            # Second Check : To check if the proof of work for each block is valid according to problem defined in proofofwork() function
            #                i.e. to check if the correct block is mined or not

            prevproof = prevblock['proof']
            currentproof = currentblock['proof']
            op = hashlib.sha256(str(currentproof**2 - prevproof**5).encode()).hexdigest()
            
            if op[:5] != "00000":
                return True

            prevblock = currentblock
            blockindex += 1

        return True



# Building a Flask based Web App for interacting with the blockchain
app = Flask(__name__)


# Creating a blockchain based on architecture defined
blockchain = Blockchain()


# Welcome page
@app.route('/', methods=['GET'])

def welcome():
    wl = '''
        <html>
        <head><title>Spyder</title></head>
        <body>
        <h1>Spyder Blockchain</h1>
        Welcome to our Blockchain Page
        <br>Lets Go !!!
        <br>
            <ul>
            <li>For Mining Blocks Visit : <a href="http://127.0.0.1:5000/mineblock">http://127.0.0.1:5000/mineblock</a></li>
            <li>For Viewing the Blockchain Visit : <a href="http://127.0.0.1:5000/getchain">http://127.0.0.1:5000/getchain</a></li>
            <li>For Validating Blockchain Visit : <a href="http://127.0.0.1:5000/validate">http://127.0.0.1:5000/validate</a></li>
            </ul>
        </body>
        </html>
        '''
#     wl = '''
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta http-equiv="X-UA-Compatible" content="IE=edge">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Greivance Registered</title>
#     <link rel="stylesheet" href="/home/deimos/Downloads>

# </head>

# <body>
#    <header>
#       <section class="box">
#           <img src="../static/images/Kliponious-green-tick.png">
#      <text> Grievance Submitted</text>
# <br/>
#      <text> corresponding block was succesfully mined. </text>
#          </section>
#   </header>
# </body>
# </html>
#     '''
    return wl


# Mining the blockchain
@app.route('/mineblock', methods=['GET'])

def mineblock():
    
    # Mining a new block
    prevblock = blockchain.getprevblock()
    prevproof = prevblock['proof']
    proof = blockchain.proofofwork(prevproof)
    prevhash = blockchain.hash(prevblock)
    if(prevblock['number']== 0):
        grievant =  "Pranav"
        stamp = str(datetime.datetime.now())
        grievance = "Ac not working properly in cs lab"
    elif(prevblock['number']== 1):
        grievant =  "Dhruvanshu"
        stamp = str(datetime.datetime.now())
        grievance = "Seniors ragged me and forced me to pay for their food"
    elif(prevblock['number']== 2):
        grievant =  "Soham"
        stamp = str(datetime.datetime.now())
        grievance = "Issue with Sophos Login"
    elif(prevblock['number']== 3):
        grievant =  "Ishaan"
        stamp = str(datetime.datetime.now())
        grievance = "Wifi not working in ht lab"
    elif(prevblock['number']== 4):
        grievant =  "Gauravi"
        stamp = str(datetime.datetime.now())
        grievance = "Mentally depressed due to degrading marks"
    elif(prevblock['number']== 5):
        grievant =  "Dhruvisha"
        stamp = str(datetime.datetime.now())
        grievance = "Eve teasing by Civil batch seniors"
    elif(prevblock['number']== 6):
        grievant =  "Sam"
        stamp = str(datetime.datetime.now())
        grievance = "Hostel D basin clogged"
    
    block = blockchain.createblock(proof, prevhash, grievant, stamp,grievance)

    # Sending the response to Postman API to display it
    response = {'message': "Congratulations, You just mined a block !", 
                'number': block['number'],
                'time': block['time'],
                'timestamp': block['timestamp'],
                'grievant': block['grievant'],
                'Complaint' : block['grievance'],
                'prevhash': block['prevhash'],
                'proof': block['proof']}

    return jsonify(response), 200


# Gwtting the full blockchain displayed in Postman
@app.route('/getchain', methods=['GET'])

def getchain():
    response = {'chain': blockchain.chain,
                'len': len(blockchain.chain)}
    return jsonify(response), 200


# Validating the Blockchain
@app.route('/validate', methods=['GET'])

def validate():
    if blockchain.ischainvalid(blockchain.chain):
        response = {'message': "The Blockchain is Valid"}
    else:
        response = {'message': "The Blockchain is Invalid"}

    return jsonify(response), 200


# Running the Web App
app.run(host='0.0.0.0', port=5000)
