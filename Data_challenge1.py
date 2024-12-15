import pandas as pd
from dash import Dash, dash_table, html, dcc
import plotly.express as px
from dash.dependencies import Input, Output

# from data_processing import load_and_process_data

color_map = {
    "France": "#1f77b4",  
    "Italy": "#2ca02c" ,   
    "Germany": "#000000", 
    "Poland": "#d62728" ,
    "Spain": "#e86100"
}


app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

df = pd.read_csv('C:\\Users\\Administrateur PC\\R et Python\\AppDash\\df_eu_day.csv')

app.layout = html.Div([
server = app.server
     html.H1("Analyse Covid-19 dans l'espace schengen de l'Union Européenne", style={'textAlign': 'center'}),
     html.Div([
        dash_table.DataTable(
            id = 'datatable_id',
            data = df.to_dict('records'),
            columns = [
                {"name": i, "id": i, "deletable": False, "selectable" : True if i == "Country_Region" else False} for i in df.columns
            ],
            editable = False,
            filter_action = "native",
            sort_mode = "multi",
            row_selectable = "multi",
            row_deletable = False,
            selected_rows = [],
            page_action = "native",
            page_current = 0,
            page_size = 10,
            style_cell_conditional=[
            {'if': {'column_id': col}, 'textAlign': 'center'} for col in ['Country_Region', 'Confirmed','Deaths',
            'Last_Update', 'Year', 'Incident_Rate', 'Case_Fatality_Ratio']
        ]),
    ], className= 'row'),

     dcc.Dropdown(
        id="slct_year",
        options=[{"label": "Toutes les années", "value": "All"}] +
                [{"label": str(year), "value": year} for year in range(2020, 2024)],
        multi=False,
        value="All",
        style={'width': "50%"}
    ),

    html.Div([
        dcc.Graph(id='Confirmed_Map', style={'width': '48%', 'display': 'inline-block','margin': '0', 'box-sizing': 'border-box'}),
        dcc.Graph(id='Deaths_Map', style={'width': '48%', 'display': 'inline-block','margin': '0', 'box-sizing': 'border-box'})
    ], style={'display': 'flex', 'gap': '10px','width': '100%'}), 

    html.Div([
        html.Div([
            dcc.Dropdown(
                id = 'linedropdown',
                options=[{'label': 'Nombre de Confirmé', 'value': 'Confirmed'},
                         {'label': 'Nombre de Mort', 'value': 'Deaths'},
                         {'label': "Taux d'incidence", 'value': 'Incident_Rate'},
                         {'label': "Taux de letalité", 'value': 'Case_Fatality_Ratio'}],
                value = 'Case_Fatality_Ratio',
                multi = False,
                clearable = False,
                style={'width': "50%"}
            ),
        ], style={'flex': '2'}),

        html.Div([
           dcc.Dropdown(
               id = 'piedropdown',
               options=[{'label': 'Nombre de Confirmé', 'value': 'Confirmed'},
                        {'label': 'Nombre de Mort', 'value': 'Deaths'},
                        {'label': "Taux d'incidence", 'value': 'Incident_Rate'},
                        {'label': "Taux de letalité", 'value': 'Case_Fatality_Ratio'}],                    
              value = 'Case_Fatality_Ratio',
              multi = False,
              clearable = False,
              style={'width': '140px'}
        ),
        ], style={'flex': '2', 'text-align': 'right'}),  

    ],  style={
        'display': 'flex', 
        'justify-content': 'space-between', 
        'align-items': 'center', 
        'margin-bottom': '20px'
    }),  

    html.Div([
        html.Div([
            dcc.Graph(id = 'linechart'),   
        ], className = 'six columns'),

        html.Div([
            dcc.Graph(id = 'piechart'),   
        ], className = 'six columns'),
         
    ], className = 'row'),

    
    html.Div([
        dcc.Graph(id='density_mapbox'),
    ], style={'marginTop': '20px'}),

])

