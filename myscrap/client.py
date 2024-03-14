
from myscrap.extractor import Extractor, HttpSessionClient
from myscrap.load import Loader


class Client:
    def __init__(self):
        pass

    @staticmethod
    def run(url):


        
        # singleton = HttpSessionClient()
        # new_singleton = HttpSessionClient()
        
        # print(singleton is new_singleton)
        
        # singleton.singl_variable = "Singleton Variable"
        # print(new_singleton.singl_variable)


        # on instancie les objets extracteur et saver qui se chargeront des traitements
        # Extractor renvoi une liste de catégories contenant les livres et leur contenu.
        extracteur = Extractor(url)
        extracteur.initialize()
        # Loader non refactorisé
        # Loader(data)


    def __del__(self):
        pass
#       del Extractor


