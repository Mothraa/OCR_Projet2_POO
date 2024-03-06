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


def book_category(page_parsed):
    """extract the category of a book"""
    try:
        category = (page_parsed.find('ul', {'class': 'breadcrumb'}).contents[5].text).strip()
    except AttributeError:
        category = ""
    return category


def get_image(image_url):
    """extract the cover image data (binaries)"""
    try:
        image_data = requests.get(image_url, stream=True, timeout=None)
    except Exception as e:
        print(e)
        #TODO exception a revoir
    return image_data.content


class Extractor():
    def get_categories(self, category):
        category_url_list = []
        for link in category.page_parsed.find('ul', {'class': 'nav nav-list'}).find_all_next('li'):
            # filtrage complémentaire
            if link.parent.attrs.get('class') is None:
                category_url_list.append(category.url + link.contents[1].attrs['href'])
        return category_url_list

    def get_book_url(self, category):
        book_url_list = []
        # recherche des urls vers les livres
        for link in category.page_parsed.find('h3').find_all_next('a'):
            # condition complémentaire pour supprimer les doublons et le dernier lien (bouton next)
            if len(link.attrs) == 2:
                book_url_list.append(link.attrs['href'].replace('../../../', 'http://books.toscrape.com/catalogue/'))
        return book_url_list

    def fetch_book_infos(self, book):
        book.title = book_title(book.page_parsed)
        book.product_description = book_product_description(book.page_parsed)
        book.category = book_category(book.page_parsed)
        book.review_rating = book_review_rating(book.page_parsed)
        book.image_url = book_image_url(book.page_parsed)

        self.product_info_list = [b.get_text() for b in book.page_parsed.find('table', {'class': 'table table-striped'}).findAll('td')]

        book.upc = self.product_info_list[0]
        book.price_including_tax = transform.price_str_to_float(self.product_info_list[3])
        book.price_excluding_tax = transform.price_str_to_float(self.product_info_list[2])
        book.number_available = transform.str_to_int(self.product_info_list[5])

    def fetch_cover_data(self, book):
        book.image_data = get_image(book.image_url)
