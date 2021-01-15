
class Auteur:
    '''
        Attributs :
        - nom
        - ndocs
        - production : Dictionnaires des ouvrages de l'auteur
    '''

    def __init__(self, name):
        self.nom = name
        self.ndocs = 0
        self.production = {}

    def add(self, texte):
        
        self.production.update({self.ndocs: texte})
        self.ndocs+=1
    def __str__(self):
        print("Présentation du travail de ", self.nom, ":\n")
        for x, y in self.production.items():
            print(y)

