from random_parameters_generation import generate_random_parameters
from theory_calc import AuctionGeneratorTheory

import pandas as pd
import random
from scipy.stats import ttest_ind
from math import floor


def play_scenario(parameters_df, demand=1, rym=0, active_players=4):
    rounds = int(parameters_df["round"].max())

    """"Creating auction class"""
    Auctions = AuctionGeneratorTheory(parameters_df=parameters_df,
                                      active_players=active_players,
                                      rym=rym,
                                      demand=demand,
                                      supply=4,
                                      )

    Auctions.change_demand_parameter(demand=demand)

    for itteration in range(rounds):
        Auctions.split_players_random()
        Auctions.input_parameters_to_players()

        for i in Auctions.players_dic:
            Auctions.players_dic[i].place_random_bid()

        Auctions.evaluate_round_per_group()
        Auctions.results_to_players()
        Auctions.store_round_results()

    return Auctions.results_storage


def power_calc(rounds_per_treatment=50):
    writer = pd.ExcelWriter("distributions/{0}_rounds_{rounds}.xlsx".format("power_calc",
                                                                            rounds=str(rounds_per_treatment)),
                            engine="xlsxwriter")

    for ii in [1, 3]:
        power_results_subsidy = {"t": [],
                                 "p": [],
                                 "average_subsidy_no_rym": [],
                                 "average_subsidy_rym": [],
                                 }

        for i in range(0, 100):
            sample_parameters = generate_random_parameters(no_groups=1, plyers_per_group=4,
                                                             no_rounds=rounds_per_treatment,
                                                             ws_min=5, ws_max=9,
                                                             oc_min=0.8, oc_max=1.2,
                                                             ws_decimals=1,
                                                             oc_decimals=2,
                                                             base_lcoe=50,
                                                             max_bid_no_rym=90.3,
                                                             max_bid_rym=70,
                                                             random_seed=i,
                                                             name="sample_x",
                                                             )

            """playing scenario"""
            results = (play_scenario(parameters_df=sample_parameters, demand=ii))

            results_subsidy_no_rym = results["1"]["NoRYM_model_subsidy"]
            results_subsidy_rym = results["1"]["RYM_model_subsidy"]

            t_stat, p_value = ttest_ind(results_subsidy_no_rym, results_subsidy_rym)

            power_results_subsidy["t"].append(t_stat)
            power_results_subsidy["p"].append(p_value)
            power_results_subsidy["average_subsidy_no_rym"].append(
                sum(results_subsidy_no_rym) / len(results_subsidy_no_rym))
            power_results_subsidy["average_subsidy_rym"].append(sum(results_subsidy_rym) / len(results_subsidy_rym))

        print("demand", ii, )
        print(power_results_subsidy["t"])
        print(power_results_subsidy["p"])
        print("max p value is", max(power_results_subsidy["p"]))

        df_out = pd.DataFrame.from_dict(power_results_subsidy)
        df_out.to_excel(writer, sheet_name=str(ii))

    writer.save()


def power_calc_samples(rounds_per_treatment=50):
    writer = pd.ExcelWriter("distributions/{0}_samples_rounds_{rounds}.xlsx".format("power_calc",
                                                                                    rounds=str(rounds_per_treatment)),
                            engine="xlsxwriter")

    for demand in [3, 1]:
        average_subsidy_storage = {"average_subsidy_no_rym": [],
                                   "average_subsidy_rym": [],
                                   }

        for iteration in range(0, 500):
            print("sampling", iteration + 1, "out of 500")
            rand_gen = random.Random()
            random_seed = rand_gen.randint(1, 1000000)

            sample_parameters = generate_random_parameters(no_groups=1, plyers_per_group=4,
                                                             no_rounds=rounds_per_treatment,
                                                             ws_min=5, ws_max=9,
                                                             oc_min=0.8, oc_max=1.2,
                                                             ws_decimals=1,
                                                             oc_decimals=2,
                                                             base_lcoe=50,
                                                             max_bid_no_rym=90.3,
                                                             max_bid_rym=70,
                                                             random_seed=random_seed,
                                                             name="sample_x",
                                                             )

            results = (play_scenario(parameters_df=sample_parameters, demand=demand))

            results_subsidy_no_rym = sum(results["1"]["NoRYM_model_subsidy"]) / len(results["1"]["NoRYM_model_subsidy"])
            results_subsidy_rym = sum(results["1"]["RYM_model_subsidy"]) / len(results["1"]["RYM_model_subsidy"])

            average_subsidy_storage["average_subsidy_no_rym"].append(results_subsidy_no_rym)
            average_subsidy_storage["average_subsidy_rym"].append(results_subsidy_rym)

        print(average_subsidy_storage)

        storage_length = len(average_subsidy_storage["average_subsidy_rym"])

        power_results_subsidy = {}

        for samples_needed in range(2, 7):
            power_results_subsidy[str(samples_needed)] = {
                "t": [],
                "p": [],
                "average_subsidy_no_rym": [],
                "average_subsidy_rym": [],
            }

            samples_fits_in_storage_x = floor(storage_length / samples_needed)
            sample_repetition = 1

            for i in range(0, samples_fits_in_storage_x):
                sample_start = samples_needed * (sample_repetition - 1)
                sample_end = samples_needed * (sample_repetition - 1) + samples_needed

                sample_subsidy_no_rym = average_subsidy_storage["average_subsidy_no_rym"][sample_start:sample_end]
                sample_subsidy_rym = average_subsidy_storage["average_subsidy_rym"][sample_start:sample_end]

                t_stat, p_value = ttest_ind(sample_subsidy_no_rym, sample_subsidy_rym)

                power_results_subsidy[str(samples_needed)]["t"].append(t_stat)
                power_results_subsidy[str(samples_needed)]["p"].append(p_value)

                power_results_subsidy[str(samples_needed)]["average_subsidy_no_rym"]. \
                    append(sum(sample_subsidy_no_rym) / len(sample_subsidy_no_rym))

                power_results_subsidy[str(samples_needed)]["average_subsidy_rym"]. \
                    append(sum(sample_subsidy_rym) / len(sample_subsidy_rym))

                sample_repetition += 1

        print("power_results", power_results_subsidy)

        for samples in power_results_subsidy:
            df_out = pd.DataFrame.from_dict(power_results_subsidy[samples])
            df_out.to_excel(writer, sheet_name=("demand_" + str(demand)) + "_sample_" + str(samples))

    writer.save()


