import requests
from . import transform

def book_title(page_parsed):
    """extract the title of a book"""
    try:
        title = page_parsed.find('div', {'class': 'col-sm-6 product_main'}).find('h1').contents[0]
    except AttributeError:
        title = ""
    return title


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


def book_review_rating(page_parsed):
    """extract the review rating of a book"""
    try:
        # récupération du nombre indiqué dans le nom de la classe qui indique le nombre d'étoiles par ex : 'star-rating Two'
        review_rating = page_parsed.find('p', {'class': 'star-rating'}).attrs['class'][1]
    except AttributeError:
        review_rating = ""
    return transform.book_nb_stars_to_decimal(review_rating)


def book_image_url(page_parsed):
    """extract url from the book cover"""
    try:
        image_url = page_parsed.find('div', {'id': 'product_gallery'}).find('img').attrs.get('src').replace(r"../../", "http://books.toscrape.com/")
    except AttributeError:
        image_url = ""
    return image_url



class BookProductInfo:

    def __init__(self, page_parsed):

    #"""extract the product info table of a book"""

        try:
            self.product_info_list = [p.get_text() for p in page_parsed.find('table', {'class': 'table table-striped'}).findAll('td')]

            self.upc = self.product_info_list[0]
            self.price_including_tax = transform.price_str_to_float(self.product_info_list[3])
            self.price_excluding_tax = transform.price_str_to_float(self.product_info_list[2])
            self.number_available = transform.str_to_int(self.product_info_list[5])

            del self.product_info_list

        except AttributeError as e:
            print(e)            
            #TODO exception a revoir



def book_category(page_parsed):
    """extract the category of a book"""
    try:
        category = (page_parsed.find('ul', {'class': 'breadcrumb'}).contents[5].text).strip()#.replace('\n','')
    except AttributeError:
        category = ""
    return category

def get_image(image_url):

    try:
        image_data = requests.get(image_url, stream=True, timeout=None)

    except Exception as e:
        print(e)
        #TODO exception a revoir
    return image_data