import locale
from datetime import date, timedelta
from data_visualization.models import Donnee_capteur

from django_plotly_dash import DjangoDash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

# permet de visualiser date en francais sur mon ordi.
locale.setlocale(locale.LC_ALL, '')

week = timedelta(7)

# ----------------------------------------------------------------------
# Styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash(
    'graphs', external_stylesheets=external_stylesheets, id='target_id')

# -----------------------------------------------------------------------
# DATA

df = pd.DataFrame(list(Donnee_capteur.objects.all().values()))

df = df[(df['temp_c'] <= 40) & (df['temp_c'] >= 0)  # TODO: modifier le filtre selon le flag donnee_aberrante
        & (df['hum_rh'] <= 100) & (df['hum_rh'] >= 0)]
df = df.reset_index(drop=True)

# -----------------------------------------------------------------------
# App layout
app.layout = html.Div([
    dcc.Input(id='target_id', type='hidden', value='filler text'),
    html.H2("Choisir un intervale de dates d'analyse :"),
    html.Div([dcc.DatePickerRange(
        id='date-selected',
        start_date=date.today() - week,  # (2019, 1, 20),
        # vérifier si quand plus d'une journée d'acquisition si c'est ok sans le +1 jour pour end_date.
        end_date=date.today() + timedelta(1),    # (2019, 9, 25),
        # max_date_allowed=date.today() + timedelta(1),  # can't read the future.
        min_date_allowed=date(2021, 1, 1),
    )]),

    html.Br(),

    # Pas de temps
    html.Div([html.H2("Choix du pas de temps :"),
              dcc.RadioItems(id='pas-temps',
                             options=[
                                 {'label': '15 min (défault)', 'value': 'def'},
                                 {'label': '1h', 'value': 'hour'},
                                 {'label': '24h', 'value': 'day'}
                             ],
                             value='def',
                             style={'display': 'inline-block', 'vertical-align': 'top',
                                    'margin-left': '0.5vw', }
                             ),


              #           # Ajout de seuils
              #           html.Div([
              #               daq.BooleanSwitch(
              #                   id='my-boolean-switch',
              #                   on=False,
              #                   color="#98FB98",
              #                   label="+ seuils",
              #                   labelPosition="top",
              #               )], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '18vw', }
              # ),

              dcc.Input(
        id="new-seuil-temp", type="number",
        debounce=True, placeholder="Seuil température",
        style={'display': 'inline-block', 'vertical-align': 'top',
               'margin-left': '3vw', 'margin-top': '1.7vw', 'visibility': 'visible'},
    ),

        dcc.Input(
        id="new-seuil-hum", type="number",
        debounce=True, placeholder="Seuil humidité",
        style={'display': 'inline-block', 'vertical-align': 'top',
               'margin-left': '3vw', 'margin-top': '1.7vw', 'visibility': 'visible'}
    ),

    ]),


    html.Div([dcc.Graph(id='temp-graph', style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '0.1vw', 'margin-top': '1vw'}),
              dcc.Graph(id='hum-graph', style={'display': 'inline-block',
                                               'vertical-align': 'top', 'margin-left': '0.1vw', 'margin-top': '1vw'}),
              dcc.Graph(id='pres-graph', style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '0.1vw', 'margin-top': '1vw'})]),


])


@ app.callback(
    [  # Output(component_id='my-output', component_property='children'),
        # 1er output important
        Output(component_id='temp-graph', component_property='figure'),
        # 2e output important
        Output(component_id='hum-graph', component_property='figure'),
        Output(component_id='pres-graph', component_property='figure'),
        # Output(component_id='new-seuil-temp', component_property='style'),
        # Output(component_id='new-seuil-hum', component_property='style')
    ],
    [Input(component_id='target_id', component_property='value'),
     Input(component_id='date-selected', component_property='start_date'),
     Input(component_id='date-selected', component_property='end_date'),
     Input(component_id='pas-temps', component_property='value'),
     # Input(component_id='my-boolean-switch', component_property='on')
     ])
