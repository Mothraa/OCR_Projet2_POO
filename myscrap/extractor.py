import requests
from bs4 import BeautifulSoup

from myscrap.transform import Transform
from myscrap.book import Book, BookManagement
from myscrap.category import Category


class HttpSessionClient(requests.Session):

    def __init__(self):
        super().__init__()

    # définition en tant que singleton
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(HttpSessionClient, cls).__new__(cls)
        return cls.instance

# singleton avec principe de meta-class exemple :
# class Singleton(type):
#     def __init__(cls, name, bases, dict):
#         super(Singleton, cls).__init__(name, bases, dict)
#         cls.instance = None

#     def __call__(cls,*args,**kw):
#         if cls.instance is None:
#             cls.instance = super(Singleton, cls).__call__(*args, **kw)
#         return cls.instance

# class MyClass(object):
#     __metaclass__ = Singleton

    @staticmethod
    def connect():
        # on ouvre une session http avec l'url principale du site
        return requests.Session()

    @staticmethod
    def disconnect(session):
        session.close()


class Extractor():

    def __init__(self):
        self.session = None
        self.main_url = ""

    def initialize(self, main_url: str):
        self.main_url = main_url
        self.get_session()
        self.session.connect()

    def get_session(self):
        self.session = HttpSessionClient()

    def run(self):

        extracteur_cat = CategoryExtractor()

        category_url_list = extracteur_cat.extract_urls(self.main_url)
        category_list = extracteur_cat.build_category(category_url_list)
        extracteur_cat.extract_pages(category_list)

        extracteur_livre = BookExtractor()

        book_list = []
        for category in category_list:
            # on récupère l'ensemble des URLs des livres pour chaque catégorie.
            extracteur_livre.extract_urls(category)

            # on instancie et récupère les infos des livres
            for book_url in category.book_url_list:
                parsed_page = extracteur_livre.get_parsed_page(book_url)
                book = extracteur_livre.build_book(parsed_page)
                extracteur_livre.extract_book_info(book)
                category.book_list.append(book)  # utile a garder ? a voir quand reprise Loader()
                book_list.append(book)  # utile a garder ? a voir quand reprise Loader()

        return book_list

    def get_parsed_page(self, url: str) -> BeautifulSoup:
        """Récupération des données de la page a partir d'une URL, parsée avec BeautifulSoup"""
        self.get_session()
        try:
            page_response = self.session.get(url)
            if page_response.status_code == 200:
                page_parsed = BeautifulSoup(page_response.content, 'lxml')
                page_parsed.url = url
        except Exception as err:
            print("Erreur lors de la récupération de la page ", err)
        return page_parsed

    def __del__(self) -> None:
        HttpSessionClient.disconnect(self.session)


class CategoryExtractor(Extractor):

    def __init__(self):
        self.category_url_list = []

    def extract_urls(self, main_url):
        """A partir de l'URL de la page d'accueil, récupère la liste des URLs des catégories"""
        main_page_parsed = self.get_parsed_page(main_url)

        category_url_list = []
        for link in main_page_parsed.find('ul', {'class': 'nav nav-list'}).find_all_next('li'):
            # filtrage complémentaire
            if link.parent.attrs.get('class') is None:
                category_url_list.append(main_page_parsed.url + link.contents[1].attrs['href'])
        return category_url_list

    def build_category(self, category_url_list: list) -> list:
        """Depuis une liste d'URL de catégories, instancie l'ensemble des categories"""
        category_list = []
        for category_url in category_url_list:
            page_parsed_category = self.get_parsed_page(category_url)
            category_list.append(Category(category_url, page_parsed_category))
        return category_list

    def extract_pages(self, category_list):
        for category in category_list:
            # on parse l'ensemble des pages des categories
            self.__get_all_pages_parsed(category)

    def __get_all_pages_parsed(self, category: Category):
        for url in category.all_categories_pages_list:
            category.all_pages_parsed.append(self.get_parsed_page(url))


class BookExtractor(Extractor):

    def extract_urls(self, category: Category):
        """Depuis une instance Category, génère la liste des URL des livres."""
        for page in category.all_pages_parsed:
            # recherche des urls vers les livres
            for link in page.find('h3').find_all_next('a'):
                # condition complémentaire pour supprimer les doublons et le dernier lien (bouton next)
                if len(link.attrs) == 2:
                    category.book_url_list.append(link.attrs['href'].replace('../../../', 'http://books.toscrape.com/catalogue/'))

    def build_book(self, page_parsed_book: BeautifulSoup):
        """"Instancie un livre"""
        return Book(page_parsed_book)

    def extract_book_info(self, book: Book):
        """Récupération des attributs des livres"""
        book.title = BookManagement.get_book_title(book.page_parsed)
        book.product_description = BookManagement.book_product_description(book.page_parsed)
        book.category = BookManagement.get_book_category(book.page_parsed)
        book.review_rating = BookManagement.book_review_rating(book.page_parsed)
        book.image_url = BookManagement.book_image_url(book.page_parsed)

        self.product_info_list = [b.get_text() for b in book.page_parsed.find('table', {'class': 'table table-striped'}).findAll('td')]

        book.upc = self.product_info_list[0]
        book.price_including_tax = Transform.price_str_to_float(self.product_info_list[3])
        book.price_excluding_tax = Transform.price_str_to_float(self.product_info_list[2])
        book.number_available = Transform.str_to_int(self.product_info_list[5])
        # récupération des données de la couverture (image)
        book.image_data = BookManagement.get_image(book.image_url)
