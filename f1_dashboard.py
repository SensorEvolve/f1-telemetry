"""
F1 Telemetry Dashboard - 2025 Season
Built with Dash/Plotly and FastF1
"""

import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import fastf1
import pandas as pd

# Enable FastF1 cache
fastf1.Cache.enable_cache('/tmp/fastf1_cache')

# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "F1 Telemetry Dashboard"

# Color scheme - Monochrome base
COLORS = {
    'background': '#0a0a0a',
    'card_bg': '#1a1a1a',
    'primary': '#ffffff',
    'accent': '#2a2a2a',
    'text_primary': '#ffffff',
    'text_secondary': '#888888',
    'border': '#333333',
}

# F1 Team Colors (2024-2025 season)
TEAM_COLORS = {
    'Red Bull Racing': '#3671C6',
    'Ferrari': '#E8002D',
    'Mercedes': '#27F4D2',
    'McLaren': '#FF8000',
    'Aston Martin': '#229971',
    'Alpine': '#FF87BC',
    'Williams': '#64C4FF',
    'RB': '#6692FF',
    'Kick Sauber': '#52E252',
    'Haas F1 Team': '#B6BABD',
}

# Dashboard Layout
app.layout = html.Div(style={'backgroundColor': COLORS['background'], 'minHeight': '100vh', 'padding': '10px'}, children=[

    # Header
    html.Div(className='card', style={'padding': '15px', 'marginBottom': '12px', 'borderBottom': '1px solid #333'}, children=[
        html.H1('🏎️ F1 Telemetry Dashboard', style={'color': COLORS['text_primary'], 'marginBottom': '4px', 'fontWeight': '300', 'letterSpacing': '1px', 'fontSize': '18px'}),
        html.P('Formula 1 telemetry data analysis - Season 2021-2025', style={'color': COLORS['text_secondary'], 'fontSize': '11px'})
    ]),

    # Session Selector
    html.Div(className='card', style={'padding': '15px', 'paddingBottom': '20px', 'overflow': 'visible'}, children=[
        html.H3('📊 Session Selector', style={'color': COLORS['text_primary'], 'marginBottom': '12px', 'fontSize': '14px'}),
        html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr 1fr', 'gap': '10px', 'marginBottom': '12px'}, children=[
            html.Div([
                html.Label('Year', style={'color': COLORS['text_secondary'], 'display': 'block', 'marginBottom': '6px', 'fontSize': '11px', 'fontWeight': '500'}),
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[{'label': str(year), 'value': year} for year in range(2025, 2021, -1)],
                    value=2025,
                    clearable=False,
                    optionHeight=35
                )
            ]),
            html.Div([
                html.Label('Grand Prix', style={'color': COLORS['text_secondary'], 'display': 'block', 'marginBottom': '6px', 'fontSize': '11px', 'fontWeight': '500'}),
                dcc.Dropdown(
                    id='race-dropdown',
                    value='Abu Dhabi',
                    clearable=False,
                    optionHeight=35
                )
            ]),
            html.Div([
                html.Label('Session', style={'color': COLORS['text_secondary'], 'display': 'block', 'marginBottom': '6px', 'fontSize': '11px', 'fontWeight': '500'}),
                dcc.Dropdown(
                    id='session-dropdown',
                    options=[
                        {'label': '🏁 Race', 'value': 'R'},
                        {'label': '🔥 Qualifying', 'value': 'Q'},
                        {'label': '🔧 Practice 1', 'value': 'FP1'},
                        {'label': '🔧 Practice 2', 'value': 'FP2'},
                        {'label': '🔧 Practice 3', 'value': 'FP3'},
                    ],
                    value='R',
                    clearable=False,
                    optionHeight=35
                )
            ]),
        ]),
        html.Button('Load Session Data', id='load-button', n_clicks=0, style={
            'background': '#ffffff',
            'border': '1px solid #333',
            'color': '#000',
            'padding': '6px 16px',
            'borderRadius': '4px',
            'fontSize': '12px',
            'fontWeight': '600',
            'cursor': 'pointer',
            'width': '100%',
            'transition': 'all 0.2s'
        })
    ]),

    # Loading indicator
    dcc.Loading(id="loading", type="default", color=COLORS['primary'], children=[

        html.Div(id='session-info'),
        html.Div(id='driver-selector-container'),

        # Charts container
        html.Div(id='charts-container')
    ]),

    # Hidden store
    dcc.Store(id='session-data'),
])

