explanation = """# Understanding the Parameters

Below is a list of the relevant parameters to the forecasts shown on this web app:

## Parameters
- **Starting Capital**: That's how much money you can contribute to your savings account on day 1 of your investment journey.
- **Number of Years**: For how many years in the future should we estimate the growth of your savings account?
- **Compounding Periods per Year**: How many times to apply the `Real Return Rate per Compounding Period` during a one-year span (keep this at 1 unless you really know what you're doing).
- **Contribution per Compouding Period**: the amount you'll be depositing into your account every compounding period.
- **Real Return Rate per Compounding Period**: the average real return rate you're expecting per compounding period.
    
___
## Note: Real Return Rate

The Real Return Rate per Compounding Period (RR) is a decimal number calculated by subtracting Interest Rate per Compounding Period (IR) from the Nominal Return Rate per Compounding Period (NR). Simply put, 

>***RR = NR - IR***

### Example

Let's presume that the Compounding Periods per Year = 1. That means that the Interest Rate per Compounding Period (IR) is simply the average annual inflation rate you're expecting for the duration of the forecasting. In Canada for instance, the IR has hovered around ~2-3% since 1991[^1]. 

Let's also presume that we've invested our savings in a very diversified portfolio. Empirical evidence from recent years suggest that the average annual return rate for these portfolios over 20+ years is between 4-7%[^2].

This 4-7% (let's split the difference and call it 5.5% to make things simpler) would be the Nominal Return Rate per Compounding Period (NR). The 2-3% (again, let's just call it 2.5%) would be the Interest Rate per Compounding Period (IR). So under these assumptions, the Real Return Rate per Compounding Period (RR) would be 
***= 0.055 - 0.025 = 0.03***.

[^1]: source: https://www.statista.com/statistics/271247/inflation-rate-in-canada/
[^2]: source: ...
"""

