# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 14:51:19 2020

@author: TCQF4816
"""

import pandas as pd
import numpy as np
import datetime

def lecturedfinscrits(fichier):
    
   
    
    dfinscrits=pd.read_excel(io = fichier, 
                             sheet_name = 'liste des inscrits',
                             convert_float = False)
    
    return dfinscrits

def lecturedfcorresp(fichier):
    
    dfcorrespondance = pd.read_excel(io = fichier, 
                             convert_float = False)
    
    return dfcorrespondance

def lecturedftps(fichier):   
    try:
        dftps = pd.read_excel(io = fichier,
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
        print("dftps valueerror pb ", e )
    return dftps

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
    
def lecturedfcities(fichier):
    
    dfcities = pd.read_csv(fichier, sep=";",encoding='utf-8-sig')
    
    return dfcities

def ajoutcollonglat(dfcities, dfinscrit):
        
    listevilles= list(dfinscrit['adresse établissement - ville'].unique())
    
    listecol = ['department_code','gps_lat','gps_lng']
    
    for col in listecol:
        dictvilles={}
        
        for v in listevilles:
            array_code_dpt = dfcities[dfcities['slug']==v.lower()][col].unique()
            if (len(array_code_dpt) == 0):
                dictvilles[v]=0
            else:
                dictvilles[v] = array_code_dpt[0]
        
        listevillesanscode=[]
        for v in dictvilles:
            if (dictvilles[v]==0):
                listevillesanscode.append(v)
        
        dictvillessanscode={}
        dictvillessanscode['ERAGNY SUR OISE']= 'eragny'
        dictvillessanscode['ST ETIENNE']= 'saint etienne'
        dictvillessanscode['ST BRIEUC']= 'saint brieuc'
        dictvillessanscode['MONTREUIL SOUS BOIS']= 'montreuil'
        dictvillessanscode['ST MARTIN DE CRAU']= 'saint martin de crau'
        dictvillessanscode['MALEMORT SUR CORREZE']= 'malemort'
        dictvillessanscode['BOULAZAC']= 'boulazac isle manoire'
        
        for v in dictvillessanscode:
            slugv = dictvillessanscode[v]
            dictvilles[v]= dfcities[dfcities['slug']==slugv][col].unique()[0]
            
        dfinscrit[col]=dfinscrit['adresse établissement - ville'].map(dictvilles)
        
    return dfinscrit

def modifcol(dfinscr, usecols):
    if (len(usecols) != 0):
        dfinscr = dfinscr[usecols]
        
        renamedict={'department_code': "CODE_DEPT", 
                  'adresse établissement - ville': "site",
                  'Responsable N+1 (O/N)': 'est_manager'
                  }
        for col in renamedict:
            if col not in dfinscr.columns:
                renamedict.pop(col, None) #if col not in rename, returns none
                
        dfinscr = dfinscr.rename(columns=renamedict)
        
    
    #col marché présente 2 fois, on supprime
    dfinscr = dfinscr.loc[:,~dfinscr.columns.duplicated()]

    return dfinscr

def modifspecialchar(dfinscrit):
    ###### il faut retirer les / des valeurs et les accents des colonnes

    dfinscr.replace({' / ': '_'}, inplace=True, regex=True)
    dfinscr.columns = [x.replace('é', 'e') for x in dfinscr.columns]

    return dfinscr

fichier = 'Liste nominative des inscrits DEF 201912.xlsx'
fichiercorresp = r"X:\TDB PROJET\CLEMENT\2. TABLE CORRESPONDANCE CDR.xlsx"
fichiertps = 'TPS 201912.xlsx'
dossier =   r"X:\TDB PROJET\CLEMENT\201912\\"
fichiercities = r'C:\Users\TCQF4816\Documents\data viz\carte\data\cities.csv'

dfinscr = lecturedfinscrits(dossier + fichier)
dfcorrespondance = lecturedfcorresp(fichiercorresp)
dftps = lecturedftps(dossier + fichiertps)
dfcities = lecturedfcities(fichiercities)




'''
dftps = lecturedftps(mois,dossier)
dftps = formattps(dftps,mois)   

dfinscrits = lecturedfinscrits(mois,dossier)
dfinscrits = ajoutETPHRZsurinscrits(dfinscrits, dftps, mois)
'''
usecols = ['identifiant',
           'temps partiel sénior',
                    'CDIACTIF  ', 
                    'CDDACTIF ',
                    'type contrat travail',
                    'UTILISE',
                    'libellé unité managériale',
                    'lib bassin gpec',
                    'Marché',
                    'adresse établissement - ville',
                    'libellé CDR',
                    'Responsable N+1 (O/N)',
                    'Marché',	
                    'Processus RH',	
                    'ACTIVITES RH niv1',	
                    'ACTIVITES RH niv2',	
                    'ACTIVITES RH niv3',
                    'department_code',
                    'gps_lat',
                    'gps_lng']

i=0
if ('identifiant' not in set(dfinscr.columns)):
    while (i < len(dfinscr)):
        
        if ('identifiant' in set(dfinscr.iloc[i,:])):
            #if (set(usecols).issubset(set(dfinscr.iloc[i,:]))):  ne marche pas si il manque une colonne dans dfinscr
            break
        else: 
            i = i+1
            
#que faire quand pas identifiant? (donc mauvais i)
listcol = dfinscr.iloc[i,:] 
dfinscr.columns = listcol
dfinscr = dfinscr.iloc[i+1:,:] #on a supprimé les colonnes au dessus des noms de cols

dfinscr = ajoutcollonglat(dfcities, dfinscr)

#dftps = dfinscr.groupby(['libellé CDR','Responsable N+1 - identifiant groupe'],as_index=False ).count()
    
listeum = list(dfinscr['libellé unité managériale'].unique())

"""
dictmarche={}
for x in listeum:
    
    if 'propme' in x.replace(" ", "").lower():
        dictmarche[x]='propme'
    else:
        dictmarche[x]='e'
        
