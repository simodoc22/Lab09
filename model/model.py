from database.regione_DAO import RegioneDAO
from database.tour_DAO import TourDAO
from database.attrazione_DAO import AttrazioneDAO

class Model:
    def __init__(self):
        self.max_budget = None
        self.max_giorni = None
        self.id_regione = None
        self.tour_map = {} # Mappa ID tour -> oggetti Tour
        self.attrazioni_map = {} # Mappa ID attrazione -> oggetti Attrazione

        self._pacchetto_ottimo = []
        self._valore_ottimo: int = -1
        self._costo = 0



        #Caricamento
        self.load_tour()
        self.load_attrazioni()
        self.load_relazioni()

    @staticmethod
    def load_regioni():
        """ Restituisce tutte le regioni disponibili """
        return RegioneDAO.get_regioni()

    def load_tour(self):
        """ Carica tutti i tour in un dizionario [id, Tour]"""
        self.tour_map = TourDAO.get_tour()

    def load_attrazioni(self):
        """ Carica tutte le attrazioni in un dizionario [id, Attrazione]"""
        self.attrazioni_map = AttrazioneDAO.get_attrazioni()

    def load_relazioni(self):
        lista_tour_attrazioni = TourDAO.get_tour_attrazioni()
        ##sicuramente devo sistemare lista_tour_attrazioni cercando di inserire un dizionario
        ##con chiave id_tour e valori un set di attrazioni

        nuovo_dizionario_attrazioni = {}
        for i in lista_tour_attrazioni:
            for j in i:
                if j[0] not in nuovo_dizionario_attrazioni:
                    id_tour = j[0]
                    nuovo_dizionario_attrazioni[id_tour] = set()
                    nuovo_dizionario_attrazioni[id_tour].add(j[1])
                else:
                    id_tour = j[0]
                    nuovo_dizionario_attrazioni[id_tour].add(j[1])
        ##inoltre ogni attrazione ha un set di tour quindi creiamo un altro dizionario per avere la struttura dati
        ##anche per le attrazioni
        dizionario_tour = {}
        for i in lista_tour_attrazioni:
            for j in i:
                if j[1] not in dizionario_tour:
                    id_attrazione = j[1]
                    dizionario_tour[id_attrazione] = set()
                    dizionario_tour[id_attrazione].add(j[0])
                else:
                    id_attrazione = j[1]
                    dizionario_tour[id_attrazione].add(j[1])

        return nuovo_dizionario_attrazioni, dizionario_tour

    def genera_pacchetto(self, id_regione: str, max_giorni: int = None, max_budget: float = None):
        """
        :return: self._pacchetto_ottimo (una lista di oggetti Tour)
        :return: self._costo (il costo del pacchetto)
        :return: self._valore_ottimo (il valore culturale del pacchetto)
        """
        self._pacchetto_ottimo = []
        self._costo = 0
        self._valore_ottimo = -1
        self.id_regione = id_regione
        self.max_giorni = max_giorni
        self.max_budget = max_budget

        self._pacchetto_ottimo, self._costo, self._valore_ottimo = self._ricorsione(0, [], 0, 0, 0, set(),self.id_regione,self.max_giorni,self.max_budget)
        return self._pacchetto_ottimo, self._costo, self._valore_ottimo

    def _ricorsione(self, start_index: int, pacchetto_parziale: list, durata_corrente: int, costo_corrente: float,
                        valore_corrente: int, attrazioni_usate: set,id_regione,giorni,budget):
        """ Algoritmo di ricorsione che deve trovare il pacchetto che massimizza il valore culturale"""
        tour_attrazioni, attrazioni_tour = self.load_relazioni()

        if durata_corrente == giorni:
            return pacchetto_parziale,valore_corrente,durata_corrente
        else:






            pass








