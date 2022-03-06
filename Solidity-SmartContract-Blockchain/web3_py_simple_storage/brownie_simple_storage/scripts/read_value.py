from brownie import SimpleStorage, accounts, config


def read_contract():
    simple_storage = SimpleStorage()
    print(simple_storage.retrieve())


def main():
    read_contract()