def power_calc_samples_4groups(rounds_per_treatment=50, no_groups=4):
    writer = pd.ExcelWriter("distributions/{0}_samples_rounds_{rounds}_groups_{groups}.xlsx".
                            format("power_calc",
                                   rounds=str(rounds_per_treatment),
                                   groups=no_groups),
                            engine="xlsxwriter")

    for demand in [3, 1]:
        average_subsidy_storage = {"average_subsidy_no_rym": [],
                                   "average_subsidy_rym": [],
                                   }

        for iteration in range(0, 500):
            print("rounds_per_treatment", rounds_per_treatment, "demand", demand, "sampling", iteration + 1,
                  "out of 500")
            rand_gen = random.Random()
            random_seed = rand_gen.randint(1, 1000000)

            sample_parameters = generate_random_parameters(no_groups=no_groups, plyers_per_group=4,
                                                           no_rounds=rounds_per_treatment,
                                                           ws_min=5, ws_max=9,
                                                           oc_min=0.8, oc_max=1.2,
                                                           ws_decimals=1,
                                                           oc_decimals=2,
                                                           base_lcoe=50,
                                                           max_bid_no_rym=90.3,
                                                           max_bid_rym=70,
                                                           random_seed=random_seed,
                                                           name="sample_x",
                                                           )

            results = (play_scenario(parameters_df=sample_parameters, demand=demand, active_players=16))

            results_subsidy_no_rym = []
            results_subsidy_rym = []

            for round_x in range(0, rounds_per_treatment):
                results_subsidy_no_rym_groups = 0
                results_subsidy_rym_groups = 0

                for group in range(1, no_groups + 1):
                    results_subsidy_no_rym_groups += results[str(group)]["NoRYM_model_subsidy"][round_x]
                    results_subsidy_rym_groups += results[str(group)]["RYM_model_subsidy"][round_x]

                results_subsidy_no_rym.append(results_subsidy_no_rym_groups / no_groups)
                results_subsidy_rym.append(results_subsidy_rym_groups / no_groups)

            average_subsidy_storage["average_subsidy_no_rym"].append(
                sum(results_subsidy_no_rym) / len(results_subsidy_no_rym))
            average_subsidy_storage["average_subsidy_rym"].append(sum(results_subsidy_rym) / len(results_subsidy_rym))

        storage_length = len(average_subsidy_storage["average_subsidy_rym"])

        power_results_subsidy = {}

        for samples_needed in range(2, 7):
            power_results_subsidy[str(samples_needed)] = {
                "t": [],
                "p": [],
                "average_subsidy_no_rym": [],
                "average_subsidy_rym": [],
            }

            samples_fits_in_storage_x = floor(storage_length / samples_needed)
            sample_repetition = 1

            for i in range(0, samples_fits_in_storage_x):
                sample_start = samples_needed * (sample_repetition - 1)
                sample_end = samples_needed * (sample_repetition - 1) + samples_needed

                sample_subsidy_no_rym = average_subsidy_storage["average_subsidy_no_rym"][sample_start:sample_end]
                sample_subsidy_rym = average_subsidy_storage["average_subsidy_rym"][sample_start:sample_end]

                t_stat, p_value = ttest_ind(sample_subsidy_no_rym, sample_subsidy_rym)

                power_results_subsidy[str(samples_needed)]["t"].append(t_stat)
                power_results_subsidy[str(samples_needed)]["p"].append(p_value)

                power_results_subsidy[str(samples_needed)]["average_subsidy_no_rym"]. \
                    append(sum(sample_subsidy_no_rym) / len(sample_subsidy_no_rym))

                power_results_subsidy[str(samples_needed)]["average_subsidy_rym"]. \
                    append(sum(sample_subsidy_rym) / len(sample_subsidy_rym))

                sample_repetition += 1

        print("power_results", power_results_subsidy)

        for samples in power_results_subsidy:
            df_out = pd.DataFrame.from_dict(power_results_subsidy[samples])
            df_out.to_excel(writer, sheet_name=("demand_" + str(demand)) + "_sample_" + str(samples))

    writer.save()


if __name__ == '__main__':
    # power_calc(rounds_per_treatment=25)
    # power_calc(rounds_per_treatment=50)

    """
    for i in [25, 50]:
        power_calc_samples(rounds_per_treatment=i)
    """

    for i in [25, 50]:
        power_calc_samples_4groups(rounds_per_treatment=i)
