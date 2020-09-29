import pandas as pd

from helpers import minutesDiff

def getDataframe():
    df = pd.read_csv(
        "./2019/01.csv",
        delimiter=";",
        parse_dates=[
            "Partida Prevista",
            "Partida Real",
            "Chegada Prevista",
            "Chegada Real",
        ],
    )

    df = df.rename(columns={
        "ICAO Empresa A�rea": "Empresa",
        "N�mero Voo": "Numero Voo",
        "C�digo DI": "Codigo DI",
        "C�digo Tipo Linha": "Codigo Tipo Linha",
        "ICAO Aer�dromo Origem": "Origem",
        "ICAO Aer�dromo Destino": "Destino",
        "Situa��o Voo": "Situacao Voo",
        "C�digo Justificativa": "Codigo Justificativa",
        "Partida Prevista": "Partida Prevista",
        "Partida Real": "Partida Real",
        "Chegada Prevista": "Chegada Prevista",
        "Chegada Real": "Chegada Real",
    })

    df["Partida Delay"] = df.apply(lambda x: minutesDiff(x["Partida Real"], x["Partida Prevista"]), axis=1)
    df["Chegada Delay"] = df.apply(lambda x: minutesDiff(x["Chegada Real"], x["Chegada Prevista"]), axis=1)

    return df
