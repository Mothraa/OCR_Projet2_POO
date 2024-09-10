# import pprint

from myscrap.client import Client


if __name__ == "__main__":

    main_url = "http://books.toscrape.com/"

    Client.run(main_url)
    # pprint(category_list, indent=4)

    # print(Book.__doc__)
    # print(Book.__repr__)
