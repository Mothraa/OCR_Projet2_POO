
import requests

from bs4 import BeautifulSoup

from myscrap import extract
from myscrap import load

"""Créer export.py, transform.py, load.py"""

class Category:

    def __init__(self):
        category_name = ""
        pass

    def connect(self, url):
        pass

    def __repr__(self):
        return "{}".format(self.category_name)


class Book:
    """parsing a book page from one url and return a dict
    Args:
     book_url_dict:
        {
        'category': category of the book
        'book_url': url of the book
        }
    Returns:
     book_dict: a dict with informations about the book
        {
            'product_page_url': url of the book page
            'upc': upc unique code
            'title': title of the book
            'price_including_tax': price with taxes in pound sterling
            'price_excluding_tax': price without taxes in pound sterling
            'number_available': number of books availables
            'product_description': all informations about the book (summary,...)
            'category': category of book
            'review_rating': number of stars of the review rating
            'image_url': url of the image cover
        }
    """
    # timeout de connexion
    TIMEOUT = None

    def __init__(self):
        product_page_url = ""
        upc = ""
        title = ""
        price_including_tax = None
        price_excluding_tax = None
        number_available = None
        product_description = ""
        category = ""
        review_rating = None
        image_url = ""


    def connect(self, url):
        try:
            page = requests.get(url, self.TIMEOUT)

            if page.status_code == 200:
                self.product_page_url = url
                self.page_parsed = BeautifulSoup(page.content, 'lxml')
                page.close()

        except TimeoutError as err:
            print("timeout lors de la récupération des pages de catégorie", err)
        except Exception as err:
            print("Erreur lors de la récupération des pages de catégorie", err)

    def extract(self):
        """find ?"""

        self.title = extract.book_title(self.page_parsed)
        self.product_description = extract.book_product_description(self.page_parsed)
        self.category = extract.book_category(self.page_parsed)
        self.review_rating = extract.book_review_rating(self.page_parsed)
        self.image_url = extract.book_image_url(self.page_parsed)

        self.product_info = extract.BookProductInfo(self.page_parsed)

        self.image_data = extract.get_image(self.image_url)

    def load(self, path):
        image_path = path + self.product_info.upc + ".jpg"
        load.save_image_file(image_path, self.image_data.raw)


    def __repr__(self):
        return "{}".format(self.title)



if __name__ == "__main__":

    main_url = "http://books.toscrape.com/"
    url = "http://books.toscrape.com/catalogue/the-book-of-basketball-the-nba-according-to-the-sports-guy_232/index.html"
    page1 = Book()

    page1.connect(url)
    page1.extract()

    path = "./"
    page1.load(path)

    print(Book.__doc__)
    print(Book.__repr__)
