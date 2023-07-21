"""Setup and run a Dash web app for Toothbrush XYZ data"""

from dash import Dash, html, page_container, dcc, page_registry

app = Dash(__name__, use_pages=True)

app.layout = html.Main([
	html.H1('Toothbrush XYZ Dashboard'),

    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']}", href=page["relative_path"]
                )
            )
            for page in page_registry.values()
        ]
    ),

	page_container
])

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True, port=8080)