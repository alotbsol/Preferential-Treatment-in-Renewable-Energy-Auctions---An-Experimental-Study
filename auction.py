from distributions import DistributionGenerator
from players import Player

import random as random
from operator import itemgetter
import pandas as pd


class AuctionGenerator:
    def __init__(self, active_players=16, rym=0, demand=3, supply=4,
                 maximum_bid=90.3, ws_min=5, ws_max=9, oc_min=0.8, oc_max=1.2,
                 ):

        self.active_players = active_players
        self.rym = rym

        self.demand = demand
        self.supply = supply

        self.maximum_bid = maximum_bid

        self.ws_min = ws_min
        self.ws_max = ws_max
        self.oc_min = oc_min
        self.oc_max = oc_max

        self.InputDistribution = DistributionGenerator(min_ws=ws_min, max_ws=ws_max, base_lcoe=50,
                                                       oc_min=oc_min, oc_max=oc_max)

        self.input_parameters_df = pd.DataFrame()

        self.number_of_groups = int(active_players / supply)
        self.groups = {}

        self.players_dic = {}
        self.results_storage = {}

        self.current_round = 0
        self.winning_bids = {}

        self.no_rym_winning_bids_proxy = {}
        self.no_rym_first_losing_proxy = {}

        self.rym_winning_bids_proxy = {}
        self.rym_first_losing_proxy = {}

        self.generate_players()
        self.generate_storage()

    def generate_players(self):
        for i in range(1, self.active_players + 1):
            self.players_dic["player{0}".format(i)] = Player(my_name="player{0}".format(i))
            self.players_dic["player{0}".format(i)].pass_distribution(self.InputDistribution.distribution)

    def generate_storage(self):
        for i in range(self.number_of_groups):
            self.results_storage[str(i + 1)] = {}
            self.results_storage[str(i + 1)]["round"] = []
            self.results_storage[str(i + 1)]["supply"] = []
            self.results_storage[str(i + 1)]["demand"] = []
            self.results_storage[str(i + 1)]["rym"] = []

            self.results_storage[str(i + 1)]["NoRYM_model_subsidy"] = []
            self.results_storage[str(i + 1)]["NoRYM_model_profit"] = []
            self.results_storage[str(i + 1)]["NoRYM_model_production"] = []

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

    def generate_random_parameters(self):
        for i in self.players_dic:
            """random generation of parameters"""
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

    def store_input_parameters_csv(self, input_df):
        self.input_parameters_df = input_df

    def input_parameters(self):
        self.current_round += 1

        for i in self.groups:
            player_slot = 0
            for player in self.groups[i]:
                player_slot += 1

                parameters = self.input_parameters_df.loc[(self.input_parameters_df['round'] == self.current_round) &
                                                 (self.input_parameters_df['group'] == int(i)) &
                                                 (self.input_parameters_df['player_slot'] == int(player_slot)),
                                                 ["ws", "other_costs"]]

                ws = parameters.iloc[0]["ws"]
                other_costs = parameters.iloc[0]["other_costs"]

                """ Loaded from original distributions"""
                ws_index = self.InputDistribution.distribution["ws"].index(ws)

                production = self.InputDistribution.distribution["production"][ws_index]
                correction_factor = self.InputDistribution.distribution["correction_factor"][ws_index]
                lcoe = self.InputDistribution.distribution["lcoe"][ws_index] * other_costs

                if self.rym == 0:
                    minimum_bid = lcoe
                else:
                    minimum_bid = lcoe / correction_factor

                self.players_dic[player].update_parameters(ws=ws, production=production, other_costs=other_costs,
                                                           lcoe=lcoe, correction_factor=correction_factor,
                                                           minimum_bid=minimum_bid, rym=self.rym,
                                                           maximum_bid=self.maximum_bid, demand=self.demand,
                                                           supply=self.supply, current_round=self.current_round)

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
        winning_bids = {}

        no_rym_winning_bids_proxy = {}
        no_rym_first_losing_proxy = {}

        rym_winning_bids_proxy = {}
        rym_first_losing_proxy = {}

        """Winning bids based on place bids"""
        for i in self.groups:
            placed_bids = {}
            for ii in self.groups[i]:
                placed_bids[str(ii)] = self.players_dic[ii].my_bid

            winning_bids[str(i)] = dict(sorted(placed_bids.items(), key=itemgetter(1))[:self.demand])

        self.winning_bids = winning_bids

        """Winning bids based on no rym; i.e. lcoe"""
        for i in self.groups:
            bids = {}
            for ii in self.groups[i]:
                bids[str(ii)] = self.players_dic[ii].parameters["lcoe"]

            no_rym_winning_bids_proxy[str(i)] = dict(sorted(bids.items(), key=itemgetter(1))[:self.demand])
            no_rym_first_losing_proxy[str(i)] = dict(sorted(bids.items(), key=itemgetter(1))[self.demand:self.demand+1])

        self.no_rym_winning_bids_proxy = no_rym_winning_bids_proxy
        self.no_rym_first_losing_proxy = no_rym_first_losing_proxy

        """Winning bids based on rym; i.e. lcoe/correction factor"""
        for i in self.groups:
            bids = {}
            for ii in self.groups[i]:
                bids[str(ii)] = self.players_dic[ii].parameters["lcoe"]/self.players_dic[ii].parameters["correction_factor"]

            rym_winning_bids_proxy[str(i)] = dict(sorted(bids.items(), key=itemgetter(1))[:self.demand])
            rym_first_losing_proxy[str(i)] = dict(sorted(bids.items(), key=itemgetter(1))[self.demand:self.demand+1])

        self.rym_winning_bids_proxy = rym_winning_bids_proxy
        self.rym_first_losing_proxy = rym_first_losing_proxy

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

            no_rym_subsidy = 0
            no_rym_profit = 0
            no_rym_production = 0

            no_rym_marginal = list(self.no_rym_first_losing_proxy[i].values())[0]

            for ii in self.no_rym_winning_bids_proxy[i]:
                no_rym_production += self.players_dic[ii].parameters["production"]

            for ii in self.no_rym_winning_bids_proxy[i]:
                no_rym_subsidy += no_rym_marginal * (self.players_dic[ii].parameters["production"]
                                                                     / no_rym_production)
                no_rym_profit += (no_rym_marginal - self.players_dic[ii].parameters["lcoe"]) \
                                 * (self.players_dic[ii].parameters["production"] / no_rym_production)

            self.results_storage[str(i)]["NoRYM_model_subsidy"].append(no_rym_subsidy)
            self.results_storage[str(i)]["NoRYM_model_profit"].append(no_rym_profit)
            self.results_storage[str(i)]["NoRYM_model_production"].append(no_rym_production)

            rym_subsidy = 0
            rym_profit = 0
            rym_production = 0

            rym_marginal = list(self.rym_first_losing_proxy[i].values())[0]

            for ii in self.rym_winning_bids_proxy[i]:
                rym_production += self.players_dic[ii].parameters["production"]

            for ii in self.rym_winning_bids_proxy[i]:
                rym_subsidy += rym_marginal * self.players_dic[ii].parameters["correction_factor"] * \
                               (self.players_dic[ii].parameters["production"] / rym_production)

                rym_profit += (rym_marginal * self.players_dic[ii].parameters["correction_factor"] - self.players_dic[ii].parameters["lcoe"]) \
                                 * (self.players_dic[ii].parameters["production"] / rym_production)

            self.results_storage[str(i)]["RYM_model_subsidy"].append(rym_subsidy)
            self.results_storage[str(i)]["RYM_model_profit"].append(rym_profit)
            self.results_storage[str(i)]["RYM_model_production"].append(rym_production)

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

        df_out = pd.DataFrame.from_dict(self.InputDistribution.distribution)
        df_out.to_excel(writer, sheet_name="parameters")

        self.input_parameters_df.to_excel(writer, sheet_name="input_parameters")

        writer.save()

    def change_rym_parameter(self, rym):
        self.rym = rym

    def change_demand_parameter(self, demand):
        self.demand = demand

    def change_maximum_bid(self, maximum_bid):
        self.maximum_bid = maximum_bid

