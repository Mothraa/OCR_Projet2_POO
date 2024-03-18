import requests
from bs4 import BeautifulSoup

from myscrap.transform import Transform


class Book:

    def __init__(self, page_parsed_book: BeautifulSoup):
        self.page_parsed = page_parsed_book
        self.product_page_url = page_parsed_book.book_url
        self.upc = ""
        self.title = ""
        self.price_including_tax = None
        self.price_excluding_tax = None
        self.number_available = None
        self.product_description = ""
        self.category = ""
        self.review_rating = None
        self.image_url = ""
        self.image_data = None

    def __repr__(self):
        return "{}".format(self.title)


class BookManagement:

    @staticmethod
    def get_book_title(page_parsed):
        """extract the title of a book"""
        try:
            title = page_parsed.find('div', {'class': 'col-sm-6 product_main'}).find('h1').contents[0]
        except AttributeError:
            title = ""
        return title

    @staticmethod
    def book_product_description(page_parsed):
        """extract the product description of a book"""
        try:
            # on va chercher l'element (sibling) suivant
            product_description = page_parsed.find('div', {'id': 'product_description'}).find_next_sibling().contents[0]
        # exception quand Product Description n'existe pas
        # ex: http://books.toscrape.com/catalogue/alice-in-wonderland-alices-adventures-in-wonderland-1_5/index.html
        except AttributeError:
            product_description = ""
        return product_description

    @staticmethod
    def book_review_rating(page_parsed):
        """extract the review rating of a book"""
        try:
            # récupération du nombre indiqué dans le nom de la classe conernant les étoiles par ex : 'star-rating Two'
            review_rating = page_parsed.find('p', {'class': 'star-rating'}).attrs['class'][1]
        except AttributeError:
            review_rating = ""
        return Transform.book_nb_stars_to_decimal(review_rating)

    @staticmethod
    def book_image_url(page_parsed):
        """extract url from the book cover"""
        try:
            image_url = page_parsed.find('div', {'id': 'product_gallery'}).find('img').attrs.get('src')
            image_url = image_url.replace(r"../../", "http://books.toscrape.com/")
        except AttributeError:
            image_url = ""
        return image_url

    @staticmethod
    def get_book_category(page_parsed):
        """extract the category of a book"""
        try:
            category = (page_parsed.find('ul', {'class': 'breadcrumb'}).contents[5].text).strip()
        except AttributeError:
            category = ""
        return category

    @staticmethod
    def get_image(image_url):
        """extract the cover image data (binaries)"""
        try:
            image_data = requests.get(image_url, stream=True, timeout=None)
        except Exception as e:
            print(e)
            # TODO exception a revoir
        return image_data.content
