
# BILAN HYDRIQUE D'UNE CULTURE ET CALENDRIER D'IRRIGATION

import numpy as np
import matplotlib.pyplot as plt

#Le problème que va résoudre ce modèle  consiste à savoir à quel moment la pluie ne
#suffit elle plus pour une plante et combien d'eau la culture a besoin pour ne pas souffrir

# DEFINIR LA COURBE DE BESOIN EN EAU DE LA CULTURE (ETc)

#La duréé d'une saison de 120 jours decoupée en 12 décades(10jours)
n_decades=12

#Le coefficient cultural Kc qui indique le besoin en eau d'un plante 
#à un stade de son développement
Kc=np.array([0.3,0.3,0.5,0.7,0.9,1.15,1.15,1.15,1.15,0.9,0.7,0.5])#valeurs choisies de façon intuitive
"""Plus la plante pousse et a des feuilles, plus elle a besoin d'eau jusqu'a floraison où
 son besoin en eau chute à nouveau"""

#la valeur climatique de base la région ETO c'est-à-dire la demande en eau de l'atmosphère
 #dûe à la température, au vent et l'ensoleillement
ETO_decade=50.0        #(50mm par décade) valeur réaliste pour une zone tropicale Ouest-africaine

ETc=Kc*ETO_decade       # besoin réel de la culture décade par décade

# SIMULER LA PLUVIOMETRIE PAR DECADE

# générer des valeurs de pluies  avec la loi normale N(40,22), 40mm la moyenne de pluies
 #d'ecart-type 22mm par decade 
np.random.seed(0)
pluie=np.random.normal(40,22,n_decades)   # Données simulées
pluie=np.clip(pluie,0,None)   # Pour empecher qu'une valeur de pluie soit négative

# CONSTRUCTION DU MODELE DU RESERVOIR (BILAN HYDRIQUE)

# La reserve utile Ru (100mm) c'est-à-dire la quantité d'eau que peut contenir un sol limoneux en général
# Un sol sablonneux aurait un Ru plus faible
Ru=100.0 
seuil_irrigation= 0.5*Ru
stock_initial=Ru   # Sol saturé au semis, debut de la saison des pluies

stock=np.zeros(n_decades)
irrigation=np.zeros(n_decades)
stock_precedent=stock_initial

#On utilisera une boucle for car de la decade i depend de celui de i-1
for i in range(n_decades) :
    stock_apres_bilan=stock_precedent+pluie[i]-ETc[i]
    if stock_apres_bilan <= seuil_irrigation :
       irrigation[i]=Ru-stock_apres_bilan  # On ramène le sol à sa capacité maximale
       stock_apres_bilan=Ru
    stock_apres_bilan=np.clip(stock_apres_bilan,0,Ru)
    #Le stock d'eau ne peut pas être inferieur à zéro et ne peut pas dépasser Ru
    #car le surplus sera drainé
    stock[i]=stock_apres_bilan
    stock_precedent=stock_apres_bilan

# VISUALISATION DES RESULTATS
decades=np.arange(1,n_decades+1)

fig, axes=plt.subplots(1,2, figsize=(13, 4.8))

# Figure1 : évolution de la reserve d'eu du sol
axes[0].plot(decades, stock, color="navy", linewidth=2,marker="o", markersize=4, label="Réserve d'eau du sol")
axes[0].axhline(seuil_irrigation, color="red",linestyle="--",label="Seuil de déclenchement d'irrigation(50%Ru)")
axes[0].axhline(Ru, color="green",linestyle=":",label="Capacité maximale du sol")
axes[0].set_title("Evolution de la réserve d'eau du sol")
axes[0].set_xlabel("Décade (période de 10 jours)")
axes[0].set_ylabel("Eau disponible dans le sol (mm)")
axes[0].legend(fontsize=8)
axes[0].set_ylim(0,Ru*1.15)

# Figure2 : besoin en eau , pluie et irrigation par decade
width= 0.35
axes[1].bar(decades - width/2, ETc, width=width, color="red", alpha=0.8, label="Besoin de la culture (ETc)")
axes[1].bar(decades + width/2, pluie, width=width, color="blue", alpha=0.8, label="Pluie reçue")
axes[1].plot(decades, irrigation, color="green", linewidth=2,marker="s", markersize=4, label="Irrigation apportée")
axes[1].set_title("besoin en eau , pluie et irrigation par decade")
axes[1].set_xlabel("Décade (période de 10 jours)")
axes[1].set_ylabel("mm d'eau")
axes[1].legend(fontsize=8)
plt.tight_layout()
plt.savefig("Résultat_de_modélisation.png",dpi=150)
plt.show()
