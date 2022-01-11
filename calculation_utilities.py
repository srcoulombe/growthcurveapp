# calculation_utilities.py

# standard library dependencies
from typing import Tuple

# external dependencies
import numpy as np
import pandas as pd

def calc(starting_principle: float, 
         contribution_per_compounding_period: float,
         compounding_periods_per_year: int = 1, 
         real_return_rate: float = 0.05,
         num_years: int = 10) -> pd.DataFrame:
    """Main function handling the generation of the compound growth forecast.

    Parameters
    ----------
    starting_principle : float 
        Float indicating the amount of money in the savings account at the start.
    contribution_per_compounding_period : float
        Contibutes made to the account per compounding period.
    compounding_periods_per_year : int, optional
        Number of compounding periods per 12-month cycle, by default 1.
    real_return_rate : float, optional
        Expected Real Return Rate, by default 0.05.
    num_years : int, optional
        Number of years to include in the forecast, by default 10

    Returns
    -------
    df : pd.DataFrame
        Pandas DataFrame with the following columns:
            "years_elapsed",
            "contributions",
            "accrued_gains",
            "gains",
            "total"
        Where 
            "years_elapsed": simply denote the number of years since the start of the
                forecasting
            "contributions": sum of the contributions made to the savings account
                (with respect to the timeframe specified by the corresponding 
                "years_elapsed" value)
            "accrued_gains": the gains accrued over interest (with respect 
                to the timeframe specified by the corresponding "years_elapsed" value)
            "gains": the sum of all gains accrued over interest so far 
                (with respect to the timeframe specified by the corresponding 
                "years_elapsed" value)
            "total": the total value of the savings account (with respect to the 
                timeframe specified by the corresponding "years_elapsed" value)
        
    """
    # cleaning up user input
    starting_principle = max(0, starting_principle)
    contribution_per_compounding_period = max(0, contribution_per_compounding_period)
    compounding_periods_per_year = max(1, compounding_periods_per_year)
    real_return_rate = max(0, real_return_rate)
    num_years = max(1, num_years) + 1
    
    n_points = int(num_years * compounding_periods_per_year)
    contributions = np.array(
        [starting_principle + i * contribution_per_compounding_period for i in range(n_points)],
        dtype = float
    )
    accrued_gains = np.zeros_like(contributions)
    gains = np.zeros_like(contributions)
    total = np.zeros_like(contributions)
    
    for i in range(n_points):
        if i == 0:
            total[i] = starting_principle
            gains[i] = 0.0
            accrued_gains[i] = 0.0
        else:
            gain = real_return_rate * total[i-1]
            gains[i] = gain
            accrued_gains[i] = accrued_gains[i-1] + gain
            total[i] = total[i-1] + contribution_per_compounding_period + gain
    
    df = pd.DataFrame({
        "years_elapsed": np.arange(0, num_years, 1/compounding_periods_per_year),
        "contributions": contributions,
        "accrued_gains": accrued_gains,
        "gains": gains,
        "total": total,
    })
    
    return df
  
def find_indices_of_multiples(starting_capital: float, df: pd.DataFrame) -> np.ndarray:
    """Returns the row indices in the provided `df` DataFrame where
    the total value of the savings account has grown to a new multiple of 
    `starting_capital`.

    Parameters
    ----------
    starting_capital : float
        Float indicating the amount of money in the savings account at the start.
    df : pd.DataFrame
        Pandas DataFrame containing the data from the growth curve forecast (see
        `calc`).

    Returns
    -------
    np.ndarray
        1-D vector of integers indicating at which compounding period the total
        value of the savings account has grown to a new multiple of `starting_capital`.
    """
    as_factor = df.total.values // starting_capital
    return 1+np.where(as_factor[1:] != as_factor[:-1])[0]

def find_doubling_points(df: pd.DataFrame,
                         starting_capital: float,
                         contribution_per_compounding_period: float) -> pd.DataFrame:
    """Returns the rows in the provided `df` DataFrame where
    the total value of the savings account has grown to a new multiple of 
    `starting_capital`.

    Parameters
    ----------
    df : pd.DataFrame
        Pandas DataFrame containing the data from the growth curve forecast (see
        `calc`).
    starting_principle : float 
        Float indicating the amount of money in the savings account at the start.
    contribution_per_compounding_period : float
        Contibutes made to the account per compounding period.

    Returns
    -------
    pd.DataFrame
        (Sub)DataFrame of the provided `df` DataFrame comprised only of the rows in
        `df` representing compounding periods where the total value of the savings
        account has reached a new multiple of `starting_principle`.
    """
    starting_capital = contribution_per_compounding_period if starting_capital == 0 else starting_capital
    doubled = find_indices_of_multiples(
        contribution_per_compounding_period if starting_capital == 0 else starting_capital,
        df
    )
    return df.iloc[doubled]

def find_overtaking_point(df: pd.DataFrame,
                          contribution_per_compounding_period: float) -> pd.DataFrame:
    """Returns a Pandas (sub)DataFrame of `df` comprised of the rows
    for which the gains from compound interest exceed the contribution made
    on each compounding period.

    Parameters
    ----------
    df : pd.DataFrame
        Pandas DataFrame containing the data from the growth curve forecast (see
        `calc`).
    contribution_per_compounding_period : float
        Contibutes made to the account per compounding period.

    Returns
    -------
    pd.DataFrame
        (Sub)DataFrame of the provided `df` DataFrame comprised only of the rows in
        `df` representing compounding periods where the gains made through compounding
        interest have exceeded the corresponding compounding periods' contributions.
    """
    overtaking_idx = np.where(df.gains > contribution_per_compounding_period)[0]
    if overtaking_idx.shape[0] > 0:
        return df.iloc[overtaking_idx]
    else:
        return pd.DataFrame()

def find_points_of_interest(df: pd.DataFrame,
                            starting_capital: float,
                            contribution_per_compounding_period: float) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Wrapper around `find_doubling_points` and `find_overtaking_point` 
    that returns the Pandas (sub)DataFrames made of the rows in `df` where either

    *   the total value of the savings account has reached a new multiple of 
        `starting_principle`, or
    *   the gains made through compounding interest have exceeded the corresponding 
        compounding periods' contributions

    Parameters
    ----------
    df : pd.DataFrame
        [description]
    starting_principle : float 
        Float indicating the amount of money in the savings account at the start.
    contribution_per_compounding_period : float
        Contibutes made to the account per compounding period.

    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame]
        (Sub)DataFrames of the provided `df` DataFrame comprised only of the rows in
        `df` representing compounding periods where either 
        *   (first DataFrame) the total value of the savings account has reached a new multiple of 
            `starting_principle`, or
        *   (second DataFrame) the gains made through compounding interest have exceeded the corresponding 
            compounding periods' contributions
    """
    doubling_points_df = find_doubling_points(
        df,
        starting_capital,
        contribution_per_compounding_period
    )
    overtaking_point_df = find_overtaking_point(
        df,
        contribution_per_compounding_period
    )
    return doubling_points_df, overtaking_point_df
    