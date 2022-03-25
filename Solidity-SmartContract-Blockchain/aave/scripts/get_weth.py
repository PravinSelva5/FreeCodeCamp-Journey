from scripts.helpful_scripts import get_account
from brownie import interface, config, network, accounts


def main():
    get_weth()


def get_weth():
    """
    Mints wETH by depositing ETH
    """
    # To interact with the kovan wETH contract, we need to interact with an ABI and Contract Address
    account = get_account()
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value": 0.1 * 10**18})
    tx.wait(1)
    print(f"Received 0.1 wETH")
    return tx
