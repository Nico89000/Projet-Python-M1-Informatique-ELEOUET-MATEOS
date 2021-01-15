# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 10:18:49 2020

@author: eleou
"""
from Auteur import Auteur
from Document import Document
import pickle

class Corpus :
    '''
        nom : nom du corpus
        authors : dictionnaire contenant les auteurs
        id2Aut : dictionnaire contenant les identifiants des auteurs
        collection : dictionnaire des différents documents du corpus
        id2Doc : dictionnaire des identifiants de chaque documents
        nDoc : nombre de documents
        nAut : nombre d'auteurs
    '''
    def __init__(self, name):
        self.nom = name
        self.authors = {}
        self.id2Aut = {}
        self.collection = {}
        self.id2Doc = {}
        self.nDoc = 0
        self.nAut = 0
    
    def addAuthor(self, author):
        #Ajoute un auteur a la liste des auteurs du corpus
        for k,v in self.id2Aut.items():
            if(v == author):
                return False
        self.id2Aut.update({self.nAut : author.nom})
        self.authors.update({self.nAut : author})
        self.nAut+=1
        return True
    
    def addDoc(self, document):
        #Ajoute un Document à la collection du corpus
        self.id2Doc.update({self.nDoc : document.titre})
        self.collection.update({self.nDoc : document})
        self.nDoc+=1
        
    def __str__(self, orderBy=0, nreturn=None):
        #la methode affiche la liste des elements triés par titre ou par date de publication
        #selon la valeur de Order by
        if(orderBy == 0):
           #Trie par titre de doc
           if nreturn is None:
               nreturn = self.nDoc
           return [self.collection[k].txt for k, v in sorted(self.collection.items(), key=lambda item: item[1].titre)][:(nreturn)]
        else:
            if nreturn is None:
                nreturn = self.nDoc
            return [self.collection[k] for k, v in sorted(self.collection.items(), key=lambda item: item[1].date, reverse=True)][:(nreturn)]
               
    def __repr__(self):
        return self.name
    
    def save(self, fileName):
        #Sauvegarde un Corpus dans un fichier
        pickle.dump(self, open(fileName, "wb" ))    
        
    def load(self,fileName):
        #Charge un Corpus depuis un fichier
        file = open(fileName, "rb")
        doc = pickle.load(file)
        file.close()
        return doc
    
    