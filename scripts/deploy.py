from brownie import accounts, network, TestCompound, interface


def main():
    deploy()


def deploy():

    # ctoken (weth) address
    cWETH = "0xC11b1268C1A384e55C48c2391d8d480264A3A7F4"

    # weth address
    weth = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"

    # weth whale
    whale = "0xF04a5cC80B1E94C69B48f5ee68a08CD2F09A7c3E"

    contract = TestCompound.deploy(weth, cWETH, {"from": whale})

    print(contract)

    # Initialize
    print(
        "The balance of the whale account is ", interface.IERC20(weth).balanceOf(whale)
    )
