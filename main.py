
import requests
from bs4 import BeautifulSoup

from myscrap import extract


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
        except TimeoutError as err:
            print("timeout lors de la récupération des pages de catégorie", err)
        except Exception as err:
            print("Erreur lors de la récupération des pages de catégorie", err)

        if page.status_code == 200:
            self.page_parsed = BeautifulSoup(page.content, 'lxml')
            page.close()
            # return self.page_parsed

    def extract(self):
        """find ?"""
        self.page_parsed
        self.title = self.page_parsed.find('div', {'class': 'col-sm-6 product_main'}).find('h1').contents[0]
#        self.title = extract.title(self.page_parsed)

        try:
            # on va chercher l'element (sibling) suivant
            product_description = self.page_parsed.find('div', {'id': 'product_description'}).find_next_sibling().contents[0]
        # exception quand Product Description n'existe pas
        # ex: http://books.toscrape.com/catalogue/alice-in-wonderland-alices-adventures-in-wonderland-1_5/index.html
        except AttributeError:
            product_description = ''


        #self.get_image_url()

    def get_image_url(self):
        return

    def __repr__(self):
        return "{}".format(self.title)






# def parsing_page_book(book_url_dict):



#     if page.status_code == 200:

#         page_parsed = BeautifulSoup(page.content, 'lxml')

#         book_title = page_parsed.find('div', {'class': 'col-sm-6 product_main'}).find('h1').contents[0]

#         try:
#             # on va chercher l'element (sibling) suivant
#             product_description = page_parsed.find('div', {'id': 'product_description'}).find_next_sibling().contents[0]
#         # exception quand Product Description n'existe pas
#         # ex: http://books.toscrape.com/catalogue/alice-in-wonderland-alices-adventures-in-wonderland-1_5/index.html
#         except AttributeError:
#             product_description = ''

#         # récupération du nombre indiqué dans le nom de la classe qui indique le nombre d'étoiles par ex : 'star-rating Two'
#         review_rating = page_parsed.find('p', {'class': 'star-rating'}).attrs['class'][1]

#         # url de l'image de couverture
#         image_url = page_parsed.find('div', {'id': 'product_gallery'}).find('img').attrs.get('src').replace(r"../../", "http://books.toscrape.com/")

#         # récupération des valeurs contenues dans le tableau "Product Information"
#         product_info_list = [p.get_text() for p in page_parsed.find('table', {'class': 'table table-striped'}).findAll('td')]

#         # Enregistrement dans un dictionnaire les éléments de chaque page
#         book_dict = {
#             'product_page_url': book_url_dict.get('book_url'),
#             'upc': product_info_list[0],
#             'title': book_title,
#             'price_including_tax': transform.price_str_to_float(product_info_list[3]),
#             'price_excluding_tax': transform.price_str_to_float(product_info_list[2]),
#             'number_available': transform.str_to_int(product_info_list[5]),
#             'product_description': product_description,
#             'category': book_url_dict.get('category'),
#             'review_rating': transform.book_nb_stars_to_decimal(review_rating),
#             'image_url': image_url,
#         }
#     page.close()

#     return book_dict

if __name__ == "__main__":

    main_url = "http://books.toscrape.com/"
    url = "http://books.toscrape.com/catalogue/the-book-of-basketball-the-nba-according-to-the-sports-guy_232/index.html"
    page1 = Book()

    page1.connect(url)
    page1.extract()
    print(page1.title)

    print(Book.__doc__)
    print(Book.__repr__)
