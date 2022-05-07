from brownie import accounts, network, TestCompound, interface
from web3 import Web3
import time

SUPPLY_AMOUNT = Web3.toWei(1000, "ether")


def snapshot(TestCompound, DAI, cDAI):
    exchangeRate, supplyRate = TestCompound.getInfo.call()

    return (
        exchangeRate,
        supplyRate,
        TestCompound.estimateBalanceOfUnderlying.call(),
        TestCompound.balanceOfUnderlying.call(),
        DAI.balanceOf(TestCompound.address),
        cDAI.balanceOf(TestCompound.address),
    )


def main():
    deploy()


def deploy():

    # ctoken (weth) address
    cDAI = "0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643"

    # weth address
    DAI = "0x6B175474E89094C44Da98b954EedeAC495271d0F"

    # DAI whale
    whale = "0xcffad3200574698b78f32232aa9d63eabd290703"

    token_to_borrow = "0x0D8775F648430679A709E98d2b0Cb6250d2887EF"
    c_token_to_borrow = "0x6C8c6b02E7b2BE14d4fA6022Dfd6d75921D90E4E"
    bat_whale = "0x12274c71304bC0E6B38a56b94D2949B118feb838"

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

    print("Supplied DAI...")

    print("Checking the cDAI balance of the contract")
    print(contract.getCTokenBalance())

    # tx = contract.getInfo({"from": whale})
    # print(
    #     f"Current exchange rate is {tx.return_value[0]} and supplyRate is {tx.return_value[1]}"
    # )

    # print("----- SNAPSHOT ----")
    # dai_instance = interface.ERC20(DAI)
    # cdai_instance = interface.ERC20(cDAI)

    # exR, spR, estimatedB, balance, daiB, cDaiB = snapshot(
    #     contract, dai_instance, cdai_instance
    # )
    # print(
    #     f"The exchangerate is {exR}\nThe supply rate is {spR}\nThe estimated balance is {estimatedB}\nThe balance is {balance}\nThe dai balanc of contract is {daiB}\nThe cDAI balance of contract is {cDaiB}"
    # )

    # print("-------- REDEEM -------")
    # tx = contract.redeem(cDaiB, {"from": whale})
    # tx.wait(1)

    # exR, spR, estimatedB, balance, daiB, cDaiB = snapshot(
    #     contract, dai_instance, cdai_instance
    # )
    # print(
    #     f"\nThe dai balance of contract after reed is {daiB}\nThe cDAI balance of contract after reed is {cDaiB}"
    # )

    # print("Checking the collateral factor...")
    # colFactor, isTrue = contract.getCollateralFactor.call({"from": whale})
    # print("Token is available? ", isTrue)
    # print("Colleral factor is ", colFactor)

    # price = contract.getPriceFeed(cDAI)

    # print("Price feed", price)

    print()
    print("Price of BAT token", contract.getPriceFeed(c_token_to_borrow))
    print("Getting colleteral factor..")
    print(contract.getCollateralFactor())
    print(contract.getAccountLiquidity.call())
    tx = contract.borrow(c_token_to_borrow, 18, {"from": whale})
    tx.wait(1)

    print("Checking the BAT amount of contract...")
    bat_balance = interface.CErc20(token_to_borrow).balanceOf(contract.address)
    print(bat_balance)
