
import tkinter as tk
from tkinter import ttk
from tkinter import  filedialog


class FenetreAjoutObjet(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.title("Ajouter un objet")
        self.callback = callback

        tk.Label(self, text="Nom :").grid(row=0, column=0, padx=5, pady=5)
        self.nom_entry = tk.Entry(self)
        self.nom_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Poids :").grid(row=1, column=0, padx=5, pady=5)
        self.poids_entry = tk.Entry(self)
        self.poids_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self, text="Valeur :").grid(row=2, column=0, padx=5, pady=5)
        self.valeur_entry = tk.Entry(self)
        self.valeur_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(self, text="Ajouter", command=self.ajouter).grid(row=3, column=0, columnspan=2, pady=10)

    def ajouter(self):
        nom = self.nom_entry.get().strip()
        try:
            poids = int(self.poids_entry.get())
            valeur = int(self.valeur_entry.get())
        except ValueError:
            tk.messagebox.showerror("Erreur", "Poids et valeur doivent être des entiers")
            return
        if not nom:
            tk.messagebox.showerror("Erreur", "Le nom ne peut pas être vide")
            return
        # Créer l'objet (on passe un identifiant provisoire)
        from modele import Objet
        objet = Objet(None, nom, poids, valeur)  # L'identifiant sera réattribué plus tard
        self.callback(objet)
        self.destroy()
        
        
