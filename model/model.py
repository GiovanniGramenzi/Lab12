import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        # TODO
        self.G = nx.Graph()
        self.lista_rifugi=DAO.get_rifugi()
        self.rif_dict={}
        for rif in self.lista_rifugi:
            self.rif_dict[rif.id]=rif


    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # TODO
        fattore_difficolta=0
        self.G.clear()
        connessioni=DAO.get_connessioni(year)
        for c in connessioni:
            if c.difficolta=='facile':
                fattore_difficolta=1
            elif c.difficolta=='media':
                fattore_difficolta=1.5
            elif c.difficolta=='difficile':
                fattore_difficolta=2
            peso=float(c.distanza)*fattore_difficolta
            self.G.add_edge(self.rif_dict[c.id_rifugio1],self.rif_dict[c.id_rifugio2],weight=peso)

    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        # TODO
        pesi=nx.get_edge_attributes(self.G,'weight').values()
        peso_min=min(pesi)
        peso_max=max(pesi)
        return peso_min,peso_max

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        # TODO
        minori=[]
        maggiori=[]
        for e in self.G.edges(data='weight'):
            if e[2]<soglia:
                minori.append(e)
            elif e[2]>soglia:
                maggiori.append(e)
        return len(minori),len(maggiori)


    """Implementare la parte di ricerca del cammino minimo"""
    # TODO
