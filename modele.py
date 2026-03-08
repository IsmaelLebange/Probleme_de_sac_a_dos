class Objet:
    def __init__(self, identifiant: int, nom: str, poids: int, valeur: int):
        self.identifiant = identifiant
        self.nom = nom
        self.poids = poids
        self.valeur = valeur

    def __repr__(self):
        return f"{self.nom}(poids={self.poids}, valeur={self.valeur})"



class SacADos:
    def __init__(self, capacite: int):
        self.capacite = capacite
        self.objets_selectionnes = []
        self.valeur_totale = 0
        self.poids_total = 0

    def ajouter_objet(self, objet: Objet):
        self.objets_selectionnes.append(objet)
        self.poids_total += objet.poids
        self.valeur_totale += objet.valeur

    def __repr__(self):
        return (f"Sac(capacite={self.capacite}, poids_total={self.poids_total}, "
                f"valeur_totale={self.valeur_totale}, objets={self.objets_selectionnes})")



class InstanceSacADos:
    def __init__(self, liste_objets: list, capacite: int):
        self.liste_objets = liste_objets  # liste d'objets
        self.capacite = capacite
        self.nombre_objets = len(liste_objets)

    def __repr__(self):
        return (f"Instance(capacite={self.capacite}, nombre_objets={self.nombre_objets}, "
                f"objets={self.liste_objets})")