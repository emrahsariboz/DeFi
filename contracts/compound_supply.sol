// SPDX-License-Identifier: MIT

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "../interfaces/compound.sol";

pragma solidity ^0.8.0;

// Supply and Redeem
contract TestCompound {
    // Lending token
    IERC20 public token;

    // What we will receive
    CErc20 public cToken;

    constructor(address _token, address _cToken) {
        token = IERC20(_token);
        cToken = CErc20(_cToken);
    }

    function supply(uint256 _amount) external {
        token.transferFrom(msg.sender, address(this), _amount);
        token.approve(address(cToken), _amount);
        // Transfer _amount of token from SC
        // to cToken.
        require(cToken.mint(_amount) == 0, "mint failed");
    }

    // ctoken balance
    function getCTokenBalance() external view returns (uint256) {
        return cToken.balanceOf(address(this));
    }

    function getInfo()
        external
        returns (uint256 exchangeRate, uint256 supplyRate)
    {
        exchangeRate = cToken.exchangeRateCurrent();
        supplyRate = cToken.supplyRatePerBlock();
    }

    function estimateBalance() external returns (uint256) {
        uint256 cTokenBal = cToken.balanceOf(address(this));
        uint256 exchangeRate = cToken.exchangeRateCurrent();
        // Supply token is WBTC
        uint256 decimals = 8;
        uint256 cTokenDecimals = 8;

        return
            (cTokenBal * exchangeRate) / 10**(18 + decimals - cTokenDecimals);
    }

    function redeem(uint256 _cTokenAmount) external {
        require(cToken.redeem(_cTokenAmount) == 0, "redeem failed");
    }
}
