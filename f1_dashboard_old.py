"""
F1 Telemetry Dashboard - 2025 Season
Built with Dash/Plotly and FastF1
"""

import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import fastf1
import pandas as pd
import numpy as np
from datetime import datetime

# Enable FastF1 cache
fastf1.Cache.enable_cache('/tmp/fastf1_cache')

# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "F1 Telemetry Dashboard"

# Color scheme inspired by the reference image
COLORS = {
    'background': '#0a0e27',
    'card_bg': '#151932',
    'card_border': '#1e2442',
    'primary': '#9b87f5',
    'primary_hover': '#b5a3ff',
    'accent': '#7c3aed',
    'text_primary': '#ffffff',
    'text_secondary': '#8b92b8',
    'success': '#10b981',
    'danger': '#ef4444',
    'warning': '#f59e0b',
    'chart_line_1': '#9b87f5',
    'chart_line_2': '#f59e0b',
    'chart_line_3': '#10b981',
}

# CSS will be loaded from assets/custom.css automatically

# Dashboard Layout
app.layout = html.Div(style={
    'backgroundColor': COLORS['background'],
    'minHeight': '100vh',
    'padding': '20px'
}, children=[
    # Header
    html.Div(style={
        'background': f'linear-gradient(135deg, {COLORS["card_bg"]} 0%, {COLORS["accent"]} 100%)',
        'padding': '30px',
        'borderRadius': '16px',
        'marginBottom': '24px',
        'border': f'1px solid {COLORS["card_border"]}'
    }, children=[
        html.H1('🏎️ F1 Telemetry Dashboard', style={
            'fontSize': '42px',
            'fontWeight': '700',
            'marginBottom': '8px',
            'background': 'linear-gradient(90deg, #ffffff 0%, #9b87f5 100%)',
            'WebkitBackgroundClip': 'text',
            'WebkitTextFillColor': 'transparent'
        }),
        html.P('Real-time analysis of Formula 1 telemetry data - 2025 Season', style={
            'fontSize': '16px',
            'color': COLORS['text_secondary'],
            'margin': '0'
        })
    ]),

    # Session Selector Card
    html.Div(className='card', children=[
        html.H3('📊 Session Selector', style={'color': COLORS['text_primary'], 'marginBottom': '20px'}),
        html.Div(style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(200px, 1fr))', 'gap': '16px'}, children=[
            html.Div([
                html.Label('Year', style={'color': COLORS['text_secondary'], 'fontSize': '14px', 'marginBottom': '8px', 'display': 'block'}),
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[{'label': str(year), 'value': year} for year in range(2025, 2022, -1)],
                    value=2024,
                    style={
                        'backgroundColor': COLORS['card_bg'],
                        'color': COLORS['text_primary']
                    },
                    className='custom-dropdown'
                )
            ]),
            html.Div([
                html.Label('Grand Prix', style={'color': COLORS['text_secondary'], 'fontSize': '14px', 'marginBottom': '8px', 'display': 'block'}),
                dcc.Dropdown(
                    id='race-dropdown',
                    value='Abu Dhabi',
                    style={
                        'backgroundColor': COLORS['card_bg'],
                        'color': COLORS['text_primary']
                    }
                )
            ]),
            html.Div([
                html.Label('Session', style={'color': COLORS['text_secondary'], 'fontSize': '14px', 'marginBottom': '8px', 'display': 'block'}),
                dcc.Dropdown(
                    id='session-dropdown',
                    options=[
                        {'label': '🏁 Race', 'value': 'R'},
                        {'label': '🔥 Qualifying', 'value': 'Q'},
                        {'label': '🔧 Practice 1', 'value': 'FP1'},
                        {'label': '🔧 Practice 2', 'value': 'FP2'},
                        {'label': '🔧 Practice 3', 'value': 'FP3'},
                        {'label': '🚀 Sprint', 'value': 'S'},
                    ],
                    value='R',
                    style={
                        'backgroundColor': COLORS['card_bg'],
                        'color': COLORS['text_primary']
                    }
                )
            ]),
        ]),
        html.Div(style={'marginTop': '20px', 'textAlign': 'center'}, children=[
            html.Button('Load Session Data', id='load-button', n_clicks=0, style={
                'background': f'linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["accent"]} 100%)',
                'border': 'none',
                'color': 'white',
                'padding': '12px 32px',
                'borderRadius': '8px',
                'fontSize': '16px',
                'fontWeight': '600',
                'cursor': 'pointer',
                'transition': 'all 0.3s',
                'boxShadow': '0 4px 12px rgba(155, 135, 245, 0.3)'
            })
        ])
    ]),

    # Loading indicator
    dcc.Loading(
        id="loading",
        type="cube",
        color=COLORS['primary'],
        children=[
            html.Div(id='session-info'),

            # Driver Selector
            html.Div(id='driver-selector-container'),

            # Main Content Grid
            html.Div(style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(400px, 1fr))', 'gap': '20px'}, children=[
                # Lap Times Chart
                html.Div(className='card', children=[
                    html.H3('⏱️ Lap Time Analysis', style={'color': COLORS['text_primary']}),
                    dcc.Graph(id='lap-times-chart', config={'displayModeBar': False})
                ]),

                # Speed Comparison
                html.Div(className='card', children=[
                    html.H3('🚀 Speed Comparison', style={'color': COLORS['text_primary']}),
                    dcc.Graph(id='speed-chart', config={'displayModeBar': False})
                ]),
            ]),

            # Telemetry Chart
            html.Div(className='card', children=[
                html.H3('📡 Detailed Telemetry', style={'color': COLORS['text_primary']}),
                dcc.Graph(id='telemetry-chart', config={'displayModeBar': False}, style={'height': '600px'})
            ]),

            # Track Position Map
            html.Div(className='card', children=[
                html.H3('🗺️ Track Position & Speed Heatmap', style={'color': COLORS['text_primary']}),
                dcc.Graph(id='track-map', config={'displayModeBar': False}, style={'height': '600px'})
            ]),

            # Additional Stats
            html.Div(style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(250px, 1fr))', 'gap': '20px'}, children=[
                html.Div(className='card', children=[
                    html.H3('🏁 Tire Strategy', style={'color': COLORS['text_primary']}),
                    dcc.Graph(id='tire-strategy', config={'displayModeBar': False})
                ]),
                html.Div(className='card', children=[
                    html.H3('🌤️ Weather Conditions', style={'color': COLORS['text_primary']}),
                    html.Div(id='weather-info')
                ]),
            ])
        ]
    ),

    # Hidden div to store session data
    dcc.Store(id='session-data'),
])

