import base64

from ufcevents import parser
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from groupy.client import Client
import os

_collection = "card_events"

if __name__ == '__main__':
    
    bot_id = os.getenv("GROUPME_BOT")
    api_key = os.getenv("GROUPME_KEY")
    cert64 = os.getenv("GCP_SA")
    cert = base64.b64decode(cert64).decode('ascii')
    with open('sa.json', 'w') as f:
        f.write(cert)
        f.flush()

        real_dates = parser.get_card_events()

        cred = credentials.Certificate("sa.json")
        app = firebase_admin.initialize_app(cred)
        db = firestore.client(app=app)

        new_cards = set()
        for k, data in real_dates.items():
            s = k.strftime("%m-%d")
            ref = db.collection(_collection).document(s)
            if not ref.get().exists:
                db.collection(_collection).document(s).set(data)
                new_cards.add(k)

        full = []
        for n in new_cards:
            nice_date = n.strftime("%B %d")
            link = real_dates[n]["link"]
            full.append(f"There is a new UFC event scheduled: {nice_date}\nMore info here: {link}")

        full = "\n---".join(full)

        groupme = Client.from_token(api_key)
        groupme.bots.post(bot_id, full)
