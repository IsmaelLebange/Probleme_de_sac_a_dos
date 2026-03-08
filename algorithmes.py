from abc import ABC, abstractmethod
from modele import InstanceSacADos

class AlgoSacADos(ABC):
    def __init__(self, nom_algorithme):
        self.nom_algorithme = nom_algorithme

    @abstractmethod
    def resoudre(self, instance: InstanceSacADos, verbose: bool = False):
        pass


class AlgoGlouton(AlgoSacADos):
    def __init__(self):
        super().__init__("Glouton")

    def resoudre(self, instance, verbose=False):
        self.operations = 0
        objets = instance.liste_objets
        capacite = instance.capacite
        objets_tries = sorted(objets, key=lambda o: o.valeur / o.poids, reverse=True)
        sac = []
        poids_total = 0
        valeur_totale = 0
        for objet in objets_tries:
            self.operations += 1
            if verbose:
                print(f"Glouton: examen de {objet.nom} (poids={objet.poids}, valeur={objet.valeur})")
            if poids_total + objet.poids <= capacite:
                sac.append(objet)
                poids_total += objet.poids
                valeur_totale += objet.valeur
                if verbose:
                    print(f"  -> Objet ajouté, sac: poids={poids_total}, valeur={valeur_totale}")
        return sac, poids_total, valeur_totale, self.operations


class AlgoForceBrute(AlgoSacADos):
    def __init__(self):
        super().__init__("Force Brute")

    def resoudre(self, instance, verbose=False):
        self.operations = 0
        objets = instance.liste_objets
        capacite = instance.capacite
        n = len(objets)
        meilleure_valeur = 0
        meilleur_poids = 0
        meilleure_combinaison = []
        for masque in range(1 << n):
            self.operations += 1
            poids = 0
            valeur = 0
            combinaison = []
            for i in range(n):
                if masque & (1 << i):
                    o = objets[i]
                    poids += o.poids
                    valeur += o.valeur
                    combinaison.append(o)
            if poids <= capacite and valeur > meilleure_valeur:
                meilleure_valeur = valeur
                meilleur_poids = poids
                meilleure_combinaison = combinaison
                if verbose:
                    print(f"Force brute: nouvelle meilleure solution trouvée: valeur={valeur}, poids={poids}")
        return meilleure_combinaison, meilleur_poids, meilleure_valeur, self.operations


class AlgoDynamique(AlgoSacADos):
    def __init__(self):
        super().__init__("Programmation Dynamique")

    def resoudre(self, instance, verbose=False):
        self.operations = 0
        objets = instance.liste_objets
        capacite = instance.capacite
        n = len(objets)
        dp = [[0] * (capacite + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            o = objets[i - 1]
            for w in range(capacite + 1):
                self.operations += 1
                if o.poids <= w:
                    dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - o.poids] + o.valeur)
                else:
                    dp[i][w] = dp[i - 1][w]
        # Reconstruction
        w = capacite
        selection = []
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i - 1][w]:
                o = objets[i - 1]
                selection.append(o)
                w -= o.poids
        poids_total = sum(o.poids for o in selection)
        valeur_totale = sum(o.valeur for o in selection)
        return selection, poids_total, valeur_totale, self.operations, dp


class AlgoBranchBound(AlgoSacADos):
    def __init__(self):
        super().__init__("Branch and Bound")

    def resoudre(self, instance, verbose=False):
        self.operations = 0
        objets = sorted(instance.liste_objets, key=lambda o: o.valeur / o.poids, reverse=True)
        capacite = instance.capacite
        meilleure_valeur = 0
        meilleure_solution = []

        def borne(index, poids, valeur):
            if poids >= capacite:
                return 0
            bv = valeur
            w_total = poids
            i = index
            while i < len(objets) and w_total + objets[i].poids <= capacite:
                w_total += objets[i].poids
                bv += objets[i].valeur
                i += 1
            if i < len(objets):
                reste = capacite - w_total
                bv += objets[i].valeur * (reste / objets[i].poids)
            return bv

        def explorer(index, poids, valeur, solution):
            nonlocal meilleure_valeur, meilleure_solution
            self.operations += 1
            if verbose:
                print(f"Branch&Bound: nœud {index}, poids={poids}, valeur={valeur}")
            if index >= len(objets):
                if valeur > meilleure_valeur:
                    meilleure_valeur = valeur
                    meilleure_solution = solution.copy()
                    if verbose:
                        print(f"  -> Nouvelle meilleure solution: valeur={valeur}")
                return
            if borne(index, poids, valeur) <= meilleure_valeur:
                if verbose:
                    print("  -> Élagage")
                return
            o = objets[index]
            if poids + o.poids <= capacite:
                solution.append(o)
                explorer(index + 1, poids + o.poids, valeur + o.valeur, solution)
                solution.pop()
            explorer(index + 1, poids, valeur, solution)

        explorer(0, 0, 0, [])
        poids_total = sum(o.poids for o in meilleure_solution)
        return meilleure_solution, poids_total, meilleure_valeur, self.operations