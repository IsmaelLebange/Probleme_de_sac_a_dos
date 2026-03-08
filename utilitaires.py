
import random
from modele import Objet, InstanceSacADos

class GenerateurInstances:

    def __init__(self):
        pass

    def generer_instance(
        self, 
        nombre_objets=10, 
        poids_min=1, poids_max=20, 
        valeur_min=1, valeur_max=50, 
        capacite=None
    ):
        objets = []
        for i in range(nombre_objets):
            poids = random.randint(poids_min, poids_max)
            valeur = random.randint(valeur_min, valeur_max)
            nom = f"Objet{i+1}"
            objets.append(Objet(i, nom, poids, valeur))

        if capacite is None:
            capacite = sum(o.poids for o in objets) // 2  # capacité raisonnable

        return InstanceSacADos(objets, capacite)





class LecteurFichier:

    def __init__(self):
        pass

    def charger_instance(self, chemin_fichier):
        objets = []
        with open(chemin_fichier, "r") as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]
            capacite = int(lines[0])
            for idx, ligne in enumerate(lines[1:]):
                parts = ligne.split()
                if len(parts) != 3:
                    continue  # ignorer ligne mal formée
                nom, poids, valeur = parts
                objets.append(Objet(idx, nom, int(poids), int(valeur)))
        return InstanceSacADos(objets, capacite)










from algorithmes import AlgoDynamique
from visualisation import AffichageConsole


gen = GenerateurInstances()
instance = gen.generer_instance(nombre_objets=6, poids_max=15, valeur_max=30)

AffichageConsole.afficher_instance(instance)


lecteur = LecteurFichier()

algo = AlgoDynamique()
res = algo.resoudre(instance)
if len(res)==4:
    selection,poids_total,valeur_totale,dp=res
else:
    selection,poids_total,valeur_totale=res
AffichageConsole.afficher_solution(selection, poids_total, valeur_totale)