@app.callback(
    [Output('Confirmed_Map', 'figure'),
     Output('Deaths_Map', 'figure'),
     Output('piechart', 'figure'),
     Output('linechart', 'figure'),
     Output('density_mapbox', 'figure')],
    [Input('datatable_id', 'selected_rows'),
     Input('slct_year', 'value'),
     Input('piedropdown', 'value'),
     Input('linedropdown', 'value')]
)
def update_data(chosen_rows, selection_year, piedropval, linedropval):
    if selection_year == "All":
        df_filt = df
    else:
        df_filt = df[df["Year"] == selection_year]

    
    confirmed_fig = px.choropleth(
        df_filt,
        locations='Country_Region',
        locationmode='country names',
        color='Confirmed',
        hover_name='Country_Region',
        animation_frame='Last_Update',
        color_continuous_scale=px.colors.sequential.Inferno,
        labels={'Confirmed': 'Confirmé'})
    
    confirmed_fig.update_layout(
        title=dict(
            text="Nombre de Cas Confirmés",
            font=dict(family="Times New Roman, bold", size=24, color="black"),
            x=0.5),
        coloraxis_showscale=True,
        width=500,
        height=500
    )
    confirmed_fig.update_geos(
        projection_type="mercator",
        showcountries=True,
        countrycolor="Black",
        showcoastlines=True,
        coastlinecolor="Black",
        lataxis_range=[30, 70],
        lonaxis_range=[-20, 55],
    )

    
    Deaths_fig = px.choropleth(
        df_filt,
        locations='Country_Region',
        locationmode='country names',
        color='Deaths',
        hover_name='Country_Region',
        animation_frame='Last_Update',
        color_continuous_scale=px.colors.sequential.Inferno,
        labels={'Deaths': 'Décès'}
    )

    Deaths_fig.update_layout(
        title=dict(
            text="Nombre de Cas Decedes",
            font=dict(family="Times New Roman, bold", size=24, color="black"),
            x=0.5),
        coloraxis_showscale=True,
        width=500,
        height=500
    )
    Deaths_fig.update_geos(
        projection_type="mercator",
        showcountries=True,
        countrycolor="Black",
        showcoastlines=True,
        coastlinecolor="Black",
        lataxis_range=[30, 70],
        lonaxis_range=[-20, 55],
    )
     
    if chosen_rows:
        selected_countries = df.iloc[chosen_rows]['Country_Region'].tolist()
        df_filt = df_filt[df_filt['Country_Region'].isin(selected_countries)]
    else:
        default_countries = ['France', 'Italy', 'Germany', 'Spain', 'Poland']
        df_filt = df_filt[df_filt['Country_Region'].isin(default_countries)]
    
    pie_chart = px.pie(
        data_frame = df_filt,
        names = 'Country_Region',
        values = piedropval,    
        hole=.3,
        color = 'Country_Region',
        color_discrete_map=color_map
    )

    line_chart = px.line(
        data_frame = df_filt,
        x = 'Last_Update',
        y = linedropval,   
        color = 'Country_Region',
        color_discrete_map=color_map,
        labels= {'Country_Region' : 'Country','Last_Update': 'Date' } 
    )

    density_mapbox_fig = px.density_mapbox(df, lat = 'Latitude', lon = 'Longitude', hover_name = 'Country_Region',
                        hover_data = ['Province_State', 'Confirmed', 'Deaths'],
                        animation_frame ='Last_Update', color_continuous_scale = 'Portland',
                        radius = 7, zoom = 3, height = 700)

    density_mapbox_fig.update_layout(mapbox_style = "open-street-map", 
                  mapbox_center={"lat": 50, "lon": 10},
                  title=dict(
                        text="Carte geographique UE Covid-19 ",
                        font=dict(family="Times New Roman, bold", size=24, color="black"),
                        x=0.5), )

    return (confirmed_fig, Deaths_fig, pie_chart, line_chart, density_mapbox_fig)
    
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)







