# Import modules and packages

from meta_heuristics import MetaHeuristics
from Parametros_UHE import Leitura, Volume_Turbinado
import numpy as np
import timeit
import os
from Agenda_OTM import Optimize_Operation
from Display_Resultados import plota_Agenda
from Simula_FID import Calculo_Indicadores
import matplotlib.pyplot as plt

# UHE Data Read

print('Begin Data Reading')
start = timeit.default_timer()

dir_name = 'Excel_Sheets'
main_path = os.path.realpath(dir_name)

path_hydrology = main_path + '/Hydrology.xlsx'
path_maintenance = main_path + '/Maintenance_Duration.xlsx'
path_rfo = main_path + '/Data_Mining_SAMUG.xlsx'
path_pdf = main_path + '/Data_Mining_SAMUG_SMC.xlsx'

UHE_Data = Leitura(path_vazao=path_hydrology, path_manutencao=path_maintenance,
                   path_rfo=path_rfo, path_pdf=path_pdf, calendario_def=None)

print('- Files Reading Completed')

# Max Daily Turbined Flow

VT_Data = Volume_Turbinado(UHE_Data.vaz_afl, UHE_Data.lista_turbinas)
print('- Max Daily Turbined Flow Calculated')

stop = timeit.default_timer()
time = stop - start
print('Data Reading Completed: %4.2f s' % time)

# bat algorithm application

maintenance_duration = UHE_Data.dr_man
n_ug = 50         # number of generating units
n_days = 365      # number of days
ind_size = n_ug   # individual size
n_ind = 1000      # denotes population size,
n_gen = 5         # denotes number of generations (iterations),

alpha = 0.6   # sound wave amplitude decrease rate
lbd = 0.5     # sound wave pulse emission increase rate

n_rounds = 4
maintenance_result = np.zeros(shape=(n_ug, n_rounds))
defined_calendar = np.zeros(shape=(n_ug, n_days))

# UHE_Data.rfo_dia = np.zeros(shape=(n_ug, n_days))

# first optimization
Agenda = Optimize_Operation(Dados_UHE=UHE_Data, Dados_VT=VT_Data, calendar=defined_calendar,
                            previous_calendar=np.zeros(shape=(n_ug, n_days)), n_days=n_days, n_ug=n_ug)

arr = Agenda.Operacao
# original_operation = tuple(map(tuple, arr))
# original_spilled = tuple(Agenda.Vertido)
original_operation = Agenda.Operacao
original_spilled = Agenda.Vertido

for current_round in range(n_rounds):
    print('Maintenance Round: %i' % (current_round + 1))
    maintenance_round = current_round

    Bat = MetaHeuristics(uhe_data=UHE_Data, n_ug=n_ug, n_days=n_days,
                         maintenance_round=maintenance_round, maintenance_duration=maintenance_duration,
                         previous_calendar=defined_calendar, n_ind=n_ind)

    start = timeit.default_timer()
    Bat.bat_algorithm_process(uhe_data=UHE_Data, previous_calendar=defined_calendar, vt_data=VT_Data,
                              n_gen=n_gen, alpha=alpha, lbd=lbd, n_ind=n_ind, maintenance_round=current_round,
                              original_operation=original_operation, original_spill=original_spilled)

    stop = timeit.default_timer()
    time = stop - start
    print('Bat Algorithm Completed: %4.2f s' % time)

    # update calendar with current maintenance result
    maintenance_result[:, current_round] = Bat.best_bat_result
    current_maintenance = maintenance_duration[:, maintenance_round]

    for ug in range(n_ug):
        m = int(current_maintenance[ug])
        start = int(Bat.best_bat_result[ug])

        defined_calendar[ug, start:start + m] = 1

    Agenda = Optimize_Operation(Dados_UHE=UHE_Data, Dados_VT=VT_Data, calendar=defined_calendar,
                                previous_calendar=np.zeros(shape=(n_ug, n_days)), n_days=n_days, n_ug=n_ug)

    original_operation = Agenda.Operacao
    original_spilled = Agenda.Vertido

Agenda = Optimize_Operation(Dados_UHE=UHE_Data, Dados_VT=VT_Data, calendar=defined_calendar,
                            previous_calendar=np.zeros(shape=(n_ug, n_days)), n_days=n_days, n_ug=n_ug)

plota_Agenda(Agenda.Turbinado, Agenda.Vertido, UHE_Data.vaz_afl, Agenda.Operacao, Agenda.Agenda, UHE_Data.rfo_dia,
             vert_turb=True, ug_op_man=True, vert_n_turb=False, calendario=True)

# HDF and HDP indexes

Indexes = Calculo_Indicadores(Agenda, UHE_Data, VT_Data)
x = np.arange(1, 13, 1)
plt.figure()
plt.bar(x, Indexes.HDF_mes, color='blue')
plt.title('HDF Projection')
plt.xlabel('Month')
plt.ylabel('HDF')
plt.show()

plt.figure()
plt.bar(x, Indexes.HDP_mes, color='orange')
plt.title('HDP Projection')
plt.xlabel('Month')
plt.ylabel('HDP')
plt.show()
