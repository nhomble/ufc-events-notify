from datetime import datetime

import requests
from bs4 import BeautifulSoup

_url = "https://ufc.com"
_div_card_dates = "c-card-event--result__date"


def _get_cards(soup):
    divs = soup.find_all("div", class_="c-card-event--result__date")

    def _parse(div):
        return {
            "title": div["data-card-event-title"],
            "date_full": div["data-main-card"],
            "date_day": div["data-main-card"].split("/")[0].strip(),
            "link": _url + div.find('a')['href']
        }

    return [_parse(div) for div in divs]


def get_card_events():
    r = requests.get(_url + "/events")
    html = r.text
    soup = BeautifulSoup(html, features="html.parser")

    dates = {datetime.strptime(card["date_day"], "%a, %b %d"): card for card in _get_cards(soup)}
    return dates
