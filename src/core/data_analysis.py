from src.core.plot_settings_handler import setup_ax
import matplotlib.pyplot as plt
from pandas.core import frame
import pandas as pd
from collections import Counter
import re


class DataAnalysis:
    def __init__(self, data_frame: pd.core.frame.DataFrame):
        self.data_frame = data_frame

    def make_a_histogram_in_kgs(self, weight_column: str) -> None:
        print("Questão 1")

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
        setup_ax(ax, x_label='Weight [kg]', y_label='Amount of People', title="Histogram of People Weight")
        plt.savefig("histograma_da_distribuicao_de_peso")

        print("Uma imagem que responde a este item foi gerada. Ela está armazenada em storage/data/histograma_da_distribuicao_de_peso.png")

    def get_biggest_rented_for(self, rented_for_column: str, fit_column: str, fit_value: str) -> None:
        print("\n\nQuestão 2")

        # Slicing the data frame
        rented_for_data_frame = self.data_frame[[fit_column, rented_for_column]].copy()

        # Removing 'non fit' values
        rented_for_data_frame = rented_for_data_frame.loc[(rented_for_data_frame[fit_column] == fit_value)]

        # Calculating mode - It generated a Pandas Series with a single value.
        mode_series = rented_for_data_frame[rented_for_column].mode()
        mode_value = mode_series[0]
        print(f"O motivo de aluguel que possui maior número absoluto de fits é o '{mode_value.upper()}'.")

        # Counting occurrences of the mode value in the rented for column
        number_of_occurrences_of_mode = self.data_frame.loc[self.data_frame[rented_for_column] == mode_value].shape[0]
        print(f"A quantidade de fits para o motivo de aluguel {mode_value.upper()} é {number_of_occurrences_of_mode}.")

    def find_biggest_relative_rented_for(self, rented_for_column: str, fit_column: str, fit_value: str) -> None:
        print("\n\nQuestão 3")

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

                relations[rented_for_key] = rented_for_with_fit_value_count / rented_for_count

        largest_relative_rented_for = max(relations, key=relations.get)
        largest_relative_value = max(relations.values())

        print(f"O motivo de aluguel que tem o maior número relativo de fits é o '{largest_relative_rented_for.upper()}'.")
        print(f"O percentual de fits para este motivo de aluguel é {largest_relative_value * 100}%.")

    def most_common_words_in_review(self, review_column: str, top_words: int) -> None:
        print('\n\nQuestão 4')

        # Slicing data frame
        review_data_frame = self.data_frame[[review_column]].copy()

        # Removing punctuation marks
        punctuation_marks = [',', '.', '!', '?', ":", "_", "-", ";", "\\", "/", "&", "*", "(", ")", "[", "]", "'"]
        for punctuation_mark in punctuation_marks:
            review_data_frame[review_column] = review_data_frame[review_column].str.replace(punctuation_mark, "")

        # Lowering case in all words
        review_data_frame[review_column] = review_data_frame[review_column].str.lower()

        # keeping only letters, numbers and whitespaces - removing emojis and characters like that
        review_data_frame[review_column] = review_data_frame[review_column].apply(lambda x: re.sub(r'[^a-zA-Z ]+', '', str(x)))

        # Calculating most common words
        most_common_words_relation = Counter(" ".join(review_data_frame[review_column]).split()).most_common(top_words)

        # Removing meaningless words
        meaningless_words = [
            'i', 'am', 'the', 'a', 'and', 'an', 'of', 'so', 'is', 'are', 'was', 'but', 'with', 'not',
            'were', 'it', 'to', 'this', 'that', 'those', 'these', 'for', 'in', 'on'
        ]
        most_common_useful_words_relation = []
        [most_common_useful_words_relation.append((common_word, amount)) for common_word, amount in most_common_words_relation if common_word not in meaningless_words]

        fig = plt.figure()
        plt.scatter(*zip(*most_common_useful_words_relation))
        plt.title("Most Frequent Words in Review Text")
        plt.xlabel("Most Frequent Words".upper())
        plt.ylabel("Amount of Occurrences".upper())
        plt.grid()
        fig.set_figheight(10)
        fig.set_figwidth(15)
        plt.savefig("palavras_mais_usadas")

        print(
            "Uma imagem que responde a este item foi gerada. Ela está armazenada em storage/data/palavras_mais_usadas.png")

    def exploratory_data_analysis(self):
        print("\n\nQuestão 5")

        """
        Analisando o dataset fornecido, duas colunas parecem pertinentes:
            - age;
            - rating.

        Age: fornece a idade dos clientes que compraram algum produto
        Rating: satisfazação do cliente
        """

        age_column = 'age'
        rating_column = 'rating'

        # Slicing data frame
        age_data_frame = self.data_frame[[age_column]].copy()

        # Transforming from str to int -> pandas automatically sets int columns as string if there are NaN values
        age_data_frame[age_column] = age_data_frame[age_column].fillna(0)  # An int cannot be NaN
        age_data_frame[age_column] = age_data_frame[age_column].astype('int16')

        # Removing not given data
        age_data_frame = age_data_frame.loc[~(age_data_frame[age_column] == 0)]

        # Calculating average age
        average_age = age_data_frame[age_column].mean()
        average_age = "{:.2f}".format(average_age)

        print(f"A idade média do consumidor é {average_age} anos. É interessante abrir a idade do consumidor "
              f"de acordo com o produto comprado. Desta forma saberíamos com mais detalhes que consumidor costuma "
              f"comprar que tipo de produto, melhorando a abordagem do vendedor para com o cliente. Se, por exemplo, "
              f"mochilas costumam ser compradas por clientes de 10 a 20 anos, então os vendedores devem oferecer mais "
              f"mochilas para este público.\n")

        # Slicing data frame

        rating_data_frame = self.data_frame[[rating_column]].copy()

        # Transforming from str to int -> pandas automatically sets int columns as string if there are NaN values
        rating_data_frame[rating_column] = rating_data_frame[rating_column].fillna(0)  # An int cannot be NaN
        rating_data_frame[rating_column] = rating_data_frame[rating_column].astype(float)

        # Removing not given data
        rating_data_frame = rating_data_frame.loc[~(rating_data_frame[rating_column] == 0)]

        # Calculating average age
        average_rating = rating_data_frame[rating_column].mean()
        average_rating = "{:.2f}".format(average_rating)

        print(f"A satisfação média do consumidor é {average_rating}, de 0 a 10. Assim como no caso anterior, "
              f"é importante entender que produto tem recebido as melhores notas e quais produtos têm recebido as "
              f"piores notas. Assim poderíamos entender se, tanto para mais quanto para menos, temos nossos produtos "
              f"atendendo as faixas de tolerância. Caso tenhamos um produto com muito destaque, acima do esperado, "
              f"é essencial que entendamos se temos exemplares suficientes para atender um possível aumento de demanda. "
              f"Quando falamos de produtos com nota abaixo do rating esperado, precisamos entender se este é um produto "
              f"sazonal ou não e se ocorreu algo que justifique o rating ruim do mesmo, de forma que possamos pensar em "
              f"um plano de ação, se pertinente, para melhorar a satisfação do cliente deste produto.")
