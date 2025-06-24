import pancake_swap_engine

engine = pancake_swap_engine.PancakeSwapEngine()
#engine.setkeys("0xYourPublicAddress", "your-private-key")
engine.setkeys("0x6a14CEf468FB30ee2402DFe5407b763b603baC26", "0x0c4baae9nigb87j87j897979565f56dfg")

# Full balance swap
engine.swapUsdtToCake()
engine.swapCakeToUsdt()

# Partial amount swap
engine.swapUsdtToCake(amount=1)      # 1 USDT → CAKE
engine.swapCakeToUsdt(amount=2.5)    # 2.5 CAKE → USDT
