if __name__=="main":
    from interface_graphique import FenetrePrincipale
    from services import GestionInstances
    from algorithmes import AlgoGlouton
    from algorithmes import AlgoDynamique
    from algorithmes import AlgoForceBrute
    from algorithmes import AlgoBranchBound

    gestion_instances = GestionInstances()
    algos = [AlgoGlouton(), AlgoDynamique(), AlgoForceBrute(), AlgoBranchBound()]


    app = FenetrePrincipale(gestion_instances, algos)
    app.mainloop()





















    from services import GestionInstances
    from algorithmes import AlgoGlouton
    from algorithmes import AlgoDynamique
    from algorithmes import AlgoForceBrute
    from algorithmes import AlgoBranchBound
    from visualisation import AffichageConsole

    gestion = GestionInstances()
    instance = gestion.generer_instance(5, 10, 20, 15)

    AffichageConsole.afficher_instance(instance)

    algos = [AlgoGlouton(), AlgoDynamique(), AlgoForceBrute(), AlgoBranchBound()]

    for algo in algos:
        res = algo.resoudre(instance)

        # Déstructurer correctement
        if len(res) == 4:
            selection, poids_total, valeur_totale, dp = res
        else:
            selection, poids_total, valeur_totale = res

        AffichageConsole.afficher_solution(selection, poids_total, valeur_totale)
