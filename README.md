# DeFi
A repository containing a list of DeFi protocols and how to interact them using python/brownie. 


### How to run 

- You need to fork Ethereum and deploy your contract there. To do so:
```brownie networks add Development network_name cmd=ganache-cli host=http://127.0.0.1 fork=[URL] accounts=10 mnemonic=brownie port=8545```
- I used `ALCHEMY API` to fork. You can register and get your API for free. 
- ```brownie run scripts/deploy_sc --network network_name```
- 
