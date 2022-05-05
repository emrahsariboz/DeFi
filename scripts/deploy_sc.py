from brownie import accounts, network, TestCompound, interface
from web3 import Web3
import time

# SUPPLY_AMOUNT = Web3.toWei(1, "ether")

SUPPLY_AMOUNT = 100000000


def main():
    deploy()


def deploy():

    # ctoken (weth) address
    cDAI = "0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643"

    # weth address
    DAI = "0x6B175474E89094C44Da98b954EedeAC495271d0F"

    # DAI whale
    whale = "0xcffad3200574698b78f32232aa9d63eabd290703"

    # cWBTC
    # cWBTC = "0xC11b1268C1A384e55C48c2391d8d480264A3A7F4"
    # wbtc = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"
    # wbtc

    contract = TestCompound.deploy(
        DAI,
        cDAI,
        {"from": whale},
    )

    print(contract)

    # Initialize
    print("The balance of the whale account is ", interface.ERC20(DAI).balanceOf(whale))

    print(
        "Giving permission for the smart contract to transfer the supply_amount from msg.sender"
    )
    tx = interface.ERC20(DAI).approve(contract.address, SUPPLY_AMOUNT, {"from": whale})

    tx.wait(1)

    print("Supplying DAI...")
    tx = contract.supply_token(SUPPLY_AMOUNT, {"from": whale})
    tx.wait(1)

    # print("Supplied DAI...")
