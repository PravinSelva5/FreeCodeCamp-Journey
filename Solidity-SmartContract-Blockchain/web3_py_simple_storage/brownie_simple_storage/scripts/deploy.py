from brownie import accounts
import os


def deploy_simple_storage():
    # account = accounts[0]
    # print(account)
    # account = accounts.load("freecodecamp-development-account")
    # print(account)
    account = accounts.add(os.getenv("PRIVATE_KEY"))
    print(account)


def main():
    deploy_simple_storage()
