from distributions import DistributionGenerator
from players import Player

import random as random
from operator import itemgetter


class AuctionGenerator:
    def __init__(self, active_players=16, rym=0, demand=3, supply=4,
                 maximum_bid=90.3, ws_min=5, ws_max=9, oc_min=0.8, oc_max=1.2,
                 random_seed=16180339):

        random.seed(a=random_seed)

        self.active_players = active_players
        self.rym = rym

        self.demand = demand
        self.supply = supply

        self.maximum_bid = maximum_bid

        self.ws_min = ws_min
        self.ws_max = ws_max
        self.oc_min = oc_min
        self.oc_max = oc_max

        self.InputDistribution = DistributionGenerator(min_ws=ws_min, max_ws=ws_max, base_lcoe=50)

        self.players_dic = {}
        self.results_storage = {"supply": [],
                                "demand": [],
                                "rym": [],
                                }

        self.number_of_groups = active_players/supply
        self.groups = {}

        self.current_round = 0

        self.generate_players()

    def generate_players(self):
        for i in range(1, self.active_players + 1):
            self.players_dic["player{0}".format(i)] = Player()

        self.current_round += 1

    def generate_parameters(self):
        for i in self.players_dic:
            """here randim generation should be done differently to prevent different number of players"""
            ws = random.randint(self.ws_min * 10, self.ws_max * 10) / 10
            other_costs = random.randint(self.oc_min * 100, self.oc_max * 100) / 100

            """ Loaded from original distributions"""
            ws_index = self.InputDistribution.distribution["ws"].index(ws)

            correction_factor = self.InputDistribution.distribution["correction_factor"][ws_index]
            lcoe = self.InputDistribution.distribution["lcoe"][ws_index] * other_costs

            if self.rym == 0:
                minimum_bid = lcoe
            else:
                minimum_bid = lcoe / correction_factor

            self.players_dic[i].update_parameters(ws=ws, other_costs=other_costs, lcoe=lcoe,
                                                  correction_factor=correction_factor, minimum_bid=minimum_bid,
                                                  rym=self.rym, maximum_bid=self.maximum_bid,
                                                  demand=self.demand, supply=self.supply,
                                                  current_round=self.current_round)

    def split_players(self):
        shuffled_players = random.shuffle(self.players_dic.keys())






    def update_demand_supply(self, demand, supply):
        self.demand = demand
        self.supply = supply

    def evaluate_round(self):
        placed_bids = {}
        for i in self.players_dic:
            placed_bids[str(i)] = Auctions.players_dic[i].my_bid

        """this should be shuffled to deal with equal bids"""
        winning_bids = dict(sorted(placed_bids.items(), key=itemgetter(1))[:self.demand])

        print("printing winning_bids", winning_bids)

        # store results to each player
        # store_round

    def evaluate_auction(self):
        pass


if __name__ == '__main__':
    Auctions = AuctionGenerator(active_players=4)
    print("players dictionary", Auctions.players_dic)

    Auctions.generate_parameters()

    for i in Auctions.players_dic:
        print("generated parameters:", i, Auctions.players_dic[i].parameters)

    for i in Auctions.players_dic:
       Auctions.players_dic[i].place_random_bid()
       print("placed bid:", i, Auctions.players_dic[i].my_bid)

    Auctions.evaluate_round()




