from myscrap.extract import Extractor
from myscrap.load import Saver
from myscrap import elements


if __name__ == "__main__":

    main_url = "http://books.toscrape.com/"

    # print(Book.__doc__)
    # print(Book.__repr__)

# on ouvre une session http avec l'url principale du site
    http_session = elements.HttpSession(main_url)

# on instancie les objets extracteur et saver qui se chargeront des traitements
    extracteur = Extractor()
    saver = Saver()

# on boucle sur l'ensemble des url des categories pour récupérer l'ensemble des url des livres
    book_url_list = []

    for category in extracteur.get_categories(http_session):
            cat = elements.Category(category)
            book_url_list.extend(extracteur.get_book_url(cat))

# récupération des données pour chaque livre, enregistrement dans une liste de livres
    book_list = list()
    for book_url in book_url_list:
        book = elements.Book(book_url)
        # récupération des données de la page
        extracteur.fetch_book_infos(book)
        # récupération de la couverture
        extracteur.fetch_cover_data(book)

        # enregitrement des données du livre dans le csv
        saver.save_as_csv(book)
        # enregistrement de la couverture
        saver.save_image_cover(book)
        # enregistrement du livre dans une liste
        book_list.append(book)

# on ferme la session http
    http_session.disconnect
