from dataclasses import dataclass
import datetime
from typing import Dict, List
from serde import serde, field, from_tuple
from serde.json import from_json, to_json
from pathlib import Path
from pytz import timezone, utc

year = datetime.datetime.now().year


@serde
@dataclass
class RaceEvent:
    name: str
    time: datetime.datetime


@serde
@dataclass
class GrandPrix:
    name: str
    events: List[RaceEvent]


@serde
@dataclass
class GrandsPrix:
    grand_prix: List[GrandPrix]


def scrape_race_info(file_path: Path = Path(__file__).parent / "test2.json"):
    import requests
    from bs4 import BeautifulSoup
    import json

    URL = "https://f1calendar.com/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    race_tables = soup.select("tbody[id]")
    races: List[GrandPrix] = []
    for race_table in race_tables:
        prix_name = race_table.select_one("td span").text  # type: ignore
        # races[prix_name] = {}
        prix = GrandPrix(prix_name, [])
        race_rows = race_table.find_all("tr")
        for race_row in race_rows:
            race_type = race_row.select_one("td:nth-of-type(2)").text.strip()
            race_date = race_row.select_one("td:nth-of-type(3)").text.strip()

            if race_date == "":
                continue
            day, month = race_date.split(" ")
            race_time = race_row.select_one("td:nth-of-type(4)").text.strip()
            # convert race_time to datetime.time object

            race_time = utc.localize(
                datetime.datetime.strptime(
                    f"{int(day):02} {month} {year} {race_time}", "%d %b %Y %H:%M"
                ),
            ).astimezone(timezone("America/Chicago"))

            # race_time = correct_for_timezone(race_time)
            event = RaceEvent(race_type, race_time)
            # if "Grand Prix Grand Prix" not in race_type:
            prix.events.append(event)
            # races[prix_name][race_type] = {"date": race_date, "time": race_time}
        races.append(prix)
    with open("Daddy-Bot-env/Assets/test.json", "w") as f1Info:
        f1Info.write(to_json(races))


if __name__ == "__main__":
    scrape_race_info()
    # with open("Daddy-Bot-env/Assets/test.json", "r") as f1Info:
    #     tmp = from_json(List[GrandPrix], f1Info.read())
    #     print(tmp)
