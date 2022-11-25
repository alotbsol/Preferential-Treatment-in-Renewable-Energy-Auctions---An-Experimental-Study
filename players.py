

class Player:
    def __init__(self, ):
        # specific project parameters
        self.parameters = {"ws": 0,
                           "other_costs": 0,
                           "lcoe": 0,
                           "correction_factor": 0,
                           "minimum_bid": 0}

        # duplicate info from general auction parameters
        self.maximum_bid = 0
        self.demand = 0
        self.supply = 0

        # related to players bids
        self.my_bid = 0
        self.potential_subsidy = 0
        self.potential_profit = 0

        # history of auctions and bids
        self.history = {}

    def update_parameters(self, ws, other_costs, lcoe, correction_factor, minimum_bid):
        self.parameters["ws"] = ws
        self.parameters["other_costs"] = other_costs
        self.parameters["lcoe"] = lcoe
        self.parameters["correction_factor"] = correction_factor
        self.parameters["minimum_bid"] = minimum_bid

    def graph_project(self):
        pass





