from brownie import Test, accounts, interface
from web3 import Web3


def main():
    deploy()


def deploy():
    amount_in = Web3.toWei(1000000, "ether")

    # DAI address
    DAI = "0x6B175474E89094C44Da98b954EedeAC495271d0F"

    # DAI whale
    whale = "0xcffad3200574698b78f32232aa9d63eabd290703"

    WBTC = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"

    contract = Test.deploy({"from": whale})

    # Approve Contract
    tx = interface.IERC20(DAI).approve(contract.address, amount_in, {"from": whale})
    tx.wait(1)

    amount_out_min = 1
    token_int = DAI
    token_out = WBTC
    to = accounts[0]

    tx = contract.swap(
        DAI,
        WBTC,
        amount_in,
        amount_out_min,
        to,
        {
            "from": whale,
        },
    )
    tx.wait(1)

    print("The balance of to ", interface.IERC20(WBTC).balanceOf(to))
