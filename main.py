import requests
from bs4 import BeautifulSoup

nazwa_kategorii = input("Podaj nazwę kategorii: ")
nazwa_kategorii = nazwa_kategorii.replace(" ", "_")
url = "https://pl.wikipedia.org/wiki/Kategoria:" + nazwa_kategorii
odpowiedz = requests.get(url)

if odpowiedz.status_code == 200:

    zupa = BeautifulSoup(odpowiedz.text, "html.parser")
    div_strony = zupa.find("div", id="mw-pages")

    if div_strony:
        artykuly = []
        linki = div_strony.find_all("a")

        for link in linki:
            if "title" in link.attrs and not link["href"].startswith("/wiki/Kategoria:"):
                url_artykulu = link["href"]
                nazwa_artykulu = link["title"]
                artykuly.append({"url": url_artykulu, "nazwa": nazwa_artykulu})

        for i in range(2):

            if i < len(artykuly):
                artykul = artykuly[i]
                url_artykulu = "https://pl.wikipedia.org" + artykul["url"]
                odpowiedz_artykul = requests.get(url_artykulu)
                zupa_artykul = BeautifulSoup(odpowiedz_artykul.text, "html.parser")
                tytuly = []
                kontener_div = zupa_artykul.find('div', {'id': 'mw-content-text', 'class': 'mw-body-content'})

                if kontener_div:
                    linki = kontener_div.select('a:not(.extiw)')
                    for link in linki:
                        tytul = link.get('title')
                        tekst = link.get_text(strip=True)
                        if tytul and tekst and not tytul.startswith("Kategoria:"):
                            tytuly.append(tytul)
                            if len(tytuly) == 5:
                                break

                div_tresc = zupa_artykul.find("div", {"class": "mw-content-ltr mw-parser-output"})
                if div_tresc:
                    obrazy = div_tresc.find_all("img", src=True)
                    url_obrazow = [img["src"] for img in obrazy[:3]]
                else:
                    url_obrazow = []

                # Zbieranie linków zewnętrznych z całej treści, z wykluczeniem niechcianych domen
                zewnetrzne_linki = zupa_artykul.find_all('a', href=True)
                url_przypisow = []
                for link in zewnetrzne_linki:
                    if (link['href'].startswith('http') and
                        'wikipedia.org' not in link['href'] and
                        'wikidata.org' not in link['href'] and
                        'mediawiki.org' not in link['href'] and
                        'wikibooks.org' not in link['href'] and
                        'commons.wikimedia.org' not in link['href'] and
                        'creativecommons.org' not in link['href'] and
                        'foundation.wikimedia.org' not in link['href']):
                        url_przypisow.append(link['href'])
                    if len(url_przypisow) >= 3:
                        break

                url_przypisow = [url.replace("&", "&amp;") for url in url_przypisow]

                kategorie = zupa_artykul.find("div", {"id": "mw-normal-catlinks"})
                if kategorie:
                    nazwy_kategorii = [kat.get_text() for kat in kategorie.find_all("a")[1:4]]
                else:
                    nazwy_kategorii = []

                # Formatowanie i wyświetlanie wyników
                sformatowany_tytul = " | ".join(tytuly) if tytuly else ""
                sformatowany_url_obrazu = " | ".join(url_obrazow) if url_obrazow else ""
                sformatowany_url_przypisu = " | ".join(url_przypisow) if url_przypisow else ""
                sformatowana_nazwa_kategorii = " | ".join(nazwy_kategorii) if nazwy_kategorii else ""

                print(sformatowany_tytul)
                print(sformatowany_url_obrazu)
                print(sformatowany_url_przypisu)
                print(sformatowana_nazwa_kategorii)

            else:
                print(f"Artykuł {i + 1}: Brak informacji")
    else:
        print("Brak sekcji mw-pages")
else:
    print(f"Kod statusu: {odpowiedz.status_code}")
