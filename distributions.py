import exporter

from math import log
import numpy as np


class DistributionGenerator:
    def __init__(self, min_ws=5, max_ws=9, base_lcoe=50):
        self.min_ws = min_ws
        self.max_ws = max_ws
        self.base_lcoe = base_lcoe
        self.hub_height = 128
        self.installed_capacity = 3
        self.losses = 0.8

        # https://en.wind-turbine-models.com/turbines/832-enercon-e-115-3.000
        self.power_curve = [0, 0, 3, 48, 155, 339, 627, 1035, 1549, 2090,
                            2580, 2900, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000,
                            3000, 3000, 3000, 3000, 3000, 3000, 0, 0, 0, 0, 0]

        self.hours = 8760

        self.site_qualities = np.array([0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5])
        self.correction_factors = {0.7: 1.29, 0.8: 1.16, 0.9: 1.07, 1: 1, 1.1: 0.94, 1.2: 0.89, 1.3: 0.85, 1.4: 0.81,
                                   1.5: 0.79}

        self.reference_production = self.calc_production(ws_input=self.calculate_wsHH(ws100_input=6.45)) \
                                    / self.installed_capacity

        self.distribution = {"ws": [],
                             "production": [],
                             "site_quality": [],
                             "correction_factor": [],
                             "extra_correction_factor": [],
                             "lcoe": []}

        self.calc_distribution()

    def calc_distribution(self):
        self.create_ws_dist()

        for i in self.distribution["ws"]:
            self.distribution["production"].append(self.calc_production(ws_input=self.calculate_wsHH(ws100_input=i))
                                                   / self.installed_capacity)

        for i in self.distribution["production"]:
            self.distribution["site_quality"].append(i / self.reference_production)

        for i in self.distribution["site_quality"]:
            self.distribution["correction_factor"].append(self.calc_correction(input_sq=i))
            self.distribution["extra_correction_factor"].append(self.calc_extrapolated_correction(input_sq=i))

        for i in self.distribution["extra_correction_factor"]:
            self.distribution["lcoe"].append(i*self.base_lcoe)


    def create_ws_dist(self):
        scale = 10

        generated_list = [i for i in range(self.min_ws*scale, self.max_ws*scale + 1)]
        generated_list = [i/scale for i in generated_list]

        self.distribution["ws"] = generated_list

    def calculate_wsHH(self, ws100_input):
        reference_hub = 100
        roughness_length = 0.1

        return ws100_input*(log(self.hub_height/roughness_length)/log(reference_hub/roughness_length))

    def calc_production(self, ws_input):
        wind_speed_dist = []

        constant = 1.12
        a = 2
        b = ws_input * constant
        x_min = 1
        x_max = 30
        e = np.exp(1)

        val = 0
        for i in range(x_min, x_max):
            cumulative = (1 - e ** -(i / b) ** a)

            wind_speed_dist.append(cumulative - val)
            val = cumulative

        production_list = []

        for i in range(0, len(wind_speed_dist)):
            production_list.append(((self.power_curve[i] + self.power_curve[i+1])/2) * wind_speed_dist[i]
                                   * self.hours * self.losses)

        return sum(production_list)/1000

    def calc_correction(self, input_sq):
        if input_sq > 1.5:
            correction_factor = 0.79
            return correction_factor

        else:
            if input_sq < 0.7:
                correction_factor = 1.29
                return correction_factor

            else:
                lower = self.site_qualities[self.site_qualities <= input_sq].max()
                upper = self.site_qualities[self.site_qualities > input_sq].min()

                proportion_lower = round((0.1 - (upper - input_sq)) / 0.1, 5)
                correction_factor_difference = self.correction_factors[lower] - self.correction_factors[upper]
                correction_factor = self.correction_factors[lower] - (correction_factor_difference * proportion_lower)

                return correction_factor

    def calc_extrapolated_correction(self, input_sq):
        if input_sq > 1.5:
            correction_factor = 0.79 - (input_sq - 1.5) / 0.1 * 0.02
            return correction_factor

        else:
            if input_sq < 0.7:
                correction_factor = 1.29 + (0.7 - input_sq) / 0.1 * 0.13
                return correction_factor

            else:
                lower = self.site_qualities[self.site_qualities <= input_sq].max()
                upper = self.site_qualities[self.site_qualities > input_sq].min()

                proportion_lower = round((0.1 - (upper - input_sq)) / 0.1, 5)
                correction_factor_difference = self.correction_factors[lower] - self.correction_factors[upper]
                correction_factor = self.correction_factors[lower] - (correction_factor_difference * proportion_lower)

                return correction_factor


if __name__ == '__main__':
    Distributions = DistributionGenerator()
    print(Distributions.distribution)

    exporter.export_data(input_data=Distributions.distribution, name="test")


