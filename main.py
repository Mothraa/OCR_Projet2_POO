from myscrap.extract import Extractor
from myscrap import elements


if __name__ == "__main__":

    main_url = "http://books.toscrape.com/"

    # print(Book.__doc__)
    # print(Book.__repr__)

# on ouvre une session http avec l'url principale du site
    http_session = elements.HttpSession(main_url)

# on instancie un objet extracteur qui se chargera des traitements
    extracteur = Extractor()

# on boucle sur l'ensemble des url des categories pour récupérer l'ensemble des url des livres
    book_url_list = []

    i = 0
    for category in extracteur.get_categories(http_session):
        # boucle while qui limite le traitement pour tests
        while i < 3:
            cat = elements.Category(category)
            book_url_list.extend(extracteur.get_book_url(cat))
            i += 1

# récupération des données pour chaque livre, enregistrement dans une liste de livres
    book_list = list()
    for book_url in book_url_list:
        book = elements.Book(book_url)
        # récupération des données de la page
        extracteur.fetch_book_infos(book)
        # récupération de la couverture
        extracteur.fetch_cover_data(book)
        book_list.append(book)

# on ferme la session http
    http_session.disconnect
