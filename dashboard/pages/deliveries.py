"""Page for delivery queries on dash web app"""

from dash import html, dcc, register_page, callback, Input, Output

from pages.plot import get_tb_df, unsuccessful_deliveries_plot, deliveries_pie_chart

register_page(__name__)

toothbrush_data = get_tb_df()

layout = html.Main(children=[
    html.H1("Deliveries"),
    html.Div(children="Visualisations for Delivery queries."),
    html.H2("Current Deliveries"),
    dcc.Dropdown(["Total", "Toothbrush 2000", "Toothbrush 4000"], id="pie_dropdown", value="Total"),
    dcc.Graph(figure=deliveries_pie_chart(toothbrush_data, "2000"), id="tb_pie"),
    html.H2("Unsuccessful Deliveries"),
    dcc.Graph(figure=unsuccessful_deliveries_plot(toothbrush_data))
    ]
)

@callback(Output(component_id="tb_pie", component_property="figure"),
          Input(component_id="pie_dropdown", component_property="value"))
def change_tb_type(value):
    value = value.replace("Toothbrush ", "")
    return deliveries_pie_chart(toothbrush_data, value)
