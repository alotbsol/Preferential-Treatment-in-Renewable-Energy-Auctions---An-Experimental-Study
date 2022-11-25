from distributions import DistributionGenerator
from players import Player

import random as random


class AuctionGenerator:
    def __init__(self, active_players=16, rym=0, random_seed=1618033):
        random.seed(a=random_seed)

        self.active_players = active_players
        self.rym = rym

        self.players_dic = {}
        self.results_storage = {}

        self.generate_players()

    def generate_players(self):
        for i in range(1, self.active_players + 1):
            self.players_dic["player{0}".format(i)] = Player()

    def generate_parameters(self):
        for i in self.players_dic:
            ws = random.random()
            other_costs = random.random()
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

