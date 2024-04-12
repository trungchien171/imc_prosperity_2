import collections
from datamodel import OrderDepth, TradingState, Order
from typing import List
import numpy as np
import math
import pandas as pd
import json
import jsonpickle

class Vwap_amethysts:
    def __init__(self, bv=0, sv=0, bpv=0, spv=0):
        self.buy_volume = bv
        self.sell_volume = sv
        self.buy_price_volume = bpv
        self.sell_price_volume = spv

class Data:
    def __init__(self):
        self.amethysts_vwap = Vwap_amethysts()
        self.starfruit_cache = []

class Trader:
    INF = int(1e9)
    STARFRUIT_CACHE_SIZE = 39
    position = {'AMETHYSTS': 0, 'STARFRUIT': 0}
    POSITION_LIMIT = {'AMETHYSTS' : 20, 'STARFRUIT' : 20}
    amethysts_spread = 1
    amethysts_default_price = 10_000
    starfruit_spread = 2

    def predict_amethysts_price(self, orders):
        total_volume = sum(amount for _, amount in orders.items())
        total_price_volume = sum(price * amount for price, amount in orders.items())
        if total_volume == 0:
            return 0
        return total_price_volume / total_volume

    def predict_starfruit_price(self, cache):
        x = np.array([i for i in range(self.STARFRUIT_CACHE_SIZE)])
        y = np.array(cache)
        A = np.vstack([x, np.ones(len(x))]).T
        m, c = np.linalg.lstsq(A, y, rcond=None)[0]
        return int(round(self.STARFRUIT_CACHE_SIZE*m + c))
    
    def get_volume_and_best_price(self, orders, buy_order):
        volume = 0
        best = 0 if buy_order else self.INF

        for price, vol in orders.items():
            if buy_order:
                volume += vol
                best = max(best, price)
            else:
                volume -= vol
                best = min(best, price)

        return volume, best
    
    def compute_orders(self, product, order_depth, acc_bid, acc_ask):
        orders: list[Order] = []
        
        sell_orders = collections.OrderedDict(sorted(order_depth.sell_orders.items()))
        buy_orders = collections.OrderedDict(sorted(order_depth.buy_orders.items(), reverse=True))

        sell_vol, best_sell_price = self.get_volume_and_best_price(sell_orders, buy_order=False)
        buy_vol, best_buy_price = self.get_volume_and_best_price(buy_orders, buy_order=True)

        position = self.position[product]
        limit = self.POSITION_LIMIT[product]

        penny_buy = best_buy_price+1
        penny_sell = best_sell_price-1

        bid_price = min(penny_buy, acc_bid)
        ask_price = max(penny_sell, acc_ask)

        for ask, vol in sell_orders.items():
            if position < limit and (ask <= acc_bid or (position < 0 and ask == acc_bid+1)): 
                num_orders = min(-vol, limit - position)
                position += num_orders
                orders.append(Order(product, ask, num_orders))

        if position < limit:
            num_orders = limit - position
            orders.append(Order(product, bid_price, num_orders))
            position += num_orders

        position = self.position[product]

        for bid, vol in buy_orders.items():
            if position > -limit and (bid >= acc_ask or (position > 0 and bid+1 == acc_ask)):
                num_orders = max(-vol, -limit-position)
                position += num_orders
                orders.append(Order(product, bid, num_orders))

        if position > -limit:
            num_orders = -limit - position
            orders.append(Order(product, ask_price, num_orders))
            position += num_orders 

        return orders

    def run(self, state: TradingState):
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        result = {}
 
        for product in state.order_depths:
            self.position[product] = state.position[product] if product in state.position else 0

        if state.traderData == '':
            data = Data()
        else:
            data = jsonpickle.decode(state.traderData)
        
        global price_history_starfruit
        for product in state.order_depths:
            position = state.position[product] if product in state.position else 0
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            if product == 'AMETHYSTS':
                orders += self.compute_orders(product, order_depth, self.amethysts_default_price - self.amethysts_spread, self.amethysts_default_price + self.amethysts_spread)
                result[product] = orders
                

            if product == "STARFRUIT":  
                if len(data.starfruit_cache) == self.STARFRUIT_CACHE_SIZE:
                    data.starfruit_cache.pop(0)

                _, best_sell_price = self.get_volume_and_best_price(order_depth.sell_orders, buy_order=False)
                _, best_buy_price = self.get_volume_and_best_price(order_depth.buy_orders, buy_order=True)

                data.starfruit_cache.append((best_sell_price+best_buy_price)/2)

                lower_bound = -self.INF
                upper_bound = self.INF

                if len(data.starfruit_cache) == self.STARFRUIT_CACHE_SIZE:
                    lower_bound = self.predict_starfruit_price(data.starfruit_cache)-self.starfruit_spread
                    upper_bound = self.predict_starfruit_price(data.starfruit_cache)+self.starfruit_spread


                orders += self.compute_orders(product, order_depth, lower_bound, upper_bound)

                result[product] = orders

        traderData = jsonpickle.encode(data)
        conversions = 1
        return result, conversions, traderData