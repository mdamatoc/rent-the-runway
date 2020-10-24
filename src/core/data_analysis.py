from src.core.plot_settings_handler import setup_ax
import matplotlib.pyplot as plt
from pandas.core import frame
import pandas as pd


class DataAnalysis:
    def __init__(self, data_frame: pd.core.frame.DataFrame):
        self.data_frame = data_frame

    def make_a_histogram_in_kgs(self, weight_column: str) -> None:
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
        histogram_data_frame['weight_kgs'] = histogram_data_frame['weight_kgs'].astype(int)

        # Grouping Data
        ax = histogram_data_frame.hist(column='weight_kgs', bins=100, grid=False, figsize=(12, 8), color='#86bf91', zorder=2, rwidth=0.9)
        setup_ax(ax, x_label='Weight [kg]', y_label='Amount of People', title="People Weight's Histogram")
        # plt.show()  # todo comment this line to hide the histogram figure

    def get_biggest_rented_for(self, rented_for_column: str, fit_column: str, fit_value: str) -> None:
        print("\n\nQuestão 2\n")

        # Slicing the data frame
        rented_for_data_frame = self.data_frame[[fit_column, rented_for_column]].copy()

        # Removing 'non fit' values
        rented_for_data_frame = rented_for_data_frame.loc[(rented_for_data_frame[fit_column] == fit_value)]

        # Calculating mode - It generated a Pandas Series with a single value.
        mode_series = rented_for_data_frame[rented_for_column].mode()
        mode_value = mode_series[0]
        print(f"O motivo de aluguel que possui maior número absoluto é o '{mode_value.upper()}'.")

        # Counting occurrences of the mode value in the rented for column
        number_of_occurrences_of_mode = self.data_frame.loc[self.data_frame[rented_for_column] == mode_value].shape[0]
        print(f"A quantidade de fits para o motivo de alguel {mode_value.upper()} é {number_of_occurrences_of_mode}.")

    def find_biggest_relative_rented_for(self, rented_for_column: str, fit_column: str, fit_value: str) -> None:
        print("\n\nQuestão 3\n")

        # Slicing the data frame
        rented_for_relative_data_frame = self.data_frame[[fit_column, rented_for_column]].copy()

        # Grouping by rented_for and counting the values in fit
        grouped_data = rented_for_relative_data_frame.groupby(rented_for_column)[fit_column].value_counts()

        # Switching the rows to columns to get the rented for counts as features
        # Using fillna(0) because unstack may created NaN numbers.
        # Using astype(int) because unstack will create float numbers
        # Now we got a data frame once again
        processed_data_frame = grouped_data.unstack().fillna(0).astype(int)

        # Transposing and transforming to dict to make manipulation easier
        processed_data_in_dict = processed_data_frame.T.to_dict()

        relations = {}
        for rented_for_key in processed_data_in_dict:
            rented_for_count = 0
            rented_for_with_fit_value_count = 0

            for fit_key in processed_data_in_dict.get(rented_for_key):
                rented_for_count += processed_data_in_dict.get(rented_for_key).get(fit_key)
                if fit_key == fit_value:
                    rented_for_with_fit_value_count = processed_data_in_dict.get(rented_for_key).get(fit_key)

                relations[rented_for_key] = rented_for_with_fit_value_count/rented_for_count

        largest_relative_rented_for = max(relations, key=relations.get)
        largest_relative_value = max(relations.values())

        print(f"O motivo de aluguel que tem o maior número relativo de fits é o '{largest_relative_rented_for.upper()}'.")
        print(f"O percentual de fits para este motivo de aluguel é {largest_relative_value * 100}%")
