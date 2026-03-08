from services import GestionInstances
from algorithmes import AlgoDynamique

class AffichageConsole:

    @staticmethod
    def afficher_instance(instance):
        print("--- Instance Sac à Dos ---")
        print(f"Capacité : {instance.capacite}")
        print(f"Nombre d'objets : {instance.nombre_objets}")
        print("Objets disponibles :")
        for o in instance.liste_objets:
            print(f"  {o.nom} | Poids: {o.poids} | Valeur: {o.valeur}")
        print("\n")

    @staticmethod
    def afficher_solution(selection, poids_total, valeur_totale):
        print("--- Solution ---")
        print(f"Poids total : {poids_total}")
        print(f"Valeur totale : {valeur_totale}")
        print("Objets sélectionnés :")
        for o in selection:
            print(f"  {o.nom} | Poids: {o.poids} | Valeur: {o.valeur}")
        print("\n")

    @staticmethod
    def afficher_comparaison(resultats):
        print("=== Comparaison des Algorithmes ===")
        for r in resultats:
            print(f"{r['nom']}: Valeur={r['valeur_totale']} | Poids={r['poids_total']} | Temps={r['temps']:.6f}s")



class VisualisationMatrice:

    @staticmethod
    def afficher_matrice(dp):
        print("--- Matrice DP ---")
        for ligne in dp:
            print(" ".join(str(v) for v in ligne))
        print("\n")





gestion = GestionInstances()
instance = gestion.generer_instance(5, 10, 20, 15)

AffichageConsole.afficher_instance(instance)

algo = AlgoDynamique()
selection, poids_total, valeur_totale, dp = algo.resoudre(instance)

AffichageConsole.afficher_solution(selection, poids_total, valeur_totale)

VisualisationMatrice.afficher_matrice(dp)
