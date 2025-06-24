from web3 import Web3
from web3.middleware import geth_poa_middleware
import json

class PancakeSwapEngine:
    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        self.user_address = None
        self.private_key = None

        # Constants
        self.FEE = 2500
        self.BASE_TOKEN_ADDRESS = self.web3.to_checksum_address('0x55d398326f99059fF775485246999027B3197955')  # USDT
        self.DESIRE_TOKEN_ADDRESS = self.web3.to_checksum_address('0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82')  # CAKE
        self.QUOTER_CONTRACT_ADDRESS = self.web3.to_checksum_address('0xB048Bbc1Ee6b733FFfCFb9e9CeF7375518e25997')
        self.ROUTER_V3_ADDRESS = self.web3.to_checksum_address('0x13f4EA83D0bd40E75C8222255bc855a974568Dd4')

        # Load ABIs
        with open('quoter.json') as f:
            self.QUOTER_ABI = json.load(f)
        with open('erc20.json') as f:
            self.ERC20_ABI = json.load(f)
        with open('router.json') as f:
            self.ROUTER_V3_ABI = json.load(f)

        # Contracts
        self.QUOTER_CONTRACT = self.web3.eth.contract(address=self.QUOTER_CONTRACT_ADDRESS, abi=self.QUOTER_ABI)
        self.BASE_TOKEN_CONTRACT = self.web3.eth.contract(address=self.BASE_TOKEN_ADDRESS, abi=self.ERC20_ABI)
        self.DESIRE_TOKEN_CONTRACT = self.web3.eth.contract(address=self.DESIRE_TOKEN_ADDRESS, abi=self.ERC20_ABI)
        self.ROUTER_CONTRACT = self.web3.eth.contract(address=self.ROUTER_V3_ADDRESS, abi=self.ROUTER_V3_ABI)

    def setkeys(self, public, private):
        self.user_address = self.web3.to_checksum_address(public)
        self.private_key = private

    def _get_gas_price(self):
        return int(self.web3.eth.gas_price * 1.1)

    def _get_nonce(self):
        return self.web3.eth.get_transaction_count(self.user_address, 'pending')

    def _approve_token(self, token_contract, amount, nonce):
        tx = token_contract.functions.approve(
            self.ROUTER_V3_ADDRESS, amount
        ).build_transaction({
            'from': self.user_address,
            'gas': 100000,
            'gasPrice': self._get_gas_price(),
            'nonce': nonce,
        })
        signed = self.web3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed.raw_transaction)
        print(f"[+] Approved token - TX: {self.web3.to_hex(tx_hash)}")
        self.web3.eth.wait_for_transaction_receipt(tx_hash)

    def _confirm_swap(self, amount_in, token_in, token_out):
        quote = self.QUOTER_CONTRACT.functions.quoteExactInputSingle(
            (token_in, token_out, amount_in, self.FEE, 0)
        ).call()

        amount_out = quote[0]
        min_amount_out = int((amount_out / 10 ** 18) * 0.999 * 10 ** 18)

        print(f"[!] Quoted Output: {amount_out / 10**18:.6f} tokens")
        print(f"[!] Min Acceptable After 0.1% Slippage: {min_amount_out / 10**18:.6f} tokens")
        confirm = input("Do you want to proceed with this swap? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("[x] Swap cancelled by user.")
            return None
        return min_amount_out

    def _swap(self, token_in, token_out, token_contract, amount_in=None):
        if amount_in is None:
            amount_in = token_contract.functions.balanceOf(self.user_address).call()
        else:
            amount_in = int(float(amount_in) * 10 ** 18)

        if amount_in == 0:
            print("[!] No balance to swap.")
            return

        min_amount_out = self._confirm_swap(amount_in, token_in, token_out)
        if min_amount_out is None:
            return

        nonce = self._get_nonce()
        self._approve_token(token_contract, amount_in, nonce)
        nonce += 1

        tx = self.ROUTER_CONTRACT.functions.exactInputSingle({
            'tokenIn': token_in,
            'tokenOut': token_out,
            'fee': self.FEE,
            'recipient': self.user_address,
            'deadline': self.web3.eth.get_block('latest')['timestamp'] + 300,
            'amountIn': amount_in,
            'amountOutMinimum': min_amount_out,
            'sqrtPriceLimitX96': 0
        }).build_transaction({
            'from': self.user_address,
            'gas': 500000,
            'gasPrice': self._get_gas_price(),
            'nonce': nonce,
        })

        signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"[+] Swap TX Hash: {self.web3.to_hex(tx_hash)}")

    def swapUsdtToCake(self, amount=None):
        print("[*] Swapping USDT to CAKE")
        self._swap(
            token_in=self.BASE_TOKEN_ADDRESS,
            token_out=self.DESIRE_TOKEN_ADDRESS,
            token_contract=self.BASE_TOKEN_CONTRACT,
            amount_in=amount
        )

    def swapCakeToUsdt(self, amount=None):
        print("[*] Swapping CAKE to USDT")
        self._swap(
            token_in=self.DESIRE_TOKEN_ADDRESS,
            token_out=self.BASE_TOKEN_ADDRESS,
            token_contract=self.DESIRE_TOKEN_CONTRACT,
            amount_in=amount
        )
