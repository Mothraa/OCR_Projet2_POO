
from myscrap.extractor import Extractor
from myscrap.load import Loader


class Client:
    def __init__(self):
        pass

    @staticmethod
    def run(url):
        # on instancie les objets extracteur et saver qui se chargeront des traitements
        # Extractor renvoi une liste de catégories contenant les livres et leur contenu.
        data = Extractor(url)
        # Loader non refactorisé
        # Loader(data)


    def __del__(self):
        pass
#       del Extractor
