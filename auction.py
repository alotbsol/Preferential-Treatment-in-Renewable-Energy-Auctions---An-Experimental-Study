from players import Player

import random as random
from operator import itemgetter
import pandas as pd


class AuctionGenerator:
    def __init__(self, parameters_df="",
                 active_players=16, rym=0, demand=3, supply=4,
                 ):

        self.active_players = active_players
        self.rym = rym

        self.demand = demand
        self.supply = supply

        self.input_parameters_df = parameters_df

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
            self.players_dic["player{0}".format(i)] = Player(my_name="player{0}".format(i))

    def generate_storage(self):
        for i in range(self.number_of_groups):
            self.results_storage[str(i + 1)] = {}
            self.results_storage[str(i + 1)]["round"] = []
            self.results_storage[str(i + 1)]["supply"] = []
            self.results_storage[str(i + 1)]["demand"] = []
            self.results_storage[str(i + 1)]["rym"] = []

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

    def input_parameters_to_players(self):
        self.current_round += 1

        for i in self.groups:
            player_slot = 0
            for player in self.groups[i]:
                player_slot += 1

                parameters = self.input_parameters_df.loc[(self.input_parameters_df['round'] == self.current_round) &
                                                 (self.input_parameters_df['group'] == int(i)) &
                                                 (self.input_parameters_df['player_slot'] == int(player_slot)),
                                                 ["ws", "other_costs", "cost_A", "cost_B", "production",
                                                  "correction_factor", "cost",
                                                  "break_even_bid_no_rym", "break_even_bid_rym",
                                                  "percentile_no_rym", "percentile_rym",
                                                  "max_bid_no_rym", "max_bid_rym"]]

                if self.rym == 0:
                    break_even_bid = parameters.iloc[0]["break_even_bid_no_rym"]
                    maximum_bid = parameters.iloc[0]["max_bid_no_rym"]
                    percentile = parameters.iloc[0]["percentile_no_rym"]
                else:
                    break_even_bid = parameters.iloc[0]["break_even_bid_rym"]
                    maximum_bid = parameters.iloc[0]["max_bid_rym"]
                    percentile = parameters.iloc[0]["percentile_rym"]

                self.players_dic[player].update_parameters(ws=parameters.iloc[0]["ws"],
                                                           production=parameters.iloc[0]["production"],
                                                           other_costs=parameters.iloc[0]["other_costs"],
                                                           cost_A=parameters.iloc[0]["cost_A"],
                                                           cost_B=parameters.iloc[0]["cost_B"],
                                                           cost=parameters.iloc[0]["cost"],
                                                           correction_factor=parameters.iloc[0]["correction_factor"],
                                                           break_even_bid=break_even_bid,
                                                           percentile=percentile,
                                                           rym=self.rym,
                                                           maximum_bid=maximum_bid,
                                                           demand=self.demand,
                                                           supply=self.supply,
                                                           current_round=self.current_round)

    def split_players_random(self):
        shuffled_players = list(self.players_dic.keys())
        random.shuffle(shuffled_players)

        groups = {}

        for i in range(self.number_of_groups):
            groups[str(i+1)] = shuffled_players[i * self.supply: i * self.supply + self.supply]

        self.groups = groups

        for i in self.groups:
            for ii in self.groups[i]:
                self.players_dic[ii].update_round(current_round=self.current_round, current_group=i)

    def update_demand_supply(self, demand, supply):
        self.demand = demand
        self.supply = supply

    def evaluate_round_per_group(self):
        """not taking into account equal bids, shuffling might be introduced"""
        """Winning bids based on place bids"""
        winning_bids = {}

        for i in self.groups:
            placed_bids = {}
            for ii in self.groups[i]:
                placed_bids[str(ii)] = self.players_dic[ii].my_bid

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

    def change_rym_parameter(self, rym):
        self.rym = rym

    def change_demand_parameter(self, demand):
        self.demand = demand

    def change_maximum_bid(self, maximum_bid):
        self.maximum_bid = maximum_bid

    def export_everything(self, name="default_export"):
        writer = pd.ExcelWriter("results/{name}.xlsx".format(name=name), engine="xlsxwriter")

        """calculating and exporting profit of players"""
        evaluate_players = {"player": [], "profit": []}
        for i in self.players_dic:
            evaluate_players["player"].append(i)
            evaluate_players["profit"].append(sum(self.players_dic[i].history["profit"]))

        df_out = pd.DataFrame.from_dict(evaluate_players)
        df_out["%"] = df_out.profit / df_out.profit.sum()
        df_out.to_excel(writer, sheet_name="evaluation")

        """expoorting all results of all rounds and results per group"""
        frames = []
        for i in self.results_storage:
            df_out = pd.DataFrame.from_dict(self.results_storage[i])
            df_out.to_excel(writer, sheet_name="group{}".format(i))

            df_out.insert(loc=0, column='group', value=int(i))
            frames.append(df_out)

        all_data = pd.concat(frames)
        all_data.to_excel(writer, sheet_name="all_data")

        """expoorting results per player"""
        for i in self.players_dic:
            df_out = pd.DataFrame.from_dict(self.players_dic[i].history)
            df_out.to_excel(writer, sheet_name=str(i))

        self.input_parameters_df.to_excel(writer, sheet_name="input_parameters")

        writer.save()
