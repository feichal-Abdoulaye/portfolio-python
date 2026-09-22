
# PROJECTION DE LA DEFORESTATION ET EFFET D'UN PROGRAMME DE REBOISEMENT

import numpy as np
import matplotlib.pyplot as plt

# Face à la deforestation année par année la question qu'on se pose est que si on ne fait rien
# dans combien de temps aurons-nous perdu une part critique de la forêt ? et quel est l'effet réel
# d'un programme de reboisement, si on en met une en place aujourd'hui?

# ce modèle est une projection dans le temps plus précisement 40 ans. on mesure l'etat actuel 
# on essaie d'anticiper la trajectoire future et on essaiera de comparer les conséquences 
# d'agir et ne rien faire 

# MODELISER LE SCENARIO SANS INTERVENTION << STATU QUO >>

n_annees= 40

# la surface initiale de la forêt Si en hectare pour faciliter les calculs
Si=500_000   #surface réaliste pour une zone forestière régionale

# le taux de déforestation par an c'est-à-dire la surface forestière perdue chaque année 
taux_de_deforestation=0.025  # valeur prise en prenant en compte les études du FAO dans certaines 
#zones tropicale d'afrique de l'Ouest et centrale (de 1% à 3%)

# les 2.5% seront constant dans notre bien que dans la réalité ça peut changer

annees=np.arange(0,n_annees+1)

# Nous allons opter pour un modèle de decroissance exponentielle plus réaliste 
# c'est-à-dire on perd les 2.5% de la surface actuelle chaque année et non la surface de départ
Surface_sans_intervention = Si * (1 - taux_de_deforestation) ** annees

# je rappelle que cela peut se faire avec une boucle mais grâce à numpy, on peut calculer la surface 
# restante chaque années en une seule ligne et les recupérer au moment voulu puisque chaque année
# ne depend que l'année zero

# MODELISER LE SCENARIO AVEC REBOISEMENT

# Ici, contrairement au scénario précédent, on ajoute un espace reboisé fixe chaque année
reboisement_annuel= 6000     # 6000 hectares (environ 1,2% de la surface initial)
surface_avec_intervention=np.zeros(n_annees+1)
surface_avec_intervention[0]=Si
for k in range(1, n_annees + 1) :
    surface_avec_intervention[k]=surface_avec_intervention[k-1]*(1-taux_de_deforestation)+reboisement_annuel
    surface_avec_intervention[k]=min(surface_avec_intervention[k],Si)
    # pour empecher de façon logique que la surface avec intervention ne depasse la suface initial 
    # que nous avons

# DETERMINER EN QUELLE ANNEE LE SEUIL CRITIQUE SERA ATTEINT SANS INTERVENTION ET AVEC REBOISEMENT

# On choisit comme seuil critique la moitié de l'espace initial
seuil_critique= Si * 0.5

# définissons une fonction ne paq à refaire la même chose deux fois
def annee_seuil(surface,seuil,tableau_annees):
    sous_seuil=np.where(surface <= seuil)[0]          #la première année où le seuil est franchi
    return tableau_annees[sous_seuil[0]] if len(sous_seuil) > 0 else None

annee_seuil_sans_intervention=annee_seuil(Surface_sans_intervention,seuil_critique,annees)
annee_seuil_avec_intervention=annee_seuil(surface_avec_intervention,seuil_critique,annees)

# VISUALISATION DES RESULTATS

fig, axes=plt.subplots(1,2, figsize=(13,4.8))

# Graphique 1: Les deux trajectoires sur 40 ans
axes[0].plot(annees,Surface_sans_intervention, color="firebrick", linewidth=2, label="Sans intervention (statu quo)")
axes[0].plot(annees,surface_avec_intervention, color="forestgreen", linewidth=2, label="Avec intervention (reboisement)")
axes[0].axhline(seuil_critique, color="black", linestyle="--", linewidth=2, label="Seuil critique (50% de Si)")
axes[0].set_title("Projection de la surface forestière sur 40 ans")
axes[0].set_xlabel("Années")
axes[0].set_ylabel("Surface forestiere (ha)")
axes[0].legend(fontsize=8)

# Graphique 2: comparaison en barres du nombres d'années avant le seuil critique
categories=["Sans intervention", "Avec intervention"]
valeurs_annees=[annee_seuil_sans_intervention if annee_seuil_sans_intervention is not None else n_annees,
                annee_seuil_avec_intervention if annee_seuil_avec_intervention is not None else n_annees]
bars=axes[1].bar(categories,valeurs_annees, color=["firebrick","forestgreen"], alpha=0.85)
labels_bar=[f"{annee_seuil_sans_intervention} ans" if annee_seuil_sans_intervention is not None else ">40 ans",
            f"{annee_seuil_avec_intervention} ans" if annee_seuil_avec_intervention is not None else ">40 ans (jamais atteint)"]
for bar, lbl in zip(bars, labels_bar):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, lbl, ha="center", fontsize=10)

axes[1].set_title("Nombre d'annéé avant d'atteindre le seuil critique")
axes[1].set_ylabel("Années")

plt.tight_layout()
plt.savefig("Résultat_de_modélisation_Env",dpi=150)
plt.show()

# INTERPRETATION DES RESULTATS 

# Dans le scénario sans intervention, le seuil critique (250 000 ha) est atteint dès l'année 28 ans

# Alors qu'avec un programme de 6000 ha par an, ce seuil n'est plus atteint sur les 40 années de projection. La surface se 
# se stabilise autour de 334 000 ha en fin de période. Ce résultat nous montre qu'un effort de reboisement, même modeste peut suffire
# à inverser durablement une tendance si l'intervention est maintenue dans le temps.