import json
from web3 import Web3

# In the video, we forget to `install_solc`
# from solcx import compile_standard
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv

load_dotenv()


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# We add these two lines that we forgot from the video!
install_solc("0.6.0")

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get ABI
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connecting to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x68cca1eDcbdd5dC39041F142FFb65e0A2fC766ba"
private_key = os.getenv("PRIVATE_KEY")


# Create the contract on python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
print(SimpleStorage)

# Account Nonces just track the number of transactions made.
nonce = w3.eth.getTransactionCount(my_address)

# 1. Build a Transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)

# 2. Sign a Transaction
# NEVER HARD CODE YOUR PRIVATE KEY
# USE ENVIRONMENT VARIABLES
#### THE ECHO approach is only valid while the shell is live. Once the shell is closed, the environment variables will be lost
signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)

# 3. Send a transaction
tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


# Working with the contract
### YOU ALWAYS NEED TWO THINGS:
######## Contract Address ########
######## Contract ABI ########
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Now that you have the contract address & abi, you can start interacting with it

# Call -> Simulate making the call and getting a return value. It's important to know that Calls don't make a state change
# Transact -> Actually makes a state change

# Initial value of the stored number
print(simple_storage.functions.retrieve().call())
print(simple_storage.functions.store().call())
