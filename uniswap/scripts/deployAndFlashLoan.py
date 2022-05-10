import math
from brownie import accounts, network, Test, interface, config


def main():
    deploy()


def deploy():

    USDC_DECIMAL = 6

    BORROW_AMOUNT = math.pow(10, 6) * 1000000
    FUND_AMOUNT = math.pow(10, 6) * 2000000

    usdc_instance = interface.IERC20(config["addresses"]["USDC"])

    # Send some ether to cover gax

    contract = Test.deploy({"from": accounts[0]})

    usdc_instance.transfer(
        contract.address, FUND_AMOUNT, {"from": (config["addresses"]["USDC_WHALE"])}
    )

    print(
        "The balance of the whale is ",
        usdc_instance.balanceOf((config["addresses"]["USDC_WHALE"])),
    )

    print("Requesting flash loan")

    tx = contract.flashLoan(
        config["addresses"]["USDC"],
        BORROW_AMOUNT,
        {
            "from": config["addresses"]["USDC_WHALE"],
        },
    )

    tx.wait(1)

    for i in tx.events["Log"]:
        print(i)
