# calculation_utilities.py

# external dependencies
import numpy as np
import pandas as pd

def calc(starting_principle: float, 
         contribution_per_compounding_period: float,
         compounding_periods_per_year: int = 1, 
         real_return_rate: float = 0.05,
         num_years: int = 10) -> pd.DataFrame:
    
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
  
def find_indices_of_multiples(starting_capital: float, df: pd.DataFrame):
    as_factor = df.total.values // starting_capital
    return 1+np.where(as_factor[1:] != as_factor[:-1])[0]

def find_doubling_points(df: pd.DataFrame,
                         starting_capital: float,
                         contribution_per_compounding_period: float) -> pd.DataFrame:
    starting_capital = contribution_per_compounding_period if starting_capital == 0 else starting_capital
    as_factor = df.total.values % starting_capital
    doubled = find_indices_of_multiples(
        contribution_per_compounding_period if starting_capital == 0 else starting_capital,
        df
    )
    return df.iloc[doubled]

def find_overtaking_point(df: pd.DataFrame,
                          contribution_per_compounding_period: float) -> pd.DataFrame:
    overtaking_idx = np.where(df.gains > contribution_per_compounding_period)[0]
    if overtaking_idx.shape[0] > 0:
        return df.iloc[overtaking_idx]
    else:
        return pd.DataFrame()

def find_points_of_interest(df: pd.DataFrame,
                            starting_capital: float,
                            contribution_per_compounding_period: float):
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
    