import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class Player:
    def __init__(self, my_name):
        # specific project parameters
        self.my_name = my_name

        self.parameters = {"ws": 0,
                           "production": 0,
                           "other_costs": 0,
                           "lcoe": 0,
                           "correction_factor": 0,
                           "minimum_bid": 0}

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
                        "ws": [],
                        "production": [],
                        "other_costs": [],
                        "lcoe": [],
                        "correction_factor": [],
                        "minimum_bid": [],
                        "bid": [],
                        "subsidy": [],
                        "profit": [],
                        "highest_suc": [],
                        "lowest_suc": [],
                        }

        self.distribution_df = ""

    def pass_distribution(self, distribution):
        self.distribution_df = pd.DataFrame.from_dict(distribution)

    def update_parameters(self, ws, production, other_costs, lcoe, correction_factor, minimum_bid,
                          rym, maximum_bid, demand, supply, current_round):
        """updating project parameters based on new draw from probability distribution, calculation in
        AuctionGenerator class"""

        self.parameters["ws"] = ws
        self.parameters["production"] = production
        self.parameters["other_costs"] = other_costs
        self.parameters["lcoe"] = lcoe
        self.parameters["correction_factor"] = correction_factor
        self.parameters["minimum_bid"] = minimum_bid

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
        self.my_bid = random.randint(round(self.parameters["minimum_bid"] * 100), round(self.maximum_bid * 100)) / 100
        self.update_subsidy_profit()

    def update_subsidy_profit(self):
        """calculating subsidy and profit based on bid"""
        if self.rym == 0:
            self.potential_subsidy = self.my_bid
        elif self.rym == 1:
            self.potential_subsidy = self.my_bid * self.parameters["correction_factor"]
        else:
            self.potential_subsidy = "error"

        self.potential_profit = self.potential_subsidy - self.parameters["lcoe"]

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
        self.history["ws"].append(self.parameters["ws"])
        self.history["production"].append(self.parameters["production"])
        self.history["other_costs"].append(self.parameters["other_costs"])
        self.history["lcoe"].append(self.parameters["lcoe"])
        self.history["correction_factor"].append(self.parameters["correction_factor"])
        self.history["minimum_bid"].append(self.parameters["minimum_bid"])
        self.history["bid"].append(self.my_bid)

        self.subsidy = self.potential_subsidy * win
        self.history["subsidy"].append(self.subsidy)

        self.profit = self.potential_profit * win
        self.history["profit"].append(self.profit)

        self.history["highest_suc"].append(highest_suc)
        self.history["lowest_suc"].append(lowest_suc)

    def graph_project_input(self):
        """graph is saved to the directory not sure how to display it to all players in their workstation"""
        color_map = ["#FFFFFF", "#8497B0"]

        if self.rym == 1:
            plt.figure(self.my_name)
            plt.stackplot(self.distribution_df["ws"], [self.distribution_df["min_lcoe_rym"],
                                                       self.distribution_df["max_lcoe_rym"] - self.distribution_df[
                                                           "min_lcoe_rym"]],
                          colors=color_map)

            plt.plot(self.parameters["ws"], self.parameters["minimum_bid"], marker="o", markerfacecolor="red")
            plt.grid()
            plt.xlim(min(self.distribution_df["ws"]), max(self.distribution_df["ws"]))
            plt.ylim(35, 70)
            plt.yticks(np.arange(35, 70, 5))
            plt.title("Distribution of minimum bids and position of your project")
            plt.xlabel("Wind speed")
            plt.ylabel("Minimum bid EUR/MWh")


            plt.savefig(self.my_name)
            plt.close()

        else:
            plt.figure(self.my_name)
            plt.stackplot(self.distribution_df["ws"], [self.distribution_df["min_lcoe"],
                                                       self.distribution_df["max_lcoe"] - self.distribution_df[
                                                           "min_lcoe"]],
                          colors=color_map)

            plt.plot(self.parameters["ws"], self.parameters["minimum_bid"], marker="o", markerfacecolor="red")
            plt.grid()
            plt.xlim(min(self.distribution_df["ws"]), max(self.distribution_df["ws"]))
            plt.ylim(30, 90)
            plt.yticks(np.arange(30, 90, 5))
            plt.title("Distribution of minimum bids and position of your project")
            plt.xlabel("Wind speed")
            plt.ylabel("Minimum bid EUR/MWh")

            plt.savefig(self.my_name)
            plt.close()






