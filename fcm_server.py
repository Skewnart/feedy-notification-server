from datetime import datetime
from datetime import timedelta

import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from firebase_admin import firestore

# Récupération des credentials Firebase
cred = credentials.Certificate("/home/feedy/serviceAccountKey.json")
# Initialisation des services
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialisation des collections users et plantType (+ construction du dictionnaire des types de plantes)
users_ref = db.collection(u'users')
planttype_ref = db.collection(u'plantType')

plant_types_dict = {}
for plant_type in planttype_ref.stream() :
	plant_types_dict[plant_type.id] = plant_type.to_dict()

# Parcours des users pour envoyer une notification à ceux qui en ont besoin
for user in users_ref.stream() :
	user_attrs = user.to_dict()
	ask_notification = user_attrs["ask_notification"] # Envoi des notifications uniquement aux users configurés pour
	if ask_notification :
# Comptage des plantes dans le besoin
		nb_plants_need = 0
# Récupération de la référénce des plantes pour le user
		plants_ref = users_ref.document(user.id).collection(u'plants')

# Parcours des plantes
		for plant in plants_ref.stream() :
			plant_attrs = plant.to_dict()
			current_type = plant_types_dict[plant_attrs["plantType"]]
			
# Test de la validité du dernier arrosage et dernière brumisation
			if (current_type["interval_watering"] > 0 and ((plant_attrs["last_watering"] + timedelta(days=current_type["interval_watering"])).date() < datetime.now().date())) or (current_type["interval_misting"] > 0 and ((plant_attrs["last_misting"] + timedelta(days=current_type["interval_misting"])).date() < datetime.now().date())) :
				nb_plants_need += 1
		
# Si user éligible à l'envoi du message, on construit le titre et le corps et on envoie
		if nb_plants_need > 0 :
			fcm_token = user_attrs["fcm_token"]
			message_title = "Une plante a besoin de toi aujourd'hui" if nb_plants_need == 1 else str(nb_plants_need)+ " plantes ont besoin de toi aujourd'hui"
			message = messaging.Message(
				notification = messaging.Notification(
					title = message_title,
					body = "Viens t'en occuper !" 
				),
				token=fcm_token,
			)

			response = messaging.send(message)
			#print('Envoi notification')

