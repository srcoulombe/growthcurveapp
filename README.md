# README
Small web app used to visualize the effect of different parameters on the 
growth of a portfolio subject to periodic contributions.

Inspired by Wealthsimple's curve plots.

# Quickstart
0. Clone this repo using: `git clone https://github.com/srcoulombe/growthcurveapp.git`
1. Navigate into the repository's directory and create a virtual environment by using: `python3 -m venv compounding-growth-venv`
2. Activate the virtual environment by using: `source compounding-growth-venv/bin/activate` if you're using MacOS/Linux or `.\compounding-growth-venv\Scripts\activate` if you're a Windows user.
3. Install the dependencies into your virtual environment by using: `python3 -m pip install -r requirements.txt`
4. Run the app by using: `panel serve web_app_notebook.ipynb --autoreload`

# TODO
## Development
- [ ] Fix css
- [ ] Add a Purchasing-Power Analysis; could be a plot showing how much $1 now would be worth in `Y` years if we presume a fixed real return rate of `RR`. Could actually show this for multiple Ys:
```       
^
|  /
| / /
|/ / /
+----->
```

# Tech Stack
- `NumPy`
- `Pandas`
- `Panel`
- `Bokeh`
# Journal
I originally considered this project as an opportunity to finally play with `Voila` and review the basics of `Bokeh`'s interactive functionalities. However, I learned that `Voila` does not support some of the `Bokeh` features I intended to use. So the project pivoted away from `Voila` towards `Panel`.

