# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 16:34:11 2021

@author: eleou
"""
import pandas as pd
from Corpus import *
from Text import *
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import networkx as nx
import pickle
class Graph:
    '''
        name : nom du graphe
        df : Dataframe contenant les informations sur les co-occurences entre les mots
        graph : Graphe de co-occurences au format de networkX
        fig : Figure plotly qui sert pour l'affichage du graphe sur dash
    '''

    def __init__(self, name):   
        self.name = name
        self.df = None
        self.graph = nx.Graph()
        self.fig = None
    def calculCoOccurences(self, text):
        #Fonction qui Prend un text formaté en paramètre et qui remplit la matrice de co-occurences          
        if(self.df is None):
            #Si il n'y a pas de matrice existante on la créer à partir du texte courant
            words = text.wordsList
            self.initMatrix(words)
        else:
            #Si une matrice existe deja, il suffit d'ajouter aux lignes/colonnes la listes des nouveaux mots du texte courant
            words = text.wordsList
            #On créer une liste des mots deja existants
            columns = list(self.df.columns)
            for word in words:
                if word not in columns:
                    #Si le mot courant n'a pas encore été répertorié on ajoute une ligne et une colonne
                    self.df.loc[word,:] = int(0)
                    self.df.loc[:,word] = int(0)         
            #Concaténation des deux listes pour effectuer les comparaisons
            words = words + columns
        #Parcours de la listes des mots par deux boucles pour verifier les co occurences des mots dans le texte qui est analysé
        for word1 in words:
            for word2 in words:
                if (word1 in text.textFormate) and (word2 in text.textFormate) and not(word1 == word2):
                    #Si les deux mots sont dans le texte on incrémente la valeur dans la cellule correspondante. 
                    self.df.loc[word1, word2] +=1
                    self.df.loc[word2, word1] +=1
        for word in words:
            self.df.loc[word, word]+=text.textFormate.count(word)
    
    def initMatrix(self,words): 
        #Creation et initialisation a 0 de la matrice de co occurences
        self.df = pd.DataFrame(columns = words, index = words)
        self.df[:] = int(0)
    
    
    def save(self, fileName):
        #Sauvegarde le graphe dans le repertoire courant
        pickle.dump(self.fig, open(fileName, "wb" ))  
        
    def load(self, fileName):
        #Charge un graphe et le stocke dans l'atttribut fig du repertoire courant
        file = open(fileName, "rb")
        self.fig = pickle.load(file)
        file.close()
        
    def build(self):
        #Construit le graphe à partir du dataframe des co occurences de l'objet graphe courant
        self.graph= nx.Graph()
        self.graph.nodes(data=True)
        #Recupération des mots pour les noeuds
        nodes = list(self.df.columns)
        self.graph.add_nodes_from(nodes)
        i = 0
        for i in nodes:
            for j in nodes:
                if(self.df[i][j]>0):
                    self.graph.add_edge(i, j)
                    
        #Construction de la figure plotly qui sert pour l'affichage sur dash
        pos = nx.layout.spring_layout(self.graph)
        for node in self.graph.nodes:
            self.graph.nodes[node]['pos'] = list(pos[node])
  
        
        edge_x = []
        edge_y = []
        edgeSizes = []
        #Initialisation des jeux de coordonnées pour la contruction des arrêtes de la figure plotly
        for edge in self.graph.edges():
            x0, y0 = self.graph.nodes[edge[0]]['pos']
            x1, y1 = self.graph.nodes[edge[1]]['pos']
            edgeSizes.append(self.df[edge[0]][edge[1]])
            edgeSizes.append(None)
            edgeSizes.append(None)
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)
            
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='text',
            mode='lines')
        
        node_x = []
        node_y = []
        #Initialisation des jeux de coordonnées pour la contruction des noeuds de la figure plotly
        for node in self.graph.nodes():
            x, y = self.graph.nodes[node]['pos']
            node_x.append(x)
            node_y.append(y)
        size=[]
        #Pour faire varier la taille des noeuds en fonction de leur présence on créer un tableau des tailles puis on les affectes aux noeuds 
        for node in nodes:
            size.append(self.df[node][node])
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                reversescale=True,
                color=[],
                #Affectation des tailles sur les noeuds
                size=size,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=2))
        node_adjacencies = []
        for node, adjacencies in enumerate(self.graph.adjacency()):
            node_adjacencies.append(len(adjacencies[1]))
        #Données qui définissent l'allure des noeud et de leur label
        node_trace.marker.color = node_adjacencies
        node_trace.text = nodes
        #Construction de la figure finale
        self.fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    title='<br>Graphes de Co-ocurences',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="graphe.grp",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    
    def display(self):
        return self.fig
        