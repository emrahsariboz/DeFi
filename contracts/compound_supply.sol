pragma solidity ^0.8;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "../interfaces/compound.sol";

// supply
// borrow
// repay
// redeem

contract TestCompound {
    IERC20 public token;
    CErc20 public cToken;

    event Allowence2(uint256);

    constructor(address _token, address _cToken) {
        token = IERC20(_token);
        cToken = CErc20(_cToken);
    }

    function supply_token(uint256 _amount) external payable {
        token.transferFrom(msg.sender, address(this), _amount);
        token.approve(address(cToken), _amount);
        uint256 mintResult = cToken.mint(_amount);

        require(mintResult == 0, "Somthing is wrong");
    }

    fallback() external payable {}
}
