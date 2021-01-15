class Document:
    '''
        Attributs :
        - titre,
        - auteur,
        - date,
        - url,
        - txt.
    '''
    def __init__(self, title, aut, date, txt, url):
        self.titre = title
        self.auteur = aut
        self.date = date
        self.txt = txt
        self.url = url      
    def __str__(self):
        print("Voici les informations sur ", self.titre, " :\n","- Auteur : ", self.auteur, "\n- date de parution : ", str(self.date))


class RedditDocument(Document):
    '''
        Attribut supplémentaire : 
            nbrComments, qui contient le nombre de commentaire en reaction
            au document présenté
    '''
    def __init__(self, title, aut, date, url, txt,nbrComments):
        super(self, title, aut, date, url, txt)
        self.nbrComments = nbrComments
    
    def __str__(self):
        Document.__str__(self)
        print("Nombre de commentaires : ", self.nbrComments)
        
class ArxivDocument(Document):
    '''
        Attribut supplémentaire : 
            La liste des auteurs ayants travaillés sur le document
    '''
    
    def __init__(self, title, aut, date, url, txt, auteurs=list()):
        super(self, title, aut, date, url, txt)
        self.auteurs = auteurs
    
    def __str__(self):
        Document.__str__(self)
        print("Liste des auteurs : ", self.auteurs)
        
        