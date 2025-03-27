# pancakeswapV3_simple_swap
Pancakeswapv3 CAKE&lt;->USDT in 100 lines of code

My thoughts:
Pancakeswapv3 was more tricky to develop for. 
The json files are Application Binary Interfaces (ABIs) and are needed for this to work. 

New to pancakeswap v3 is `amountOutMinimum` parameter which is how you define slippage. this feature is great. you see in my code, i am using 0.10% slippage, which is the cheapest you can use on the pancakeswap v3 ui as well.

From my testing, gas prices are much cheaper as well. This should be the primary reason why you should move over to V3.

Pancakeswapv3 expects you to now interface with the `Quoter smart contract` via the `quoteExactInputSingle` function, which is why pancakeswap v3 will not work with v2.

I recommend you to still use the fee of 0.25% like my code is using. This is because 95% of liquidity proviers are providing liquidity on this tier only. you will see, the  quote you can get is usually not good when you change the fee %. Also like Pancakeswap v2, the quote you can get sometimes is not market accurate so you should have logic to reject bad quotes.   

Please dontate 🥺 (i always need more BNB gas 😭)
BNB: 0xE80089A6158901469e4DD3c13ac01f39BDF9bEE5 
