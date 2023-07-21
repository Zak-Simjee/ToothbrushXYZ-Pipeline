"""Page for sales queries on dash web app"""

from dash import html, dcc, register_page, Output, Input, callback

from pages.plot import get_tb_df, pyramid_plot, hour_of_day_plot

register_page(__name__)

toothbrush_data = get_tb_df()

layout = html.Main(children=[html.H1("Sales"), 
                             html.Div('''Visualisations for Sales queries.'''),
                             dcc.Graph(id="pyramid", figure=pyramid_plot(toothbrush_data)),
                             html.Div(children=[dcc.Dropdown(["Toothbrush 2000", "Toothbrush 4000"], value="Toothbrush 2000", id="tb_dropdown"),
                                                dcc.Graph(id="hour_of_day", figure=hour_of_day_plot(toothbrush_data, "2000"))])
                             ])

@callback(Output(component_id="hour_of_day", component_property="figure"),
          Input(component_id="tb_dropdown", component_property="value"))
def change_toothbrush_type(value):
    return hour_of_day_plot(toothbrush_data, value.split()[1])