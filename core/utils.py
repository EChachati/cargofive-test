import pandas as pd
from core.models import Rate, Contract


def read_excel_data(file, contract):
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


def compare_last_two_files():
    contract_1, contract_2 = list(
        Contract.objects.filter(
            id__gte=Contract.objects.count() - 1
        )
    )

    print(contract_1.name)
    print(contract_2.name)

    df_1 = pd.DataFrame(
        list(
            Rate.objects.filter(
                contract=contract_1
            )
            .values(
                'origin', 'destination'  # , 'currency', 'twenty', 'forty', 'fortyhc'
            )
        )
    ).reset_index()

    df_2 = pd.DataFrame(
        list(
            Rate.objects.filter(
                contract=contract_2
            )
            .values(
                'origin', 'destination'  # , 'currency', 'twenty', 'forty', 'fortyhc'
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

    return [item[1] for item in list(df.iterrows())]
