import pandas as pd
import numpy as np
import datetime
from os import listdir

'''
header = np.where(dfinscrits.iloc[:,0] == 'identifiant')[0][0]
dfinscrits.columns = dfinscrits.iloc[header,:] 
dfinscrits = dfinscrits[header:]

dfinscrits = dfinscrits[['identifiant',
                                        'CDIACTIF  ', 
                                        'CDDACTIF ',
                                        'type contrat travail',
                                        'UTILISE',
                                        'CDR']]
'''
def lecturedfinscrits(mois,dossier):
    try:
        
        headerrow = 6
        
        if '2020' in mois:
            headerrow = 5
            
        dfinscrits=pd.read_excel(io = dossier + str(mois) + 
                                 "\Liste nominative des inscrits DEF " + 
                                 str(mois) + ".xlsx", 
                             sheet_name = 'liste des inscrits', 
                             usecols = ['identifiant',
                                        'CDIACTIF  ', 
                                        'CDDACTIF ',
                                        'type contrat travail',
                                        'UTILISE',
                                        'CDR',
                                        'libellé unité managériale',
                                        'temps partiel sénior',
                                        'ALTERN'],
                             convert_float = False,
                             header=headerrow)
        
    except ValueError as e:
        print("dfinscrits valueerror pb ",mois, e )
    
    return dfinscrits

def lecturedfbudget(mois,dossier):        
    try:
        
        if '2020' in mois:
            
            dfbudget = pd.read_excel(io = dossier + str(mois) + r"\BI 2020 DEF.xlsx",
                                 sheet_name='HRZ janv2020',
                                 convert_float = False,
                                 header=5)
        else:
            
            dfbudget = pd.read_excel(io = dossier + str(mois) + r"\Budget BI 2019 DEF.xlsx",
                                 sheet_name='ETP',
                                 convert_float = False)
        
    except ValueError as e:
        print("dfbudget valueerror pb ",mois, e )
    
    return dfbudget

def lecturedffluxent(mois,dossier):
    try:                     
        dffluxent = pd.read_excel(io = dossier + str(mois) + 
                               "\Liste nominative des entrants et sortants sur "+
                               str(mois)+ ".xlsx",
                                 sheet_name='flux entrants',
                                 usecols = ['identifiant',
                                            'RECEXTG',
                                            'MOBIGENT',
                                            'RACTIG ',
                                            'cdr ap'],
                                 convert_float = False,
                                 header=5)
        
    except ValueError as e:
        print("dffluxent valueerror pb ",mois, e )
    return dffluxent

def lecturedffluxsort(mois,dossier):
    try:
        dffluxsort = pd.read_excel(io = dossier + str(mois) + 
                               "\Liste nominative des entrants et sortants sur "+
                               str(mois)+ ".xlsx",
                                 sheet_name='flux sortants',
                                 usecols = ['identifiant',
                                            ' ASORDEFG',
                                            'DEMIG',
                                            'DEPVOLG',
                                            'INPERES',
                                            'LICENG',
                                            'RETRAITG',
                                            'MOBIGSOR',
                                            '  SUSPENG',
                                            'cdr av'],
                                 convert_float = False,
                                 header=5)
        
    except ValueError as e:
        print("dffluxsort valueerror pb ",mois, e )
    return dffluxsort

def lecturedfmobent(mois,dossier):
    try:
        dfmobent = pd.read_excel(io = dossier + str(mois) + 
                               "\Liste nominative des entrants et sortants sur "+
                               str(mois)+ ".xlsx",
                                 sheet_name='mobilités entrantes',
                                 usecols = ['identifiant',
                                            'MOBENT Umag',
                                            'cdr ap'],
                                 convert_float = False,
                                 header=5)
        
    except ValueError as e: 
        print("dfmobent valueerror pb ",mois, e )
    return dfmobent

def lecturedfmobsort(mois,dossier):
    try:
        dfmobsort = pd.read_excel(io = dossier + str(mois) + 
                               "\Liste nominative des entrants et sortants sur "+
                               str(mois)+ ".xlsx",
                                 sheet_name='mobilités sortantes',
                                 usecols = ['identifiant',
                                            'MOBSOR Umag',
                                            'cdr av'],
                                 convert_float = False,
                                 header=5)
        
    except ValueError as e: 
        print("dfmobsort valueerror pb ",mois, e )
    return dfmobsort

