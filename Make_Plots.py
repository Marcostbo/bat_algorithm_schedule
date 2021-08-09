import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib as mpl

mpl.rcParams["legend.loc"] = 'upper right'
mpl.rcParams['figure.figsize'] = (10, 6)
mpl.rcParams['font.size'] = 16

df_HDF = pd.read_excel('HDF_old.xlsx')

rename_map = {'Unnamed: 0': 'Cenario'}
df_HDF = df_HDF.rename(columns=rename_map)

soma = []
N_Cen = 5000

for s in range(N_Cen):
    a = df_HDF.loc[df_HDF['Cenario'] == s]
    b = np.sum(a.values)
    soma.append(b)

df_HDF['Soma_Ano'] = soma

# PLOT HDF ANUAL
plt.figure()
sns.histplot(data=df_HDF, x='Soma_Ano', binwidth=500, kde=True)
plt.xlabel('HDF Anual')
plt.ylabel('Frequência')
plt.savefig('hdf_histograma.pdf', bbox_inches='tight')
plt.show()

plt.figure()
ax = sns.boxplot(x=df_HDF['Soma_Ano'], notch=True)
plt.ylabel('Ano de Simulação')
plt.xlabel('HDF Anual')
plt.savefig('hdf_boxplot.pdf', bbox_inches='tight')
plt.show()

# Plot High Inflow Months

plt.figure()
sns.histplot(data=df_HDF, x=2, binwidth=100, kde=True, color='blue', label='Fevereiro')
sns.histplot(data=df_HDF, x=3, binwidth=100, kde=True, color='orange', label='Março')
sns.histplot(data=df_HDF, x=4, binwidth=100, kde=True, color='green', label='Abril')
plt.xlabel('HDF Mensal')
plt.ylabel('Frequência')
plt.legend()
plt.savefig('hdf_mes.pdf', bbox_inches='tight')
plt.show()

array = [df_HDF[2].values,
         df_HDF[3].values,
         df_HDF[4].values]

plt.figure()
sns.boxplot(data=array, orient='h', linewidth=1.5)
plt.yticks([0, 1, 2], ['Fev', 'Mar', 'Abr'])
plt.ylabel('Mês')
plt.xlabel('HDF Mensal')
plt.savefig('boxplot_mes.pdf', bbox_inches='tight')
plt.show()

t1 = 0
t2 = 2190
t3 = 6570
t4 = 10950
t5 = 15330
j = df_HDF['Soma_Ano'].values

otimo = sum(t1 < i < t2 for i in j)/N_Cen
bom = sum(t2 < i < t3 for i in j)/N_Cen
regular = sum(t3 < i < t4 for i in j)/N_Cen
ruim = sum(t4 < i < t5 for i in j)/N_Cen
critico = sum(t5 < i for i in j)/N_Cen

bom_valores = []
regular_valores = []
ruim_valores = []
situacao = []

for n in range(N_Cen):
    a = df_HDF['Soma_Ano'].values[n]
    if t2 < a < t3:
        bom_valores.append(a)
        situacao.append('Bom')
    if t3 < a < t4:
        regular_valores.append(a)
        situacao.append('Regular')
    if t4 < a < t5:
        ruim_valores.append(a)
        situacao.append('Ruim')

df_HDF['Situação'] = situacao
data_stack = [regular_valores,
              ruim_valores]

plt.figure()
sns.histplot(data=df_HDF, x='Soma_Ano', hue='Situação',
             multiple="stack", binwidth=500, palette=["blue", "green", "red"])
plt.xlabel('HDF Anual')
plt.ylabel('Frequência')
plt.savefig('histograma_situacao.pdf', bbox_inches='tight')
plt.show()
