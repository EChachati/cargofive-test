import pandas as pd
from core.models import Rate


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
