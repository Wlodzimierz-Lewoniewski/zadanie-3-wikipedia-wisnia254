import requests
from bs4 import BeautifulSoup

def szukaj():
    nazwa_kategorii = input()
    url = "https://pl.wikipedia.org/wiki/Kategoria:" + nazwa_kategorii.replace(' ', '_')
    odpowiedz = requests.get(url)

    if odpowiedz.status_code == 200:
        zupa = BeautifulSoup(odpowiedz.text, "html.parser")
        strony_div = zupa.find("div", id="mw-pages")

        if strony_div:
            artykuly = [
                {"url": link["href"], "nazwa": link["title"]}
                for link in strony_div.find_all("a") if "title" in link.attrs
            ]

            for idx in range(2):
                if idx < len(artykuly):
                    artykul = artykuly[idx]
                    pelny_url = "https://pl.wikipedia.org" + artykul["url"]
                    odpowiedz_artykul = requests.get(pelny_url)
                    zupa_artykul = BeautifulSoup(odpowiedz_artykul.text, "html.parser")

                    zawartosc = zupa_artykul.find('div', {'id': 'mw-content-text'})
                    tytuly = []
                    if zawartosc:
                        znaczniki_a = zawartosc.select('a:not(.extiw)')
                        tytuly = [znacznik.get('title') for znacznik in znaczniki_a if znacznik.get('title') and znacznik.get_text(strip=True)]
                        tytuly = list(dict.fromkeys(tytuly))[:5]  # Usunięcie duplikatów i ograniczenie do 5

                    div_tresc = zupa_artykul.find("div", {"class": "mw-parser-output"})
                    url_obrazow = []
                    if div_tresc:
                        znaczniki_obrazow = div_tresc.find_all("img", src=True)
                        url_obrazow = ["//upload.wikimedia.org" + obraz["src"] for obraz in znaczniki_obrazow[:3]]

                    przypisy_div = zupa_artykul.find("div", {"class": "mw-references-wrap"})
                    url_przypisow = []
                    if przypisy_div:
                        linki_przypisow = przypisy_div.find_all('a', class_='external text')
                        for link in linki_przypisow:
                            url_przypisow.append(link.get('href'))
                            if len(url_przypisow) == 3:
                                break

                    url_przypisow = [url.replace("&", "&amp;") for url in url_przypisow]

                    div_kategorie = zupa_artykul.find("div", {"id": "mw-normal-catlinks"})
                    nazwy_kategorii = []
                    if div_kategorie:
                        linki_kategorii = div_kategorie.find_all("a")
                        nazwy_kategorii = [kategoria.get_text() for kategoria in linki_kategorii[1:4]]

                    wynik_tytuly = " | ".join(tytuly)
                    wynik_obrazy = " | ".join(url_obrazow)
                    wynik_przypisy = " | ".join(url_przypisow)
                    wynik_kategorie = " | ".join(nazwy_kategorii)

                    print(wynik_tytuly)
                    print(wynik_obrazy)
                    print(wynik_przypisy)
                    print(wynik_kategorie)
                else:
                    print(f"Artykuł {idx + 1}: Informacje nie znalezione")
        else:
            print("Nie znaleziono stron")
    else:
        print(f"Kod statusu: {odpowiedz.status_code}")

if __name__ == "__main__":
    szukaj()
