# Import Packages and Methods

from Parametros_UHE import Leitura, Volume_Turbinado
from Display_Resultados import plota_Agenda
from Agenda_OTM import Otimizacao
from Display_Resultados import plota_Agenda
from Simula_FID import Calculo_Indicadores
import matplotlib.pyplot as plt
import numpy as np
import timeit
import os

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
# UHE_Data.rfo_dia = np.zeros(shape=(50, 365))

print('- Files Reading Completed')

# Max Daily Turbined Flow

VT_Data = Volume_Turbinado(UHE_Data.vaz_afl, UHE_Data.lista_turbinas)
print('- Max Daily Turbined Flow Calculated')

stop = timeit.default_timer()
time = stop - start
print('Data Reading Completed: %4.2f s' % time)

# Scheduling Optimization

print('Begin Optimization')
start = timeit.default_timer()

Agenda = Otimizacao(UHE_Data, VT_Data)

stop = timeit.default_timer()
time = stop - start
print('Total Optimization Elapsed Time: %4.2f s' % time)

# Graphs

plota_Agenda(Agenda.Turbinado, Agenda.Vertido, UHE_Data.vaz_afl, Agenda.Operacao, Agenda.Agenda, UHE_Data.rfo_dia,
             vert_turb=True, ug_op_man=True, vert_n_turb=True, calendario=True)

# HDF and HDP indexes

Indexes = Calculo_Indicadores(Agenda, UHE_Data, VT_Data)

x = np.arange(1, 13, 1)
plt.figure()
plt.bar(x, Indexes.HDF_mes, color='blue')
plt.title('Projeção de HDF')
plt.xlabel('Mês')
plt.ylabel('HDF')
plt.show()

plt.figure()
plt.bar(x, Indexes.HDP_mes, color='orange')
plt.title('Projeção de HDP')
plt.xlabel('Mês')
plt.ylabel('HDP')
plt.show()

