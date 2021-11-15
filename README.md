# README
Small web app used to visualize the effect of different parameters on the 
growth of a portfolio subject to periodic contributions.

Inspired by Wealthsimple's curve plots.

To run the app, `cd` to the project directory and use the following:

`$ panel serve Compounded_Growth_Curve.ipynb --autoreload`

# TODO
## Development
[ ] - Add `requirements.txt`
[x] - Add explanation
[ ] - Add explanation of math behind it
[x] - Add tab functionality (tab for explanation and demo, tab for comparison)
[x] - Fix colour palette
[x] - Add a templated Summary section containing relevant findings (time-to-double, end/start, sum of accrued gains, number of years until overtake)
[x] - Add header

## Deployment
[ ] - Deploy on `Heroku`

# Journal
I originally considered this project as an opportunity to finally play with `Voila` and review the basics of `Bokeh`'s interactive functionalities. However, I learned that `Voila` does not support some of the `Bokeh` features I intended to use. So the project pivoted away from `Voila` towards `Panel`.

# Tech Stack
- `Panel`
- `Bokeh`