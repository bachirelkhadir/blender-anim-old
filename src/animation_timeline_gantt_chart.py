#!/usr/bin/env python3

import plotly.express as px
import pandas as pd

def outline_to_gantt(outline):
    outline = pd.DataFrame(outline)
    fig = px.timeline(outline, x_start="start", x_end="end", y="name",
                      color="animation")
    fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up
    return fig
