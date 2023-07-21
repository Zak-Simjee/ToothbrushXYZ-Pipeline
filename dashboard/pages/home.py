"""Homepage for dash web app"""

from dash import html, register_page

register_page(__name__, path='/')

layout = (html.H1('Please select a page of visualisations.'))