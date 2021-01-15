# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 18:34:55 2021

@author: eleou
"""
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string


class Text:
    '''
        - Text : str
        - textFormate : Version du texte sans la ponctuation
        - wordsList : list
    '''
    def __init__(self, txt):
        self.text = txt
        self.formatText()
        self.initWordsList()
    def formatText(self):
        #Fonction qui met en forme le texte pour eviter les problèmes lors de l'analyse
        #Listes des caractères à bannir
        punctuations=['(', ')', '?', ':', ';', ',', '.', '!', '/', '"', "'", "|", '*']
        self.textFormate = self.text
        #Formatage, on enleve les symboles de ponctuation en les remplaçants par des espaces 
        punct = string.punctuation
        for c in punct:
            self.textFormate = self.textFormate.replace(c, "")
    

    
    def initWordsList(self):
        #Fonction qui créer la liste des mots dont il faut calculer le nombre d'occurences
        # On initilialise une liste des mots à ne pas prendre en compte, ici dans la langue anglaise
        useless = stopwords.words('english')
        words = word_tokenize(self.textFormate)
        wordsFiltered = []
        for w in words:
            if (w not in useless) and (w.lower() not in useless):
                wordsFiltered.append(w)      
        #Suppression des doublons dans la listes pour eviter les colonnes/lignes du même nom
        self.wordsList = list(set(wordsFiltered))
        nbWords = len(self.wordsList)
    
    
    