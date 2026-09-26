# SIMULATEUR DE PRIME DE D'ASSURANCE-VIE TEMPORAIRE

# Ce modèle va résoudre le problème central du metier d'actuaire c'est-à-dire determiner combien un assuré doit payer aujourd'hui 
# (prime) pour que ce payement ne soit juste, ni trop élevé (l'assureur s'enrichirait injustement), ni trop faible (l'assureur 
# ne pourrait pas payer tous les capitaux dus)

# ici le modèle sera une assurance-vie temporaire sur une durée de 10 ans

#CONSTRUIRE LA TABLE DE MORTALITE 

import numpy as np
import matplotlib.pyplot as plt

ages=np.arange(20,71)   # l'âge des assurés

# A defaut d'une vraie table de mortalité on utilisera cette formule ci-dessous qui reproduit le comportement typique d'une mortalité 
# croissante avec l'âge , avec une accélération après un certains âge (l'exposant 1.6)
qx= 0.0005 + 0.00007 * (ages - 20) ** 1.6   # qx est la probabilité de déces dans l'année, pour une personne d'âge x

# CALCULER LA TABLE DE SURVIE

l0= 100_000     # l'echantillon d'assurés sur lequel nous allons opérer
px= 1 - qx      # la probabilité de survivre dans l'anné, pour une personne d'âge x

# Pour être encore en vie à l'âge x, il faut avoir survécu à tous les âges précédents. C'est une chaine de probabilité qui
#  se multiplie
lx= l0 * np.cumprod(np.insert(px[:-1],0 ,1))    # np.cumprod effectue le produit cumulé
# np.insert(px[:-1],0 ,1) décale le tableau des probabilités de survie d'une position et insère un 1 au debut (à l'âge de départ,
# personne n'a encore eu l'occasion de mourir, donc la probabilité cumulée de survie est 1 à 100%) 

dx= lx * qx    # dx le nombre de décès survenus exactement à l'âge x

# CALCULER LA PRIME PURE D'UNE ASSURANCE TEMPORAIRE 

def prime_temporaire(age_entree, duree_n, capital_K, taux_i):
    idx_debut = age_entree - ages[0]
    idx_fin = idx_debut + duree_n
    lx_periode = lx[idx_debut:idx_fin]
    dx_periode = dx[idx_debut:idx_fin]
    t = np.arange(1, duree_n + 1)
    facteur_actualisation = (1 + taux_i) ** (-t) # permet de donner une valeur présente à un capital futur
    APV = capital_K * np.sum(dx_periode * facteur_actualisation) / lx[idx_debut]
    return APV

print(f"Prime à 30 ans : {prime_temporaire(30, 10, 5_000_000, 0.03)} FCFA")      # environ 229 000 FCFA
print(f"Prime à 50 ans : {prime_temporaire(50, 10, 5_000_000, 0.03)} FCFA")      # environ 803 000 FCFA

# pour chaque année du contrat, dx_periode donne le nombre de décès attendus au cours cette année précise 
# on multiplie par le capital K (ce que l'assureur devrait payer) et par le facteur d'actualisation (pour ramener ce paiement 
# futur à sa valeur d'aujourd'hui) 
# np.sum additionne ces contributions sur toute la durée du contrat ; enfin, on divise par lx[idx_debut] (le nombre de personnes 
# vivantes au début du contrat) pour obtenir un résultat par personne assurée, et non pour toute la population 

# VISUALISATION DES RESULTATS

ages_test = np.arange(20, 61)
duree, capital, taux = 10 , 5_000_000 , 0.03
primes_par_age = np.array([prime_temporaire(age, duree, capital, taux) for age in ages_test])

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

# Graphique 1 : la table de survie
axes[0].plot(ages, lx, color="skyblue", linewidth=2)
axes[0].set_title("Table de survie (lx) — population de 100 000 à l'âge 20 ans")
axes[0].set_xlabel("Âge")
axes[0].set_ylabel("Nombre de survivants")
axes[0].grid(alpha=0.3)

# Graphique 2 : la prime selon l'âge d'entrée
axes[1].plot(ages_test, primes_par_age, color="red", linewidth=2, marker="o", markersize=3)
axes[1].set_title(f"Prime pure vs âge d'entrée\n(capital {capital:,.0f} FCFA, durée {duree} ans, taux {taux*100:.0f}%)")
axes[1].ticklabel_format(style='plain', axis='y')
axes[1].set_xlabel("Âge d'entrée dans le contrat")
axes[1].set_ylabel("Prime pure (FCFA)")
axes[1].grid(alpha=0.3)
plt.tight_layout()
plt.savefig("Resultat_de_modelisation.png", dpi=150)
plt.show()
plt.close()

# La prime passe d'environ 229 000 FCFA à 30 ans à environ 803 000 FCFA à 50 ans (presque 3,5 fois plus élevée), pour exactement 
# le même capital et la même durée de contrat. Ce résultat traduit numériquement une intuition que tout le monde a : 
# s'assurer jeune coûte moins cher, parce que le risque de décès dans les 10 années suivantes est nettement plus faible à 30 ans 
# qu'à 50 ans.