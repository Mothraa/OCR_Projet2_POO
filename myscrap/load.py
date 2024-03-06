from pathlib import Path

from datetime import datetime
import csv


class Saver:

    # date du jour pour le nommage des csv
    jour = datetime.now().strftime(r'%Y%m%d')

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
    #                writer = csv.DictWriter(f, fieldnames=book_list[0].keys(), delimiter=";")
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
    #                writer = csv.DictWriter(f, fieldnames=book_list[0].keys(), delimiter=";")
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


# def same_category_book_list(list_of_books):
#     """from a list of books, extract books with the same category
#     Args:
#      category_name: category name to filter
#      list_of_books: list of all books
#     Returns:
#      books_list_by_category: a list of books of one category
#     """
#     books_list_by_category = []

#     for book in list_of_books:
#         if book['category'] == category_name:
#             books_list_by_category.append(book)

#     return books_list_by_category
