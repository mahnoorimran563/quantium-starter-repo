# tests/test_app_ui.py
import pytest
from dash.testing.application_runners import import_app

@pytest.fixture
def dash_app():
    app = import_app("app")  # Assumes your Dash app is in app.py
    return app

def test_header_present(dash_duo, dash_app):
    dash_duo.start_server(dash_app)
    header = dash_duo.find_element("h1")
    assert "Pink Morsel Sales Visualiser" in header.text

def test_graph_present(dash_duo, dash_app):
    dash_duo.start_server(dash_app)
    graph = dash_duo.find_element("#sales-line-chart")
    assert graph is not None

def test_region_picker_present(dash_duo, dash_app):
    dash_duo.start_server(dash_app)
    region_picker = dash_duo.find_element("#region-filter")
    assert region_picker is not None
