import requests
from bs4 import BeautifulSoup

def search():
    wiki_name = input()
    url = "https://pl.wikipedia.org/wiki/Kategoria:" + wiki_name.replace(' ', '_')
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        pages = soup.find("div", id="mw-pages")

        if pages:
            articles = [
                {"url": link["href"], "name": link["title"]}
                for link in pages.find_all("a") if "title" in link.attrs
            ]

            for idx in range(2):  # Przechodzenie przez pierwsze dwa artykuły
                if idx < len(articles):
                    article = articles[idx]
                    full_url = "https://pl.wikipedia.org" + article["url"]
                    article_response = requests.get(full_url)
                    article_soup = BeautifulSoup(article_response.text, "html.parser")

                    content = article_soup.find('div', {'id': 'mw-content-text'})
                    titles = []
                    if content:
                        anchor_tags = content.select('a:not(.extiw)')
                        titles = [anchor.get('title') for anchor in anchor_tags if anchor.get('title') and anchor.get_text(strip=True)]
                        titles = list(dict.fromkeys(titles))[:5]  # Usunięcie duplikatów i ograniczenie do 5

                    content_text_div = article_soup.find("div", {"class": "mw-parser-output"})
                    image_urls = []
                    if content_text_div:
                        image_tags = content_text_div.find_all("img", src=True)
                        image_urls = ["//upload.wikimedia.org" + img["src"] for img in image_tags[:3]]

                    # Pobieranie linków z przypisów i bibliografii
                    reference_urls = []
                    references_div = article_soup.find("div", {"class": "mw-references-wrap"})
                    if references_div:
                        links = references_div.find_all('a', class_='external text')
                        for link in links:
                            reference_urls.append(link.get('href'))
                            if len(reference_urls) == 3:
                                break

                    # Pobieranie dodatkowych zewnętrznych linków z sekcji "Bibliografia" lub "Linki zewnętrzne"
                    external_sections = article_soup.find_all('span', {'class': 'mw-headline'})
                    for section in external_sections:
                        if section.text.lower() in ['bibliografia', 'linki zewnętrzne']:
                            parent = section.find_parent('h2').find_next_sibling('ul')
                            if parent:
                                for link in parent.find_all('a', href=True):
                                    href = link['href']
                                    if href.startswith('http') and href not in reference_urls:
                                        reference_urls.append(href)
                                    if len(reference_urls) == 3:
                                        break

                    reference_urls = list(dict.fromkeys(reference_urls))[:3]  # Unikalne i ograniczenie do 3
                    reference_urls = [url.replace("&", "&amp;") for url in reference_urls]

                    categories_div = article_soup.find("div", {"id": "mw-normal-catlinks"})
                    category_names = []
                    if categories_div:
                        category_links = categories_div.find_all("a")
                        category_names = [cat.get_text() for cat in category_links[1:4]]

                    # Formatowanie danych wyjściowych
                    output_titles = " | ".join(titles)
                    output_images = " | ".join(image_urls)
                    output_references = " | ".join(reference_urls)
                    output_categories = " | ".join(category_names)

                    print(output_titles)
                    print(output_images)
                    print(output_references)
                    print(output_categories)
                else:
                    print(f"Artykuł {idx + 1}: Informacje nie znalezione")
        else:
            print("Nie znaleziono stron")
    else:
        print(f"Kod statusu: {response.status_code}")

if __name__ == "__main__":
    search()
