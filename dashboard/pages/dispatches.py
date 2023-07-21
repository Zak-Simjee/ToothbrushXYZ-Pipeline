"""Page for dispatch queries on dash web app"""

from dash import html, dcc, register_page

from pages.plot import get_tb_df, dispatch_time_plot

register_page(__name__)

toothbrush_data = get_tb_df()

layout = html.Main(children=[
    html.H1("Dispatches"),
    html.Div(children="Visualisations for Dispatch queries."),
    dcc.Graph(figure=dispatch_time_plot(toothbrush_data))
    ]
)