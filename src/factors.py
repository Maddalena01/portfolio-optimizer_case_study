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

def align_returns_with_factors(portfolio_returns, factors):
    """
    Align a portfolio's daily returns with the Fama-French factors
    on matching dates, and compute the excess return (return - RF).
    """
    combined = factors.join(portfolio_returns.rename("portfolio"), how="inner")
    combined["portfolio_excess"] = combined["portfolio"] - combined["RF"]
    return combined

import statsmodels.api as sm


def run_factor_regression(reg_data, factor_columns=("Mkt-RF", "SMB", "HML"), robust=False):
    """
    Regress a portfolio's excess return on the Fama-French factors.

    If robust=True, uses HAC (Newey-West) standard errors with 5 lags,
    more reliable when residuals show autocorrelation or non-normality
    (both common with daily financial return data, as seen in the
    Jarque-Bera test results).

    Returns the fitted statsmodels OLS results object, which exposes
    .params (alpha and betas), .pvalues, .rsquared, and .summary().
    """
    X = reg_data[list(factor_columns)]
    X = sm.add_constant(X)
    y = reg_data["portfolio_excess"]
    if robust:
        model = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
    else:
        model = sm.OLS(y, X).fit()
    return model