dfinscr['marché']= dfinscr['libellé unité managériale'].map(dictmarche)
""" 

if (set(dfinscr['CDR']) - set(dfcorrespondance['CDR'])) != set() : 
    print('il manque des cdr dans la table:', (set(dfinscr['CDR']) - set(dfcorrespondance['CDR'])))
    
#obtenir colonnes activitées rh et marché
dfinscr = dfinscr.merge(dfcorrespondance, how='left', left_on='CDR', right_on='CDR',suffixes = ('','_y'))
#filtre les coloones en double    
#dfinscr.drop(list(dfinscr.filter(regex='_y$')), axis=1, inplace=True)     


#si colonnes dont on a besoin sont dans le fichier
if (set(usecols).issubset(set(dfinscr.columns))):
    dfinscr = modifcol(dfinscr, usecols)
else: 
    missingscols = [x for x in usecols if x not in dfinscr.columns]
    print('missings columns :',missingscols)
    
dfinscr = dfinscr[dfinscr['CDIACTIF  ']==1]

dfinscr = modifspecialchar(dfinscr)
    
nomfichier = 'fichierpourmap.csv'
dfinscr.to_csv(path_or_buf = dossier+'2'+nomfichier, index=False, sep=";",encoding='utf-8-sig')

'''
dftest = dfinscr.groupby(['libellé CDR',
                          'site',
                          'est_manager',
                          'Marché',	
                          'Processus RH',	
                          'ACTIVITES RH niv1',	
                          'ACTIVITES RH niv2',	
                          'ACTIVITES RH niv3',
                          'libellé unité managériale',
                           #'bassin gpec',
                           #'department_code',
                           "CODE_DEPT",
                            'gps_lat',
                            'gps_lng'],as_index=False ).count()
    '''

    
#dfinscr.to_csv(path_or_buf = dossier+'5'+nomfichier, index=False, sep=";",encoding='utf-8-sig')


#fichier lourd, changer float en str ne change rien
#dfinscr = dfinscr.astype({'gps_lat': 'str','gps_lng': 'str'})