# Callback to populate race dropdown based on year
@app.callback(
    Output('race-dropdown', 'options'),
    Input('year-dropdown', 'value')
)
def update_races(year):
    try:
        schedule = fastf1.get_event_schedule(year)
        races = [{'label': f"{row['EventName']}", 'value': row['EventName']}
                for idx, row in schedule.iterrows()]
        return races
    except:
        return [{'label': 'Abu Dhabi', 'value': 'Abu Dhabi'}]

# Main callback to load session data
@app.callback(
    [Output('session-data', 'data'),
     Output('session-info', 'children')],
    [Input('load-button', 'n_clicks')],
    [State('year-dropdown', 'value'),
     State('race-dropdown', 'value'),
     State('session-dropdown', 'value')]
)
def load_session(n_clicks, year, race, session_type):
    if n_clicks == 0:
        return None, html.Div()

    try:
        # Load session
        session = fastf1.get_session(year, race, session_type)
        session.load()

        # Get basic info
        drivers = session.drivers
        driver_info = []
        for drv in drivers:
            driver = session.get_driver(drv)
            driver_info.append({
                'number': drv,
                'name': driver['FullName'],
                'team': driver['TeamName'],
                'abbreviation': driver['Abbreviation']
            })

        # Session info display
        info_card = html.Div(className='card', style={'marginTop': '20px'}, children=[
            html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'}, children=[
                html.Div([
                    html.H2(f"{session.event['EventName']} - {session.name}", style={'color': COLORS['text_primary'], 'marginBottom': '8px'}),
                    html.P(f"📅 {session.event['EventDate']}", style={'color': COLORS['text_secondary'], 'fontSize': '14px'})
                ]),
                html.Div([
                    html.Span(f"{len(drivers)} Drivers", className='pill')
                ])
            ])
        ])

        return {'year': year, 'race': race, 'session_type': session_type, 'drivers': driver_info}, info_card

    except Exception as e:
        error_card = html.Div(className='card', style={'background': f'linear-gradient(135deg, {COLORS["danger"]}22 0%, {COLORS["danger"]}11 100%)', 'border': f'1px solid {COLORS["danger"]}'}, children=[
            html.H3('❌ Error Loading Session', style={'color': COLORS['danger']}),
            html.P(str(e), style={'color': COLORS['text_secondary']})
        ])
        return None, error_card