# , switch_state):
def update_graph_date(montage_id, input_start, input_end, time_period):

    dff = df.copy()
    dff = dff[dff['montage_id'] == int(montage_id)]
    dff_temp = dff[(dff['timestamp_sys'] >= input_start)
                   & (dff['timestamp_sys'] <= input_end)]
    dff_hum = dff[(dff['timestamp_sys'] >= input_start)
                  & (dff['timestamp_sys'] <= input_end)]
    dff_pres = dff[(dff['timestamp_sys'] >= input_start)
                   & (dff['timestamp_sys'] <= input_end)]

# modification du dataset pour le pas de temps sélectionné

    if time_period == 'hour':
        dff_temp = (dff_temp.set_index('timestamp_sys')
                    .resample('H').first()
                    .reset_index()
                    .reindex(columns=dff_temp.columns))
        dff_hum = (dff_hum.set_index('timestamp_sys')
                   .resample('H').first()
                   .reset_index()
                   .reindex(columns=dff_hum.columns))
        dff_pres = (dff_hum.set_index('timestamp_sys')
                    .resample('H').first()
                    .reset_index()
                    .reindex(columns=dff_hum.columns))

    elif time_period == 'day':
        dff_temp = (dff_temp.set_index('timestamp_sys')
                    .resample('D').first()
                    .reset_index()
                    .reindex(columns=dff_temp.columns))
        dff_hum = (dff_hum.set_index('timestamp_sys')
                   .resample('D').first()
                   .reset_index()
                   .reindex(columns=dff_hum.columns))
        dff_pres = (dff_hum.set_index('timestamp_sys')
                    .resample('D').first()
                    .reset_index()
                    .reindex(columns=dff_hum.columns))

##########################################################

    fig_temp = px.scatter(dff_temp, x="timestamp_sys",
                          y="temp_c", labels={
                              'timestamp_sys': 'Date d\'acquistion',
                              'temp_c': 'Température (' + u'\u00B0' + 'C)'
                          },
                          color_discrete_sequence=px.colors.qualitative.Vivid,)  # title="")
    fig_temp.add_hline(y=18, line_dash="dot", line_color="blue")
    fig_temp.add_hline(y=26, line_dash="dot", line_color="red")

    fig_hum = px.scatter(dff_hum, x="timestamp_sys",
                         y="hum_rh", labels={
                             'timestamp_sys': 'Date d\'acquistion',
                             'hum_rh': 'Humidité relative (%)'
                         }, color_discrete_sequence=["rgb(82,188,163)"])    # Ou par nom de couleur: color_discrete_sequence=["magenta"]
    fig_hum.add_hline(y=30, line_dash="dot", line_color="blue")
    fig_hum.add_hline(y=60, line_dash="dot", line_color="red")

    fig_pres = px.scatter(dff_pres, x="timestamp_sys",
                          y="pres_kpa", labels={
                              'timestamp_sys': 'Date d\'acquistion',
                              'pres_kpa': 'Pression (kpa)'
                          }, color_discrete_sequence=["rgb(8,10,120)"])

    # TODO add thresholds for pressure

    # ------------------------ toggle of the threshold inputs

    # if switch_state:
    #     return container, fig_temp, fig_hum, {'display': 'inline-block', 'vertical-align': 'top',
    #                                           'margin-left': '3vw', 'margin-top': '1.7vw', 'visibility': 'visible'}, {'display': 'inline-block', 'vertical-align': 'top',
    #                                                                                                                   'margin-left': '3vw', 'margin-top': '1.7vw', 'visibility': 'visible'}
    # else:
    #     return container, fig_temp, fig_hum, {'display': 'inline-block', 'vertical-align': 'top',
    #                                           'margin-left': '3vw', 'margin-top': '1.7vw', 'visibility': 'hidden'}, {'display': 'inline-block', 'vertical-align': 'top',
    #                                                                                                                  'margin-left': '3vw', 'margin-top': '1.7vw', 'visibility': 'hidden'}

    return fig_temp, fig_hum, fig_pres


"""
TODO:
1-Ajouter radio items pour sélectionner le pas de temps (ici par défaut =15min mais normalement sera notre période éch aka 5 minutes).
2-voir .state pour bouton, et 2 callbacks un à la suite de l'autre... et pause dans CB...
3-Ajouter un boolean toggle pour activer l'ajout de seuil, ensuite il y aurait input box pour mettre la température voulue...??
4-Bouton avec state... pour download to csv... Voir comment récupérer le df courant... return du premier callback??
"""