def lecturedftps(mois,dossier):   
    try:
        dftps = pd.read_excel(io = dossier + str(mois) + 
                               "\TPS "+
                               str(mois)+ ".xlsx",
                               usecols = ['IDENTIFIANT GROUPE_CUID',
                                          'MATRICULE',
                                          ' DATE ENTREE TPS',
                                          'DATE SORTIE TPS',
                                          ' MARQUAGE TEMPS LIBERE MANAGERIAL',
                                          ' MARQUAGE TEMPS LIBERE FINANCIER',
                                          'MECENAT DE COMPETENCE', 
                                          'TAUX UTILISATION FINANCIER CORRIGE',
                                          'PERIODE',
                                          'CDR (NIVEAU 1 ARIANE)'],
                                          
                                 convert_float = False)
        
               
    except ValueError as e:
        print("dftps valueerror pb ",mois, e )
    return dftps

def lecturedfteletravail(mois,dossier):    
    try:
        dfteletravail = pd.read_excel(io = dossier + str(mois) + 
                               "\Liste nominative des salariés en télétravail DEF "+
                               str(mois)+ ".xlsx",
                               usecols = ['identifiant',
                                          'libellé télétravail',
                                          'CDR'],
                                 convert_float = False,
                                 header=3)
        
    except ValueError as e:
        print("dfteletravail valueerror pb ",mois, e )
    
    
    return dfteletravail
    
def formattps(dftps,mois):
    
    if (len(dftps) != 0):
    #format date similaire aux fichiers
        if isinstance(dftps[' DATE ENTREE TPS'].iloc[0], datetime.date):
            dftps[' DATE ENTREE TPS'] = dftps[' DATE ENTREE TPS'].dt.strftime('%Y%m').values
        
        if isinstance(dftps['DATE SORTIE TPS'].iloc[0], datetime.date):
            dftps['DATE SORTIE TPS'] = dftps['DATE SORTIE TPS'].dt.strftime('%Y%m').values
        
        #bonne période
        dftps = dftps[dftps['PERIODE']==int(mois)]
    
    return dftps
    
def ajoutETPHRZsurinscrits(dfinscrits, dftps, mois):
    
    dftps = formattps(dftps,mois)
    
    dfinscrits = dfinscrits.merge(dftps[['MATRICULE', 'TAUX UTILISATION FINANCIER CORRIGE']], how='left', left_on='identifiant', right_on='MATRICULE')
    
    dfinscrits['ETP HRZ'] = np.where(dfinscrits['MATRICULE'].isna(),dfinscrits['UTILISE'],dfinscrits['TAUX UTILISATION FINANCIER CORRIGE'])
    dfinscrits = dfinscrits.drop_duplicates('identifiant')
    
    return dfinscrits  
    
