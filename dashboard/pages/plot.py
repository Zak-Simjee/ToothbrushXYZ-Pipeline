"""Module to provide functions for loading toothbrush xyz production data 
and plotting visualisations."""

from os import environ
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
config = environ
DB_URI = f"postgresql+psycopg2://{config['DB_USER']}:{config['DB_PASS']}@{config['DB_HOST']}:{config['DB_PORT']}/{config['DB_NAME']}"
SCHEMA = "week4_zaak_production"

def get_tb_df() -> pd.DataFrame:
    """Return toothbrush xyz data using an sqlalchemy engine"""

    engine = create_engine(DB_URI)
    return pd.read_sql_table("production_ecommerce", engine, schema=SCHEMA)


def dispatch_time_plot(df: pd.DataFrame) -> go.Figure:
    """Create a bar chart for order to dispatch time in hours for toothbrush xyz data"""

    avg_time_df = df.copy()

    avg_time_df = avg_time_df[avg_time_df["dispatch_status"] == "Dispatched"]

    avg_time_df["diff"] = avg_time_df["dispatched_date"] - avg_time_df["order_date"]

    hour_count = avg_time_df['diff'].groupby(avg_time_df["diff"].dt.components["hours"]).count()

    fig = px.bar(x=hour_count.index, y=hour_count, color=hour_count.index, 
                 labels={"x": "Time Taken in Hours", "y": "Number of Dispatches"}, 
                 title="Order to Dispatch Time in Hours")

    return fig


def pyramid_plot(df: pd.DataFrame) -> go.Figure:
    """Create a pyramid plot for sales per age group for toothbrush xyz data.
    Displays both toothbrush types"""

    pyramid_df = df.sort_values(by="customer_age")

    labels = [f"{num} - {num + 10}" for num in range(10, 100, 10)]

    pyramid_df["bins"] = pd.cut(df["customer_age"].sort_values(), bins=9, precision=0, labels=labels)

    tb_2000_pyramid = pyramid_df[pyramid_df["toothbrush_type"] == "Toothbrush 2000"].groupby(["bins", "toothbrush_type"], as_index=False).count()

    tb_4000_pyramid = pyramid_df[pyramid_df["toothbrush_type"] == "Toothbrush 4000"].groupby(["bins", "toothbrush_type"], as_index=False).count()

    tb_4000_pyramid["order_number"] = tb_4000_pyramid["order_number"].apply(lambda x: x / -1)

    layout = go.Layout(title="Sales per Age Group",
                       yaxis=go.layout.YAxis(title='Age'),
                       xaxis=go.layout.XAxis(
                            range=[-2000, 2000],
                            tickvals=[-2000, -1500, -1000, -500, 0, 500, 1000, 1500, 2000],
                            ticktext=[2000, 1500, 1000, 500, 0, 500, 1000, 1500, 2000],
                            title='Sales'),
                        barmode='overlay',
                        bargap=0)

    data = [go.Bar(y=tb_2000_pyramid["bins"],
                x=tb_2000_pyramid["order_number"],
                orientation='h',
                name='Toothbrush 2000',
                marker=dict(color='skyblue')
                ),
            go.Bar(y=tb_4000_pyramid["bins"],
                x=tb_4000_pyramid["order_number"],
                orientation='h',
                name='Toothbrush 4000',
                marker=dict(color='indianred')
                )]

    return go.Figure(data=data, layout=layout)


def hour_of_day_plot(df: pd.DataFrame, tb_type: str) -> go.Figure:
    """Create a bar chart for orders per hour of the day for toothbrush xyz data
    for a particular toothbrush type"""

    if tb_type == "2000":

        tb_2000_df =  df[df["toothbrush_type"] == "Toothbrush 2000"]

        orders_by_hour_2000 = tb_2000_df.groupby(tb_2000_df["order_date"].dt.hour).count()

        ax = px.bar(x=orders_by_hour_2000.index, y=orders_by_hour_2000["order_number"],
                    labels={"x": "Hour of the Day", "y": "Number of Orders"},
                    title="Orders per Hour of the Day for Toothbrush 2000", color=orders_by_hour_2000.index,
                    color_continuous_scale="thermal_r")

        return ax

    elif tb_type == "4000":

        tb_4000_df =  df[df["toothbrush_type"] == "Toothbrush 4000"]

        orders_by_hour_4000 = tb_4000_df.groupby(tb_4000_df["order_date"].dt.hour).count()

        ax = px.bar(x=orders_by_hour_4000.index, y=orders_by_hour_4000["order_number"],
                    labels={"x": "Hour of the Day", "y": "Number of Orders"},
                    title="Orders per Hour of the Day for Toothbrush 4000", color=orders_by_hour_4000.index,
                    color_continuous_scale="haline_r")

        return ax
    

def unsuccessful_deliveries_plot(df: pd.DataFrame) -> go.Figure:
    """Create a bar chart for unsuccessful deliveries per day for toothbrush xyz data"""

    unsuccessful_deliveries = df[df["delivery_status"] == "Unsuccessful"]

    bad_delivery_count = unsuccessful_deliveries.groupby(unsuccessful_deliveries["delivery_date"].dt.date).count()

    if len(bad_delivery_count.index) == 0:
        ax = go.Figure().add_annotation(x=2, y=2,text="No Data to Display",
                                        font=dict(size=25), showarrow=False, yshift=10)
        return ax

    ax = px.bar(x=bad_delivery_count.index, y=bad_delivery_count["order_number"],
                labels={"x": "Delivery Date", "y": "Unsuccessful Deliveries"},
                title="Number of Unsuccessful Deliveries per Day")
    
    ax.update_xaxes(dtick="%d-%m-%Y", tickformat="%d-%m-%Y")

    return ax


def deliveries_pie_chart(df: pd.DataFrame, tb_type: str) -> go.Figure:
    """Create a pie chart for proportions of delivery statuses for toothbrush xyz data
    for a particular toothbrush type or both"""

    if tb_type == "2000":

        tb_2000_df = df[df["toothbrush_type"] == "Toothbrush 2000"]

        deliveries = tb_2000_df.groupby("delivery_status").count()

        ax = px.pie(names=deliveries.index, values=deliveries["order_number"],
                    title="Chart of Current Delivery Statuses (Toothbrush 2000)")

        return ax
    
    elif tb_type == "4000":

        tb_4000_df = df[df["toothbrush_type"] == "Toothbrush 4000"]

        deliveries = tb_4000_df.groupby("delivery_status").count()

        ax = px.pie(names=deliveries.index, values=deliveries["order_number"],
                    title="Chart of Current Delivery Statuses (Toothbrush 4000)")

        return ax

    else:

        deliveries = df.groupby("delivery_status").count()

        ax = px.pie(names=deliveries.index, values=deliveries["order_number"],
                    title="Chart of Current Delivery Statuses (Total)")

        return ax