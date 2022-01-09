# plotting_utilities.py

# external dependencies
from bokeh.models import HoverTool
from bokeh.plotting import figure
from bokeh.palettes import brewer

import panel as pn
pn.extension()

# local dependencies
from calculation_utilities import calc, find_points_of_interest

def plot_curve(    starting_capital: float,
                   contribution_per_compounding_period: float,
                   compounding_periods_per_year: int = 1, 
                   real_return_rate: float = 0.05,
                   num_years: int = 10):

    df = calc(
        starting_capital,
        contribution_per_compounding_period,
        compounding_periods_per_year = compounding_periods_per_year,
        real_return_rate = real_return_rate,
        num_years = num_years
    )

    #curdoc().theme = 'dark_minimal'

    p = figure(
        x_range=(0, df.years_elapsed.max()), 
        y_range=(0, 1.1*df.total.max()),
        height=300
    )
    p.xaxis.ticker = list(range(1, round(df.years_elapsed.max() + 1)))

    v_areas = p.varea_stack(
        stackers=['contributions', 'accrued_gains'], 
        x='years_elapsed', 
        color=brewer['Spectral'][10][3:5], 
        legend_label=['Contributions', 'Accrued Gains'], 
        source=df,
        hover_alpha=0.75,
        fill_alpha=0.5,
        hover_color=brewer['Spectral'][10][3:5],
    )
    p.add_tools(
        HoverTool(
            tooltips=[],
            mode='mouse'
        )
    )

    total_line = p.line(
        x='years_elapsed', 
        y='total', 
        line_color='red', 
        source=df,
        legend_label='Total Value',
        line_width=3
    )
    p.add_layout(total_line)
    
    doubling_points_df, overtaking_points_df = find_points_of_interest(
        df,
        starting_capital,
        contribution_per_compounding_period
    )
    if overtaking_points_df.shape[0] > 0:
        first = int(overtaking_points_df.years_elapsed.values.min())
        xs = list(
            range(first, round(df.years_elapsed.values.max())+1)
        )
        varea = p.varea(
            x=xs,
            y1=0, 
            y2=[1.1*overtaking_points_df.total.values.max()]*len(xs), 
            alpha=0.1,
            fill_color='blue',
            legend_label='Gains > Contribution'
        )
        p.add_layout(varea)
        
    if doubling_points_df.shape[0] > 0:        
        factor_points = p.scatter(
            'years_elapsed',
            'total',
            source=doubling_points_df,
            fill_alpha=1,
            fill_color='red',
            line_color='white',
            size=12,
            marker='star',
            legend_label='Multiple of Starting Capital'
        )
        p.add_layout(factor_points)      
    
    p.add_tools(HoverTool(
        tooltips=[
            ('Years Since Initial Contribution',   '@years_elapsed'),
            ('Total Contributions',  '$@contributions'), 
            ('Accrued Gains', '$@accrued_gains'),
            ('Total', '$@total')
        ],
        mode='mouse'
    ))
    
    p.legend.location = "top_left"
    p.legend.orientation = "vertical"
    p.legend.background_fill_color = "#fafafa"

    p.grid.minor_grid_line_alpha = 0
    p.xaxis.axis_label = "Years Since Initial Contribution"
    p.yaxis.axis_label = "Value"
    p.toolbar.logo = None
    p.toolbar_location = None
    return  p, \
            doubling_points_df.years_elapsed.values[0] if doubling_points_df.shape[0] > 0 else None, \
            df.total.values[-1], \
            df.accrued_gains.values[-1], \
            overtaking_points_df.years_elapsed.values[0] if overtaking_points_df.shape[0] > 0 else None

def plot_curve_with_highlights( starting_capital: float,
                                contribution_per_compounding_period: float,
                                compounding_periods_per_year: int = 1, 
                                real_return_rate: float = 0.05,
                                num_years: int = 10):
    p, \
    years_to_first_doubling, \
    total, \
    total_accrued_gains, \
    years_to_overtaking = plot_curve(    
        starting_capital,
        contribution_per_compounding_period,
        compounding_periods_per_year = compounding_periods_per_year,
        real_return_rate = real_return_rate,
        num_years = num_years,
    )
    summary = f"""## Summary
___
In this scenario:

* you would have grown your starting capital **~{round(total/starting_capital, 1)}x**.
* you would have approximately **${round(total, 2)}** after {num_years} years.
* your accrued gains would total to roughly **${round(total_accrued_gains, 2)}**.
"""
    if years_to_first_doubling:
        summary += f"* **your starting capital doubled** for the first time **after {round(years_to_first_doubling)} years**."
    if years_to_overtaking:
        summary += f"\n* the **gains realized through your {real_return_rate} real return rate** would have **surpassed your ${contribution_per_compounding_period} contributions** after **{round(years_to_overtaking)} years**."

    return pn.Column(p, summary)
