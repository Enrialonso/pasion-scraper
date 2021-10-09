import re

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Advertisements


def clean_text(text: str):
    to_clean = ["\n", "\t"]
    for c in to_clean:
        text = text.replace(c, "")
    return text.strip()


def create_sql_session():
    engine = create_engine("sqlite:///db/db.sqlite")
    session = sessionmaker()
    session.configure(bind=engine)
    return session()


def get_advertisements_info(advertisements):
    list_advertisements = []
    for anuncio in advertisements:
        try:
            body = anuncio.query_selector("//*[@class='x7']")
            titulo = clean_text(body.query_selector("a").inner_text())
        except Exception:
            body = anuncio.query_selector("//*[@class='x9']")
            titulo = clean_text(body.query_selector("a").inner_text())
        texto = clean_text(anuncio.query_selector("//*[@class='tx']").inner_text())
        id = clean_text(anuncio.query_selector("//*[@class='x5']").inner_text())
        # print(id, titulo, texto)
        list_advertisements.append({"id": id, "title": titulo, "text": texto})
    return list_advertisements


def get_data_ad_load_on_table(page, session, category, city, scraping_date):
    anuncios = page.query_selector_all("//*[@class='x1']")
    anuncios_data = get_advertisements_info(anuncios)
    for item in anuncios_data:
        ad = Advertisements(
            category=category,
            city=city,
            id_ad=item["id"],
            title=item["title"],
            text=item["text"],
            scraping_date=scraping_date,
        )
        session.add(ad)
        session.commit()


def get_and_save_ad_id(page, session, category, city, scraping_date):
    anuncios = page.query_selector_all("//*[@class='x1']")
    list_anuncios_id = [clean_text(anuncio.query_selector("//*[@class='x5']").inner_text()) for anuncio in anuncios]

    session.bulk_save_objects(
        [Advertisements(category=category, city=city, id_ad=id, scraping_date=scraping_date) for id in list_anuncios_id]
    )
    session.commit()


def extract_phones(html):
    phone_list = set()
    charts_to_decode = re.findall("eval\(unescape\(\"document.write\('(.+?)'\)\"\)\)</script>", html)
    for chart in charts_to_decode:
        phone_html = re.sub(r"%u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})", lambda text: chr(int(text.group(1), 16)), chart)
        phone = re.findall('tef.gif">(.+?)</div>', phone_html)
        if phone:
            phone_list.add(phone[0])

    return list(phone_list) if phone_list else None