# Callback to create driver selector
@app.callback(
    Output('driver-selector-container', 'children'),
    Input('session-data', 'data')
)
def create_driver_selector(session_data):
    if not session_data:
        return html.Div()

    driver_options = [{'label': f"{d['abbreviation']} - {d['name']} ({d['team']})", 'value': d['number']}
                     for d in session_data['drivers']]

    return html.Div(className='card', children=[
        html.H3('👥 Select Drivers to Compare', style={'color': COLORS['text_primary'], 'marginBottom': '20px'}),
        dcc.Dropdown(
            id='driver-selector',
            options=driver_options,
            value=[session_data['drivers'][0]['number'], session_data['drivers'][1]['number']] if len(session_data['drivers']) >= 2 else [session_data['drivers'][0]['number']],
            multi=True,
            style={'backgroundColor': COLORS['card_bg'], 'color': COLORS['text_primary']}
        )
    ])

# Callback for lap times chart
@app.callback(
    Output('lap-times-chart', 'figure'),
    [Input('driver-selector', 'value')],
    [State('session-data', 'data')]
)
def update_lap_times(selected_drivers, session_data):
    fig = go.Figure()

    if not session_data or not selected_drivers:
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor=COLORS['card_bg'],
            plot_bgcolor=COLORS['card_bg'],
            font=dict(color=COLORS['text_primary'])
        )
        return fig

    try:
        session = fastf1.get_session(session_data['year'], session_data['race'], session_data['session_type'])
        session.load()

        colors_list = [COLORS['chart_line_1'], COLORS['chart_line_2'], COLORS['chart_line_3'], '#ef4444', '#10b981']

        for idx, driver in enumerate(selected_drivers[:5]):
            laps = session.laps.pick_driver(driver)
            laps = laps[laps['LapTime'].notna()]

            lap_times = laps['LapTime'].dt.total_seconds()

            driver_info = next((d for d in session_data['drivers'] if d['number'] == driver), None)
            driver_name = driver_info['abbreviation'] if driver_info else str(driver)

            fig.add_trace(go.Scatter(
                x=laps['LapNumber'],
                y=lap_times,
                mode='lines+markers',
                name=driver_name,
                line=dict(color=colors_list[idx % len(colors_list)], width=3),
                marker=dict(size=6)
            ))

        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor=COLORS['card_bg'],
            plot_bgcolor=COLORS['card_bg'],
            font=dict(color=COLORS['text_primary'], family='Inter'),
            xaxis_title='Lap Number',
            yaxis_title='Lap Time (seconds)',
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=40, r=40, t=40, b=40)
        )

    except Exception as e:
        print(f"Error in lap times: {e}")

    return fig

