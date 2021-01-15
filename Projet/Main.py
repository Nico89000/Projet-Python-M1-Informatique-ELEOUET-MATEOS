# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 11:07:19 2020

@author: Clement Eleouet

"""


from Corpus import *
from Text import *
from Graphe import *
from Appli import *

def addCorpus(subject, ndocs):
    #Même fonction que dans Appli.py mais nous l'avons  gardés ici pour le graphe de démo
    reddit = praw.Reddit(client_id='dENxD867d8c7Dw', client_secret='Fuyt_tgLd-Jm7_PP8FOeBDqEEg4', user_agent='TD1_partie1') 
    corpus = Corpus(subject)
    hot_posts = reddit.subreddit(subject).hot(limit=ndocs)
    for post in hot_posts:
        datet = dt.datetime.fromtimestamp(post.created)
        txt = post.title + ". "+ post.selftext
        txt = txt.replace('\n', ' ')
        txt = txt.replace('\r', ' ')
        doc = Document(datet,
                       post.title,
                       post.author_fullname,
                       txt,
                       post.url)
        corpus.addDoc(doc)
    return corpus
def main():
    #Fonction qui lance l'application et affiche un graphe de démonstration sur le thème du coronavirus
    graph = Graph("Graphe Co-occurence")
    monCorpus = addCorpus("Coronavirus", 3)
    for doc in monCorpus.collection:
        txt = Text(monCorpus.collection[doc].txt)
        graph.calculCoOccurences(txt)
    graph.build()    
    app = Appli(graph.display(), graph)
    app.run()
if __name__ == "__main__":
    main()
