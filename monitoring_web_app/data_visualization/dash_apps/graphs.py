import locale
from datetime import date, timedelta
from data_visualization.models import Donnee_capteur, Climat_exterieur, Salle

from django_plotly_dash import DjangoDash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

import os
import time

# permet de visualiser date en francais sur mon ordi.
locale.setlocale(locale.LC_ALL, '')

desktop_path = os.path.join(os.environ["HOMEPATH"], "Desktop")

week = timedelta(7)
today = date.today()
number_of_click = 0

# ----------------------------------------------------------------------
# Styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash(
    'graphs', external_stylesheets=external_stylesheets, id='target_id')

# -----------------------------------------------------------------------
# DATA

# df = pd.DataFrame(list(Donnee_capteur.objects.all().values()))

# df = df[df['donnee_aberrante'] == False]
# df = df.reset_index(drop=True)

# -----------------------------------------------------------------------
# App layout
app.layout = html.Div([
    dcc.Input(id='target_id', type='hidden', value='filler text'),
    html.H2("Choisir un intervale de dates d'analyse :"),
    html.Div([dcc.DatePickerRange(
        id='date-selected',
        start_date=today - week,  # (2019, 1, 20),
        # vérifier si quand plus d'une journée d'acquisition si c'est ok sans le +1 jour pour end_date.
        end_date=today + timedelta(1),    # (2019, 9, 25),
        # max_date_allowed=date.today() + timedelta(1),  # can't read the future.
        min_date_allowed=date(2021, 1, 1),
    )]),

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

              #           dcc.Input(
              #     id="new-seuil-temp", type="number",
              #     debounce=True, placeholder="Seuil température",
              #     style={'display': 'inline-block', 'vertical-align': 'top',
              #            'margin-left': '3vw', 'margin-top': '1.7vw', 'visibility': 'visible'},
              # ),

              #     dcc.Input(
              #     id="new-seuil-hum", type="number",
              #     debounce=True, placeholder="Seuil humidité",
              #     style={'display': 'inline-block', 'vertical-align': 'top',
              #            'margin-left': '3vw', 'margin-top': '1.7vw', 'visibility': 'visible'}
              # ),

              ]),

    html.Br(),
    html.Br(),

    html.Div([dcc.Graph(id='temp-graph', style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '0.1vw', 'margin-top': '1vw'}),
              dcc.Graph(id='hum-graph', style={'display': 'inline-block',
                                               'vertical-align': 'top', 'margin-left': '0.1vw', 'margin-top': '1vw'}),
              dcc.Graph(id='pres-graph', style={'display': 'inline-block',
                                                'vertical-align': 'top', 'margin-left': '0.1vw', 'margin-top': '1vw'}),
              html.Br(),
              html.Br(),
              html.Div([html.Div(id='output-daily-readings'), html.Div(id='output-daily-errors')], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '10vw', 'margin-top': '4vw'})]),

    html.Button('Extraire données au format CSV',
                id='save-as-csv', n_clicks=0),


])


@ app.callback(
    [  # 1er output important
        Output(component_id='temp-graph', component_property='figure'),
        # 2e output important
        Output(component_id='hum-graph', component_property='figure'),
        Output(component_id='pres-graph', component_property='figure'),
        Output(component_id='output-daily-readings',
               component_property='children'),
        Output(component_id='output-daily-errors',
               component_property='children'),
        # Output(component_id='new-seuil-temp', component_property='style'),
        # Output(component_id='new-seuil-hum', component_property='style')
    ],
    [Input(component_id='target_id', component_property='value'),
     Input(component_id='date-selected', component_property='start_date'),
     Input(component_id='date-selected', component_property='end_date'),
     Input(component_id='pas-temps', component_property='value'),
     Input(component_id='save-as-csv', component_property='n_clicks'),
     # Input(component_id='my-boolean-switch', component_property='on')
     ])
# , switch_state):
def update_graph_date(montage_id, input_start, input_end, time_period, n_clicks):

    if montage_id == "meteo":
        dff = pd.DataFrame(list(Climat_exterieur.objects.all().values()))
        dff = dff.rename(columns={'timestamp': 'timestamp_sys'})
    else:
        df = pd.DataFrame(list(Donnee_capteur.objects.filter(
            montage=(int(montage_id)), donnee_aberrante=False).values()))
        dff = df.copy()
        #dff = dff[dff['montage_id'] == int(montage_id)]

        salle = Salle.objects.filter(
            boitier__montage__donnee_capteur__montage=montage_id).last()

    dff = dff[(dff['timestamp_sys'] >= input_start)
              & (dff['timestamp_sys'] <= input_end)]

