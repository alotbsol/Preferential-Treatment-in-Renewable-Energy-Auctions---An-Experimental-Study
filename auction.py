from distributions import DistributionGenerator
from players import Player

import random as random


class AuctionGenerator:
    def __init__(self, active_players=16, rym=0, ws_min=5, ws_max=9, oc_min=0.8, oc_max=1.2, random_seed=1618033):
        random.seed(a=random_seed)

        self.active_players = active_players
        self.rym = rym

        self.ws_min = ws_min
        self.ws_max = ws_max
        self.oc_min = oc_min
        self.oc_max = oc_max

        InputDistribution = DistributionGenerator(min_ws=ws_min, max_ws=ws_max, base_lcoe=50)

        self.players_dic = {}
        self.results_storage = {}

        self.generate_players()

    def generate_players(self):
        for i in range(1, self.active_players + 1):
            self.players_dic["player{0}".format(i)] = Player()

    def generate_parameters(self):
        for i in self.players_dic:
            ws = random.randint(self.ws_min * 10, self.ws_max * 10) / 10
            other_costs = random.randint(self.oc_min * 100, self.oc_max * 100) / 100
            """ Needs to be loaded from original distributions"""

            # list.index(element, start, end)

            lcoe = random.random()
            correction_factor = random.random()
            minimum_bid = random.random()

            self.players_dic[i].update_parameters(ws=ws, other_costs=other_costs, lcoe=lcoe,
                                                  correction_factor=correction_factor, minimum_bid=minimum_bid)

    def generate_round(self):
        pass

    def evaluate_round(self):
        pass

    def evaluate_auction(self):
        pass


if __name__ == '__main__':
    Auctions = AuctionGenerator(active_players=2)
    print(Auctions.players_dic)

    Auctions.generate_parameters()

    for i in Auctions.players_dic:
        print(Auctions.players_dic[i].parameters)

