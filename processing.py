"""CSC110 Fall 2020 Final Project: Data Processing

This file contains any code needed to process the read and formatted data. This includes
sorting, point generation, regression, and finally prediction.

This file is Copyright (c) 2020 Aidan Ryan, Meet Patel, Hieu Duc Duong, Tejvir Singh Baidwan
"""
from typing import Dict, List, Tuple
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from reader import Wildfire

from reader import read_csv_data
import matplotlib.pyplot as plt


def year_sort(fires: List[Wildfire]) -> Dict[int, List[float]]:
    """Returns a mapping of years to lists of acreages burned by fires in that year.

    Preconditions:
      - fires != []

    >>> fires_test = [Wildfire(year=1995, acres=20.0), Wildfire(year=2015, acres=26.67), \
    Wildfire(year=2015, acres=32.0)]
    >>> result = year_sort(fires_test)
    >>> result == {1995: [20.0], 2015: [26.67, 32.0]}
    True
    """
    dict_so_far = {}

    for fire in fires:
        if fire.year in dict_so_far:
            dict_so_far[fire.year].append(fire.acres)
        else:
            dict_so_far[fire.year] = [fire.acres]
    return dict_so_far


def convert_to_points(fires: Dict[int, List[float]], desired_y: int) -> Tuple[List[int], list]:
    """Returns a tuple containing two lists, representing the x and y coords of different
    data points.
    The x coordinate represents a year,
    The y can represent multiple different values, which is determined by the inputted integer:
        - 0 = Number of fires in a year
        - 1 = Total acreage burned in a year
        - 2 = Average acreage burned by a fire in a year

    Preconditions:
      - desired_y in {0, 1, 2}
    """
    years = list(fires.keys())

    if desired_y == 0:
        num_fires = [len(fires[key]) for key in sorted(fires.keys())]
        return (years, num_fires)
    elif desired_y == 1:
        num_acres = [sum(fires[key]) for key in sorted(fires.keys())]
        return (years, num_acres)
    else:
        avg_acres = [sum(fires[key]) / len(fires[key]) for key in sorted(fires.keys())]
        return (years, avg_acres)


def predict_from_regression(fire_data: Tuple[List[int], list],
                            end_year: int) -> Tuple[List[int], list]:
    """Uses sklearn to fit a reasonably accurate polynomial regression to the dataset, and then
    predicts future relative y values to a specified end year, inclusive.
    Works with any of the 3 potential y axes as the regression is not predetermined."""
    x_train, x_test, y_train, y_test = train_test_split(fire_data[0], fire_data[1],
                                                        test_size=0.3, random_state=0)
    print(x_train)
    print(x_test)
    print(y_train)
    print(y_test)

    # This upper bound on the range is arbitrary, but I would rather have higher bias and
    # avoid overfitting the curve to the data.
    for i in range(2, 6):
        polynom = PolynomialFeatures(degree=i)
        x_polynom = polynom.fit_transform(x_train)

        poly_reg = LinearRegression()
        poly_reg.fit(x_polynom, y_train)

        y_predict = poly_reg.predict(polynom.fit_transform(x_test))

        r_square = metrics.r2_score(y_test, y_predict)

        # Due to the much larger changing variables like development of tech to
        # prevent fires and others, an r_square value >= 0.8 will be considered sufficient.
        # I also will go with the first to meet this, to again ward off overfitting.
        if r_square >= 0.8:
            fire_data_predicted = fire_data  # Tuple is immutable so this is effectively a copy
            for year in range(2020, end_year + 1):  # dataset ends with 2019, so start from 2020
                y_predicted = poly_reg.predict(polynom.fit_transform([[year]]))

                fire_data_predicted[0].append(year)
                fire_data_predicted[1].append(y_predicted)

                plt.scatter(x_train, y_train, color='green')
                plt.plot(x_train, poly_reg.predict(polynom.fit_transform(x_train)), color='blue')
            return fire_data_predicted


# if __name__ == '__main__':
#     import python_ta
#     import python_ta.contracts
#
#     python_ta.contracts.DEBUG_CONTRACTS = False
#     python_ta.contracts.check_all_contracts()
#
#     import doctest
#
#     doctest.testmod()
#
#     python_ta.check_all(config={
#         'extra-imports': ['reader', 'typing', 'datetime', 'csv', 'python_ta.contracts',
#                           'sklearn', 'sklearn.model_selection', 'sklearn.linear_model',
#                           'sklearn.preprocessing'],
#         'allowed-io': ['read_csv_data'],
#         'max-line-length': 100,
#         'disable': ['R1705', 'C0200']
#     })
