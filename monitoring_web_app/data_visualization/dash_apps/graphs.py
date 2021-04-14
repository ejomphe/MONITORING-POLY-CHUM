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
#locale.setlocale(locale.LC_ALL, '')

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
# App layout
app.layout = html.Div([
    dcc.Input(id='target_id', type='hidden', value='filler text'),
    html.H2("Choisir un intervalle de dates d'analyse :",
            style={'fontSize': 24}),
    html.Div([dcc.DatePickerRange(
        id='date-selected',
        start_date=today - week,
        # vérifier si quand plus d'une journée d'acquisition si c'est ok sans le +1 jour pour end_date.
        end_date=today + timedelta(1),
        max_date_allowed=today + timedelta(2),  # can't read the future.
        min_date_allowed=date(2021, 1, 1),
    )]),

    # Pas de temps
    html.Div([html.H2("Choix du pas de temps :", style={'fontSize': 24}),
              dcc.RadioItems(id='pas-temps',
                             options=[
                                 {'label': '5 min (défault)', 'value': 'def'},
                                 {'label': '1h', 'value': 'hour'},
                                 {'label': '24h', 'value': 'day'}
                             ],
                             value='def',
                             style={'display': 'inline-block', 'vertical-align': 'top',
                                    'margin-left': '0.5vw', 'fontSize': 18}
                             ),
              ]),

    html.Br(),
    html.Br(),

    html.Div([dcc.Graph(id='temp-graph', style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '0.1vw', 'margin-top': '1vw'}),
              dcc.Graph(id='hum-graph', style={'display': 'inline-block',
                                               'vertical-align': 'top', 'margin-left': '0.1vw', 'margin-top': '1vw'}),
              dcc.Graph(id='pres-graph', style={'display': 'inline-block',
                                                'vertical-align': 'top', 'margin-left': '0.1vw', 'margin-top': '1vw'}),
              html.Br(),
              html.Br(), ]),
    html.Div([html.Div(id='output-daily-readings'), html.Div(id='output-daily-errors'), html.Div([html.Button('Extraire données au format CSV',
                                                                                                              id='save-as-csv', n_clicks=0, style={'color': 'white', 'backgroundColor': '#4CAF50', 'border': '2px solid #008000', 'padding': '20px 12px', 'fontSize': 18, 'borderRadius': '8px', 'cursor': 'pointer', 'margin-bottom': '10px'})], style={'margin-top': '1vw'})],
             style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '6vw', 'margin-top': '4vw', 'fontSize': 19}),




])


@ app.callback(
    [Output(component_id='temp-graph', component_property='figure'),
        Output(component_id='hum-graph', component_property='figure'),
        Output(component_id='pres-graph', component_property='figure'),
        Output(component_id='output-daily-readings',
               component_property='children'),
        Output(component_id='output-daily-errors',
               component_property='children'),
     ],
    [Input(component_id='target_id', component_property='value'),
     Input(component_id='date-selected', component_property='start_date'),
     Input(component_id='date-selected', component_property='end_date'),
     Input(component_id='pas-temps', component_property='value'),
     Input(component_id='save-as-csv', component_property='n_clicks'),
     ])
def update_graph_date(montage_id, input_start, input_end, time_period, n_clicks):

    if montage_id == "meteo":  # Ajouter filtre timestamp entre start et end... va permettre de visualiser dans graph les abberrants
        df = pd.DataFrame(list(Climat_exterieur.objects.filter(
            timestamp__gte=input_start, timestamp__lte=input_end).values()))
        df = df.rename(columns={'timestamp': 'real_time_clock'})
        # on fait les graphiques avec dff, mais df est utile pour le nb de données quotidiennes et abb. Note on affiche graphiquement les données abb pour météo.
        dff = df.copy()

    # Donnee moyennée et non aberrante. Car panne peut être non moyenné et non aberrant.
    else:
        df = pd.DataFrame(list(Donnee_capteur.objects.filter(
            montage__pk=(int(montage_id)), real_time_clock__gte=input_start, real_time_clock__lte=input_end).values()))
        dff = df.copy()
        # pour les graphiques on ne veut pas les aberrantes. Or c'est utile de les conserver pour le comptage du nb de données aberrantes.
        # TODO: fix bug for an empty data set (if the montage is not inactive... and there are no available data for a given interval)
        # if not dff.empty:
        dff = dff[dff['donnee_aberrante'] == False]
        salle = Salle.objects.get(
            boitier__montage__pk=montage_id)

# modification du dataset pour le pas de temps sélectionné

# TODO: voir si on peut conserver heure originale dans resample.
    if time_period == 'hour':
        dff = (dff.set_index('real_time_clock')
               .resample('H').first()
               .reset_index()
               .reindex(columns=dff.columns))

    elif time_period == 'day':
        dff = (dff.set_index('real_time_clock')
               .resample('D').first()
               .reset_index()
               .reindex(columns=dff.columns))

##########################################################

    fig_temp = px.scatter(dff, x="real_time_clock",
                          y="temp_c", title='Graphique Température', labels={
                              'real_time_clock': 'Date d\'acquistion',
                              'temp_c': 'Température (' + u'\u00B0' + 'C)'
                          },
                          color_discrete_sequence=px.colors.qualitative.Vivid,)  # title="")

    # fig_temp.update(layout=dict(title=dict(x=0.5))) # pour centrer le titre.

    fig_hum = px.scatter(dff, x="real_time_clock",
                         y="hum_rh", title='Graphique Humidité', labels={
                             'real_time_clock': 'Date d\'acquistion',
                             'hum_rh': 'Humidité relative (%)'
                         }, color_discrete_sequence=["rgb(82,188,163)"])    # Ou par nom de couleur: color_discrete_sequence=["magenta"]

    fig_pres = px.scatter(dff, x="real_time_clock",
                          y="pres_kpa", title='Graphique Pression', labels={
                              'real_time_clock': 'Date d\'acquistion',
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

# TODO: voir si on veut plutôt donner nb lectures totales et abb dans intervalle input_start-input_end ou ajd seulement...
    nb_lectures = len(
        df[(df['real_time_clock'] >= today.strftime('%Y-%m-%d'))])
    nb_lectures_abb = len(df[(df['real_time_clock'] >= today.strftime('%Y-%m-%d')) & (
        df['donnee_aberrante'] == True)])

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

    return fig_temp, fig_hum, fig_pres, str1, str2
