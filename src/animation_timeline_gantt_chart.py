#!/usr/bin/env python3

import plotly.express as px
import pandas as pd


# https://stackoverflow.com/questions/66078893/plotly-express-timeline-for-gantt-chart-with-integer-xaxis

def my_process_dataframe_timeline(args):
    """
    Massage input for bar traces for px.timeline()
    """
    args["is_timeline"] = True
    if args["x_start"] is None or args["x_end"] is None:
        raise ValueError("Both x_start and x_end are required")

    x_start = args["data_frame"][args["x_start"]]
    x_end = args["data_frame"][args["x_end"]]

    # note that we are not adding any columns to the data frame here, so no risk of overwrite
    args["data_frame"][args["x_end"]] = (x_end - x_start)
    args["x"] = args["x_end"]
    del args["x_end"]
    args["base"] = args["x_start"]
    del args["x_start"]
    return args
px._core.process_dataframe_timeline = my_process_dataframe_timeline


def outline_to_gantt(outline):
    outline = pd.DataFrame(outline)
    fig = px.timeline(outline, x_start="start", x_end="end", y="name",
                      color="animation")
    fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up
    outline["start"] -= 1
    outline['delta'] = outline['end'] - outline['start']
    fig.layout.xaxis.type = 'linear'
    #fig.data[0].x = outline.delta.tolist()
    #fig = fig.full_figure_for_development(warn=False)
    return fig
