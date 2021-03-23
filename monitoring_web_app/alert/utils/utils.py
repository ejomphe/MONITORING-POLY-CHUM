# fichier pour mettre fonctions relatives à l'envoie d'alertes.

'''Let's say you have a file called utils.py that contains some of your python code and you want to import it.

Wherever you want to import then import your python script like

from utils.utils import YourClassOrFunction'''

import smtplib
import ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
# Créer un compte dédié à l'envoie de email d'alertes
sender_email = "monitoringpolychum2@gmail.com"
password = "Projet4!"
# Faire fonction get email address qui va chercher l'adresse associée au numéro de montage
receiver_email = "monitoringpolychum@gmail.com"
message = """\
Subject: Alerte salle + {variable_nom_salle}

Une {temp/hum/press} trop {élevée/faible} a été enregistrée dans la salle {variable_nom_salle} à {timestamp}."""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
