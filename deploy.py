import json
import os
from solcx import compile_standard, install_solc
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        'language': 'Solidity',
        'sources': {'SimpleStorage.sol': {'content': simple_storage_file}},
        'settings': {
            'outputSelection': {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            
        },
    },
    solc_version = install_solc("0.6.0")
)

# with open('compiled_code.json', 'w') as file:
    #json.dump(compiled_sol, file)

# get byte code
bytecode =  compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['evm'][
    'bytecode']['object']

# get abi
abi = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['abi']

# connecting to ganache (simulated blockchain network)
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
chain_id = 1337
my_address = '0xc073360E02049DacdAd9Cad9eC3BD49Fc11D44Fc'
private_key = os.getenv('PRIVATE_KEY')

# creating contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# Creating a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)

# Signing the transaction
signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# Sending the transaction
print('Deploying contract...\n')
send_transaction = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
transaction_receipt = w3.eth.wait_for_transaction_receipt(send_transaction)

print('Deployed!\n')

# working with contract requires the abi and contract address
simple_storage = w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)
print(simple_storage.functions.retrieve().call())

# Create new store transaction
print('Updating contract...\n')
store_transaction = simple_storage.functions.store(23).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
sign_store_transaction = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key)
send_store_transaction = w3.eth.send_raw_transaction(sign_store_transaction.rawTransaction)
store_receipt = w3.eth.wait_for_transaction_receipt(send_store_transaction)

print('Updated!\n')
print(simple_storage.functions.retrieve().call())