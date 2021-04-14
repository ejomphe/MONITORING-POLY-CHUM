# fichier pour mettre fonctions relatives à l'envoie d'alertes.

'''Let's say you have a file called utils.py that contains some of your python code and you want to import it.

Wherever you want to import then import your python script like

from utils.utils import YourClassOrFunction'''

import smtplib
import ssl

from data_visualization.models import Salle, Montage, Donnee_capteur


def check_for_alert(last_data, salle):

    montage = getattr(last_data, 'montage')
    montage_id = getattr(montage, 'id')
    timestamp = getattr(last_data, 'timestamp_sys')
    temp = getattr(last_data, 'temp_c')
    hum = getattr(last_data, 'hum_rh')
    pres = getattr(last_data, 'pres_kpa')

    # Si 3 paramètres sont en alertes, on envoie juste le email pour la température qui semble être le paramètre le plus important.
    if temp > getattr(salle, 'seuil_temp_max_c'):
        send_email(temp, "temperature", "max", montage_id, timestamp)

    elif temp < getattr(salle, 'seuil_temp_min_c'):
        send_email(temp, "temperature", "min", montage_id, timestamp)

    elif hum > getattr(salle, 'seuil_hum_max_rh'):
        send_email(hum, "humidite", "max", montage_id, timestamp)

    elif hum < getattr(salle, 'seuil_hum_min_rh'):
        send_email(hum, "humidite", "min", montage_id, timestamp)

    elif pres > getattr(salle, 'seuil_press_max_kpa'):
        send_email(pres, "pression", "max", montage_id, timestamp)

    elif pres < getattr(salle, 'seuil_press_min_kpa'):
        send_email(pres, "pression", "min", montage_id, timestamp)


# TODO: éventuellement voir unicode pour géréer accent aigu dans string courriel:
# https://stackoverflow.com/questions/9942594/unicodeencodeerror-ascii-codec-cant-encode-character-u-xa0-in-position-20

def send_email(value, var_env, seuil_min_or_max, montage_id, timestamp):
    port = 465
    smtp_server = "smtp.gmail.com"

    sender_email = "monitoringpolychum2@gmail.com"
    password = "Projet4!"

    salle = Salle.objects.get(
        boitier__montage__pk=montage_id)

    nom_salle = salle.nom_salle

    if seuil_min_or_max == "max":
        seuil = "elevee"
    elif seuil_min_or_max == "min":
        seuil = "faible"

    subject = "Subject: Alerte salle " + '{}'.format(nom_salle) + '\n\n'
    content = "Une " + '{}'.format(var_env) + " de " + '{}'.format(value) + " (trop " + '{}'.format(
        seuil) + ")" + " a ete enregistree dans la salle " + '{}'.format(nom_salle) + " le " + '{}'.format(timestamp)
    message = subject + content

    responsable_list = Montage.objects.get(pk=montage_id).responsable.all()

    for responsable in responsable_list:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, responsable.email, message)


def auto_email_task():

    montages_actif = Montage.objects.filter(actif=True)

    for montage in montages_actif:
        check_for_alert(Donnee_capteur.objects.filter(montage=montage.id, donnee_aberrante=False).last(
        ), Salle.objects.get(boitier__montage__pk=montage.id))
