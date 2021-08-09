# Import Packages and Methods

from numpy import ndarray
from Parametros_UHE import Leitura, Volume_Turbinado
from Agenda_OTM import Optimize_Operation, Otimizacao
from Simula_FID import Calculo_Indicadores
import os
import timeit
import numpy as np
import pandas as pd

print('Define Optimal Schedule for Monte Carlo Simulation')

# UHE Data Read

print('- Begin Data Reading')
start = timeit.default_timer()

dir_name = 'Excel_Sheets'
main_path = os.path.realpath(dir_name)

path_hydrology = main_path + '/Hydrology.xlsx'
path_maintenance = main_path + '/Maintenance_Duration.xlsx'
path_rfo = main_path + '/Data_Mining_SAMUG.xlsx'
path_pdf = main_path + '/Data_Mining_SAMUG_SMC.xlsx'

UHE_Data = Leitura(path_vazao=path_hydrology, path_manutencao=path_maintenance,
                   path_rfo=path_rfo, path_pdf=path_pdf, calendario_def=None)

print('-- Files Reading Completed')

# Max Daily Turbined Flow

VT_Data = Volume_Turbinado(UHE_Data.vaz_afl, UHE_Data.lista_turbinas)
print('-- Max Daily Turbined Flow Calculated')

stop = timeit.default_timer()
time = stop - start
print('- Data Reading Completed: %4.2f s' % time)

# Scheduling Optimization

print('- Begin Optimization')
start = timeit.default_timer()

Agenda = Otimizacao(UHE_Data, VT_Data)

stop = timeit.default_timer()
time = stop - start
print('- Total Optimization Elapsed Time: %4.2f s' % time)

N_Rounds = 5000
HDF_mes = {}
HDP_mes = {}

# Monte Carlo Simulation

start = timeit.default_timer()
print('Start Monte Carlo Simulation')
defined_calendar = Agenda.Agenda

for n in range(N_Rounds):

    # UHE_Data = Leitura(path_vazao=path_hydrology, path_manutencao=path_maintenance,
    #                    path_rfo=path_rfo, path_pdf=path_pdf, calendario_def=None)
    #new_rfo = Leitura.ler_rfo_pdf(UHE_Data, path_rfo=path_rfo, path_pdf=path_pdf)

    # Update RFO days for MCS
    UHE_Data = Optimize_Operation.update_rfo(Parametros_UHE=UHE_Data, path_rfo=path_rfo)

    # Optimize Operation
    Agenda = Optimize_Operation(UHE_Data, VT_Data, calendar=defined_calendar, n_days=365, n_ug=50)

    # Build FID Indexes
    Indexes = Calculo_Indicadores(Agenda, UHE_Data, VT_Data)

    HDF_mes[n] = Indexes.HDF_mes
    HDP_mes[n] = Indexes.HDP_mes

    print('-> Round %i of MCS Completed' % (n + 1))

stop = timeit.default_timer()
time = stop - start
print('Monte Carlo Simulation Completed, Time: %4.2f' % time)

# Export Monte Carlo Results

HDF: ndarray = np.zeros(shape=(N_Rounds, 12))
HDF_ano: ndarray = np.zeros(N_Rounds)
HDP = np.zeros(shape=(N_Rounds, 12))
HDP_ano = np.zeros(N_Rounds)

for n in range(N_Rounds):
    HDF[n, :] = HDF_mes[n]
    HDF_ano[n] = sum(HDF_mes[n])
    HDP[n, :] = HDP_mes[n]
    HDP_ano[n] = sum(HDP_mes[n])

HDF_df = pd.DataFrame(HDF, columns=np.arange(1, 13))
HDP_df = pd.DataFrame(HDP, columns=np.arange(1, 13))

export = False
if export:
    HDF_df.to_excel('HDF.xlsx')
    HDP_df.to_excel('HDP.xlsx')
