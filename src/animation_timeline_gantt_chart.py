#!/usr/bin/env python3

import plotly.express as px
import pandas as pd

def outline_to_gantt(outline):
    outline = pd.DataFrame(outline)
    print(outline.head())
