## IMC Prosperity 2
The 15 days of simulation of Prosperity are divided into 5 rounds. Each round lasts 72 hours. At the end of every round - before the timer runs out - all teams will have to submit their algorithmic and manual trades to be processed. The algorithms will then participate in a full day of trading against the Prosperity trading bots.
## Round 1
We were given 2 products to trade named AMETHYSTS and STARFRUIT. We realized that AMETHYSTS prices are stable throughtout the history while the value for STARFRUIT had been going up and down over time. For AMETHYSTS, we did the market-take and market-make around the mean price. We adjusted for penny jumping, which means the bid and ask prices always be one penny better than the best prices in the order book to make the orders more competitive. For STARFRUIT, we ran a linear regression to predict next prices based on historical prices in the cache. we continued doing market-make and market take for the predicted price adjusted by a predefined spread. The algorithmic trading results were quite reasonably and we got a profit of 30k. The manual trading was straightforward, we got a profit of 46k but it was quite low in comparing with average benchmark. 
 
At Round 1, we ended up with:
- Rank #2178 in Overall
- Rank #15 in Vietnam (National)
- Rank #411 in Algorithmic trading
- Rank #2467 in Manual trading

## Round 2
In round 2, a new product was introduced named "ORCHIDS". ORCHIDS are very delicate and their value is dependent on all sorts of observable factors like hours of sun light, humidity, shipping costs, in- & export tariffs and suitable storage space. To remain competitive and flexible in trading ORCHIDS, we set the dynamic price bounds around the calculated buy price incorporating with penny jumping. The purchase price was determined by adding the market ask to the sum of shipping cost and import tariff costs, indicating the total cost of acquiring the product. We also tried to improve our strategies for AMETHYSTS and STARFRUIT. For AMETHYSTS, we took the same trading logic as in round 1 but we predicted the future price instead of taking the mean price. We predicted the price using MACD and Volatility. Specifically, the MACD is calculated as the difference between the 12-period EMA and the 26-period EMA. We also had a 9-period EMA of the MACD itself, which is a signal line, acts as a trigger for buying and selling decisions. Then, we calculated the volatility of AMETHYSTS using the standard deviation of logarithmic returns. For the decision rules, if the MACD is positive (upward momentum) and the volatility is relatively low (we set it less than 5% of average price), the strategy predicts a 2% increase in price. Conversely, it predicts a 2% decrease. Otherwise, it predicts the price will remain stable around the last known price. For STARFRUIT, the method we used to predict the future price was by applying a smoothing constant to the price data. This gives more weight to recent observations while exponentially decreasing the weight for older observations. The smoothing level was set at 0.2 to control the rate at which the influence of older data decreases. The predicted price then was calculated as the last value from smoothing series. The manual trading in this round was to find the optimal profit for currency exchanging. Our sequence is Seashells -> Pizza -> Wasabi -> Seashells -> Pizza -> Seashells.

At Round 2 (accompany with results from the preceding round), we ended up with:
- Rank #116 in Overall
- Rank #2 in Vietnam (National)
- Rank #67 in Algorithmic trading
- Rank #1449 in Manual trading

  ### Updating...
