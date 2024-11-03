import requests
from bs4 import BeautifulSoup

nazwa_kategorii = input()
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

            if "title" in link.attrs:

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
                        if tytul and tekst:
                            tytuly.append(tytul)
                            if len(tytuly) == 5:
                                break

                div_tresc = zupa_artykul.find("div", {"class": "mw-content-ltr mw-parser-output"})
                obrazy = div_tresc.find_all("img", src=True)
                url_obrazow = [img["src"] for img in obrazy[:3]]
                przypisy_h2 = zupa_artykul.find('span', {"id": "Przypisy"})

                if przypisy_h2:
                    przypisy = przypisy_h2.find_next("ol", {"class": "references"})
                    zewnetrzne_linki = przypisy.find_all('a', {"class": 'external text'})
                    url_przypisow = [link['href'] for link in zewnetrzne_linki[:3]]
                    url_przypisow = [url.replace("&", "&amp;") for url in url_przypisow]

                else:
                    url_przypisow = []

                kategorie = zupa_artykul.find("div", {"id": "mw-normal-catlinks"}).find_all("a")
                nazwy_kategorii = [kat.get_text() for kat in kategorie[1:4]]

                sformatowany_tytul = ""
                sformatowany_url_obrazu = ""
                sformatowany_url_przypisu = ""
                sformatowana_nazwa_kategorii = ""
                for tytul in tytuly:
                    sformatowany_tytul += tytul + " | "
                sformatowany_tytul = sformatowany_tytul[:-3]
                print(sformatowany_tytul)
                for url_obraz in url_obrazow:
                    sformatowany_url_obrazu += url_obraz + " | "
                sformatowany_url_obrazu = sformatowany_url_obrazu[:-3]
                print(sformatowany_url_obrazu)

                for url_przypis in url_przypisow:
                    sformatowany_url_przypisu += url_przypis + " | "
                sformatowany_url_przypisu = sformatowany_url_przypisu[:-3]
                print(sformatowany_url_przypisu)

                for nazwa_kategorii in nazwy_kategorii:
                    sformatowana_nazwa_kategorii += nazwa_kategorii + " | "
                sformatowana_nazwa_kategorii = sformatowana_nazwa_kategorii[:-3]
                print(sformatowana_nazwa_kategorii)

            else:
                print(f"Artykuł {i + 1}: Brak informacji")
    else:
        print("Brak sekcji mw-pages")
else:
    print(f"Kod statusu: {odpowiedz.status_code}")