# Callback for speed comparison
@app.callback(
    Output('speed-chart', 'figure'),
    [Input('driver-selector', 'value')],
    [State('session-data', 'data')]
)
def update_speed_chart(selected_drivers, session_data):
    fig = go.Figure()

    if not session_data or not selected_drivers:
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor=COLORS['card_bg'],
            plot_bgcolor=COLORS['card_bg'],
            font=dict(color=COLORS['text_primary'])
        )
        return fig

    try:
        session = fastf1.get_session(session_data['year'], session_data['race'], session_data['session_type'])
        session.load()

        colors_list = [COLORS['chart_line_1'], COLORS['chart_line_2'], COLORS['chart_line_3'], '#ef4444', '#10b981']

        for idx, driver in enumerate(selected_drivers[:5]):
            laps = session.laps.pick_driver(driver)
            fastest_lap = laps.pick_fastest()

            if fastest_lap is not None and not fastest_lap.empty:
                telemetry = fastest_lap.get_telemetry()

                driver_info = next((d for d in session_data['drivers'] if d['number'] == driver), None)
                driver_name = driver_info['abbreviation'] if driver_info else str(driver)

                fig.add_trace(go.Scatter(
                    x=telemetry['Distance'],
                    y=telemetry['Speed'],
                    mode='lines',
                    name=driver_name,
                    line=dict(color=colors_list[idx % len(colors_list)], width=2.5)
                ))

        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor=COLORS['card_bg'],
            plot_bgcolor=COLORS['card_bg'],
            font=dict(color=COLORS['text_primary'], family='Inter'),
            xaxis_title='Distance (m)',
            yaxis_title='Speed (km/h)',
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=40, r=40, t=40, b=40)
        )

    except Exception as e:
        print(f"Error in speed chart: {e}")

    return fig

# Callback for detailed telemetry
@app.callback(
    Output('telemetry-chart', 'figure'),
    [Input('driver-selector', 'value')],
    [State('session-data', 'data')]
)
def update_telemetry(selected_drivers, session_data):
    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=True,
        subplot_titles=('Speed', 'Throttle %', 'Brake', 'Gear'),
        vertical_spacing=0.05
    )

    if not session_data or not selected_drivers:
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor=COLORS['card_bg'],
            plot_bgcolor=COLORS['card_bg'],
            font=dict(color=COLORS['text_primary'])
        )
        return fig

    try:
        session = fastf1.get_session(session_data['year'], session_data['race'], session_data['session_type'])
        session.load()

        colors_list = [COLORS['chart_line_1'], COLORS['chart_line_2'], COLORS['chart_line_3'], '#ef4444', '#10b981']

        for idx, driver in enumerate(selected_drivers[:3]):  # Limit to 3 for readability
            laps = session.laps.pick_driver(driver)
            fastest_lap = laps.pick_fastest()

            if fastest_lap is not None and not fastest_lap.empty:
                telemetry = fastest_lap.get_telemetry()
                driver_info = next((d for d in session_data['drivers'] if d['number'] == driver), None)
                driver_name = driver_info['abbreviation'] if driver_info else str(driver)
                color = colors_list[idx % len(colors_list)]

                # Speed
                fig.add_trace(go.Scatter(
                    x=telemetry['Distance'], y=telemetry['Speed'],
                    mode='lines', name=driver_name, line=dict(color=color, width=2),
                    showlegend=True
                ), row=1, col=1)

                # Throttle
                fig.add_trace(go.Scatter(
                    x=telemetry['Distance'], y=telemetry['Throttle'],
                    mode='lines', name=driver_name, line=dict(color=color, width=2),
                    showlegend=False
                ), row=2, col=1)

                # Brake
                fig.add_trace(go.Scatter(
                    x=telemetry['Distance'], y=telemetry['Brake'],
                    mode='lines', name=driver_name, line=dict(color=color, width=2),
                    showlegend=False,
                    fill='tozeroy', fillcolor=f'rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.3)'
                ), row=3, col=1)

                # Gear
                fig.add_trace(go.Scatter(
                    x=telemetry['Distance'], y=telemetry['nGear'],
                    mode='lines', name=driver_name, line=dict(color=color, width=2),
                    showlegend=False
                ), row=4, col=1)

        fig.update_xaxes(title_text="Distance (m)", row=4, col=1)
        fig.update_yaxes(title_text="km/h", row=1, col=1)
        fig.update_yaxes(title_text="%", row=2, col=1)
        fig.update_yaxes(title_text="On/Off", row=3, col=1)
        fig.update_yaxes(title_text="Gear", row=4, col=1)

        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor=COLORS['card_bg'],
            plot_bgcolor=COLORS['card_bg'],
            font=dict(color=COLORS['text_primary'], family='Inter'),
            hovermode='x unified',
            height=600,
            margin=dict(l=40, r=40, t=60, b=40),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

    except Exception as e:
        print(f"Error in telemetry: {e}")

    return fig

