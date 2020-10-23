import pandas as pd
from pandas.core import frame
import matplotlib.pyplot as plt
from src.core.plot_settings_handler import setup_ax


class DataAnalysis:
    def __init__(self, data_frame: pd.core.frame.DataFrame):
        self.data_frame = data_frame

    def make_a_histogram_in_kgs(self, weight_column: str):
        # Removing unit of weight
        self.data_frame[weight_column] = self.data_frame[weight_column].str.slice(0, -3)

        # Converting to float because it needs to be multiplied by a float
        self.data_frame[weight_column] = self.data_frame[weight_column].astype(float)

        # Removing Not a Number data - not given data
        histogram_data_frame = self.data_frame.loc[~self.data_frame[weight_column].isnull()]

        # Removing not necessary data
        histogram_data_frame = histogram_data_frame[[weight_column]]

        # Converting from lbs to kgs
        histogram_data_frame['weight_kgs'] = histogram_data_frame[weight_column] * 0.453592

        # Rounding data
        histogram_data_frame['weight_kgs'] = histogram_data_frame['weight_kgs'].round(decimals=0)
        histogram_data_frame['weight_kgs'] = histogram_data_frame['weight_kgs'].astype('int16')

        # print(histogram_data_frame['weight_kgs'])

        # Grouping Data
        ax = histogram_data_frame.hist(column='weight_kgs', bins=100, grid=False, figsize=(12, 8), color='#86bf91', zorder=2, rwidth=0.9)
        setup_ax(ax, x_label='Weight [kg]', y_label='Amount of People', title="People Weight's Histogram")
        plt.show()

