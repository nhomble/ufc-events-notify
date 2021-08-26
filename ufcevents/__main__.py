import base64

from ufcevents import parser
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from groupy.client import Client
import os
import hashlib
import base64

_collection = "card_events"


def make_doc_id(card):
    link = card["link"].encode("utf-8")
    sha1 = hashlib.sha1(link)
    d = sha1.digest()
    b64 = base64.urlsafe_b64encode(d).decode()
    return b64


if __name__ == '__main__':

    bot_id = os.getenv("GROUPME_BOT")
    api_key = os.getenv("GROUPME_KEY")
    cert = os.getenv("GCP_SA")
    with open('sa.json', 'w') as f:
        f.write(cert)
        f.flush()

        real_dates = parser.get_card_events()

        cred = credentials.Certificate("sa.json")
        app = firebase_admin.initialize_app(cred)
        db = firestore.client(app=app)

        new_cards = set()
        for k, data in real_dates.items():
            doc_id = make_doc_id(data)
            ref = db.collection(_collection).document(doc_id)
            if not ref.get().exists:
                db.collection(_collection).document(doc_id).set(data)
                new_cards.add(k)

        if new_cards:
            full = []
            for n in new_cards:
                nice_date = n.strftime("%B %d")
                link = real_dates[n]["link"]
                title = real_dates[n]["title"]
                full.append(f"There is a new UFC event scheduled: {nice_date}: {title}\nMore info here: {link}")

            full = "\n---\n".join(full)

            groupme = Client.from_token(api_key)
            groupme.bots.post(bot_id, full)
