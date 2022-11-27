from distributions import DistributionGenerator
from players import Player

import random as random
from operator import itemgetter
import pandas as pd


class AuctionGenerator:
    def __init__(self, active_players=16, rym=0, demand=3, supply=4,
                 maximum_bid=90.3, ws_min=5, ws_max=9, oc_min=0.8, oc_max=1.2,
                 random_seed=16180339):

        """random seed needs to be changed, the whole process needs to be reproducible"""
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

        self.number_of_groups = int(active_players / supply)
        self.groups = {}

        self.players_dic = {}
        self.results_storage = {}

        self.current_round = 0
        self.winning_bids = {}

        self.generate_players()
        self.generate_storage()

    def generate_players(self):
        for i in range(1, self.active_players + 1):
            self.players_dic["player{0}".format(i)] = Player()

    def generate_storage(self):
        for i in range(self.number_of_groups):
            self.results_storage[str(i + 1)] = {}
            self.results_storage[str(i + 1)]["round"] = []
            self.results_storage[str(i + 1)]["supply"] = []
            self.results_storage[str(i + 1)]["demand"] = []
            self.results_storage[str(i + 1)]["rym"] = []

            self.results_storage[str(i + 1)]["NoRYM_model_subsidy_min"] = []
            self.results_storage[str(i + 1)]["NoRYM_model_subsidy"] = []
            self.results_storage[str(i + 1)]["NoRYM_model_profit"] = []
            self.results_storage[str(i + 1)]["NoRYM_model_production"] = []

            self.results_storage[str(i + 1)]["RYM_model_subsidy_min"] = []
            self.results_storage[str(i + 1)]["RYM_model_subsidy"] = []
            self.results_storage[str(i + 1)]["RYM_model_profit"] = []
            self.results_storage[str(i + 1)]["RYM_model_production"] = []

            self.results_storage[str(i + 1)]["players_subsidy"] = []
            self.results_storage[str(i + 1)]["players_profit"] = []
            self.results_storage[str(i + 1)]["players_production"] = []

            self.results_storage[str(i + 1)]["highest_suc"] = []
            self.results_storage[str(i + 1)]["lowest_suc"] = []

            for ii in range(self.supply):
                self.results_storage[str(i + 1)]["slot"+str(ii + 1)+"_player"] = []
                self.results_storage[str(i + 1)]["slot" + str(ii + 1) + "_bid"] = []
                self.results_storage[str(i + 1)]["slot" + str(ii + 1) + "_subsidy"] = []
                self.results_storage[str(i + 1)]["slot" + str(ii + 1) + "_profit"] = []

    def generate_parameters(self):
        for i in self.players_dic:
            """here randim generation should be done differently to prevent different number of players"""
            ws = random.randint(self.ws_min * 10, self.ws_max * 10) / 10
            other_costs = random.randint(self.oc_min * 100, self.oc_max * 100) / 100

            """ Loaded from original distributions"""
            ws_index = self.InputDistribution.distribution["ws"].index(ws)

            production = self.InputDistribution.distribution["production"][ws_index]
            correction_factor = self.InputDistribution.distribution["correction_factor"][ws_index]
            lcoe = self.InputDistribution.distribution["lcoe"][ws_index] * other_costs

            if self.rym == 0:
                minimum_bid = lcoe
            else:
                minimum_bid = lcoe / correction_factor

            self.players_dic[i].update_parameters(ws=ws, production=production, other_costs=other_costs, lcoe=lcoe,
                                                  correction_factor=correction_factor, minimum_bid=minimum_bid,
                                                  rym=self.rym, maximum_bid=self.maximum_bid,
                                                  demand=self.demand, supply=self.supply,
                                                  current_round=self.current_round)

        self.current_round += 1

    def split_players(self):
        shuffled_players = list(self.players_dic.keys())
        random.shuffle(shuffled_players)

        groups = {}

        for i in range(self.number_of_groups):
            groups[str(i+1)] = shuffled_players[i * self.supply : i * self.supply + self.supply]

        self.groups = groups

        for i in self.groups:
            for ii in self.groups[i]:
                self.players_dic[ii].update_round(current_round=self.current_round, current_group=i)

    def update_demand_supply(self, demand, supply):
        self.demand = demand
        self.supply = supply

    def evaluate_round_per_group(self):
        winning_bids = {}

        for i in self.groups:
            placed_bids = {}
            for ii in self.groups[i]:
                placed_bids[str(ii)] = self.players_dic[ii].my_bid

            """this should be shuffled to deal with equal bids"""
            winning_bids[str(i)] = dict(sorted(placed_bids.items(), key=itemgetter(1))[:self.demand])

        self.winning_bids = winning_bids

    def results_to_players(self):
        for i in self.groups:
            for ii in self.groups[i]:
                if ii in list(self.winning_bids[i].keys()):
                    win = 1
                else:
                    win = 0

                self.players_dic[ii].store_round(win=win,
                                                 supply=self.supply, demand=self.demand, rym=self.rym,
                                                 highest_suc=max(self.winning_bids[i].values()),
                                                 lowest_suc=min(self.winning_bids[i].values()))

    def store_round_results(self):
        for i in self.groups:
            self.results_storage[str(i)]["round"].append(self.current_round)
            self.results_storage[str(i)]["supply"].append(self.supply)
            self.results_storage[str(i)]["demand"].append(self.demand)
            self.results_storage[str(i)]["rym"].append(self.rym)

            self.results_storage[str(i)]["NoRYM_model_subsidy_min"].append("to be calculated")
            self.results_storage[str(i)]["NoRYM_model_subsidy"].append("to be calculated")
            self.results_storage[str(i)]["NoRYM_model_profit"].append("to be calculated")
            self.results_storage[str(i)]["NoRYM_model_production"].append("to be calculated")

            self.results_storage[str(i)]["RYM_model_subsidy_min"].append("to be calculated")
            self.results_storage[str(i)]["RYM_model_subsidy"].append("to be calculated")
            self.results_storage[str(i)]["RYM_model_profit"].append("to be calculated")
            self.results_storage[str(i)]["RYM_model_production"].append("to be calculated")

            subsidy = 0
            profit = 0
            production = 0

            for ii in self.winning_bids[i]:
                production += self.players_dic[ii].parameters["production"]

            for ii in self.winning_bids[i]:
                subsidy += self.players_dic[ii].potential_subsidy*(self.players_dic[ii].parameters["production"]
                                                                   /production)
                profit += self.players_dic[ii].potential_profit*(self.players_dic[ii].parameters["production"]
                                                                   /production)

            self.results_storage[str(i)]["players_subsidy"].append(subsidy)
            self.results_storage[str(i)]["players_profit"].append(profit)
            self.results_storage[str(i)]["players_production"].append(production)
            self.results_storage[str(i)]["highest_suc"].append(max(self.winning_bids[i].values()))
            self.results_storage[str(i)]["lowest_suc"].append(min(self.winning_bids[i].values()))

            for ii in range(self.supply):
                player = self.groups[i][ii]
                self.results_storage[str(i)]["slot"+str(ii + 1)+"_player"].append(player)
                self.results_storage[str(i)]["slot" + str(ii + 1) + "_bid"].append(self.players_dic[player].my_bid)
                self.results_storage[str(i)]["slot" + str(ii + 1) + "_subsidy"].append(self.players_dic[player].subsidy)
                self.results_storage[str(i)]["slot" + str(ii + 1) + "_profit"].append(self.players_dic[player].profit)

    def evaluate_auction(self):
        pass

    def export_everything(self, name="default_export"):
        writer = pd.ExcelWriter("{0}.xlsx".format(name), engine="xlsxwriter")

        for i in self.results_storage:
            df_out = pd.DataFrame.from_dict(self.results_storage[i])
            df_out.to_excel(writer, sheet_name="group{}".format(i))

        for i in self.players_dic:
            df_out = pd.DataFrame.from_dict(self.players_dic[i].history)
            df_out.to_excel(writer, sheet_name=str(i))

        writer.save()

    def change_rym_parameter(self, rym):
        self.rym = rym

    def change_demand_parameter(self, demand):
        self.demand = demand

