# README
Small web app used to visualize the effect of different parameters on the 
growth of a portfolio subject to periodic contributions.

Inspired by Wealthsimple's curve plots.

To run the app, `cd` to the project directory and use the following:

`$ panel serve wealthsimpleplus.ipynb --autoreload`

# TODO
## Development
[x] - Add `requirements.txt`
[x] - Add explanation
[ ] - Add explanation of math behind it
[x] - Add tab functionality (tab for explanation and demo, tab for comparison)
[x] - Fix colour palette
[x] - Add a templated Summary section containing relevant findings (time-to-double, end/start, sum of accrued gains, number of years until overtake)
[x] - Add header
[ ] - Add to documentation in notebook
[ ] - Fix css (blargh)
[ ] - Separate the Explanation tab into "Explanation" and "About"
[ ] - Move business case to the "About" tab
[ ] - Add image of what Wealthsimple has to the "About" tab
[ ] - Add a Purchasing-Power aspect
    Basically a plot showing how much $# now would be worth in Y years
        Could actually show this for multiple Ys:
        ^
        |  /
        | / /
        |/ / /
        +----->

## Deployment
[x] - Deploy on `Heroku`

# Journal
I originally considered this project as an opportunity to finally play with `Voila` and review the basics of `Bokeh`'s interactive functionalities. However, I learned that `Voila` does not support some of the `Bokeh` features I intended to use. So the project pivoted away from `Voila` towards `Panel`.

# Tech Stack
- `Panel`
- `Bokeh`