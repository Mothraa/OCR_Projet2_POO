from pathlib import Path

from datetime import datetime
import csv


class Loader:

    # date du jour pour le nommage des csv
    jour = datetime.now().strftime(r'%Y%m%d')

    def persistent(self):
    # récupération des données pour chaque livre, enregistrement dans une liste de livres
        book_list = list()
        for book_url in book_url_list:
            book = elements.Book(book_url)
            # récupération des données de la page
            extracteur.fetch_book_infos(book)
            # récupération de la couverture
            extracteur.fetch_cover_data(book)

            # enregitrement des données du livre dans le csv
            Loader.save_as_csv(book)
            # enregistrement de la couverture
            Loader.save_image_cover(book)
            # enregistrement du livre dans une liste
            book_list.append(book)

    def save_as_csv(self, book):
        directory_path = Path.cwd() / "output" / book.category
        create_directory(directory_path)
        path_file_csv = directory_path.joinpath(self.jour + "-" + book.category + "-list.csv")

        fields = [
            "upc",
            "product_page_url",
            "title",
            "price_including_tax",
            "price_excluding_tax",
            "number_available",
            "product_description",
            "category",
            "review_rating",
            "image_url",
            ]

        datas = [
            book.upc,
            book.url,
            book.title,
            book.price_including_tax,
            book.price_excluding_tax,
            book.number_available,
            book.product_description,
            book.category,
            book.review_rating,
            book.image_url,
            ]
        zipped_dict = dict(zip(fields, datas))

        if not path_file_csv.exists():
            try:
                with open(str(path_file_csv), 'w', encoding='utf-8', newline='') as f:
                    # writer = csv.DictWriter(f, fieldnames=book_list[0].keys(), delimiter=";")
                    writer = csv.DictWriter(f, fieldnames=zipped_dict.keys(), delimiter=";")
                    # on créé les entêtes de colonne
                    writer.writeheader()
                    # puis on écrit la ligne
                    writer.writerow(zipped_dict)
            except Exception as err:
                print("Un problème est survenu lors de l'écriture du csv :", err)
        else:
            try:
                with open(str(path_file_csv), 'a', encoding='utf-8', newline='') as f:
                    # writer = csv.DictWriter(f, fieldnames=book_list[0].keys(), delimiter=";")
                    writer = csv.DictWriter(f, fieldnames=zipped_dict.keys(), delimiter=";")
                    # puis on écrit la ligne
                    writer.writerow(zipped_dict)
            except Exception as err:
                print("Un problème est survenu lors de l'écriture du csv :", err)

#        p.joinpath("")
    def save_image_cover(self, book):
        directory_path = Path.cwd() / "output" / book.category / "images"
        create_directory(directory_path)

        image_path = directory_path.joinpath(f"{book.upc}.jpg")
        save_file(image_path, book.image_data)


def create_directory(directory_path):
    """from a path name, create a directory
    Args:
     directory_path: path name
    Returns:
     None
    """
    directory_path.mkdir(parents=True, exist_ok=True)


def save_file(file_path, data):

    file_path.touch(exist_ok=True)
    file_path.write_bytes(data)