def conversionfichiers(mois, dossier):
    
    #mois au format YYYYMM
    
    dossiermois = dossier+mois
    fichiersmois = listdir(dossiermois)
    
    nomfichier = 'dftps '+mois+'.csv'
    if nomfichier not in fichiersmois:
        print('traitement dftps',mois)
        dftps = lecturedftps(mois,dossier)
        dftps = formattps(dftps,mois)    
        dftps.to_csv(path_or_buf = dossiermois+'\\'+nomfichier, index=False, sep=";",encoding='utf-8-sig')   
    else: 
        dftps = pd.read_csv(dossiermois+'\\'+nomfichier, sep=";",encoding='utf-8-sig')
        
    nomfichier ='dfinscrits '+mois+'.csv'
    if nomfichier not in fichiersmois:   
        print('traitement dfinscrits', mois)
        dfinscrits = lecturedfinscrits(mois,dossier)
        dfinscrits = ajoutETPHRZsurinscrits(dfinscrits, dftps, mois)
        dfinscrits.to_csv(path_or_buf = dossiermois+'\\'+nomfichier, index=False, sep=";",encoding='utf-8-sig')
    else: 
        dfinscrits = pd.read_csv(dossiermois+'\\'+nomfichier, sep=";",encoding='utf-8-sig')
        
    nomfichier = 'dfbudget '+mois+'.csv'
    if nomfichier not in fichiersmois:    
        print('traitement dfbudget', mois)
        dfbudget = lecturedfbudget(mois,dossier)
        dfbudget.to_csv(path_or_buf = dossiermois+'\\'+nomfichier, index=False, sep=";",encoding='utf-8-sig')
    else: 
        dfbudget = pd.read_csv(dossiermois+'\\'+nomfichier, sep=";",encoding='utf-8-sig')
        
    nomfichier = 'dffluxent '+mois+'.csv'
    if nomfichier not in fichiersmois:    
        print('traitement dffluxent', mois)
        dffluxent = lecturedffluxent(mois,dossier)
        dffluxent.to_csv(path_or_buf = dossiermois+'\\'+nomfichier, index=False, sep=";",encoding='utf-8-sig')
    else: 
        dffluxent = pd.read_csv(dossiermois+'\\'+nomfichier, sep=";",encoding='utf-8-sig')
        
    nomfichier = 'dffluxsort '+mois+'.csv'
    if nomfichier not in fichiersmois:   
        print('traitement dffluxsort', mois)
        dffluxsort = lecturedffluxsort(mois,dossier)
        dffluxsort.to_csv(path_or_buf = dossiermois+'\\'+nomfichier, index=False, sep=";",encoding='utf-8-sig')
    else: 
        dffluxsort = pd.read_csv(dossiermois+'\\'+nomfichier, sep=";",encoding='utf-8-sig')
        
    nomfichier = 'dfmobent '+mois+'.csv'
    if nomfichier not in fichiersmois:   
        print('traitement dfmobent', mois)
        dfmobent = lecturedfmobent(mois,dossier)
        dfmobent.to_csv(path_or_buf = dossiermois+'\\'+nomfichier, index=False, sep=";",encoding='utf-8-sig')
    else: 
        dfmobent = pd.read_csv(dossiermois+'\\'+nomfichier, sep=";",encoding='utf-8-sig')
        
    nomfichier = 'dfmobsort '+mois+'.csv'
    if nomfichier not in fichiersmois: 
        print('traitement dfmobsort', mois)
        dfmobsort = lecturedfmobsort(mois,dossier)
        dfmobsort.to_csv(path_or_buf = dossiermois+'\\'+nomfichier, index=False, sep=";",encoding='utf-8-sig')
    else: 
        dfmobsort = pd.read_csv(dossiermois+'\\'+nomfichier, sep=";",encoding='utf-8-sig')
    '''    
    nomfichier = 'dfteletravail '+mois+'.csv'
    if nomfichier not in fichiersmois:
        print('traitement dfteletravail', mois)
        dfteletravail = lecturedfteletravail(mois,dossier)
        dfteletravail.to_csv(path_or_buf = dossiermois+'\\'+nomfichier, index=False, sep=";",encoding='utf-8-sig')
    else: 
        dfteletravail = pd.read_csv(dossiermois+'\\'+nomfichier, sep=";",encoding='utf-8-sig')
    '''    
    
def traitementdossiers(dossier,listemois):
    
    listedossier = [x for x in listdir(dossier)]
    
    for mois in listemois:
        if mois in listedossier: 
            print('traitement', mois)
            conversionfichiers(mois, dossier)
        else: 
            print(mois, ' pas encore dispo')



lecteur = input("Lettre du lecteur Budget_DEF? \n").upper()
dossier =  lecteur + r":\TDB PROJET\CLEMENT\\"

#listemois = ['201910']
'''
listemois = [str(x) for x in range(201901,201913,1)]
listesuivante = list(map(lambda x: str(int(x)+100), listemois))
listemois.extend(listesuivante)
'''

listemois = [str(x) for x in range(202001,202013,1)]

traitementdossiers(dossier,listemois)

input('Appuyez sur Entrée pour éteindre le terminal \n')