# Callback for track map
@app.callback(
    Output('track-map', 'figure'),
    [Input('driver-selector', 'value')],
    [State('session-data', 'data')]
)
def update_track_map(selected_drivers, session_data):
    fig = go.Figure()

    if not session_data or not selected_drivers:
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor=COLORS['card_bg'],
            plot_bgcolor=COLORS['card_bg'],
            font=dict(color=COLORS['text_primary'])
        )
        return fig

    try:
        session = fastf1.get_session(session_data['year'], session_data['race'], session_data['session_type'])
        session.load()

        colors_list = [COLORS['chart_line_1'], COLORS['chart_line_2'], COLORS['chart_line_3'], '#ef4444', '#10b981']

        for idx, driver in enumerate(selected_drivers[:3]):
            laps = session.laps.pick_driver(driver)
            fastest_lap = laps.pick_fastest()

            if fastest_lap is not None and not fastest_lap.empty:
                telemetry = fastest_lap.get_telemetry()
                driver_info = next((d for d in session_data['drivers'] if d['number'] == driver), None)
                driver_name = driver_info['abbreviation'] if driver_info else str(driver)

                # Create speed-colored track line
                fig.add_trace(go.Scatter(
                    x=telemetry['X'],
                    y=telemetry['Y'],
                    mode='lines',
                    name=driver_name,
                    line=dict(
                        color=colors_list[idx % len(colors_list)],
                        width=4
                    ),
                    hovertemplate=f'<b>{driver_name}</b><br>Speed: %{{text}} km/h<extra></extra>',
                    text=telemetry['Speed'].round(1)
                ))

        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor=COLORS['card_bg'],
            plot_bgcolor=COLORS['card_bg'],
            font=dict(color=COLORS['text_primary'], family='Inter'),
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, scaleanchor="x", scaleratio=1),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=20, r=20, t=40, b=20),
            hovermode='closest'
        )

    except Exception as e:
        print(f"Error in track map: {e}")

    return fig

