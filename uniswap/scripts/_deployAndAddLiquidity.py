from lib2to3.pgen2 import token
from brownie import Test, accounts, interface
from eth_utils import to_wei
from web3 import Web3


def main():
    deploy()


def deploy():
    amount_in = Web3.toWei(1000000, "ether")

    # DAI address
    DAI = "0x6B175474E89094C44Da98b954EedeAC495271d0F"

    # DAI whale
    DAI_WHALE = "0xcffad3200574698b78f32232aa9d63eabd290703"

    # WETH
    WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"

    # WETH whale
    WETH_WHALE = "0xeD1840223484483C0cb050E6fC344d1eBF0778a9"

    print("===Transferring gas cost covers===")
    # covering the transaction cost
    # accounts[0].transfer(DAI_WHALE, "1 ether")
    # accounts[0].transfer(WETH_WHALE, "1 ether")

    tokenA = interface.IERC20(DAI)
    tokenB = interface.IERC20(WETH)
    print("===Transferring the tokenA and tokenB amounts from whales to account[0]===")
    tokenA.transfer(accounts[0], Web3.toWei(2400, "ether"), {"from": DAI_WHALE})
    tokenB.transfer(accounts[0], Web3.toWei(1, "ether"), {"from": WETH_WHALE})

    contract = Test.deploy({"from": accounts[0]})

    tokenA.approve(contract.address, Web3.toWei(2400, "ether"), {"from": accounts[0]})
    tokenB.approve(contract.address, Web3.toWei(1, "ether"), {"from": accounts[0]})

    print("Adding liquidity...")
    tx = contract.addLiquidity(
        DAI,
        WETH,
        Web3.toWei(2400, "ether"),
        Web3.toWei(1, "ether"),
        {"from": accounts[0]},
    )
    tx.wait(1)

    print("Added Liquidity...")

    for i in tx.events["Log"]:
        print(i)

    print("=== Removing Liquidity ===")

    tx = contract.removeLiquidity(DAI, WETH, {"from": accounts[0]})

    tx.wait(1)

    for i in tx.events["Log"]:
        print(i)
