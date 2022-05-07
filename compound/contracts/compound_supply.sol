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

    function supply_token(uint256 _amount) external {
        token.transferFrom(msg.sender, address(this), _amount);
        token.approve(address(cToken), _amount);
        uint256 mintResult = cToken.mint(_amount);
        require(mintResult == 0, "Somthing is wrong");
    }

    function getCTokenBalance() public view returns (uint256) {
        return cToken.balanceOf(address(this));
    }

    function getInfo()
        external
        returns (uint256 exchangeRate, uint256 supplyRate)
    {
        exchangeRate = cToken.exchangeRateCurrent();
        supplyRate = cToken.supplyRatePerBlock();
    }

    function estimateBalanceOfUnderlying() external returns (uint256) {
        uint256 cTokenBalance = cToken.balanceOf(address(this));
        uint256 exchangeRate = cToken.exchangeRateCurrent();

        uint256 decimals = 18;

        return (cTokenBalance * exchangeRate) / 10**18;
    }

    function balanceOfUnderlying() external returns (uint256) {
        return cToken.balanceOfUnderlying(address(this));
    }

    function redeem(uint256 _cTokenAmount) external {
        require(cToken.redeem(_cTokenAmount) == 0, "redeed failed!");
    }

    Comptroller public comptroller =
        Comptroller(0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B);

    PriceFeed public priceFeed =
        PriceFeed(0x922018674c12a7F0D394ebEEf9B58F186CdE13c1);

    function getCollateralFactor() external view returns (uint256, bool) {
        (bool isListed, uint256 colFactor, bool isComped) = comptroller.markets(
            address(cToken)
        );
        return (colFactor, isComped);
    }

    function getAccountLiquidity() external view returns (uint256 liquidity) {
        (uint256 error, uint256 _liquidity, uint256 _shortfall) = comptroller
            .getAccountLiquidity(address(this));

        require(error == 0, "error");
        return (_liquidity);
    }

    function getPriceFeed(address _cToken) external view returns (uint256) {
        return priceFeed.getUnderlyingPrice(_cToken);
    }

    function borrow(address _cTokenBorrow, uint256 _decimals) external {
        // Enter the market
        address[] memory cTokens = new address[](1);
        cTokens[0] = address(cToken);
        uint256[] memory errors = comptroller.enterMarkets(cTokens);

        require(errors[0] == 0, "Comptroller enterMarkets failed");

        // Check liquidity
        (uint256 error, uint256 _liquidity, uint256 shortfall) = comptroller
            .getAccountLiquidity(address(this));

        require(error == 0, "error");
        require(shortfall == 0, "shortfall >0 ");
        require(_liquidity > 0, "liqudity = 0");

        // Get max barrow
        uint256 price = priceFeed.getUnderlyingPrice(_cTokenBorrow);
        uint256 maxBorrow = (_liquidity * (_decimals)) / price;

        require(maxBorrow > 0, "You cant borrow");

        uint256 amount = (maxBorrow * 50) / 100;
        require(CErc20(_cTokenBorrow).borrow(amount) == 0, "borrow failed");
    }

    function getBorrowedBalance(address _cTokenBorroed)
        public
        returns (uint256)
    {
        return CErc20(_cTokenBorroed).borrowBalanceCurrent(address(this));
    }

    function repay(
        address _tokenBorrowed,
        address _cTokenBorrowed,
        uint256 _amount
    ) external {
        IERC20(_tokenBorrowed).approve(_cTokenBorrowed, _amount);
        require(
            CErc20(_tokenBorrowed).repayBorrow(_amount) == 0,
            "repay failed"
        );
    }
}
