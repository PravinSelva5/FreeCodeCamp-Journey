import json
from web3 import Web3
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()


# Compile Our Solidity

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.0",
)


with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compile_sol["contracts"]["SimpleStorage.sol"]["abi"]

# to connect to ganache
w3 = Web3(Web3.HTTPProvider("http://0.0.0.0:7545"))
chain_id = 5777
my_address = "TYPE IN ADDRESS"
# Never hard-code your private key, store the variables using environment variables. The environment variables will be saved for the lifetime of the shell
# You can save the private key in a .env file but you need to add a .gitignore file so that when you push the code, the .env doesn't get pushed as well.
private_key = os.getenv("PRIVATE_KEY")

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latestest transaction
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)

"""
1. Build a transaction
2. Sign a transaction
3. Send a transaction
"""
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract...")
# Send this signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")

# Working with the contract
# Contract Address needed
# Contract ABI needed
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Call -> Simulate making the call and getting a return value
# Transact -> Actually make a state change

# Initial Value of favourite Number
print(simple_storage.functions.retrieve().call())
print("Updating Contract...")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce + 1}
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Updated!")

print(simple_storage.functions.store(15).call())
