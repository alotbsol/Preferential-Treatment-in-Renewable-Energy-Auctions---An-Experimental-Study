import random


class Player:
    def __init__(self, my_name):
        # specific project parameters
        self.my_name = my_name

        self.parameters = {"ws": 0,
                           "production": 0,
                           "other_costs": 0,
                           "cost_A": 0,
                           "cost_B": 0,
                           "cost": 0,
                           "correction_factor": 0,
                           "break_even_bid": 0,
                           "percentile": 0}

        self.current_round = 0
        self.current_group = 0

        # duplicate info from general auction parameters
        self.rym = 0
        self.maximum_bid = 0
        self.demand = 0
        self.supply = 0

        # position of project - graph
        self.my_graph = 0

        # related to players bids
        self.my_bid = 0
        self.potential_subsidy = 0
        self.potential_profit = 0
        self.subsidy = 0
        self.profit = 0

        # history of auctions and bids
        self.history = {"round": [],
                        "group": [],
                        "win": [],
                        "supply": [],
                        "demand": [],
                        "rym": [],
                        "maximum_bid": [],
                        "ws": [],
                        "production": [],
                        "other_costs": [],
                        "cost_A": [],
                        "cost_B": [],
                        "cost": [],
                        "correction_factor": [],
                        "break_even_bid": [],
                        "percentile": [],
                        "bid": [],
                        "subsidy": [],
                        "profit": [],
                        "highest_suc": [],
                        "lowest_suc": [],
                        }

    def update_parameters(self, ws, production, other_costs, cost_A, cost_B, cost, correction_factor, break_even_bid,
                          percentile, rym, maximum_bid, demand, supply, current_round):
        """updating project parameters based on new draw from probability distribution, calculation in
        AuctionGenerator class"""

        self.parameters["ws"] = ws
        self.parameters["production"] = production
        self.parameters["other_costs"] = other_costs
        self.parameters["cost_A"] = cost_A
        self.parameters["cost_B"] = cost_B
        self.parameters["cost"] = cost
        self.parameters["correction_factor"] = correction_factor
        self.parameters["break_even_bid"] = break_even_bid
        self.parameters["percentile"] = percentile

        self.rym = rym
        self.maximum_bid = maximum_bid
        self.demand = demand
        self.supply = supply

        self.current_round = current_round

    def place_bid(self, bid):
        """placeholder function for storing bid of player"""
        self.my_bid = bid
        self.update_subsidy_profit()

    def place_random_bid(self):
        """random bidding for checking purpuses only; not used in real experiment"""
        self.my_bid = random.randint(round(self.parameters["break_even_bid"] * 100), round(self.maximum_bid * 100)) / 100
        self.update_subsidy_profit()

    def update_subsidy_profit(self):
        """calculating subsidy and profit based on bid"""
        if self.rym == 0:
            self.potential_subsidy = self.my_bid
        elif self.rym == 1:
            self.potential_subsidy = self.my_bid * self.parameters["correction_factor"]
        else:
            self.potential_subsidy = "error"

        self.potential_profit = self.potential_subsidy - self.parameters["break_even_bid"]

    def update_round(self, current_round, current_group):
        """setting number of round, currently not in use"""
        self.current_round = current_round
        self.current_group = current_group

    def store_round(self, win="error", supply="error", demand="error", rym="error",
                    highest_suc="error", lowest_suc="error"):
        """storing results of each round of auction;
        win needs to be in boolean format"""

        self.history["round"].append(self.current_round)
        self.history["group"].append(self.current_group)
        self.history["win"].append(win)
        self.history["supply"].append(supply)
        self.history["demand"].append(demand)
        self.history["rym"].append(rym)
        self.history["maximum_bid"].append(self.maximum_bid)
        self.history["ws"].append(self.parameters["ws"])
        self.history["production"].append(self.parameters["production"])
        self.history["other_costs"].append(self.parameters["other_costs"])
        self.history["cost_A"].append(self.parameters["cost_A"])
        self.history["cost_B"].append(self.parameters["cost_B"])
        self.history["cost"].append(self.parameters["cost"])
        self.history["correction_factor"].append(self.parameters["correction_factor"])
        self.history["break_even_bid"].append(self.parameters["break_even_bid"])
        self.history["percentile"].append(self.parameters["percentile"])
        self.history["bid"].append(self.my_bid)

        self.subsidy = self.potential_subsidy * win
        self.history["subsidy"].append(self.subsidy)

        self.profit = self.potential_profit * win
        self.history["profit"].append(self.profit)

        self.history["highest_suc"].append(highest_suc)
        self.history["lowest_suc"].append(lowest_suc)