# modification du dataset pour le pas de temps sélectionné

    if time_period == 'hour':
        dff = (dff.set_index('timestamp_sys')
               .resample('H').first()
               .reset_index()
               .reindex(columns=dff.columns))

    elif time_period == 'day':
        dff = (dff.set_index('timestamp_sys')
               .resample('D').first()
               .reset_index()
               .reindex(columns=dff.columns))

##########################################################

    fig_temp = px.scatter(dff, x="timestamp_sys",
                          y="temp_c", title='Graphique Température', labels={
                              'timestamp_sys': 'Date d\'acquistion',
                              'temp_c': 'Température (' + u'\u00B0' + 'C)'
                          },
                          color_discrete_sequence=px.colors.qualitative.Vivid,)  # title="")

    # fig_temp.update(layout=dict(title=dict(x=0.5))) # pour centrer le titre.

    fig_hum = px.scatter(dff, x="timestamp_sys",
                         y="hum_rh", title='Graphique Humidité', labels={
                             'timestamp_sys': 'Date d\'acquistion',
                             'hum_rh': 'Humidité relative (%)'
                         }, color_discrete_sequence=["rgb(82,188,163)"])    # Ou par nom de couleur: color_discrete_sequence=["magenta"]

    fig_pres = px.scatter(dff, x="timestamp_sys",
                          y="pres_kpa", title='Graphique Pression', labels={
                              'timestamp_sys': 'Date d\'acquistion',
                              'pres_kpa': 'Pression (kpa)'
                          }, color_discrete_sequence=["rgb(8,10,120)"])

    # Thresholds.
    if montage_id != "meteo":
        fig_temp.add_hline(y=salle.seuil_temp_min_c,
                           line_dash="dot", line_color="blue")
        fig_temp.add_hline(y=salle.seuil_temp_max_c,
                           line_dash="dot", line_color="red")
        fig_hum.add_hline(y=salle.seuil_hum_min_rh,
                          line_dash="dot", line_color="blue")
        fig_hum.add_hline(y=salle.seuil_hum_max_rh,
                          line_dash="dot", line_color="red")
        fig_pres.add_hline(y=salle.seuil_press_min_kpa,
                           line_dash="dot", line_color="blue")
        fig_pres.add_hline(y=salle.seuil_press_max_kpa,
                           line_dash="dot", line_color="red")

    nb_lectures = len(
        dff[(dff['timestamp_sys'] >= today.strftime('%Y-%m-%d'))])
    nb_lectures_abb = len(dff[(dff['timestamp_sys'] >= today.strftime('%Y-%m-%d')) & (
        dff['donnee_aberrante'] == True)])
    str1 = "Nombre de lectures quotidiennes : " + '{}'.format(nb_lectures)
    str2 = "Nombre de lectures aberrantes : " + '{}'.format(nb_lectures_abb)

    # Extraction au format CSV
    global number_of_click
    if n_clicks > number_of_click:
        number_of_click = n_clicks
        if montage_id == 'meteo':
            filename = r'\data_env_can_' + \
                time.strftime("%Y%m%d-%H%M%S") + '.csv'
        else:
            filename = r'\data_salle' + \
                str(salle.nom_salle) + '_' + \
                time.strftime("%Y%m%d-%H%M%S") + '.csv'

        dff.to_csv(desktop_path + filename, index=False)

    # ------------------------ toggle of the threshold inputs

    # if switch_state:
    #     return container, fig_temp, fig_hum, {'display': 'inline-block', 'vertical-align': 'top',
    #                                           'margin-left': '3vw', 'margin-top': '1.7vw', 'visibility': 'visible'}, {'display': 'inline-block', 'vertical-align': 'top',
    #                                                                                                                   'margin-left': '3vw', 'margin-top': '1.7vw', 'visibility': 'visible'}
    # else:
    #     return container, fig_temp, fig_hum, {'display': 'inline-block', 'vertical-align': 'top',
    #                                           'margin-left': '3vw', 'margin-top': '1.7vw', 'visibility': 'hidden'}, {'display': 'inline-block', 'vertical-align': 'top',
    #                                                                                                                  'margin-left': '3vw', 'margin-top': '1.7vw', 'visibility': 'hidden'}

    return fig_temp, fig_hum, fig_pres, str1, str2


"""
TODO:
1-Ajouter radio items pour sélectionner le pas de temps (ici par défaut =15min mais normalement sera notre période éch aka 5 minutes).
2-voir .state pour bouton, et 2 callbacks un à la suite de l'autre... et pause dans CB...
3-Ajouter un boolean toggle pour activer l'ajout de seuil, ensuite il y aurait input box pour mettre la température voulue...??
4-Bouton avec state... pour download to csv... Voir comment récupérer le df courant... return du premier callback??
"""
