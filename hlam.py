

        
    # def is_book_price_belov_price_threshold(self, asks, bids, price_threshold):
    #     asks_and_bids = []

    #     for ask, bid in zip(asks[:5], bids[:5]):
    #         if isinstance(ask, (list, tuple)) and len(ask) > 0:
    #             try:
    #                 ask_price = float(ask[0])
    #                 if ask_price != 0:
    #                     asks_and_bids.append(ask_price)
                        
    #             except:
    #                 pass
    #         if isinstance(bid, (list, tuple)) and len(bid) > 0:
    #             try:
    #                 bid_price = float(bid[0])
    #                 if bid_price != 0:
    #                     asks_and_bids.append(bid_price)
    #             except:
    #                 pass
    #     if (sum(asks_and_bids) != 0) and (len(asks_and_bids) != 0):                                                   
    #         last_bid_ask_price_sum = sum(asks_and_bids) / (len(asks_and_bids))
    #         if last_bid_ask_price_sum < price_threshold:
    #             # print(f"last_bid/ask_price: {last_bid_ask_price_sum}")
    #             return True            
    #     return False


    # def is_order_book_valid(self, asks, bids):
    #     total_ask_volume = 0
    #     total_ask_volume = 0
    #     try:          
    #         total_bid_volume = sum(float(bid[1]) for bid in bids if isinstance(bid, (list, tuple)))
    #         total_ask_volume = sum(float(ask[1]) for ask in asks if isinstance(ask, (list, tuple)))
    #     except Exception as ex:
    #         # print(ex)
    #         return False

    #     if total_bid_volume == 0:
    #         return False
    #     # print(total_bid_volume)
    #     # print(total_ask_volume)

    #     if total_bid_volume != 0 and total_ask_volume != 0:
        
    #         if total_ask_volume/total_bid_volume < self.price_threshold:
    #             return False
        
    #     return True