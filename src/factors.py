import pandas_datareader.data as web


def get_fama_french_factors(start=None, end=None):
    """
    Scarica i fattori Fama-French a 3 fattori (giornalieri) dalla
    Data Library di Kenneth French.

    Ritorna un DataFrame con colonne Mkt-RF, SMB, HML, RF,
    già convertite in formato decimale (i dati grezzi sono in %).
    """
    raw = web.DataReader(
        "F-F_Research_Data_Factors_daily", "famafrench", start=start, end=end
    )
    factors = raw[0] / 100
    return factors