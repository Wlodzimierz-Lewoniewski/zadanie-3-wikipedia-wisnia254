import requests
from bs4 import BeautifulSoup

def szukaj():
    nazwa_kategorii = input()
    url = "https://pl.wikipedia.org/wiki/Kategoria:" + nazwa_kategorii.replace(' ', '_')
    odpowiedz = requests.get(url)

    if odpowiedz.status_code == 200:
        soup = BeautifulSoup(odpowiedz.text, "html.parser")
        strony = soup.find("div", id="mw-pages")

        if strony:
            artykuly = [
                {"url": link["href"], "nazwa": link["title"]}
                for link in strony.find_all("a") if "title" in link.attrs
            ]

            for idx in range(2):
                if idx < len(artykuly):
                    artykul = artykuly[idx]
                    pelny_url = "https://pl.wikipedia.org" + artykul["url"]
                    odpowiedz_artykul = requests.get(pelny_url)
                    soup_artykul = BeautifulSoup(odpowiedz_artykul.text, "html.parser")

                    tresc = soup_artykul.find('div', {'id': 'mw-content-text'})
                    tytuly = []
                    if tresc:
                        tagi_odnośników = tresc.select('a:not(.extiw)')
                        tytuly = [link.get('title') for link in tagi_odnośników if link.get('title') and link.get_text(strip=True)]
                        tytuly = list(dict.fromkeys(tytuly))[:5]

                    div_tresci = soup_artykul.find("div", {"class": "mw-content-ltr mw-parser-output"})
                    adresy_obrazow = []
                    if div_tresci:
                        tagi_obrazow = div_tresci.find_all("img", src=True)
                        adresy_obrazow = [img["src"] for img in tagi_obrazow[:3]]

                    odwolania_div = soup_artykul.find("ol", {"class": "references"})
                    adresy_odwolania = []
                    if odwolania_div:
                        linki_referencyjne = odwolania_div.find_all('a', class_='external text')
                        adresy_odwolania.extend([link.get('href') for link in linki_referencyjne if link.get('href')])

                    przypisy_div = soup_artykul.find_all("li", {"id": lambda x: x and x.startswith("cite")})
                    for przypis in przypisy_div:
                        link = przypis.find('a', class_='external text')
                        if link and link.get('href'):
                            adresy_odwolania.append(link.get('href'))

                    adresy_odwolania = list(dict.fromkeys(adresy_odwolania))[:3]
                    adresy_odwolania = [url.replace("&", "&amp;") for url in adresy_odwolania]

                    div_kategorie = soup_artykul.find("div", {"id": "mw-normal-catlinks"})
                    nazwy_kategorii = []
                    if div_kategorie:
                        linki_kategorii = div_kategorie.find_all("a")
                        nazwy_kategorii = [kat.get_text() for kat in linki_kategorii[1:4]]

                    wynik_tytuly = " | ".join(tytuly) if tytuly else ""
                    wynik_obrazy = " | ".join(adresy_obrazow) if adresy_obrazow else ""
                    wynik_odwolania = " | ".join(adresy_odwolania) if adresy_odwolania else ""
                    wynik_kategorie = " | ".join(nazwy_kategorii) if nazwy_kategorii else ""

                    print(wynik_tytuly)
                    print(wynik_obrazy)
                    print(wynik_odwolania)
                    print(wynik_kategorie)
        else:
            print("Nie znaleziono stron w tej kategorii.")
    else:
        print(f"Kod statusu: {odpowiedz.status_code}")

if __name__ == "__main__":
    szukaj()
