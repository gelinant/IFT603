# -*- coding: utf-8 -*-
"""
Execution dans un terminal

Exemple:
   python non_lineaire_classification.py rbf 100 200 0 0

Vos Noms (Vos Matricules) .~= À MODIFIER =~.
"""

import numpy as np
import sys
from map_noyau import MAPnoyau
import gestion_donnees as gd


def analyse_erreur(err_train, err_test):
    """
    Fonction qui affiche un WARNING lorsqu'il y a apparence de sur ou de sous
    apprentissage
    """
    # erreur apprentissage tres faible, erreur test elevee : sur apprentissage
    # erreur apprentissage elevee, erreur test elevee : sous apprentissage
    # deux faibles : correct
    
    #changer les valeurs en fonction de ce que ça donne car copier coller du tp1
    seuil_sur_test = 20
    seuil_sur_train = 5
    seuil_ss_test = 20
    seuil_ss_train = 20
    
    if (err_test > seuil_sur_test) and (err_train < seuil_sur_train):
        print("Warning: Vous êtes probablement en sur-apprentissage")
    elif (err_test > seuil_ss_test) and (err_train > seuil_ss_train):
        print("Warning: Vous êtes probablement en sous-apprentissage")

    #print("err_test :", err_test)
    #print("err_train :", err_train)

def main():

    if len(sys.argv) < 6:
        usage = "\n Usage: python non_lineaire_classification.py type_noyau nb_train nb_test lin validation\
        \n\n\t type_noyau: rbf, lineaire, polynomial, sigmoidal\
        \n\t nb_train, nb_test: nb de donnees d'entrainement et de test\
        \n\t lin : 0: donnees non lineairement separables, 1: donnees lineairement separable\
        \n\t validation: 0: pas de validation croisee,  1: validation croisee\n"
        print(usage)
        return

    type_noyau = sys.argv[1]
    nb_train = int(sys.argv[2])
    nb_test = int(sys.argv[3])
    lin_sep = int(sys.argv[4])
    vc = bool(int(sys.argv[5]))
    
    # On génère les données d'entraînement et de test
    generateur_donnees = gd.GestionDonnees(nb_train, nb_test, lin_sep)
    [x_train, t_train, x_test, t_test] = generateur_donnees.generer_donnees()

    # On entraine le modèle
    mp = MAPnoyau(noyau=type_noyau)

    if vc is False:
        mp.entrainement(x_train, t_train)
    else:
        mp.validation_croisee(x_train, t_train)
        
    predictions_entrainement = np.array([mp.prediction(x) for x in x_train])
    err_train = 100*np.sum(np.abs(predictions_entrainement-t_train))/len(t_train)

    predictions_test = np.array([mp.prediction(x) for x in x_test])
    err_test = 100*np.sum(np.abs(predictions_test-t_test))/len(t_test)

    print('Erreur train = ', err_train, '%')
    print('Erreur test = ', err_test, '%')
    analyse_erreur(err_train, err_test)

    # Affichage
    mp.affichage(x_test, t_test)

if __name__ == "__main__":
    main()
