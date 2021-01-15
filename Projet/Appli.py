# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 17:23:53 2021

@author: eleou
"""
import re
import pandas as pd
from Document import Document
from Auteur import Auteur
from Corpus import *
from Text import *
from Graphe import *
import plotly.graph_objs as go
import networkx as nx
import dash
import praw
import dash_core_components as dcc
import dash_html_components as html
from colour import Color
import datetime as dt
from textwrap import dedent as d
import json

class Appli:
    '''
        name : nom de l'application (inutile dans cette version de l'application)
        fig : Figure plotly courante à afficher 
        n_clicks : variable de controle de la pression du bouton d'une nouvelle recherche de co occurences
        n_clicksSave : variable de controle de la pression du bouton de lancement d'une sauvegarde du graphe courant
        n_clickImport : variable de controle de la pression du bouton de lancement de l'import d'un graphe depuis la mémoire
    '''
    
    def __init__(self, fig, graph):
        self.name='graphe'
        self.fig= fig
        self.graph = graph
        self.n_clicks = 0
        self.n_clicksSave = 0
        self.n_clicksImport = 0
    def addCorpus(self, subject, ndoc):
        #Fonction qui créer un corpus à partir d'un theme passé en paramètre
        reddit = praw.Reddit(client_id='dENxD867d8c7Dw', client_secret='Fuyt_tgLd-Jm7_PP8FOeBDqEEg4', user_agent='TD1_partie1') 
        corpus = Corpus(subject)
        #Recuperation des textes via reddit
        hot_posts = reddit.subreddit(subject).hot(limit=ndoc)
        for post in hot_posts:
            #On retire les retour de ligne pour eviter la casse
            datet = dt.datetime.fromtimestamp(post.created)
            txt = post.title + ". "+ post.selftext
            txt = txt.replace('\n', ' ')
            txt = txt.replace('\r', ' ')
            #Creation d'un Document contenant le texte et ses informations
            doc = Document(datet,
                           post.title,
                           post.author_fullname,
                           txt,
                           post.url)
            corpus.addDoc(doc)
        return corpus
    
    def run(self):
        #Fonction qui définie l'architecture de l'interface et qui lance l'application
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
        app.title = "Visualisation des co occurences"
        app.layout = html.Div([
        html.Div([html.H1("Projet python de Master 1 de Mateos Nicolas et Eleouet Clement")],
         className="row",
         style={'textAlign': "center"}),
        
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="two columns",
                    children=[
                        dcc.Markdown(d("""
                                **Combien de documents?**
                                """)),
                        html.Div(
                            className="twelve columns",
                            children=[
                                dcc.Input(id="nbDoc", type="text", placeholder="nombre de documents"),
                                html.Br(),
                            ],
                            style={'height': '300px'}
                        ),
                        html.Div(
                            className="twelve columns",
                            children=[
                                dcc.Markdown(d("""
                                **Theme du Corpus**
                                Entrez un theme de textes que vous voulez visualiser
                                """)),
                                dcc.Input(id="themeInput", type="text", placeholder="Theme"),
                                html.Button('Recherche', id='themeSubmit', n_clicks=0),
                                html.Div(id="output")
                            ],
                            style={'height': '300px'}
                        )
                    ]
                ),
                html.Div(
                    className="eight columns",
                    children = [dcc.Graph(id="my-graph", figure = self.fig)]
                ),
                html.Button('Sauvegarder', id='SaveValidation', n_clicks=0),
                html.Button('Importer', id='ImportValidation', n_clicks=0),
                html.Div(
                    className="two columns",
                    children=[
                        html.Div(
                            className='twelve columns',
                            children=[
                                dcc.Markdown(d("""
                                **Hover Data**
                                Mouse over values in the graph.
                                """)),
                                html.Pre(id='hover-data')
                            ],
                            style={'height': '400px'}),
                        ]
                    ),
                html.Div(
                    className="eight columns",
                    style={'height': '0px'},
                    id="garbage")
                ]
            )
        ])
        #Les callbacks sont en attente d'interaction de l'utilisateur et executent des fonctions selon les entrées sur l'interface
        @app.callback(
        dash.dependencies.Output('hover-data', 'children'),
        [dash.dependencies.Input('my-graph', 'hoverData')])
        def display_hover_data(hoverData):
            return json.dumps(hoverData, indent=2)
        #CallBback qui lance une nouvelle recherche dès qu'un nombre de documents et le thème sont renseignés, et que le bouton de validation est pressé   
        @app.callback(
        dash.dependencies.Output('my-graph', 'figure'),
        [dash.dependencies.Input('themeInput', 'value'),
         dash.dependencies.Input('nbDoc', 'value'),
         dash.dependencies.Input('themeSubmit','n_clicks'),
         dash.dependencies.Input('ImportValidation', 'n_clicks')])
        def displayTheme(value, val, n_clicks, n_clicksImport):
            #Fonction qui lance la recherche et affiche le graph
            if(value != None and val != None and self.n_clicks != n_clicks):
                self.n_clicks = n_clicks
                self.graph = Graph("Coro")
                corpus = self.addCorpus(value, int(val))
                for doc in corpus.collection:
                    txt = Text(corpus.collection[doc].txt)
                    self.graph.calculCoOccurences(txt)                                
                self.graph.build()
                fig = self.graph.display()
                self.fig = fig
                return fig
            elif(n_clicksImport != self.n_clicksImport):
                #Callback pour importer un graphe
                self.n_clicksImport = n_clicks
                #Appel à la fonction save de la classe Graph qui importe la figure dans le graphe
                print("Import...")
                self.graph.load("Sauvegarde.grp")
                fig = self.graph.display()
                self.fig = fig
                print("Done!")
                return fig
            else:
                return self.fig
        
        #Callback pour sauvegarder un graphe
        @app.callback(
        dash.dependencies.Output('garbage', 'children'),
        [dash.dependencies.Input('SaveValidation', 'n_clicks')])
        def saveGraphe(n_clicks):
            if(n_clicks == self.n_clicksSave or n_clicks==None):
                return self.fig
            else:
                print(n_clicks)                
            self.n_clicksSave = n_clicks
            #Appel à la fonction save de la classe Graph qui sauvegarde la figure courante
            print("Sauvegarde...")
            self.graph.save("Sauvegarde.grp")
            return self.fig
        
        app.run_server(debug = False)
    