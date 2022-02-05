import pandas as pd
from core.models import Rate, Contract
from typing import Optional, Tuple


def read_excel_data(file, contract: Contract):
    """
    This function reads the excel file sent in the FormView
    cleans his data on a pandas Dataframe
    and create the Django Rate objects from the data in the file

    :param file: Excel File to read sent in the FormView, this will also work with a string with the path to the excel file
    :param contract: Django Contract object to relate the Rate objects to

    :return: None

    Process:
    1. Read the excel file
    2. Clean the data
        2.1 Rename the selected columns to acces them easier
    4. Iterate over the rows in the dataframe and create the Django Rate objects
    3. Create the Django Rate objects
    """

    df = pd.read_excel(file)
    df.rename(columns={
        'POL': 'origin',
        'POD': 'destination',
        'Curr.': 'currency',
        "20'GP": 'twenty',
        "40'GP": 'forty',
        "40'HC": 'fortyhc'
    }, inplace=True)

    for _row in df.iterrows():
        row = _row[1]
        rate = Rate(
            origin=row.origin,
            destination=row.destination,
            currency=row.currency,
            twenty=row.twenty,
            forty=row.forty,
            fortyhc=row.fortyhc,
            contract=contract
        )
        rate.save()


def compare_two_files(contracts: Optional[Tuple[Contract]] = None):
    """
    This function compares the two files uploaded to the database
    and returns a list of the rates that are different between the two files

    :params: contracts: Optional[Tuple[Contract]] = None -> Django Contract objects to compare
    :return: an array where the first two index are the django objects from the last two files,
    and the third is a list of the rates that are different between the two files

    if no contracts are passed, it will compare the last two files

    Process:
    1. Get the last two files uploaded to the database
    2. Create the Pandas DataFrames with the origin and destination columns as strings
    3. Create a the Datafrmame mergin the data in the other DataFrames
    4. Fill empty spaces in the DataFrames with "No Info" values, in case there are new registers in one of the files
    5. Compare the two DataFrames, creating a new column with the result of the comparison
    6. return the dataframe with the comparison result, as long as the Django object representing the files compared
    """
    if not contracts:
        contract_1, contract_2 = list(
            Contract.objects.filter(
                id__gte=Contract.objects.count() - 1
            )
        )
    else:
        contract_1, contract_2 = contracts

    df_1 = pd.DataFrame(
        list(
            Rate.objects.filter(
                contract=contract_1
            )
            .values(
                'origin', 'destination'
            )
        )
    ).reset_index()

    df_2 = pd.DataFrame(
        list(
            Rate.objects.filter(
                contract=contract_2
            )
            .values(
                'origin', 'destination'
            )
        )
    ).reset_index()

    df = pd.merge(df_1, df_2, how='outer', on='index', suffixes=('_1', '_2'))

    df.fillna('No Info', inplace=True)

    df['change'] = (
        df['origin_1'] != df['origin_2']
    ) | (
        df['destination_1'] != df['destination_2']
    )

    changed_items = df[df['change']].shape[0]

    return [contract_1, contract_2, [item[1] for item in list(df.iterrows())], changed_items]
