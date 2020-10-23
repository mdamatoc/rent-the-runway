import pandas as pd
from pandas.core import frame
import matplotlib.pyplot as plt
from src.core.plot_settings_handler import setup_ax


class DataAnalysis:
    def __init__(self, data_frame: pd.core.frame.DataFrame):
        self.data_frame = data_frame

    def make_a_histogram_in_kgs(self, weight_column: str):
        # Removing not necessary data
        histogram_data_frame = self.data_frame[[weight_column]].copy()
        """
        It's using .copy() because we don't want to create a copy of a data frame, but a data frame itself!
        Using this new data frame I can handle the data without updating the source data and without getting SettingWithCopyWarning 
        """

        # Removing unit of weight
        histogram_data_frame[weight_column] = histogram_data_frame[weight_column].str.slice(0, -3)

        # Converting to float because it needs to be multiplied by a float
        histogram_data_frame[weight_column] = histogram_data_frame[weight_column].astype(float)

        # Removing Not a Number data - not given data
        histogram_data_frame = histogram_data_frame.loc[~histogram_data_frame[weight_column].isnull()]

        # Converting from lbs to kgs
        histogram_data_frame['weight_kgs'] = histogram_data_frame[weight_column] * 0.453592

        # Rounding data
        histogram_data_frame['weight_kgs'] = histogram_data_frame['weight_kgs'].round(decimals=0)
        histogram_data_frame['weight_kgs'] = histogram_data_frame['weight_kgs'].astype('int16')

        # Grouping Data
        ax = histogram_data_frame.hist(column='weight_kgs', bins=100, grid=False, figsize=(12, 8), color='#86bf91', zorder=2, rwidth=0.9)
        setup_ax(ax, x_label='Weight [kg]', y_label='Amount of People', title="People Weight's Histogram")
        plt.show()  # todo comment this line to hide the histogram figure

