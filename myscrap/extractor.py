import requests
from bs4 import BeautifulSoup

from myscrap import transform
from myscrap.book import Book, BookManagement
from myscrap.category import Category


class Extractor():

    def __init__(self, main_url: str):
        # on ouvre une session http avec l'url principale du site
        self.session = self.connect()

        # on récupère l'ensemble des url des catégories depuis l'URL d'accueil
        category_url_list = self.get_categories_url(main_url)

        # on instancie les categories a partir des URLs
        category_list = self.generate_categories(category_url_list)

        # on parse l'ensemble des pages des categories
        for category in category_list:
            self.get_all_categories_pages_parsed(category)

        # récupère les livres dans chaque catégorie
        for category in category_list:
            # récupèration de la liste des URL dans chaque catégorie
            self.get_book_url(category)
            # on instancie les livres
            self.generate_book(category)

        return category_list

    def get_parsed_page(self, url: str) -> BeautifulSoup:
        """Récupération des données de la page a partir de l'URL, parsée avec BeautifulSoup"""
        try:
            page_response = self.session.get(url)
            if page_response.status_code == 200:
                page_parsed = BeautifulSoup(page_response.content, 'lxml')
                page_parsed.url = url
        except Exception as err:
            print("Erreur lors de la récupération de la page ", err)
        return page_parsed

    def get_categories_url(self, category_url: str):
        """A partir de l'URL de la page d'accueil, récupère la liste des URLs des catégories"""
        main_page_parsed = self.get_parsed_page(category_url)

        category_url_list = []
        for link in main_page_parsed.find('ul', {'class': 'nav nav-list'}).find_all_next('li'):
            # filtrage complémentaire
            if link.parent.attrs.get('class') is None:
                category_url_list.append(main_page_parsed.url + link.contents[1].attrs['href'])
        return category_url_list


    def get_all_categories_pages_parsed(self, category):
        for url in category.all_categories_pages_list:
            category.all_pages_parsed.append(self.get_parsed_page(url))


    def generate_categories(self, category_url_list: list) -> list:
        """Depuis une liste d'URL de catégories, instancie l'ensemble des categories"""
        category_list = []
        for category_url in category_url_list:
            page_parsed_category = self.get_parsed_page(category_url)
            category_list.append(Category(category_url, page_parsed_category))
        return category_list

    @staticmethod
    def connect():
        return requests.Session()

    @staticmethod
    def disconnect(self):
        self.session.close()

    @staticmethod
    def get_book_url(category: Category):
        """Retourne depuis une instance Category, la liste des URL des livres"""

        for page in category.all_pages_parsed:
            # recherche des urls vers les livres
            for link in page.find('h3').find_all_next('a'):
                # condition complémentaire pour supprimer les doublons et le dernier lien (bouton next)
                if len(link.attrs) == 2:
                    category.book_url_list.append(link.attrs['href'].replace('../../../', 'http://books.toscrape.com/catalogue/'))





    def generate_book(self, category: Category):
        """"Instancie et rempli les attributs des livres"""
        category.book_list = []
        for book_url in category.book_url_list:
            page_parsed_book = self.get_parsed_page(book_url)
            book = Book(book_url, page_parsed_book)
            self.fetch_book_infos(book)
            self.fetch_cover_data(book)
            category.book_list.append(book)

    def fetch_book_infos(self, book: Book):
        """Récupération des attributs des livres"""
        book.title = BookManagement.get_book_title(book.page_parsed)
        book.product_description = BookManagement.book_product_description(book.page_parsed)
        book.category = BookManagement.get_book_category(book.page_parsed)
        book.review_rating = BookManagement.book_review_rating(book.page_parsed)
        book.image_url = BookManagement.book_image_url(book.page_parsed)

        self.product_info_list = [b.get_text() for b in book.page_parsed.find('table', {'class': 'table table-striped'}).findAll('td')]

        book.upc = self.product_info_list[0]
        book.price_including_tax = transform.price_str_to_float(self.product_info_list[3])
        book.price_excluding_tax = transform.price_str_to_float(self.product_info_list[2])
        book.number_available = transform.str_to_int(self.product_info_list[5])

    def fetch_cover_data(self, book: BeautifulSoup):
        """récupération des données de la couverture (image)"""
        book.image_data = BookManagement.get_image(book.image_url)

    def __del__(self, url) -> None:
        self.disconnect(url)
