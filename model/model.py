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
    def get_cammino_minimo_nx(self,soglia):
        G1=nx.Graph()
        for u,v,w in self.G.edges(data='weight'):
            if w>soglia:
                G1.add_edge(u,v,weight=w)
        best_path=[]
        best_cost=float('inf')
        for s in G1.nodes():
            dist,paths=nx.single_source_dijkstra(G1,s,weight='weight') #dist:dict{node:costomin} paths:dict{node:lista_nodi_cammino}
            for t,cost in dist.items():
                path=paths[t]
                if len(path)>=3 and cost<best_cost:
                    best_cost=cost
                    best_path=path
        return best_path,best_cost
    def cammino_min_recursive(self,nodo_corrente,cammino:list,costo:float,visitati:set):
        if costo>=self.best_costo:
            return
        if len(cammino)>=3:
            self.best_costo=costo
            self.best_path=list(cammino)
        for vicino in self.Gf.neighbors(nodo_corrente):
            if vicino not in visitati:
                visitati.add(vicino)
                cammino.append(vicino)
                nuovo_costo=costo+float(self.Gf[nodo_corrente][vicino]['weight'])
                self.cammino_min_recursive(vicino,cammino,nuovo_costo,visitati)
                cammino.pop()
                visitati.remove(vicino)



    def get_cammino_minimo_recursive(self,soglia):
        self.Gf=nx.Graph()
        for u,v,w in self.G.edges(data='weight'):
            if w>soglia:
                self.Gf.add_edge(u,v,weight=w)
        self.best_path=[]
        self.best_costo=float('inf')
        for nodo in self.Gf.nodes():
            self.cammino_min_recursive(nodo,[nodo],0,{nodo})
        return self.best_path,self.best_costo

