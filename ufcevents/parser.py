from datetime import datetime

import requests
from bs4 import BeautifulSoup

_url = "https://ufc.com"

def _get_cards(soup):
    divs = soup.find_all("div", class_="c-card-event--result__info")

    def _parse(div):
        return {
            "title": div.find("h3").text,
            "date_full": div.find("div")["data-main-card"],
            "date_day": div.find("div")["data-main-card"].split("/")[0].strip(),
            "link": _url + div.find("a")['href'],
            "parsed_date": datetime.now().strftime("%m-%d-%Y")
        }

    return [_parse(div) for div in divs]


def get_card_events():
    r = requests.get(_url + "/events")
    html = r.text
    soup = BeautifulSoup(html, features="html.parser")

    dates = {datetime.strptime(card["date_day"], "%a, %b %d"): card for card in _get_cards(soup)}
    return dates
