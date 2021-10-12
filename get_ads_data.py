import os
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
from datetime import datetime as dt

import requests
from bs4 import BeautifulSoup

from models.models import Advertisements
from utils.utils import create_sql_session

scraping_date = dt.now()


def worker(config):
    try:
        response = requests.get(
            f"https://www.pasion.com/stats/stats-ampliadas.php?id={config['id_ad'].replace('r', '')}")
        if response.ok:
            try:
                html = BeautifulSoup(response.text, "html.parser")

                no_ad = html.find('div', {'class': 'titanu'}).getText()

                if "El ID de anuncio es incorrecto, el anuncio no existe o el anuncio ha sido borrado" in no_ad:
                    raise Exception("Anuncio no existe")

                statistics = html.find_all('div', {'class': 'dato'})
                header = html.find('div', {'class': 'header'})
                link = header.find("a")["href"]

                listed = int(float(statistics[0].find("strong").getText()))
                phone_showed = int(float(statistics[1].find("strong").getText()))
                email_sent = int(float(statistics[2].find("strong").getText()))
                shared = int(float(statistics[3].find("strong").getText()))
                add_followers = int(float(statistics[4].find("strong").getText()))
                renew = int(float(statistics[5].find("strong").getText()))

                url = f"https://www.pasion.com{link}"

                res = requests.get(url)
                if res.ok:
                    html = BeautifulSoup(res.text, "html.parser")
                    title = html.find('div', {'class': 'pagAnuTituloBox'}).getText().replace("\n", "").replace("\t", "")
                else:
                    raise Exception("Title no existe")

                print(title, listed, phone_showed, email_sent, shared, add_followers, renew, url)
                session = create_sql_session()
                session.query(Advertisements).filter(Advertisements.id == config["id"]).update({
                    "title": title,
                    "listed": listed,
                    "phone_showed": phone_showed,
                    "email_sent": email_sent,
                    "shared": shared,
                    "add_followers": add_followers,
                    "renew": renew,
                    "text": url
                })
                session.commit()
            except Exception as error:
                print(f"ERROR: {error}")
        else:
            print(f"ERROR: http status code: {response.status_code}")
    except Exception as error:
        print(error)
    return None


def main():
    config_workers, count_workers = [], int(float(os.getenv("COUNT_WORKERS", 2)))
    print(f"COUNT_WORKERS = {count_workers}")
    session = create_sql_session()
    advertisements = session.query(Advertisements).filter(Advertisements.title == None).all()

    for advertisement in advertisements:
        config_workers.append({"id": advertisement.id, "id_ad": advertisement.id_ad})

    with PoolExecutor(max_workers=count_workers) as executor:
        for _ in executor.map(worker, config_workers):
            pass

    print("finish")

if __name__ == "__main__":
    main()
