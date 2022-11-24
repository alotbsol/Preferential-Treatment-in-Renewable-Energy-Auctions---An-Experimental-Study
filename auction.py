from distributions import DistributionGenerator


class AuctionGenerator:
    def __init__(self, active_players=16, rym=0,):
        self.active_players = active_players
        self.rym = rym

        self.players_dic = {}
        self.results_storage = {}

    def generate_round(self):
        pass

    def evaluate_round(self):
        pass

    def evaluate_auction(self):
        pass



