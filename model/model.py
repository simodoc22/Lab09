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
            if i["id_tour"] not in nuovo_dizionario_attrazioni:
                id_tour = i["id_tour"]
                oggetto_tour = self.tour_map[id_tour]
                nuovo_dizionario_attrazioni[oggetto_tour] = set()
                id_attrazione = i["id_attrazione"]
                oggetto_attrazione = self.attrazioni_map[id_attrazione]
                nuovo_dizionario_attrazioni[oggetto_tour].add(oggetto_attrazione)
            else:
                id_tour = i["id_tour"]
                oggetto_tour = self.tour_map[id_tour]
                id_attrazione = i["id_attrazione"]
                oggetto_attrazione = self.attrazioni_map[id_attrazione]
                nuovo_dizionario_attrazioni[oggetto_tour].add(oggetto_attrazione)

        ##in questo modo ho dizionario id_tour: {oggetto attrazione 1, 2, 3}


        ##inoltre ogni attrazione ha un set di tour quindi creiamo un altro dizionario per avere la struttura dati
        ##anche per le attrazioni
        dizionario_tour = {}
        for i in lista_tour_attrazioni:
            if i["id_attrazione"] not in dizionario_tour:
                id_tour = i["id_tour"]
                id_attrazione = i["id_attrazione"]
                oggetto_tour = self.tour_map[id_tour]
                oggetto_attrazione = self.attrazioni_map[id_attrazione]
                dizionario_tour[oggetto_attrazione] = set()
                dizionario_tour[oggetto_attrazione].add(oggetto_tour)
            else:
                id_tour = i["id_tour"]
                id_attrazione = i["id_attrazione"]
                oggetto_tour = self.tour_map[id_tour]
                oggetto_attrazione = self.attrazioni_map[id_attrazione]
                dizionario_tour[oggetto_attrazione].add(oggetto_tour)

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

        self._pacchetto_ottimo, self._costo, self._valore_ottimo = self._ricorsione([], 0, 0, 0, set(),self.id_regione,self.max_giorni,self.max_budget)
        return self._pacchetto_ottimo, self._costo, self._valore_ottimo


    def calcolo_valore_culturale(self,attrazioni):
        valore_culturale = 0
        for i in attrazioni:
            valore_culturale+=i.valore_culturale
        return valore_culturale

    def _ricorsione(self, pacchetto_parziale, durata_corrente, costo_corrente,
                    valore_corrente, attrazioni_usate, id_regione, giorni, budget):

        tour_attrazioni, _ = self.load_relazioni()

        # ---- CASO TERMINALE ----
        if durata_corrente > giorni or costo_corrente > budget:
            return [], 0, 0

        if valore_corrente > self._valore_ottimo:
            self._valore_ottimo = valore_corrente
            self._pacchetto_ottimo = pacchetto_parziale.copy()
            self._costo = costo_corrente

        best_pacchetto = pacchetto_parziale
        best_valore = valore_corrente
        best_costo = costo_corrente

        for tour, attr_set in tour_attrazioni.items():

            if str(tour.id_regione) != str(id_regione):
                continue
            if tour.durata_giorni + durata_corrente > giorni:
                continue
            if tour.costo + costo_corrente > budget:
                continue


            if len(attr_set.intersection(attrazioni_usate)) > 0:
                continue


            nuovo_valore = valore_corrente + sum(a.valore_culturale for a in attr_set)


            nuove_attr_usate = attrazioni_usate.union(attr_set)


            nuovo_pacchetto = pacchetto_parziale + [tour]

            pac, cos, val = self._ricorsione(
                nuovo_pacchetto,
                durata_corrente + tour.durata_giorni,
                costo_corrente + tour.costo,
                nuovo_valore,
                nuove_attr_usate,
                id_regione,
                giorni,
                budget
            )


            if val > best_valore:
                best_valore = val
                best_pacchetto = pac
                best_costo = cos

        return best_pacchetto, best_costo, best_valore
















