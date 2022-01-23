"""CSC110 Fall 2020 Final Project: Data Reader

This file contains any code needed to read the given dataset and convert
it to a more useable format for processing.

This file is Copyright (c) 2020 Aidan Ryan, Meet Patel, Hieu Duc Duong, Tejvir Singh Baidwan
"""
from dataclasses import dataclass
from typing import List
import csv


@dataclass
class Wildfire:
    """A representation of a single wildfire.

    Instance Attributes;
      - acres: a float representing the number of acres the fire affected.
      - start_date: the starting date of the fire, without exact time.
      - end_date: the end_date of the fire, without exact time.
      - year: the year the fire started in, easier access than start_date for sorting

    Representation Invariants:
      - self.acres > 0.0
      - 0 <= self.year <= 2020

    >>> import datetime
    >>> fire = Wildfire(1234.567, datetime.date(2020, 12, 10), datetime.date(2020,12,11), 2020)
    >>> fire
    Wildfire(acres=1234.567, year=2020)
    """
    acres: float
    year: int


def read_csv_data(filepath: str) -> List[Wildfire]:
    """Return a list of the wildfires from the given data set, formatted
    to the data type Wildfire.
    This list will be sorted later.

    Preconditions:
      - file is the path to a CSV file containing wildfire data using the same
        format as the data in data/Washington_Large_Fires_1973-2019.csv.
    """
    with open(filepath) as file:
        reader = csv.reader(file)

        # Skip header row
        next(reader)

        data_so_far = []
        for row in reader:
            if int(row[8]) >= 1985:  # Fire tracking before 1985 is very sparse in dataset
                data_so_far.append(Wildfire(acres=float(row[7]), year=int(row[8])))
    return data_so_far


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'dataclasses', 'datetime', 'csv'],
        'allowed-io': ['read_csv_data'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