# Callback: Update races based on year
@app.callback(
    Output('race-dropdown', 'options'),
    Input('year-dropdown', 'value')
)
def update_races(year):
    try:
        schedule = fastf1.get_event_schedule(year)
        # Reverse order so latest race is at top
        return [{'label': row['EventName'], 'value': row['EventName']} for idx, row in schedule.iloc[::-1].iterrows()]
    except:
        return [{'label': 'Abu Dhabi', 'value': 'Abu Dhabi'}]

# Callback: Load session
@app.callback(
    [Output('session-data', 'data'), Output('session-info', 'children')],
    [Input('load-button', 'n_clicks')],
    [State('year-dropdown', 'value'), State('race-dropdown', 'value'), State('session-dropdown', 'value')]
)
def load_session(n_clicks, year, race, session_type):
    if n_clicks == 0:
        return None, html.Div()

    try:
        session = fastf1.get_session(year, race, session_type)
        session.load()

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

        info_card = html.Div(className='card', style={'marginTop': '10px'}, children=[
            html.H2(f"{session.event['EventName']} - {session.name}", style={'color': COLORS['text_primary'], 'fontSize': '14px'}),
            html.P(f"📅 {session.event['EventDate']} | {len(drivers)} Drivers", style={'color': COLORS['text_secondary'], 'fontSize': '11px'})
        ])

        return {'year': year, 'race': race, 'session_type': session_type, 'drivers': driver_info}, info_card

    except Exception as e:
        return None, html.Div(className='card', style={'background': '#1a1a1a', 'marginTop': '10px', 'borderLeft': '2px solid #FF4444'}, children=[
            html.H3('❌ Error Loading Session', style={'color': '#FF4444', 'fontSize': '12px'}),
            html.P(str(e), style={'color': COLORS['text_secondary'], 'fontSize': '10px'})
        ])

# Callback: Driver selector
@app.callback(
    Output('driver-selector-container', 'children'),
    Input('session-data', 'data')
)
def create_driver_selector(session_data):
    if not session_data:
        return html.Div()

    options = [{'label': f"{d['abbreviation']} - {d['name']}", 'value': d['number']} for d in session_data['drivers']]
    default = [session_data['drivers'][i]['number'] for i in range(min(2, len(session_data['drivers'])))]

    return html.Div(className='card', children=[
        html.H3('👥 Select Drivers to Compare', style={'color': COLORS['text_primary'], 'marginBottom': '8px', 'fontSize': '12px'}),
        dcc.Dropdown(id='driver-selector', options=options, value=default, multi=True, maxHeight=300)
    ])

