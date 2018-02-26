# -*- coding: utf-8 -*-

####### Importez OpenFisca  ###########


import openfisca_france
from openfisca_core.simulations import Simulation
from openfisca_france.model.base import *
from openfisca_core import reforms
import json
import csv

####### Listez les entités ###########

# -*- coding: utf-8 -*-

from os import listdir
from os.path import isfile, join
from pprint import pprint

legislation_france = openfisca_france.FranceTaxBenefitSystem()

import reformes

al_reforms = [
    { 'name': 'Base', 'legislation': legislation_france },
    { 'name': 'AL_MM01', 'legislation': reformes.reforme_al01M(legislation_france) },
    { 'name': 'AL_MM03', 'legislation': reformes.reforme_al03M(legislation_france) },
    { 'name': 'AL_MM12', 'legislation': reformes.reforme_al12M(legislation_france) },
]

from situations import situations
from periods import allMonths

calculs = {
    'aide_logement_base_ressources': allMonths,
    'aide_logement': allMonths,
    'salaire_net': allMonths,
    'loyer': allMonths,
    'proportion_ressource_logement': allMonths,
    'taux_effort_logement': allMonths,
    'ppa': allMonths
}

fieldnames = ['Situation', 'Reform', 'Period', 'Variable', 'Value']

with open('resultats-.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for (name, situation) in situations.iteritems():
        results = {'Situation': name}

        ####### Initialisez la simulation (rencontre des entités avec la legislation) ##############

        for reform in al_reforms:

            results['Reform'] = reform['name']
            simulation_actuelle = Simulation(tax_benefit_system=reform['legislation'], simulation_json=situation)

            ##### Demandez l'ensemble des calculs #####
            for calcul, periods in calculs.iteritems():
                results['Variable'] = calcul
                for period in periods:
                    results['Period'] = period
                    data = simulation_actuelle.calculate(calcul, period)
                    pprint(data)
                    results['Value'] = data[0]
                    writer.writerow(results)

print 'le calcul est terminé'
