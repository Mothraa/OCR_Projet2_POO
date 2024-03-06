from pathlib import Path

import requests
from bs4 import BeautifulSoup

from myscrap.extract import Extractor
from myscrap import load
from myscrap import transform


class HttpSession:
    """ouverture d'une session de connexion pour récupérer le contenu des pages (voir documentation de requests.Session)"""
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()
        try:
            page_response = self.session.get(url)
#s.get('https://httpbin.org / cookies / set / sessioncookie / 123456789')
            if page_response.status_code == 200:
                self.page_parsed = BeautifulSoup(page_response.content, 'lxml')

        except TimeoutError as err:
            print("timeout lors de la récupération des pages de catégorie", err)
        except Exception as err:
            print("Erreur lors de la récupération des pages de catégorie", err)

    def disconnect(self):
        self.close()


class Category(HttpSession):
    """représente les categories"""
    def __init__(self, url):
        super().__init__(url)
        self.number_of_pages = self.calculate_category_page_numbers()
        self.all_pages_list = []
        self.all_pages_list = self.category_url_list(url)

    def calculate_category_page_numbers(self):
        if not self.page_parsed.find('ul', {'class': 'pager'}):
            number_of_pages = 1
        else:
            number_temp = self.page_parsed.find('ul', {'class': 'pager'}).find('li', {'class': 'current'}).contents[0]
            number_of_pages = transform.str_to_int(number_temp.split()[-1])
        return number_of_pages

    def category_url_list(self, url): 
        if self.number_of_pages == 1:
            # pas de modif, on reprend l'url tel quel
            self.all_pages_list.append(url)
        elif self.number_of_pages > 1:
            i = 1
            while i <= self.number_of_pages:
                # on récupère l'url de chaque page de résultat
                self.all_pages_list.append(url.replace('index.html', 'page-{}.html'.format(i)))
                i += 1
        return self.all_pages_list

    # def __repr__(self):
    #     return "{}".format(self.category_name)


class Book(HttpSession):

    def __init__(self, url):
        super().__init__(url)
        product_page_url = url
        upc = ""
        title = ""
        price_including_tax = None
        price_excluding_tax = None
        number_available = None
        product_description = ""
        category = ""
        review_rating = None
        image_url = ""


    def load(self):

        directory_path = Path.cwd() / "output" / self.category / "images"
        load.create_directory(directory_path)
        image_path = directory_path.joinpath(f"{self.product_info.upc}.jpg")

        load.save_file(image_path, self.image_data)
#        p.joinpath("")

    def get_cover_data(self):
        pass

    def save_as_csv(self):
        pass

    def save_image_cover(self):
        pass

    def __repr__(self):
        return "{}".format(self.title)


if __name__ == "__main__":

    main_url = "http://books.toscrape.com/"

    # print(Book.__doc__)
    # print(Book.__repr__)

# on ouvre une session http avec l'url principale du site
    http_session = HttpSession(main_url)

# on instancie un objet extracteur qui se chargera des traitements
    extracteur = Extractor()

# on boucle sur l'ensemble des url des categories pour récupérer l'ensemble des url des livres
    book_url_list = []

    i = 0
    for category in extracteur.get_categories(http_session):
        # boucle while qui limite le traitement pour tests
        while i < 3:
            cat = Category(category)
            book_url_list.extend(extracteur.get_book_url(cat))
            i += 1

# récupération des données pour chaque livre, enregistrement dans une liste de livres
    book_list = list()
    for book_url in book_url_list:
        book = Book(book_url)
        # récupération des données de la page
        extracteur.fetch_book_infos(book)
        # récupération de la couverture
        extracteur.fetch_cover_data(book)
        book_list.append(book)

# on ferme la session http
    http_session.disconnect