# Callback: Charts
@app.callback(
    Output('charts-container', 'children'),
    [Input('driver-selector', 'value')],
    [State('session-data', 'data')]
)
def update_charts(selected_drivers, session_data):
    if not session_data or not selected_drivers:
        return html.Div()

    try:
        session = fastf1.get_session(session_data['year'], session_data['race'], session_data['session_type'])
        session.load()

        # Get team colors for selected drivers
        driver_colors = {}
        for driver_num in selected_drivers:
            driver_info = next((d for d in session_data['drivers'] if d['number'] == driver_num), None)
            if driver_info:
                team_name = driver_info['team']
                driver_colors[driver_num] = TEAM_COLORS.get(team_name, '#ffffff')

        # LAP TIMES CHART
        lap_fig = go.Figure()

        # Find overall fastest lap across all selected drivers
        all_fastest_times = []
        for driver in selected_drivers[:5]:
            laps = session.laps.pick_driver(driver)
            laps = laps[laps['LapTime'].notna()]
            if not laps.empty:
                fastest = laps['LapTime'].min()
                all_fastest_times.append(fastest)

        overall_fastest = min(all_fastest_times) if all_fastest_times else None

        for idx, driver in enumerate(selected_drivers[:5]):
            laps = session.laps.pick_driver(driver)
            laps = laps[laps['LapTime'].notna()]
            lap_times = laps['LapTime'].dt.total_seconds()
            driver_info = next((d for d in session_data['drivers'] if d['number'] == driver), None)
            driver_name = driver_info['abbreviation'] if driver_info else str(driver)
            color = driver_colors.get(driver, '#ffffff')

            # Regular lap trace
            lap_fig.add_trace(go.Scatter(
                x=laps['LapNumber'], y=lap_times,
                mode='lines+markers', name=driver_name,
                line=dict(color=color, width=2),
                marker=dict(size=4, color=color)
            ))

            # Highlight fastest lap in purple
            if overall_fastest and not laps.empty:
                fastest_lap = laps[laps['LapTime'] == overall_fastest]
                if not fastest_lap.empty:
                    fastest_lap_time = fastest_lap['LapTime'].dt.total_seconds().iloc[0]
                    fastest_lap_num = fastest_lap['LapNumber'].iloc[0]
                    lap_fig.add_trace(go.Scatter(
                        x=[fastest_lap_num],
                        y=[fastest_lap_time],
                        mode='markers',
                        name=f'{driver_name} FL',
                        marker=dict(size=12, color='#9b59b6', symbol='star', line=dict(color='white', width=1)),
                        showlegend=False
                    ))

        lap_fig.update_layout(
            template='plotly_dark',
            paper_bgcolor=COLORS['card_bg'],
            plot_bgcolor=COLORS['card_bg'],
            font=dict(color=COLORS['text_primary'], size=10),
            xaxis_title='Lap Number',
            yaxis_title='Lap Time (s)',
            height=175,
            margin=dict(l=30, r=20, t=10, b=30),
            autosize=False
        )

        # SPEED CHART
        speed_fig = go.Figure()
        for idx, driver in enumerate(selected_drivers[:3]):
            laps = session.laps.pick_driver(driver)
            fastest = laps.pick_fastest()
            if fastest is not None and not fastest.empty:
                telemetry = fastest.get_telemetry()
                driver_info = next((d for d in session_data['drivers'] if d['number'] == driver), None)
                driver_name = driver_info['abbreviation'] if driver_info else str(driver)
                color = driver_colors.get(driver, '#ffffff')

                speed_fig.add_trace(go.Scatter(
                    x=telemetry['Distance'], y=telemetry['Speed'],
                    mode='lines', name=driver_name,
                    line=dict(color=color, width=3)
                ))

        speed_fig.update_layout(
            template='plotly_dark',
            paper_bgcolor=COLORS['card_bg'],
            plot_bgcolor=COLORS['card_bg'],
            font=dict(color=COLORS['text_primary'], size=10),
            xaxis_title='Distance (m)',
            yaxis_title='Speed (km/h)',
            height=175,
            margin=dict(l=30, r=20, t=10, b=30),
            autosize=False
        )

        # TELEMETRY CHART
        telem_fig = make_subplots(rows=4, cols=1, shared_xaxes=True, subplot_titles=('Speed', 'Throttle', 'Brake', 'Gear'), vertical_spacing=0.05)

        for idx, driver in enumerate(selected_drivers[:3]):
            laps = session.laps.pick_driver(driver)
            fastest = laps.pick_fastest()
            if fastest is not None and not fastest.empty:
                telemetry = fastest.get_telemetry()
                driver_info = next((d for d in session_data['drivers'] if d['number'] == driver), None)
                driver_name = driver_info['abbreviation'] if driver_info else str(driver)
                color = driver_colors.get(driver, '#ffffff')

                telem_fig.add_trace(go.Scatter(x=telemetry['Distance'], y=telemetry['Speed'], mode='lines', name=driver_name, line=dict(color=color, width=2)), row=1, col=1)
                telem_fig.add_trace(go.Scatter(x=telemetry['Distance'], y=telemetry['Throttle'], mode='lines', name=driver_name, line=dict(color=color, width=2), showlegend=False), row=2, col=1)
                telem_fig.add_trace(go.Scatter(x=telemetry['Distance'], y=telemetry['Brake'], mode='lines', name=driver_name, line=dict(color=color, width=2), showlegend=False), row=3, col=1)
                telem_fig.add_trace(go.Scatter(x=telemetry['Distance'], y=telemetry['nGear'], mode='lines', name=driver_name, line=dict(color=color, width=2), showlegend=False), row=4, col=1)

        telem_fig.update_layout(
            template='plotly_dark',
            paper_bgcolor=COLORS['card_bg'],
            plot_bgcolor=COLORS['card_bg'],
            font=dict(color=COLORS['text_primary'], size=9),
            height=300,
            margin=dict(l=30, r=20, t=30, b=30),
            autosize=False
        )

        # TRACK MAP
        track_fig = go.Figure()
        for idx, driver in enumerate(selected_drivers[:3]):
            laps = session.laps.pick_driver(driver)
            fastest = laps.pick_fastest()
            if fastest is not None and not fastest.empty:
                telemetry = fastest.get_telemetry()
                driver_info = next((d for d in session_data['drivers'] if d['number'] == driver), None)
                driver_name = driver_info['abbreviation'] if driver_info else str(driver)
                color = driver_colors.get(driver, '#ffffff')

                track_fig.add_trace(go.Scatter(
                    x=telemetry['X'], y=telemetry['Y'],
                    mode='lines', name=driver_name,
                    line=dict(color=color, width=4)
                ))

        track_fig.update_layout(
            template='plotly_dark',
            paper_bgcolor=COLORS['card_bg'],
            plot_bgcolor=COLORS['card_bg'],
            font=dict(color=COLORS['text_primary'], size=9),
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, scaleanchor="x", scaleratio=1),
            height=250,
            margin=dict(l=10, r=10, t=10, b=10),
            autosize=False
        )

        # WEATHER
        weather = session.weather_data
        weather_content = html.P("No weather data", style={'color': COLORS['text_secondary'], 'fontSize': '10px'})
        if not weather.empty:
            weather_content = html.Div([
                html.Div(className='metric-card', style={'marginBottom': '8px', 'background': 'linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%)', 'border': 'none', 'padding': '10px'}, children=[
                    html.Div('AIR TEMP', className='metric-label', style={'color': '#fff', 'fontSize': '9px'}),
                    html.Div(f"{weather['AirTemp'].mean():.1f}°C", className='metric-value', style={'color': '#fff', 'fontSize': '18px'})
                ]),
                html.Div(className='metric-card', style={'marginBottom': '8px', 'background': 'linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%)', 'border': 'none', 'padding': '10px'}, children=[
                    html.Div('TRACK TEMP', className='metric-label', style={'color': '#fff', 'fontSize': '9px'}),
                    html.Div(f"{weather['TrackTemp'].mean():.1f}°C", className='metric-value', style={'color': '#fff', 'fontSize': '18px'})
                ]),
                html.Div(className='metric-card', style={'background': 'linear-gradient(135deg, #667EEA 0%, #764BA2 100%)', 'border': 'none', 'padding': '10px'}, children=[
                    html.Div('HUMIDITY', className='metric-label', style={'color': '#fff', 'fontSize': '9px'}),
                    html.Div(f"{weather['Humidity'].mean():.1f}%", className='metric-value', style={'color': '#fff', 'fontSize': '18px'})
                ])
            ])

        # FASTEST LAPS TABLE
        fastest_laps_table = []
        for driver in selected_drivers[:5]:
            laps = session.laps.pick_driver(driver)
            laps = laps[laps['LapTime'].notna()]
            if not laps.empty:
                driver_info = next((d for d in session_data['drivers'] if d['number'] == driver), None)
                driver_name = driver_info['abbreviation'] if driver_info else str(driver)
                fastest = laps['LapTime'].min()
                fastest_lap_num = laps[laps['LapTime'] == fastest]['LapNumber'].iloc[0]
                color = driver_colors.get(driver, '#ffffff')

                # Check if this is the overall fastest
                is_fastest_overall = (fastest == overall_fastest)

                # Format time as MM:SS.mmm
                total_seconds = fastest.total_seconds()
                minutes = int(total_seconds // 60)
                seconds = total_seconds % 60
                time_str = f"{minutes}:{seconds:06.3f}"

                fastest_laps_table.append(
                    html.Tr(style={'borderBottom': '1px solid #333'}, children=[
                        html.Td(driver_name, style={'padding': '6px 8px', 'color': color, 'fontSize': '11px', 'fontWeight': '600'}),
                        html.Td(f"Lap {fastest_lap_num}", style={'padding': '6px 8px', 'color': COLORS['text_secondary'], 'fontSize': '10px'}),
                        html.Td(
                            time_str,
                            style={
                                'padding': '6px 8px',
                                'fontSize': '11px',
                                'fontWeight': '700',
                                'color': '#9b59b6' if is_fastest_overall else '#ffffff'
                            }
                        ),
                    ])
                )

        # ALL LAPS TABLE - Comprehensive lap-by-lap comparison
        all_laps_data = {}
        max_laps = 0

        for driver in selected_drivers[:5]:
            laps = session.laps.pick_driver(driver)
            laps = laps[laps['LapTime'].notna()].sort_values('LapNumber')
            if not laps.empty:
                driver_info = next((d for d in session_data['drivers'] if d['number'] == driver), None)
                driver_name = driver_info['abbreviation'] if driver_info else str(driver)
                color = driver_colors.get(driver, '#ffffff')

                lap_dict = {}
                for _, lap in laps.iterrows():
                    lap_num = int(lap['LapNumber'])
                    lap_time = lap['LapTime'].total_seconds()
                    lap_dict[lap_num] = lap_time
                    max_laps = max(max_laps, lap_num)

                all_laps_data[driver] = {
                    'name': driver_name,
                    'color': color,
                    'laps': lap_dict
                }

        # Create table rows for all laps
        all_laps_rows = []
        for lap_num in range(1, max_laps + 1):
            # Find fastest time for this lap across all drivers
            lap_times_this_lap = []
            for driver_data in all_laps_data.values():
                if lap_num in driver_data['laps']:
                    lap_times_this_lap.append(driver_data['laps'][lap_num])

            fastest_this_lap = min(lap_times_this_lap) if lap_times_this_lap else None

            row_cells = [html.Td(f"Lap {lap_num}", style={'padding': '4px 6px', 'fontSize': '10px', 'fontWeight': '600', 'color': COLORS['text_secondary'], 'position': 'sticky', 'left': '0', 'background': COLORS['card_bg'], 'borderRight': '1px solid #444'})]

            for driver in selected_drivers[:5]:
                if driver in all_laps_data:
                    driver_data = all_laps_data[driver]
                    if lap_num in driver_data['laps']:
                        lap_time = driver_data['laps'][lap_num]
                        is_fastest = (lap_time == fastest_this_lap)

                        # Format time as MM:SS.mmm
                        minutes = int(lap_time // 60)
                        seconds = lap_time % 60
                        time_str = f"{minutes}:{seconds:06.3f}"

                        # Calculate delta to fastest
                        delta = lap_time - fastest_this_lap if fastest_this_lap else 0
                        delta_str = f"+{delta:.3f}" if delta > 0 else f"{delta:.3f}" if delta < 0 else ""

                        row_cells.append(
                            html.Td(
                                html.Div([
                                    html.Div(time_str, style={'fontSize': '10px', 'fontWeight': '700' if is_fastest else '400'}),
                                    html.Div(delta_str, style={'fontSize': '8px', 'color': COLORS['text_secondary']}) if delta_str else None
                                ]),
                                style={
                                    'padding': '4px 6px',
                                    'textAlign': 'center',
                                    'backgroundColor': '#9b59b622' if is_fastest else 'transparent',
                                    'color': '#9b59b6' if is_fastest else COLORS['text_primary'],
                                    'borderLeft': f'2px solid {driver_data["color"]}' if is_fastest else 'none'
                                }
                            )
                        )
                    else:
                        row_cells.append(html.Td('-', style={'padding': '4px 6px', 'textAlign': 'center', 'fontSize': '10px', 'color': COLORS['text_secondary']}))

            all_laps_rows.append(html.Tr(style={'borderBottom': '1px solid #2a2a2a'}, children=row_cells))

        return html.Div([
            # Charts grid
            html.Div(style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(300px, 1fr))', 'gap': '10px', 'marginTop': '10px'}, children=[
                html.Div(className='card', children=[
                    html.H3('⏱️ Lap Times', style={'color': COLORS['text_primary'], 'marginBottom': '8px', 'fontSize': '11px'}),
                    dcc.Graph(figure=lap_fig, config={'displayModeBar': False}, style={'height': '175px'})
                ]),
                html.Div(className='card', children=[
                    html.H3('🚀 Speed Comparison', style={'color': COLORS['text_primary'], 'marginBottom': '8px', 'fontSize': '11px'}),
                    dcc.Graph(figure=speed_fig, config={'displayModeBar': False}, style={'height': '175px'})
                ]),
            ]),

            # Fastest Laps Table
            html.Div(className='card', style={'marginTop': '10px'}, children=[
                html.H3('⚡ Fastest Laps', style={'color': COLORS['text_primary'], 'marginBottom': '8px', 'fontSize': '11px'}),
                html.Table(style={'width': '100%', 'borderCollapse': 'collapse'}, children=[
                    html.Thead(children=[
                        html.Tr(style={'borderBottom': '2px solid #444'}, children=[
                            html.Th('Driver', style={'padding': '6px 8px', 'textAlign': 'left', 'color': COLORS['text_secondary'], 'fontSize': '9px', 'fontWeight': '600', 'textTransform': 'uppercase'}),
                            html.Th('Lap', style={'padding': '6px 8px', 'textAlign': 'left', 'color': COLORS['text_secondary'], 'fontSize': '9px', 'fontWeight': '600', 'textTransform': 'uppercase'}),
                            html.Th('Time', style={'padding': '6px 8px', 'textAlign': 'left', 'color': COLORS['text_secondary'], 'fontSize': '9px', 'fontWeight': '600', 'textTransform': 'uppercase'}),
                        ])
                    ]),
                    html.Tbody(children=fastest_laps_table)
                ])
            ]),

            # All Laps Comparison Table
            html.Div(className='card', style={'marginTop': '10px', 'overflowX': 'auto'}, children=[
                html.H3('📋 All Laps Comparison', style={'color': COLORS['text_primary'], 'marginBottom': '8px', 'fontSize': '11px'}),
                html.P('Purple highlight = fastest lap for that lap number. Delta shows difference to fastest.', style={'fontSize': '9px', 'color': COLORS['text_secondary'], 'marginBottom': '8px'}),
                html.Table(style={'width': '100%', 'borderCollapse': 'collapse', 'fontSize': '10px'}, children=[
                    html.Thead(children=[
                        html.Tr(style={'borderBottom': '2px solid #444', 'position': 'sticky', 'top': '0', 'background': COLORS['card_bg'], 'zIndex': '10'}, children=[
                            html.Th('Lap', style={'padding': '6px 8px', 'textAlign': 'left', 'color': COLORS['text_secondary'], 'fontSize': '9px', 'fontWeight': '600', 'textTransform': 'uppercase', 'position': 'sticky', 'left': '0', 'background': COLORS['card_bg'], 'borderRight': '1px solid #444'}),
                        ] + [
                            html.Th(
                                all_laps_data[driver]['name'],
                                style={
                                    'padding': '6px 8px',
                                    'textAlign': 'center',
                                    'color': all_laps_data[driver]['color'],
                                    'fontSize': '9px',
                                    'fontWeight': '700',
                                    'textTransform': 'uppercase'
                                }
                            ) for driver in selected_drivers[:5] if driver in all_laps_data
                        ])
                    ]),
                    html.Tbody(children=all_laps_rows)
                ])
            ]),

            # Full width telemetry
            html.Div(className='card', style={'marginTop': '10px'}, children=[
                html.H3('📡 Detailed Telemetry', style={'color': COLORS['text_primary'], 'marginBottom': '8px', 'fontSize': '11px'}),
                dcc.Graph(figure=telem_fig, config={'displayModeBar': False}, style={'height': '300px'})
            ]),

            # Track map and weather
            html.Div(style={'display': 'grid', 'gridTemplateColumns': '2fr 1fr', 'gap': '10px', 'marginTop': '10px'}, children=[
                html.Div(className='card', children=[
                    html.H3('🗺️ Track Map', style={'color': COLORS['text_primary'], 'marginBottom': '8px', 'fontSize': '11px'}),
                    dcc.Graph(figure=track_fig, config={'displayModeBar': False}, style={'height': '250px'})
                ]),
                html.Div(className='card', children=[
                    html.H3('🌤️ Weather', style={'color': COLORS['text_primary'], 'marginBottom': '8px', 'fontSize': '11px'}),
                    weather_content
                ]),
            ])
        ])

    except Exception as e:
        return html.Div(className='card', style={'borderLeft': '2px solid #FF4444'}, children=[
            html.H3('❌ Error', style={'color': '#FF4444', 'fontSize': '12px'}),
            html.P(str(e), style={'color': COLORS['text_secondary'], 'fontSize': '10px'})
        ])

# Expose server for deployment
server = app.server

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🏎️  F1 Telemetry Dashboard Starting...")
    print("="*60)
    print("📊 Open: http://127.0.0.1:8050")
    print("="*60 + "\n")
    app.run(debug=True, port=8050)
