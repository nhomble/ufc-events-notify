from datetime import datetime

import requests
from bs4 import BeautifulSoup

_url = "https://ufc.com"

def _get_cards(soup):
    divs = soup.find_all("div", class_="c-card-event--result__info")

    def _parse(div):
        ret = {
            "title": div.find("h3").text,
            "date_full": div.find("div")["data-main-card"],
            "date_day": div.find("div")["data-main-card"].split("/")[0].strip(),
            "link": _url + div.find("a")['href'],
            "parsed_date": datetime.now().strftime("%m-%d-%Y")
        }
        print(f"Parsed div={ret}")
        return ret

    return [_parse(div) for div in divs]


def get_card_events():
    r = requests.get(_url + "/events")
    html = r.text
    soup = BeautifulSoup(html, features="html.parser")

    dates = set()
    for card in _get_cards(soup):
        print(f"Converting card={card}")
        dates.add(datetime.strptime(card["date_day"], "%a, %b %d"))
    return dates
