from web3 import Web3 #web3 6.0.2
from web3.middleware import geth_poa_middleware #web3 6.0.2
import json
import requests

# Step 1: Setup Web3
web3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Step 2: Load ABIs and Define Contracts
with open('quoter.json') as f:
    QUOTER_ABI = json.load(f)

with open('erc20.json') as f:
    ERC20_ABI = json.load(f)

with open('router.json') as f:
    ROUTER_V3_ABI = json.load(f)


QUOTER_CONTRACT_ADDRESS = web3.to_checksum_address('0xB048Bbc1Ee6b733FFfCFb9e9CeF7375518e25997')  # PancakeSwap QuoterV2
QUOTER_CONTRACT = web3.eth.contract(address=QUOTER_CONTRACT_ADDRESS, abi=QUOTER_ABI)

BASE_TOKEN_ADDRESS =  web3.to_checksum_address('0x55d398326f99059fF775485246999027B3197955')
BASE_TOKEN_CONTRACT = web3.eth.contract(address=BASE_TOKEN_ADDRESS, abi=ERC20_ABI)

ROUTER_V3_ADDRESS = web3.to_checksum_address('0x13f4EA83D0bd40E75C8222255bc855a974568Dd4')  # PancakeSwap V3 Router
ROUTER_CONTRACT = web3.eth.contract(address=ROUTER_V3_ADDRESS, abi=ROUTER_V3_ABI)

# Step 3: Define Constants
DESIRE_TOKEN_ADDRESS = web3.to_checksum_address('0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82')
FEE = 2500  # 0.25% fee
amount = 1
amount_in_wei = int(amount * 10 ** 18)
user_address = "0xE80089A6158901469e4DD3c13ac01f39BDF9bEE5"# Replace with your actual wallet address
private_key = "input your private key"  

# Step 4: Get Gas Price
gas_price = int(web3.eth.gas_price * 1.1) # Fetch the current gas price from the network
print(f"Current Gas Price: {gas_price}")



# Step 5: Get a Quote
quote = QUOTER_CONTRACT.functions.quoteExactInputSingle(
    (BASE_TOKEN_ADDRESS, DESIRE_TOKEN_ADDRESS, amount_in_wei, FEE, 0)
).call()
print("Quote Object Recived", quote)
print(f"Quote received in human readable format: {quote[0] / 10**18} USDT")
acceptable_slippage_human_readable= (quote[0] / 10**18)*0.999
acceptable_slippage_wei = int(acceptable_slippage_human_readable * 10**18)
print("the defined slippage is:", acceptable_slippage_human_readable )
print("the defined slippage in wei:", acceptable_slippage_wei)

# Step 5.5: User Confirmation Before Proceeding
quote_human_readable = quote[0] / 10**18
acceptable_slippage_human_readable = quote_human_readable * 0.999
acceptable_slippage_wei = int(acceptable_slippage_human_readable * 10**18)

# Calculate percentage difference
percentage_difference = (1 - 0.999) * 100  # Since 0.999 is 99.9%

print(f"Quote received: {quote_human_readable:.6f} USDT")
print(f"Acceptable Slippage: {acceptable_slippage_human_readable:.6f} USDT")
print(f"Slippage Difference: {percentage_difference:.2f}%")

user_input = input("Proceed with the transaction? (yes/no): ").strip().lower()
if user_input != "yes":
    print("Transaction canceled.")
    exit()

# Step 6: Approve Router to Spend Tokens
amount_to_approve = web3.to_wei(amount+1, 'ether')  # Allow router to spend 10 CAKE (you can increase this)

tx = BASE_TOKEN_CONTRACT.functions.approve(
    ROUTER_V3_ADDRESS, amount_to_approve
).build_transaction({
    'from': user_address,
    'gas': 1000000,  # ✅ Correct gas limit for approval
    'gasPrice': gas_price,
    'nonce': web3.eth.get_transaction_count(user_address),
})

# Step 7: Sign & Send Approval Transaction
signed_tx = web3.eth.account.sign_transaction(tx, private_key)
tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
print(f"Approval TX Hash: {web3.to_hex(tx_hash)}")


# Step 8: Perform the Swap
swap_tx = ROUTER_CONTRACT.functions.exactInputSingle({
    'tokenIn': BASE_TOKEN_ADDRESS,
    'tokenOut': DESIRE_TOKEN_ADDRESS,
    'fee': FEE,
    'recipient': user_address,
    'deadline': web3.eth.get_block('latest')['timestamp'] + 300,  # 5-minute deadline
    'amountIn': amount_in_wei,
    'amountOutMinimum': acceptable_slippage_wei,  # Accept any output amount (adjust if needed)
    'sqrtPriceLimitX96': 0  # No price limit
}).build_transaction({
    'from': user_address,
    'gas': 1000000,  
    'gasPrice': gas_price,
    'nonce': web3.eth.get_transaction_count(user_address)+1,
})

# Sign and send the swap transaction
signed_swap_tx = web3.eth.account.sign_transaction(swap_tx, private_key)
swap_tx_hash = web3.eth.send_raw_transaction(signed_swap_tx.raw_transaction)
print(f"Swap TX Hash: {web3.to_hex(swap_tx_hash)}")