class FenetreSaisieManuelle(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.title("Saisie manuelle")
        self.callback = callback
        self.lignes = []

        tk.Label(self, text="Capacité du bateau :").grid(row=0, column=0, padx=5, pady=5)
        self.capacite_entry = tk.Entry(self)
        self.capacite_entry.grid(row=0, column=1, padx=5, pady=5)

        self.frame_objets = tk.Frame(self)
        self.frame_objets.grid(row=1, column=0, columnspan=2, pady=10)

        self.ajouter_ligne_objet()  # première ligne vide

        tk.Button(self, text="Ajouter un objet", command=self.ajouter_ligne_objet).grid(row=2, column=0, pady=5)
        tk.Button(self, text="Valider", command=self.valider).grid(row=2, column=1, pady=5)

    def ajouter_ligne_objet(self):
        ligne = tk.Frame(self.frame_objets)
        ligne.pack(fill=tk.X, pady=2)
        nom = tk.Entry(ligne, width=15)
        nom.pack(side=tk.LEFT, padx=2)
        poids = tk.Entry(ligne, width=8)
        poids.pack(side=tk.LEFT, padx=2)
        valeur = tk.Entry(ligne, width=8)
        valeur.pack(side=tk.LEFT, padx=2)
        self.lignes.append((nom, poids, valeur))

    def valider(self):
        try:
            capacite = int(self.capacite_entry.get())
        except ValueError:
            tk.messagebox.showerror("Erreur", "Capacité invalide")
            return

        objets = []
        for idx, (nom_entry, poids_entry, valeur_entry) in enumerate(self.lignes):
            nom = nom_entry.get().strip()
            poids_str = poids_entry.get().strip()
            valeur_str = valeur_entry.get().strip()
            if not nom and not poids_str and not valeur_str:
                continue
            try:
                poids = int(poids_str)
                valeur = int(valeur_str)
            except ValueError:
                tk.messagebox.showerror("Erreur", f"Ligne {idx+1} : poids ou valeur non entier")
                return
            from modele import Objet   # à importer en début de fichier
            objets.append(Objet(idx, nom, poids, valeur))

        if not objets:
            tk.messagebox.showerror("Erreur", "Aucun objet saisi")
            return

        from modele import InstanceSacADos
        instance = InstanceSacADos(objets, capacite)
        self.callback(instance)
        self.destroy()

class FenetrePrincipale(tk.Tk):
    def __init__(self, gestion_instances, algos):
        super().__init__()
        self.title("Optimisation Sac à Dos - Master")
        self.geometry("800x600")

        self.panneau_algos = PanneauAlgorithmes(self, gestion_instances, algos)
        self.panneau_algos.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.panneau_resultats = PanneauResultats(self)
        self.panneau_resultats.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.panneau_algos.set_panneau_resultats(self.panneau_resultats)



class PanneauAlgorithmes(tk.Frame):
    def __init__(self, parent, gestion_instances, algos):
        super().__init__(parent)
        self.gestion_instances = gestion_instances
        self.algos = algos
        self.panneau_resultats = None
        self.instance = None
        self.prochain_id = 0   # pour numéroter les objets ajoutés manuellement

        tk.Label(self, text="Algorithmes disponibles:").pack(side=tk.LEFT, padx=2)

        self.combo_algos = ttk.Combobox(self, values=[a.nom_algorithme for a in algos])
        self.combo_algos.current(0)
        self.combo_algos.pack(side=tk.LEFT, padx=2)

        tk.Button(self, text="Nouvelle instance", command=self.nouvelle_instance).pack(side=tk.LEFT, padx=2)
        tk.Button(self, text="Ajouter objet", command=self.ajouter_objet).pack(side=tk.LEFT, padx=2)
        tk.Button(self, text="Lancer algo", command=self.lancer_algo).pack(side=tk.LEFT, padx=2)
        # Optionnel : bouton pour comparer tous les algorithmes
        tk.Button(self, text="Comparer tout", command=self.comparer_tout).pack(side=tk.LEFT, padx=2)
        tk.Button(self, text="Charger fichier", command=self.charger_fichier).pack(side=tk.LEFT, padx=2)
        

    def set_panneau_resultats(self, panneau):
        self.panneau_resultats = panneau
    

    def nouvelle_instance(self):
        """Ouvre la fenêtre de saisie multiple (comme avant) mais réinitialise l'instance."""
        
        self.fenetre_capacite = tk.Toplevel(self)
        self.fenetre_capacite.title("Définir la capacité")
        tk.Label(self.fenetre_capacite, text="Capacité du bateau :").pack(padx=10, pady=5)
        self.capacite_entry = tk.Entry(self.fenetre_capacite)
        self.capacite_entry.pack(padx=10, pady=5)
        tk.Button(self.fenetre_capacite, text="Valider", command=self.valider_capacite).pack(pady=5)

    def valider_capacite(self):
        try:
            capacite = int(self.capacite_entry.get())
        except ValueError:
            tk.messagebox.showerror("Erreur", "Capacité invalide")
            return
        # Créer une instance vide
        from modele import InstanceSacADos
        self.instance = InstanceSacADos([], capacite)
        self.prochain_id = 0
        self.panneau_resultats.afficher_instance(self.instance)
        self.fenetre_capacite.destroy()

    def ajouter_objet(self):
        if self.instance is None:
            tk.messagebox.showwarning("Attention", "Commencez par définir la capacité avec 'Nouvelle instance'")
            return
        FenetreAjoutObjet(self, self.ajouter_objet_callback)

    def ajouter_objet_callback(self, objet):
        # Attribuer un identifiant
        objet.identifiant = self.prochain_id
        self.prochain_id += 1
        # Ajouter à l'instance
        self.instance.liste_objets.append(objet)
        self.instance.nombre_objets = len(self.instance.liste_objets)
        # Mettre à jour l'affichage
        self.panneau_resultats.afficher_instance(self.instance)

    def charger_fichier(self):
        chemin = filedialog.askopenfilename(title="Choisir un fichier")
        if chemin:
            self.instance = self.gestion_instances.charger_instance_depuis_fichier(chemin)
            # Réinitialiser prochain_id au max des identifiants existants +1
            if self.instance.liste_objets:
                self.prochain_id = max(o.identifiant for o in self.instance.liste_objets) + 1
            else:
                self.prochain_id = 0
            self.panneau_resultats.afficher_instance(self.instance)

    def lancer_algo(self):
        if not self.instance:
            tk.messagebox.showwarning("Attention", "Définissez une instance d'abord")
            return

        nom_algo = self.combo_algos.get()
        algo = next(a for a in self.algos if a.nom_algorithme == nom_algo)
        # On peut ajouter un paramètre verbose (par ex. avec une case à cocher)
        res = algo.resoudre(self.instance, verbose=False)  # ou True pour trace console
        self.panneau_resultats.afficher_solution(res, algo.nom_algorithme)

    def comparer_tout(self):
        """Lance tous les algorithmes et affiche une comparaison graphique."""
        if not self.instance:
            tk.messagebox.showwarning("Attention", "Définissez une instance d'abord")
            return
        from services import ComparateurAlgorithmes
        comp = ComparateurAlgorithmes(self.algos)
        resultats = comp.comparer(self.instance)
        
        comp.afficher_resultats(resultats)
        # Afficher les graphiques
        self.afficher_graphiques(resultats)

    def afficher_graphiques(self, resultats):
        fenetre = tk.Toplevel(self)
        fenetre.title("Comparaison des algorithmes")
        canvas = tk.Canvas(fenetre, width=800, height=600, bg='white')
        canvas.pack(fill=tk.BOTH, expand=True)

        marge_gauche = 100
        y_base = 500
        hauteur_max = 300
        largeur_barre = 40

        # Trouver les maximums
        max_val = max(r['valeur_totale'] for r in resultats) or 1
        max_poids = max(r['poids_total'] for r in resultats) or 1
        max_ops = max((r['operations'] or 0) for r in resultats) or 1
        max_temps = max(r['temps'] for r in resultats) or 1e-9

        x = marge_gauche

        # Légende
        canvas.create_rectangle(600, 80, 620, 100, fill="blue")
        canvas.create_text(630, 90, text="Valeur", anchor="w")
        canvas.create_rectangle(600, 110, 620, 130, fill="green")
        canvas.create_text(630, 120, text="Poids", anchor="w")
        canvas.create_rectangle(600, 140, 620, 160, fill="red")
        canvas.create_text(630, 150, text="Opérations", anchor="w")
        canvas.create_rectangle(600, 170, 620, 190, fill="orange")
        canvas.create_text(630, 180, text="Temps (ms)", anchor="w")

        for r in resultats:
            # Valeur
            h_val = (r['valeur_totale'] / max_val) * hauteur_max
            canvas.create_rectangle(x, y_base - h_val, x+largeur_barre, y_base,
                                    fill="blue", outline="black")
            # Poids
            h_pds = (r['poids_total'] / max_poids) * hauteur_max
            canvas.create_rectangle(x+largeur_barre+5, y_base - h_pds,
                                    x+2*largeur_barre+5, y_base,
                                    fill="green", outline="black")
            # Opérations
            h_ops = ((r['operations'] or 0) / max_ops) * hauteur_max
            canvas.create_rectangle(x+2*largeur_barre+10, y_base - h_ops,
                                    x+3*largeur_barre+10, y_base,
                                    fill="red", outline="black")
            # Temps (en ms)
            temps_ms = r['temps'] * 1000
            h_temps = (temps_ms / (max_temps*1000)) * hauteur_max
            canvas.create_rectangle(x+3*largeur_barre+15, y_base - h_temps,
                                    x+4*largeur_barre+15, y_base,
                                    fill="orange", outline="black")

            # Nom de l'algo
            canvas.create_text(x + 2*largeur_barre + 10, y_base + 20,
                               text=r['nom'], anchor="n")
            x += 4*largeur_barre + 30

        # Ligne de base
        canvas.create_line(marge_gauche-10, y_base, x+50, y_base, fill="black")



# panneau_resultats.py
import tkinter as tk
from tkinter import scrolledtext





class PanneauResultats(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.text = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.text.pack(fill=tk.BOTH, expand=True)

    def afficher_instance(self, instance):
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, "--- Instance ---\n")
        self.text.insert(tk.END, "Capacité: {instance.capacite}\n")
        self.text.insert(tk.END, "Objets:\n")
        for o in instance.liste_objets:
            self.text.insert(tk.END, f"  {o.nom} | Poids: {o.poids} | Valeur: {o.valeur}\n")
        self.text.insert(tk.END, "\n")

    def afficher_solution(self, res, nom_algo):
        self.text.insert(tk.END, f"--- Résultat {nom_algo} ---\n")
        # On suppose que res peut avoir 4 ou 5 éléments selon les modifs
        if len(res) == 5:
            selection, poids, valeur, ops, matrice = res
        elif len(res) == 4:
        
            selection, poids, valeur, extra = res
            if isinstance(extra, list):
                matrice = extra
                ops = None
            else:
                ops = extra
                matrice = None
        else:
            selection, poids, valeur = res
            ops = None
            matrice = None

        self.text.insert(tk.END, f"Poids total: {poids}\n")
        self.text.insert(tk.END, f"Valeur totale: {valeur}\n")
        if ops is not None:
            self.text.insert(tk.END, f"Nombre d'opérations: {ops}\n")
        self.text.insert(tk.END, "Objets choisis:\n")
        for o in selection:
            self.text.insert(tk.END, f"  {o.nom} | Poids: {o.poids} | Valeur: {o.valeur}\n")

        if matrice:
            self.text.insert(tk.END, "Matrice DP:\n")
            for ligne in matrice:
                self.text.insert(tk.END, " ".join(str(v) for v in ligne) + "\n")
        self.text.insert(tk.END, "\n")
        self.text.see(tk.END)





from services import GestionInstances
from algorithmes import AlgoGlouton
from algorithmes import AlgoDynamique
from algorithmes import AlgoForceBrute
from algorithmes import AlgoBranchBound
import tkinter as tk

if __name__ == "__main__":
    gestion = GestionInstances()
    algos = [AlgoGlouton(), AlgoDynamique(), AlgoForceBrute(), AlgoBranchBound()]

    app = FenetrePrincipale(gestion, algos)
    app.mainloop()