from modele import Objet, InstanceSacADos
import random

class GestionInstances:
    def __init__(self):
        pass

    def generer_instance(self, nombre_objets, poids_max, valeur_max, capacite):
        objets = []
        for i in range(nombre_objets):
            poids = random.randint(1, poids_max)
            valeur = random.randint(1, valeur_max)
            nom = f"Objet{i+1}"
            objets.append(Objet(i, nom, poids, valeur))
        return InstanceSacADos(objets, capacite)

    def charger_instance_depuis_fichier(self, chemin_fichier):
        objets = []
        with open(chemin_fichier, "r") as f:
            lines = f.readlines()
            capacite = int(lines[0].strip())
            for idx, ligne in enumerate(lines[1:]):
                parts = ligne.strip().split()
                if len(parts) == 3:
                    nom, poids, valeur = parts
                    objets.append(Objet(idx, nom, int(poids), int(valeur)))
        return InstanceSacADos(objets, capacite)







import time

class ComparateurAlgorithmes:
    def __init__(self, algos):
        """
        algos : liste d'instances de AlgoSacADos
        """
        self.algos = algos

    def comparer(self, instance):
        resultats = []
        for algo in self.algos:
            debut = time.time()
            res = algo.resoudre(instance)
            fin = time.time()
            temps = fin - debut

            # Extraction résultat
            if len(res) == 4:  # pour dynamique (DP)
                selection, poids, valeur, extra = res
                if isinstance(extra, list):
                    matrice=extra
                    ops=None
                else:
                    ops=extra
                    matrice=None
            elif len(res)==5:
                selection, poids, valeur,ops,matrice= res 
                
            else:
                selection, poids, valeur = res
                matrice = None
                ops=None

            resultats.append({
                "nom": algo.nom_algorithme,
                "selection": selection,
                "poids_total": poids,
                "valeur_totale": valeur,
                "temps": temps,
                "operations":ops,
                "matrice": matrice
            })
        return resultats

    def afficher_resultats(self, resultats):
        for r in resultats:
            print(f"--- {r['nom']} ---")
            print(f"Valeur totale : {r['valeur_totale']}")
            print(f"Poids total   : {r['poids_total']}")
            print(f"Temps         : {r['temps']:.6f} s")
            print(f"Objets choisis : {[o.nom for o in r['selection']]}")
            if r['matrice'] is not None:
                print("Matrice DP :")
                for ligne in r['matrice']:
                    print(ligne)
            print("\n")