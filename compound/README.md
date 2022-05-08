
### Steps were taken to borrow Compound token...

1. Supply token that `Compound` supports. In my example, I supply 1000 DAI and receive the corresponding cDAI amount (`4547571263467` as of May 7, 22). This amount is calculated using the `exchange rate`. 1000 DAI I supplied is what is called `Collateral`. 
2. `Collateral Factor` is a term that describes how much someone can borrow after the `suply`. For example, the collateral factor of DAI is 0.80\%, which means I can borrow a max of approximately $800 worth of any asset Compound supports. Check step 4 to see how to learn this amount.
3. Once the cDAI token is received, it is time for what is called `EnterMarket`. You need to entermarket with cDAI tokens, which is a way of saying I want to use these as collateral. `comptroller.enterMarkets(cTokens);`
4. To check how much account liquidity (total amount you can borrow in USD), you can call `getAccountLiquidity(address(contract))` on `Comptroller`. It returns three values error, liquidity and shortFall. Error required to be 0 in order and liquidity represents how much you can borrow before getting liquidated.
5. Finally, call `borrow` function of cERC20 token you want to borrow.

