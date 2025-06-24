# 🥞 PancakeSwap V3 Python Trading Bot

A simple Python engine for swapping tokens (e.g., USDT ↔ CAKE) on **PancakeSwap V3** using `web3.py`.

## 🚀 Features

- Interacts with PancakeSwap V3 Router on Binance Smart Chain (BSC)
- Swaps between USDT and CAKE
- Uses Uniswap V3 style Quoter to get exact output preview
- Automatic approval before swap
- Handles nonce errors and uses `pending` nonce safely
- Human confirmation before swapping

---

## 📦 Requirements

- Python 3.7+
- Web3.py
- ABIs:
  - `quoter.json`
  - `router.json`
  - `erc20.json`

Install dependencies:

```bash
pip install web3==6.2.0
````

---

## 🔧 Setup

1. **Clone the repo**

```bash
git clone https://github.com/RetributionByRevenue/pancakeswap-v3-python-bot.git
cd pancakeswap-v3-python-bot
```

2. **Add ABI files**

Ensure the following files are present in the directory:

* `quoter.json` – PancakeSwap V3 Quoter contract ABI
* `router.json` – PancakeSwap V3 Router contract ABI
* `erc20.json` – Standard ERC20 ABI

> You can get ABIs from BscScan or the official PancakeSwap V3 repo.

---

## 🔑 Configure Wallet

Update your script to set your **wallet address and private key**:

```python
engine.setkeys('YOUR_PUBLIC_ADDRESS', 'YOUR_PRIVATE_KEY')
```

---

## 💱 Swap Tokens

### Swap USDT to CAKE

```python
engine.swapUsdtToCake(amount=1)  # amount in tokens (e.g. 1 USDT)
```

### Swap CAKE to USDT

```python
engine.swapCakeToUsdt(amount=1)  # amount in tokens (e.g. 1 CAKE)
```

---

## 🔐 Safety Tips

* This project is for educational purposes. Use at your own risk.
* Always test with small amounts or on testnet.
* Never hardcode private keys in production scripts.
* Consider using a `.env` file or secure key store.

---

## 🧠 License

MIT License

---

## 🙌 Acknowledgements

* [PancakeSwap V3](https://pancakeswap.finance)
* [Web3.py](https://web3py.readthedocs.io/)
* [Ethereum Developers](https://ethereum.org/developers/)

---

## 📬 Contact

For help or improvements, open an issue or PR!

```

Let me know if you want to customize this for a CLI interface, Docker deployment, or Telegram bot integration.
```


Please dontate 🥺 (i always need more BNB gas 😭)

BNB: 0xE80089A6158901469e4DD3c13ac01f39BDF9bEE5 
