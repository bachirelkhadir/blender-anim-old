#!/usr/bin/env python3

import plotly.express as px
import pandas as pd

def outline_to_gantt(outline):
    outline = pd.DataFrame(outline)
    print(outline.head())
    fig = px.timeline(outline, x_start="start", x_end="end", y="name",
                      color="animation")
    fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up
    outline['delta'] = outline['start'] - outline['end']
    fig.layout.xaxis.type = 'linear'
    fig.data[0].x = outline.delta.tolist()
    f = fig.full_figure_for_development(warn=False)
    return fig
