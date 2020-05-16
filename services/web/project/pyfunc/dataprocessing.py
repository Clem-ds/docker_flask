# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 10:25:54 2019

@author: TCQF4816
"""
#pyi-makespec dataprocessing.py
#puis modifier hidden import
#pyinstaller dataprocessing.py --hidden-import=pandas._libs.tslibs.timedelta, pandas._libs.tslibs.c_timestamp

#pyinstaller ne marche pas avec pandas 0.25.3, mais oui avec 0.24.2 

#import numpy as np
import pandas as pd

from os import listdir
import datetime
import sys

import re


'''
listfichier = ' '.join(os.listdir(dossier))
r.findall(listfichier)
listemois = re.findall(r"[0-9]{6}",listfichier)
listemois = list(set(listemois))
listemois.sort()
'''
#dossier doivent avoir le format "YYYYMM"
def verifmois(listemois, dossier):
    
    listedossier = [x for x in listdir(dossier)]
    listebonsmois = []
    
    for mois in listemois: 
        if mois in listedossier: 
            listebonsmois.append(mois)
    
    return listebonsmois

def lecturetablecorresp(dossier): 
    dftabcorresp = pd.read_excel(io=dossier + "2. TABLE CORRESPONDANCE CDR.xlsx",
                                 convert_float=False)
    
    return dftabcorresp


def lecturefichiers(mois, dossier):
    
    dfinscrits = pd.read_csv(filepath_or_buffer = dossier+mois+ '\\dfinscrits '+mois+'.csv', sep=";" )
    dfbudget = pd.read_csv(filepath_or_buffer = dossier+mois+ '\\dfbudget '+mois+'.csv', sep=";" )
    dffluxent = pd.read_csv(filepath_or_buffer = dossier+mois+ '\\dffluxent '+mois+'.csv', sep=";" )
    dffluxsort = pd.read_csv(filepath_or_buffer = dossier+mois+ '\\dffluxsort '+mois+'.csv', sep=";" )
    dfmobent = pd.read_csv(filepath_or_buffer = dossier+mois+ '\\dfmobent '+mois+'.csv', sep=";" )
    dfmobsort = pd.read_csv(filepath_or_buffer = dossier+mois+ '\\dfmobsort '+mois+'.csv', sep=";" )
    dftps = pd.read_csv(filepath_or_buffer = dossier+mois+ '\\dftps '+mois+'.csv', sep=";" )
    #dfteletravail = pd.read_csv(filepath_or_buffer = dossier+mois+ '\\dfteletravail '+mois+'.csv', sep=";" )
    
    
    dictdf = {}
    dictdf["dfinscrits"] = dfinscrits
    dictdf["dfbudget"] = dfbudget
    dictdf["dffluxent"] = dffluxent
    dictdf["dffluxsort"] = dffluxsort
    dictdf["dfmobent"] = dfmobent
    dictdf["dfmobsort"] = dfmobsort
    dictdf["dftps"] = dftps
    #dictdf["dfteletravail"] = dfteletravail

    dictdf["dfcorresp"] = lecturetablecorresp(dossier)
    
    return dictdf


def dfresultatsinscrits(dfres, mois, listemois, dfinscrits, dftps):
    
    dfres.loc['nb_cdi_actifs',mois]= dfinscrits['CDIACTIF  '].sum()
    dfres.loc['nb_cdd_actifs',mois]= dfinscrits['CDDACTIF '].sum()
    
    dfres.loc['nb_apprentis',mois]= len(dfinscrits[dfinscrits['type contrat travail']=='APP'])
    dfres.loc['nb_contratspro',mois]= len(dfinscrits[dfinscrits['type contrat travail']=='CPD'])
    dfres.loc['nb_stagiaires',mois]= len(dfinscrits[dfinscrits['type contrat travail']=='STG'])
    
    dfres.loc['ETP_cdiactifs',mois]= dfinscrits[dfinscrits['CDIACTIF  ']==1]['UTILISE'].sum()
    
    dfres.loc['ETP_cdiactifs_HRZ', mois] = dfinscrits[dfinscrits['CDIACTIF  ']==1]['ETP HRZ'].sum()
    
    dfres.loc['ETP_cddactifs',mois]= dfinscrits[dfinscrits['CDDACTIF ']==1]['UTILISE'].sum()

    return dfres

def dfresultatsbudget(dfres,mois,listemois, dfbudget):
    if '2020' in mois:
        nomcol=datetime.datetime.strptime(mois,'%Y%m').strftime("%Y."+"%b").upper()
        dfres.loc['ETP_budgetHRZ_cdiactifs',mois]= dfbudget[dfbudget['EFFECTIFS 2']=='ETP CDI'][nomcol].sum()
        
        dfres.loc['budget_cdi',mois]= dfbudget[dfbudget['EFFECTIFS 2']=='CDI'][nomcol].sum()
        
        dfres.loc['budget_cdd',mois]= dfbudget[dfbudget['EFFECTIFS 2']=='CDD'][nomcol].sum()
    else: 
        nomcol='Somme de BUD_C'+ datetime.datetime.strptime(mois,'%Y%m').strftime("%Y."+"%b").upper()        
        dfres.loc['ETP_budgetHRZ_cdiactifs',mois]= dfbudget[(dfbudget['EDG_R_Designation']=='Total général')][nomcol].values
    
    return dfres
    
def dfresultatsfluxent(dfres, mois, listemois, dffluxent, dfmobent):
    
    dfres.loc['recrutements_externes', mois] = dffluxent['RECEXTG'].sum()
    
    dfres.loc['mobilites_entrantes', mois] = dffluxent['MOBIGENT'].sum() + dfmobent['MOBENT Umag'].sum()
    
    dfres.loc['reintegrations', mois] = dffluxent['RACTIG '].sum()
    
    return dfres

def dfresultatsfluxsort(dfres, mois, listemois, dffluxsort, dfmobsort):
    
    dfres.loc['deces_departdef', mois] = -dffluxsort[' ASORDEFG'].sum()
    dfres.loc['demission_departdef', mois] = -dffluxsort['DEMIG'].sum()
    dfres.loc['depvolontaire_departdef', mois] = -dffluxsort['DEPVOLG'].sum()
    dfres.loc['interruption_periode_essai_departdef', mois] = -dffluxsort['INPERES'].sum()
    dfres.loc['licenciement_departdef', mois] = -dffluxsort['LICENG'].sum()
    dfres.loc['retraites_departdef', mois] = -dffluxsort['RETRAITG'].sum()
    dfres.loc['mobilites_sortantes', mois] = -dffluxsort['MOBIGSOR'].sum() - dfmobsort['MOBSOR Umag'].sum()
    dfres.loc['sorties_provisoires', mois] = -dffluxsort['  SUSPENG'].sum()
    
    return dfres

def dfresultatstps(dfres, mois, listemois, dftps):
    
    dfres.loc['total_salaries_dispositif_senior', mois] = len(dftps)
    dfres.loc['nb_tps_tl_manag', mois] = len(dftps[dftps[' MARQUAGE TEMPS LIBERE MANAGERIAL']=='OUI'])
    dfres.loc['nb_tps_tl_fin', mois] = len(dftps[dftps[' MARQUAGE TEMPS LIBERE FINANCIER']=='OUI'])
    
    dfres.loc['nb_tps_mecenat', mois] = len(dftps[(dftps['MECENAT DE COMPETENCE']=='OUI') & (dftps[' MARQUAGE TEMPS LIBERE FINANCIER']=='NON')])
    
    dfres.loc['flux_entrees_dispositif_senior',mois] = len(dftps[dftps[' DATE ENTREE TPS']==int(mois)])
    
    dfres.loc['sort_disp_senior_finmois',mois] = -len(dftps[dftps['DATE SORTIE TPS']==int(mois)])
    
    return dfres


def dfresultatsteletravail(dfres, mois, listemois, dfteletravail):
    
    dfres.loc['teletravail_domicile',mois] = len(dfteletravail[dfteletravail['libellé télétravail'] == 'Télétravail à domicile']['identifiant'].unique())
    dfres.loc['teletravail_satellite',mois] = len(dfteletravail[dfteletravail['libellé télétravail'] == 'Télétravail bureau satellite']['identifiant'].unique())
    
    return dfres

def dflistestagiaires(dflistestag, mois, dfinscrits):
 
    dflistestagiairesmois = pd.DataFrame()
    
    dflistestagiairesmois['identifiant'] = dfinscrits[dfinscrits['type contrat travail']=='STG']['identifiant']
    dflistestagiairesmois['mois'] = mois
    
    dflistestag = pd.concat([dflistestag, dflistestagiairesmois[dflistestagiairesmois['identifiant'].isin(dflistestag['identifiant']) == False]])
    
    return dflistestag

def dfresultatsstagiaires(dfres, dfstagiaires, mois, listemois, dfinscrits):
    
    dfres.loc["nb_stagiaires_nouveaux", mois] = len(dfstagiaires[dfstagiaires['mois'] == mois])
    
    return dfres

#def resultats(dfres,mois,listemois,dfinscrits, dfbudget, dffluxent,dffluxsort,dfmobent,dfmobsort,dftps,dfstagiaires):
def resultats(dfres,mois,listemois,dfinscrits, dfbudget, dffluxent,dffluxsort,dfmobent,dfmobsort,dftps,dfstagiaires):
    dfresmois = pd.DataFrame()    
    
    dfresmois = dfresultatsinscrits(dfresmois, mois, listemois, dfinscrits, dftps)
    
    dfresmois = dfresultatsbudget(dfresmois,mois,listemois, dfbudget)
    
    dfresmois = dfresultatsfluxent(dfresmois, mois, listemois, dffluxent, dfmobent)
    
    dfresmois = dfresultatsfluxsort(dfresmois, mois, listemois, dffluxsort, dfmobsort)
    
    dfresmois = dfresultatstps(dfresmois, mois, listemois, dftps)
    
    #dfresmois = dfresultatsteletravail(dfresmois, mois, listemois, dfteletravail)
    
    dfresmois = dfresultatsstagiaires(dfresmois, dfstagiaires, mois, listemois, dfinscrits)
    
    return dfresmois

#pb fevrier mob entrantes, tps mecenat, mob sortantes, sorties provisoires, réintegration

#pb cumul stagiaires: cumul des identifiants

def resultatagrege(dfres,mois,listemois,dfinscrits, dfbudget, dffluxent,dffluxsort,dfmobent,dfmobsort,dftps):
#def resultatagrege(dfres,mois,listemois,dfinscrits, dfbudget, dffluxent,dffluxsort,dfmobent,dfmobsort,dftps,dfteletravail):
      
    dfres.loc['total_cdi_cdd',mois]= dfres.loc['nb_cdi_actifs',mois] + dfres.loc['nb_cdd_actifs',mois]
    
    dfres.loc['total_alternants_stages',mois] = dfres.loc['nb_stagiaires',mois] + dfres.loc['nb_contratspro',mois] + dfres.loc['nb_apprentis',mois] 
    
    
    dfres.loc['coeff_etp_cdi_actifs',mois]=dfres.loc['ETP_cdiactifs',mois]/dfres.loc['nb_cdi_actifs',mois]    
    
    dfres.loc['coeff_etp_cdi_HRZ', mois] = dfres.loc['ETP_cdiactifs_HRZ', mois]/ dfres.loc['nb_cdi_actifs',mois]
    
    dfres.loc['ecart_etpcdi_actifshrz_etpcdi_budgethrz',mois] = (dfres.loc['ETP_cdiactifs_HRZ', mois] - dfres.loc['ETP_budgetHRZ_cdiactifs',mois])
    
    dfres.loc['total_etp_cdi_hrz_ept_cdd',mois] = dfres.loc['ETP_cdiactifs_HRZ', mois] + dfres.loc['ETP_cddactifs',mois]
    
    dfres.loc['total_entrees_cdi',mois] = (dfres.loc['reintegrations', mois] 
                                    + dfres.loc['mobilites_entrantes', mois] 
                                    + dfres.loc['recrutements_externes', mois])
    
    dfres.loc['total_sorties_cdi',mois] =  (dfres.loc['deces_departdef', mois] +
                                        dfres.loc['demission_departdef', mois] +
                                        dfres.loc['depvolontaire_departdef', mois] +
                                        dfres.loc['interruption_periode_essai_departdef', mois] +
                                        dfres.loc['licenciement_departdef', mois] +
                                        dfres.loc['retraites_departdef', mois] +
                                        dfres.loc['mobilites_sortantes', mois] +
                                        dfres.loc['sorties_provisoires', mois])
    
    dfres.loc['solde_total_entrees_cdi_moins_total_sorties_cdi',mois] = dfres.loc['total_entrees_cdi',mois] + dfres.loc['total_sorties_cdi',mois]
    
    dfres.loc['tx_entrees_cdi',mois] = dfres.loc['total_entrees_cdi',mois]/dfres.loc['nb_cdi_actifs',mois]
    
    dfres.loc['tx_turnover_cdi',mois] = dfres.loc['total_sorties_cdi',mois]/dfres.loc['nb_cdi_actifs',mois]
    
    dfres.loc['tx_rotation_cdi', mois] =  (dfres.loc['total_entrees_cdi',mois] + dfres.loc['total_sorties_cdi',mois]) / dfres.loc['nb_cdi_actifs',mois]
    
    dfres.loc['nb_tps', mois] = (dfres.loc['total_salaries_dispositif_senior', mois]
                                -dfres.loc['nb_tps_mecenat', mois]                               
                                -dfres.loc['nb_tps_tl_manag', mois])
    
    moisprec = str(int(mois)-1)
    
    if (moisprec in listemois):
        dfres.loc['flux_sorties_dispositif_senior', mois] =  dfres.loc['sort_disp_senior_finmois', moisprec]
        
    else: 
        #pas possible car on a enlevé 2018 len(dftps[dftps['DATE SORTIE TPS']==moisprec])
        dfres.loc['flux_sorties_dispositif_senior', mois] = 0
        
    
    dfres.loc['solde_flux_tps', mois] = (dfres.loc['flux_entrees_dispositif_senior',mois] + dfres.loc['flux_sorties_dispositif_senior', mois])
    
    dfres.loc['total_teletravail',mois] = (dfres.loc['teletravail_domicile',mois]+dfres.loc['teletravail_satellite',mois])
    
    return dfres


def dfresultatscompar(dfres, mois, listemois):
    moisprec = str(int(mois)-1)
    
    listecompar = ['total_cdi_cdd',
                   'total_alternants_stages',
                   'total_etp_cdi_hrz_ept_cdd',
                   'total_entrees_cdi',
                   'total_sorties_cdi']
    
    
    
    if (moisprec in listemois):
        for compar in listecompar:
            dfres.loc['evol_m-1_' + compar, mois] = dfres.loc[compar,mois] / dfres.loc[compar,moisprec]
                
    else: 
        #pas possible car on a enlevé 2018 len(dftps[dftps['DATE SORTIE TPS']==moisprec])
        for compar in listecompar:
            dfres.loc['evol_m-1_'+compar, mois] = "non valide"
            
       
    return dfres

def dfresultatscumul(dfres, mois, listemois):
    
    
    moisdepart = mois[:4]+'01'
    
    listecumul = ['recrutements_externes',
                  'mobilites_entrantes',
                  'reintegrations',
                  'total_entrees_cdi',
                  'deces_departdef',
                  'demission_departdef',
                  'depvolontaire_departdef',
                  'sorties_provisoires',
                  'mobilites_sortantes',
                  'retraites_departdef',
                  'licenciement_departdef',
                  'interruption_periode_essai_departdef',
                  'total_sorties_cdi',
                  'solde_total_entrees_cdi_moins_total_sorties_cdi',
                  'sort_disp_senior_finmois',
                  'flux_entrees_dispositif_senior',
                  'flux_sorties_dispositif_senior', 
                  'solde_flux_tps',
                  "nb_stagiaires_nouveaux"
                  ]
    
    
    moisprec = str(int(mois)-1)
    #on suppose que listemois est ordonnée au mois près
    if (mois == moisdepart):
        for cumul in listecumul:
            dfres.loc['cumul_depuis_jan_'+cumul,mois] = dfres.loc[cumul,mois]
            

    else: 
        for cumul in listecumul:
            dfres.loc['cumul_depuis_jan_'+cumul,mois] = dfres.loc['cumul_depuis_jan_'+cumul,moisprec] + dfres.loc[cumul,mois]
        
    return dfres

#pb toutes les sorties en moins
def obtentionlistedf(dossier,listemois):
    
    listedossier = [x for x in listdir(dossier)]
    
    dictdfmois = {}
    for mois in listemois:
        if mois in listedossier: 
            dictdfmois[mois]=lecturefichiers(mois, dossier)
        else: 
            print(mois, ' pas encore dispo')

    return dictdfmois

def indexDFres():
    listeindex= ['EFFECTIF ACTIF \n\n',
                 
                 'NB ACTIF\n',
             
                 'nb_cdi_actifs',
                'nb_cdd_actifs',
                'total_cdi_cdd', 
                'evol_m-1_total_cdi_cdd',             

                'nb_apprentis',   
                'nb_contratspro',
                'nb_stagiaires',
                'nb_stagiaires_nouveaux',
                'cumul_depuis_jan_nb_stagiaires_nouveaux',
                'total_alternants_stages',
                'evol_m-1_total_alternants_stages',    
                 
                'ETP ACTIF\n',
                
                'ETP_cdiactifs', 
                'coeff_etp_cdi_actifs',
                
                'ETP_cdiactifs_HRZ', 
                'coeff_etp_cdi_HRZ',
                
                'ETP_cddactifs',
                'total_etp_cdi_hrz_ept_cdd',
                'evol_m-1_total_etp_cdi_hrz_ept_cdd',
                    
                'ETP_budgetHRZ_cdiactifs',  
                'ecart_etpcdi_actifshrz_etpcdi_budgethrz',
                    
                
                'FLUX CDI \n\n',
                
                'ENTREES \n',
                
                'recrutements_externes',
                'cumul_depuis_jan_recrutements_externes',
                
                'mobilites_entrantes',
                'cumul_depuis_jan_mobilites_entrantes',
                
                'reintegrations',
                'cumul_depuis_jan_reintegrations',
                
                'total_entrees_cdi',
                'cumul_depuis_jan_total_entrees_cdi',
                'evol_m-1_total_entrees_cdi', 
                    
                'SORTIES \n',
   
                'deces_departdef', 
                'cumul_depuis_jan_deces_departdef',
                
                'demission_departdef', 
                'cumul_depuis_jan_demission_departdef',
                
                'depvolontaire_departdef',
                'cumul_depuis_jan_depvolontaire_departdef',
                
                'interruption_periode_essai_departdef', 
                'cumul_depuis_jan_interruption_periode_essai_departdef',
                
                'licenciement_departdef',
                'cumul_depuis_jan_licenciement_departdef',     
                
                'retraites_departdef',
                'cumul_depuis_jan_retraites_departdef',
                
                'mobilites_sortantes', 
                'cumul_depuis_jan_mobilites_sortantes',
                
                'sorties_provisoires',
                'cumul_depuis_jan_sorties_provisoires',
                
                'total_sorties_cdi',      
                'cumul_depuis_jan_total_sorties_cdi',
                
                'evol_m-1_total_sorties_cdi',
                    
                'CALCULS ENTREES SORTIES\n',
                
                'solde_total_entrees_cdi_moins_total_sorties_cdi',
                'cumul_depuis_jan_solde_total_entrees_cdi_moins_total_sorties_cdi',
                
                'tx_entrees_cdi',
                'tx_turnover_cdi',
                'tx_rotation_cdi',
                    
                
                'TPS \n\n',
                
                'total_salaries_dispositif_senior',
                'nb_tps',      
                'nb_tps_tl_manag',
                             
                'nb_tps_tl_fin',
                              
                'nb_tps_mecenat',   
                               
                'flux_entrees_dispositif_senior', 
                
                'cumul_depuis_jan_flux_entrees_dispositif_senior',    
                'sort_disp_senior_finmois', 
                'cumul_depuis_jan_sort_disp_senior_finmois',              
                'flux_sorties_dispositif_senior',
                'cumul_depuis_jan_flux_sorties_dispositif_senior',               
                'solde_flux_tps',
                'cumul_depuis_jan_solde_flux_tps',
                
                'TELETRAVAIL \n\n',
                'teletravail_domicile', 
                'teletravail_satellite',
                'total_teletravail' ]
       
    
    return listeindex

def applicationfiltre(dossier, filtre):
    
    print('application du filtre')
    #only use if dict not empty
    if filtre:
        
        dfcorresp = lecturetablecorresp(dossier)
        
        global dfinscrits
        #global dfbudget
        global dffluxent
        global dffluxsort
        global dfmobent
        global dfmobsort
        global dftps
        #global dfteletravail
        
        #print('avant application filtre', list(dfinscrits))
        dfinscrits = dfinscrits.merge(dfcorresp, how='left', left_on='CDR', right_on='CDR')
        #print('apres application filtre', list(dfinscrits))
        #dfbudget = dfbudget.merge(dfcorresp, how='left', left_on='CDR', right_on='CDR')
        dffluxent = dffluxent.merge(dfcorresp, how='left', left_on='cdr ap', right_on='CDR')
        dffluxsort = dffluxsort.merge(dfcorresp, how='left', left_on='cdr av', right_on='CDR')
        dfmobent = dfmobent.merge(dfcorresp, how='left', left_on='cdr ap', right_on='CDR')
        dfmobsort = dfmobsort.merge(dfcorresp, how='left', left_on='cdr av', right_on='CDR')
        dftps = dftps.merge(dfcorresp, how='left', left_on='CDR (NIVEAU 1 ARIANE)', right_on='CDR')
        #dfteletravail = dfteletravail.merge(dfcorresp, how='left', left_on='CDR', right_on='CDR')
        
        listechamps = ['entite','marche', 'processusrh', 'activiterh']
        
        dictchamps= {'entite': 'libellé unité managériale',
                     'marche': 'Marché',
                     'processusrh': 'Processus RH',
                     'activiterh': 'ACTIVITES RH niv1'
                }
        
        for entree in filtre: 
            
            if entree in listechamps: 
                
                champfiltre = dictchamps[entree]
                valchamp = filtre[entree]
                
                if valchamp in set(dfcorresp[champfiltre]):
                    
                    dfinscrits = dfinscrits[dfinscrits[champfiltre] == valchamp]
                    dffluxent = dffluxent[dffluxent[champfiltre] == valchamp]
                    dffluxsort = dffluxsort[dffluxsort[champfiltre] == valchamp]
                    dfmobent = dfmobent[dfmobent[champfiltre] == valchamp]
                    dfmobsort = dfmobsort[dfmobsort[champfiltre] == valchamp]
                    dftps = dftps[dftps[champfiltre] == valchamp]
                    #dfteletravail = dfteletravail[dfteletravail[champfiltre] == valchamp]
                
                else:
                    
                    print(valchamp, 'n\'est pas dans la colonne',champfiltre, 'de la table de correspondance(les espaces/majuscules sont importantes)')
                    sys.exit()
            else: 
                print(entree, 'n\'est pas dans le choix possibles de filtre:', listechamps)
                sys.exit()
                

        
def final(listemois,dossier, filtre={}):
    
    global dfinscrits
    #global dfbudget
    global dffluxent
    global dffluxsort
    global dfmobent
    global dfmobsort
    global dftps
    #global dfteletravail
    
    listeind = indexDFres()
    dfres=pd.DataFrame(index = listeind)
    dfstagiaires = pd.DataFrame(columns=['identifiant', 'mois'])
    
    listedossier = [x for x in listdir(dossier)]
    #listemoisreduite = [x for x in listemois if x in listedossier]
    
    for mois in listemois:
        print(mois, 'en cours de traitement')
        if mois not in listedossier: 
            print(mois, ' pas encore dispo')
        else: 
                    
            dictdf = lecturefichiers(mois, dossier)   
            dfinscrits = dictdf['dfinscrits']           
            dfbudget = dictdf['dfbudget']
            dffluxent = dictdf['dffluxent']
            dffluxsort = dictdf['dffluxsort']         
            dfmobent = dictdf['dfmobent']       
            dfmobsort = dictdf['dfmobsort']
            dftps = dictdf['dftps']
            #dfteletravail = dictdf['dfteletravail']
                        
            mois = str(dftps['PERIODE'].max())
            
            applicationfiltre(dossier, filtre)
            
            #df de stagiaires s'ajoutant chaque mois
            dfstagiaires = dflistestagiaires(dfstagiaires, mois, dfinscrits)
            
            dfresmois = resultats(dfres, mois, listemois, dfinscrits, dfbudget, dffluxent,dffluxsort,dfmobent,dfmobsort,dftps,dfstagiaires)    
            
            #dfresmois = resultats(dfres, mois, listemois, dfinscrits, dfbudget, dffluxent,dffluxsort,dfmobent,dfmobsort,dftps,dfteletravail,dfstagiaires)  
            
            dfres = pd.concat([dfres,dfresmois],axis=1, ignore_index=False, sort=True)
            
            dfres = resultatagrege(dfres,mois,listemois,dfinscrits, dfbudget, dffluxent,dffluxsort,dfmobent,dfmobsort,dftps)
            
            #dfres = resultatagrege(dfres,mois,listemois,dfinscrits, dfbudget, dffluxent,dffluxsort,dfmobent,dfmobsort,dftps,dfteletravail)
            
            dfres = dfresultatscompar(dfres, mois, listemois)
            dfres = dfresultatscumul(dfres, mois, listemois)
            
            print('final', mois)
            
    if filtre: 
        listebudg = [ind for ind in dfres.index if 'budget' in ind]
        for ind in listebudg:
            dfres.drop(index=ind)
            
    dfres = dfres.reindex(indexDFres())
        
    return dfres

def creationExcel(dfres,dossier, nomfichier, filtre = {}):
    
    #empty filter
    if filtre:
        for key,val in filtre.items():
            if '/' in val:
                val = val.replace('/', '_')
            nomfichier += '_' + key + '_' + val + '_'
            
    writer = pd.ExcelWriter(dossier + nomfichier + '.xlsx')

    dfres.to_excel(writer)
    
    sheet = writer.sheets['Sheet1'] 
    sheet.write(0,0,"filtre: "+ str(filtre))   
    
    writer.save()  
    
def creationCSV(dfres,dossier, nomfichier, filtre = {}):
    
    #not empty filter
    if filtre:
        for key,val in filtre.items():
            if '/' in val:
                val = val.replace('/', '_')
            nomfichier += '_' + key + '_' + val + '_'
            

    dfres.to_csv(path_or_buf = dossier +nomfichier+ '.csv', index=False, sep=";",encoding='utf-8-sig')
    

def userInput():
    yesorno = input("Utiliser un filtre? y ou n \n")
    
    filtre = {}

    if (yesorno == "y"):
        
        entite = input("Quelle entitée? (Taper Entrée sans rien écrire si pas intéressé)\n")
        if (entite != ''):
            filtre['entite']=entite
            
        marche = input("Quel marché? (Taper Entrée sans rien écrire si pas intéressé)\n")
        if (marche != ''):
            filtre['marche']=marche
            
        activiterh = input('Quelle activité RH? (Taper Entrée sans rien écrire si pas intéressé)\n')
        if (activiterh != ''):
            filtre['activiterh']=activiterh
        
        processusrh = input('Quel processus RH? (Taper Entrée sans rien écrire si pas intéressé)\n')
        if (processusrh != ''):
            filtre['processusrh']=processusrh
            
        print('Votre filtre est donc: \n', 
              'Entité :',entite, "\n",
              'Marché :',marche, "\n",
              'Activité RH :',activiterh, "\n",
              'Processus RH :',processusrh, "\n")
        
        ok = input('Est-ce que cela vous convient? y ou n \n')
        
        if ok =='y':
            return filtre
        elif ok == 'n': 
            userInput()
        else:
            print('Il faut écrire y ou n \n')
            userInput()
            
            
    elif (yesorno == 'n'):
        certain = input("Etes vous sûrs de ne pas vouloir de filtre? y ou n \n")
        if certain =='n' :
            userInput()
        elif certain == 'y': 
            return filtre
        else: 
            print('Il faut écrire y ou n \n')
            userInput()
    
    else: 
        print('Il faut écrire y ou n \n')
        userInput()
        
    return filtre

def verificationCSV(listemois,dossier):
    
    
    #dossiermois = dossier+mois
    
    #listefichier = listdir(dossiermois)
    
    print("Vérification des CSV de", len(listemois), 'mois :', listemois)
    
    #listedf=['dftps','dfinscrits','dfbudget','dffluxent','dffluxent','dffluxsort','dfmobent','dfmobsort','dfteletravail']
    
    listedf=['dftps','dfinscrits','dfbudget','dffluxent','dffluxent','dffluxsort','dfmobent','dfmobsort']
    
    
    for mois in listemois: 
        
        dossiermois = dossier+mois
        nomsfichiersdansdossier = listdir(dossiermois)
        
        for df in listedf:
        
            nomcsv = df+' '+mois+'.csv'
            
            if nomcsv not in nomsfichiersdansdossier:
                print('Il manque un csv, utilisez xlsxtocsv. ('+df+')',mois)
            
    
        
listeentite = ['BU MOBILE ENTREPRISES',
 ' UI AFFAIRES',
 ' AE SUD EST',
 ' AE OUEST',
 ' CSE SUD',
 ' AE NORMANDIE CENTRE',
 ' AE SUD OUEST',
 ' AE PARIS',
 ' AE GRAND EST',
 ' DM PRO SOA',
 ' ProPME SO',
 ' AE CARAIBES',
 ' DM PRO SOM',
 ' DM PRO RM',
 ' ProPME NE',
 ' DM PRO GE',
 ' DM PRO GO',
 ' DM PRO NDF',
 ' DM PRO IDF',
 ' DM PRO RAA',
 ' AG PRO',
 ' PARNASSE',
 ' DEF EM',
 ' PRO PME DVI EM',
 ' DM PME OA',
 ' DM PME SOM',
 ' DM PME GE',
 ' DM PME IDF',
 ' AG PME',
 ' ProPME IDF',
 ' ProPME O',
 ' ProPME SE',
 ' AE REUNION',
 'AE ISE',
 'AE DOF',
 'AE R2A',
 'AE OCCITANIE',
 ' AE NORD',
 ' CSE IDF',
 'OBS OGSB MOBILE']

listemarche = ['UA MOBILE',
 'Support / Etat Major',
 'E',
 'PRO PME DIGITAL DVI',
 'Agence Parnasse']

listeprocessusrh = ['TPS HORS ACTIVITE',
 'UA MOBILE',
 'Support / Etat Major',
 'SERVICE E',
 'PRO PME',
 'VENTE E',
 'Agence Parnasse',
 'DVI',
 'DIGITAL',
 'SUPPORT E']

listeactiviterh = ['TPS HORS ACTIVITE',
 'CTC SIMPLICITY',
 'DELIVERY',
 'ACCOMPAGNEMENT CLIENT',
 'ACCUEIL',
 'ACE',
 'SOUTIEN-SUPPORT',
 'FARE',
 'RECLAS',
 'ORANGE EVENTS / UEFA',
 'Service / Métiers PP',
 'Support / Métiers PP',
 'Vente / Métiers PP',
 'ENVIRONNEMENT DE LA VENTE',
 'DSDE',
 'DIGITAL',
 'COMMUNICATION',
 'EM TRANSVERSES',
 'FORMATION ET PRESSIONNALISATION',
 'PROGRAMME COME',
 'ETAT MAJOR DRCE',
 'ECOLE VENTES',
 'SUPPORT ENTITE',
 'VENTE',
 'DIR. TECHNICO COMMERCIALE',
 'VENTE FIDELISATION',
 'TRANSVERSE']
'''
listemois = [str(x) for x in range(201901,201913,1)]
listesuivante = list(map(lambda x: str(int(x)+100), listemois))
listemois.extend(listesuivante)
'''


#listemois = ['201901','201902', '201903']

lecteur = input("Lettre du lecteur Budget_DEF? \n").upper()
dossier =  lecteur + r":\TDB PROJET\CLEMENT\\"
#dictdfmois = obtentionlistedf(dossier,listemois)

#filtre = {}
#filtre['entite'] = ' AE OUEST'
#filtre['marche'] = 'PRO PME DIGITAL DVI'
#filtre['processusrh'] = 'ENVIRONNEMENT DE LA VENTE'
#filtre['activiterh'] = 'ACCOMPAGNEMENT CLIENT'
filtre = userInput()

'''
filtre={}
for m in listeactiviterh: 
    filtre['activiterh'] = m
    dfres = final(listemois,dossier,filtre)
    print('fin final', str(filtre))
    nomfichier = "resemploi"
    dossierres = r"X:\TDB PROJET\CLEMENT\resultats\\"
    creationExcel(dfres,dossierres,nomfichier,filtre)
    
'''
#r = re.compile(r"^[0-9]{6}$")

#listemois = list(set(filter(r.match,listdir(dossier))))
#listemois.sort()


listemois = [str(x) for x in range(202001,202005,1)]

verificationCSV(listemois,dossier)
dfres = final(listemois,dossier,filtre)
print('fin final')
dfres = dfres.T
timefichier = ' du ' + datetime.datetime.now().strftime('%Y%m%d_%Hh%M')
nomfichier = "resemploigraph" + timefichier
dossierres = lecteur + r":\TDB PROJET\CLEMENT\resultats\\"
#creationExcel(dfres,dossierres,nomfichier,filtre)
dfres['date']=dfres.index
creationCSV(dfres,dossierres,nomfichier,filtre)

#dfres.to_csv(path_or_buf = dossierres+nomfichier+'.csv', sep=";")


#pour empêcher le terminal de se fermer tout de suite
input('Appuyez sur Entrée pour éteindre le terminal \n')

'''
import itertools
a = [listemarche, listeentite, listeprocessusrh, listeactiviterh]
len(list(itertools.product(*a)))
'''