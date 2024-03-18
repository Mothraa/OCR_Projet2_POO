from bs4 import BeautifulSoup

from myscrap.transform import Transform
from myscrap import extractor


class Category():
    """représente les categories"""
    def __init__(self, url: str, parsed_category: BeautifulSoup):

        self.main_url = url
        self.main_page_parsed = parsed_category
        self.number_of_pages = self.calculate_category_page_numbers(self.main_page_parsed)
        self.all_categories_pages_list = []
        self.all_categories_pages_list = self.get_category_url_list(url)
        self.book_url_list = []
        self.book_list = []
        self.all_pages_parsed = []

    def calculate_category_page_numbers(self, parsed_category: BeautifulSoup) -> int:
        if not parsed_category.find('ul', {'class': 'pager'}):
            number_of_pages = 1
        else:
            number_temp = parsed_category.find('ul', {'class': 'pager'}).find('li', {'class': 'current'}).contents[0]
            number_of_pages = Transform.str_to_int(number_temp.split()[-1])
        return number_of_pages

    def get_category_url_list(self, url: str) -> list:
        """renvoi une liste de l'ensemble des pages de résultat de la catégorie"""
        if self.number_of_pages == 1:
            # pas de modif, on reprend l'url tel quel
            self.all_categories_pages_list.append(url)
        elif self.number_of_pages > 1:
            i = 1
            while i <= self.number_of_pages:
                # on récupère l'url de chaque page de résultat
                url = url.replace('index.html', 'page-{}.html'.format(i))
                self.all_categories_pages_list.append(url)
                i += 1
        return self.all_categories_pages_list

    # def __repr__(self):
    #     return "{}".format(self.category_name)