# Callback for tire strategy
@app.callback(
    Output('tire-strategy', 'figure'),
    [Input('driver-selector', 'value')],
    [State('session-data', 'data')]
)
def update_tire_strategy(selected_drivers, session_data):
    fig = go.Figure()

    if not session_data or not selected_drivers:
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor=COLORS['card_bg'],
            plot_bgcolor=COLORS['card_bg'],
            font=dict(color=COLORS['text_primary'])
        )
        return fig

    try:
        session = fastf1.get_session(session_data['year'], session_data['race'], session_data['session_type'])
        session.load()

        compound_colors = {
            'SOFT': '#ef4444',
            'MEDIUM': '#f59e0b',
            'HARD': '#ffffff',
            'INTERMEDIATE': '#10b981',
            'WET': '#3b82f6'
        }

        for idx, driver in enumerate(selected_drivers[:5]):
            laps = session.laps.pick_driver(driver)
            driver_info = next((d for d in session_data['drivers'] if d['number'] == driver), None)
            driver_name = driver_info['abbreviation'] if driver_info else str(driver)

            stints = laps[['LapNumber', 'Compound', 'TyreLife']].copy()
            stints = stints.dropna(subset=['Compound'])

            for _, stint in stints.groupby((stints['Compound'] != stints['Compound'].shift()).cumsum()):
                if not stint.empty:
                    compound = stint.iloc[0]['Compound']
                    color = compound_colors.get(compound, '#9b87f5')

                    fig.add_trace(go.Scatter(
                        x=stint['LapNumber'],
                        y=[driver_name] * len(stint),
                        mode='markers',
                        marker=dict(
                            size=12,
                            color=color,
                            symbol='square',
                            line=dict(width=1, color='white')
                        ),
                        name=compound if idx == 0 else None,
                        showlegend=(idx == 0),
                        hovertemplate=f'<b>{driver_name}</b><br>Lap: %{{x}}<br>Compound: {compound}<extra></extra>'
                    ))

        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor=COLORS['card_bg'],
            plot_bgcolor=COLORS['card_bg'],
            font=dict(color=COLORS['text_primary'], family='Inter'),
            xaxis_title='Lap Number',
            yaxis_title='Driver',
            hovermode='closest',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=40, r=40, t=40, b=40)
        )

    except Exception as e:
        print(f"Error in tire strategy: {e}")

    return fig

# Callback for weather info
@app.callback(
    Output('weather-info', 'children'),
    [Input('session-data', 'data')]
)
def update_weather(session_data):
    if not session_data:
        return html.Div()

    try:
        session = fastf1.get_session(session_data['year'], session_data['race'], session_data['session_type'])
        session.load()

        weather = session.weather_data

        if weather.empty:
            return html.P("No weather data available", style={'color': COLORS['text_secondary']})

        # Get average weather conditions
        avg_air_temp = weather['AirTemp'].mean()
        avg_track_temp = weather['TrackTemp'].mean()
        avg_humidity = weather['Humidity'].mean()
        avg_pressure = weather['Pressure'].mean()
        rainfall = weather['Rainfall'].any()
        avg_wind_speed = weather['WindSpeed'].mean()

        return html.Div([
            html.Div(className='metric-card', style={'marginBottom': '16px'}, children=[
                html.Div(className='metric-label', children='Air Temperature'),
                html.Div(className='metric-value', children=f"{avg_air_temp:.1f}°C")
            ]),
            html.Div(className='metric-card', style={'marginBottom': '16px'}, children=[
                html.Div(className='metric-label', children='Track Temperature'),
                html.Div(className='metric-value', children=f"{avg_track_temp:.1f}°C")
            ]),
            html.Div(className='metric-card', style={'marginBottom': '16px'}, children=[
                html.Div(className='metric-label', children='Humidity'),
                html.Div(className='metric-value', children=f"{avg_humidity:.1f}%")
            ]),
            html.Div(className='metric-card', style={'marginBottom': '16px'}, children=[
                html.Div(className='metric-label', children='Wind Speed'),
                html.Div(className='metric-value', children=f"{avg_wind_speed:.1f} km/h")
            ]),
            html.Div(className='metric-card', children=[
                html.Div(className='metric-label', children='Rainfall'),
                html.Div(className='metric-value', style={'color': COLORS['danger'] if rainfall else COLORS['success']},
                        children='Yes ☔' if rainfall else 'No ☀️')
            ])
        ])

    except Exception as e:
        return html.P(f"Error loading weather: {str(e)}", style={'color': COLORS['danger']})

# Run the app
if __name__ == '__main__':
    print("\n" + "="*60)
    print("🏎️  F1 Telemetry Dashboard Starting...")
    print("="*60)
    print("📊 Dashboard will be available at: http://127.0.0.1:8050")
    print("🔄 Press Ctrl+C to stop the server")
    print("="*60 + "\n")

    app.run(debug=True, port=8050)
