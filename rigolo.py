import pandas
import numpy
import os
import datetime
import sys

texte = '''Dans un texte engagé, Vincent Lindon fustige le goût d'Emmanuel Macron "pour la pompe et les rites de la monarchie Dans un long texte publié sur Mediapart, Vincent Lindon a partagé sa vision sur la crise du Covid-19 et ses conséquences pour la France, en fustigeant notamment la politique menée par Emmanuel Macron depuis son arrivée à l'Elysée en 2017 Il y a de l'amertume dans les mots de Vincent Lindon, voir de la colère. Ce mercredi 6 mai, Mediapart a partagé un long texte rédigé par le comédien de 60 ans, détenteur de cinq César du Meilleur Acteur. Vincent Lindon a pris le temps de lire face caméra sa longue réflexion sur la crise du Covid-19 qui frappe actuellement la France, et sur les conséquences d'une politique menée depuis plusieurs années par les dirigeants du pays.Il n'épargne pas les différents dirigeants qui se sont succédés à la tête de l'Hexagone, en pointant du doigts l'état des services médicaux. Mais pas seulement : "Au-delà de la santé, c’est l’ensemble du secteur public qui subit depuis des décennies les coups de boutoir des présidents qui se succèdent avec toujours la même obsession : réduire la place de l’État dans l’économie. La recette est simple : privations pour ce qui coûte (l’éducation, la justice, la police, l’armée, la santé…) et privatisations pour ce qui rapporte", explique-t-il. Nicolas Sarkozy, Dominique De Villepin, François Hollande... L'acteur tire à vue, et en particulier sur Emmanuel Macron, présent à l'Eysée depuis 2017. "Dès les premiers jours, une évidence : le goût du nouveau président pour la pompe et les rites de la monarchie, se mettant régulièrement en scène dans les décors de la royauté (...) L’ego comblé, le jeune homme allait pouvoir s’attaquer à son grand œuvre : bâtir cette « start-up nation » où les « premiers de cordée » allaient tirer vers les cimes ces 'Gaulois réfractaires'. Au pas de charge : suppression de l’ISF et allègement de l’impôt sur les profits financiers pour les uns, réformes restrictives du droit du travail ou des allocations chômage et baisse des APL pour les autres", déclare-t-il.Atteint par le Covid-19, le chanteur Vianney a eu “des complications”Vincent Lindon énumère par la suite les différentes décisions prises par le Président de la République et son Gouvernement, tout comme les tensions sociales exacerbées (Gilets Jaunes), conséquences directes d'une politique à la saveur de "mondialisation ultralibérale". L'acteur se penche également sur la gestion de la crise du Covid-19 à proprement parler. "Une seule stratégie, mentir.  Relayant le discours présidentiel, l’équipe gouvernementale multiplie les déclarations absurdes et contradictoires. Ainsi affirme-t-on successivement qu’il ne s’agit que d’une 'grippette' (...) puis qu’elle est 'sous contrôle', avant de devoir avouer la gravité de la situation", dénonce le comédien. Vincent Lindon embraye en évoquant la communication de l'exécutif au sujet des masques : "Je ne vois pas qui aurait pu faire pire", lâche-t-il.Dans la dernière partie de son texte, l'acteur propose alors des pistes de réflexion avec l'espoir de voir des réformes futures se dessiner, en toute modestie et sans prendre un rôle qu'il n'estime pas être le sien. Il propose notamment à l'État de se tourner vers les plus fortunés du pays dans cette période exceptionnelle : "Comment ? En demandant aux plus grosses fortunes une solidarité envers les plus démunis. Cette idée, juste et légitime, pourrait prendre la forme d’une contribution exceptionnelle, baptisée 'Jean Valjean', conçue comme une forme d’assistance à personnes en danger, financée par les patrimoines français de plus de 10 millions d’euros, sans acrobaties, à travers une taxe progressive de 1 % à 5 %, avec une franchise pour les premiers 10 millions d’euros", détaille-t-il. Ce soir chez Baba" (C8) : Plus d'émission à partir de jeudi, Cyril Hanouna explique pourqAprès avoir exposé ses pistes constitutionnelles, électorales ou judiciaires, Vincent Lindon conclut sa longue réflexion. "Ces réformes m’apparaissent nécessaires pour rétablir l’indispensable confiance du peuple en ses représentants, enfin comptables de leurs promesses comme de leur action, et responsables de leurs erreurs", termine-t-il.'''
texte = texte.lower()
texte = texte.replace("'"," ")
texte = texte.replace(" - "," ")
texte = texte.replace("-"," ")
texte = texte.replace(". "," ")
texte = texte.replace(", "," ")
texte = texte.replace(".","")
texte = texte.replace(",","")
texte = texte.split(' ')
texte = pandas.DataFrame(texte)
texte.columns = ['texte']
mots = pandas.DataFrame(texte['texte'].unique())
mots.columns = ['mots']
mots = numpy.array(mots['mots'])
freq = pandas.DataFrame([0] * len(mots))
freq.columns = ['freq']
freq['mots'] = ''
k = 0
for m in mots:
    freq['mots'].iloc[k] = m
    freq['freq'].iloc[k] = sum(texte['texte'] == m)
    k += 1
    print(str(k) + ' - ' + str(len(mots)))
freq = freq.sort_values(['freq'],ascending = False)
freq.to_csv('C:/covid-fr/freq.csv',sep = ';',index=False,encoding='utf-8')
