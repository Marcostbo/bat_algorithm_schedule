import numpy as np
import pandas as pd
import random
from datetime import date, timedelta
import os

class Results(object):

    def __init__(self, Indicadores, UHE_Data, Agenda, path_maintenance):
        os.makedirs('Excel_Results')
        self.samug_df = None
        self.results_1_df = None
        self.results_2_df = None
        self.results_3_df = None
        self.agenda_manut_df = None
        self.cronograma_manut = None

        self.template_samug(Indicadores.HDP, Indicadores.HDF, UHE_Data.lista_turbinas)
        self.buid_results_check(UHE_Data.lista_turbinas, Agenda.Vertido, Agenda.Turbinado, UHE_Data.vaz_afl,
                                Indicadores.HDF_mes, Indicadores.HDP_mes,
                                Agenda.n_rodadas, UHE_Data.dr_man, Agenda.Agenda)
        self.relatorio_manutencao(Agenda.Agenda, path_maintenance)

    def template_samug(self, HDF, HDP, lista_turbinas):
        Num_Dias = 365

        hdf_diario_df = pd.DataFrame(HDF, columns=['HDF'])
        hdp_diario_df = pd.DataFrame(HDP, columns=['HDP'])

        """### Parte HDF"""
        samug_df_hdf = pd.DataFrame(columns=['Equipamento', 'Estado Operativo', 'Data Inicio Verificada',
                                             'Hora Inicio Verificada', 'Condição Operativa', 'Origem',
                                             'Disponibilidade(MW)', 'Nº ONS', 'Validação Agente', 'Tempo',
                                             'Tempo corrigido'])

        # ALIMENTANDO COM NOME DAS TURBINAS E GRUPO
        Turbinas = []
        Grupo = []
        for t in range(int(Num_Dias)):
            for tb, valor in enumerate(lista_turbinas):
                Turbinas.append(valor["Nome"])
                Grupo.append(valor["Grupo"])

        # ALIMENTANDO COM AS DATAS
        data = date(2019, 1, 1)
        lista_datas = []
        for t in range(365):
            for tb in range(50):
                lista_datas.append(data)
            data = data + timedelta(days=1)
            lista_datas_nova = []
        for i in range(365 * 50):
            data = lista_datas[i]
            data = data.strftime('%d/%m/%Y')
            lista_datas_nova.append(data)

        samug_df_hdf['Data Inicio Verificada'] = lista_datas_nova

        # ALIMENTANDO COLUNAS PADROZINADAS
        samug_df_hdf['Equipamento'] = Turbinas
        samug_df_hdf['Estado Operativo'] = 'LIG'
        samug_df_hdf['Hora Inicio Verificada'] = '00:00'
        samug_df_hdf['Nº ONS'] = 'SIMULACAO FID'
        samug_df_hdf['Validação Agente'] = 'NOV'
        samug_df_hdf['Tempo'] = 720.

        # CALCULADO disponibilidade
        horas_disponivel_dia = 12 * 50
        percentual_disponibilidade_diaria = []
        for t in range(365):
            valor = 1 - (hdf_diario_df['HDF'][t] / horas_disponivel_dia)
            percentual_disponibilidade_diaria.append(valor)

        disponibilidade_diaria = []
        for t in range(365):
            for tb in range(50):
                if lista_turbinas[tb]['Grupo'] == '4_pas':
                    valor = percentual_disponibilidade_diaria[t] * 73.290
                    disponibilidade_diaria.append(valor)
                if lista_turbinas[tb]['Grupo'] == '5_pas':
                    valor = percentual_disponibilidade_diaria[t] * 69.590
                    disponibilidade_diaria.append(valor)
        samug_df_hdf['Disponibilidade(MW)'] = disponibilidade_diaria

        # FAZENDO CALSSIFICAÇÃO
        lista_condicao_operativa = []
        lista_origem = []
        for i in range(365 * 50):
            if (samug_df_hdf['Disponibilidade(MW)'][i] == 73.290 or samug_df_hdf['Disponibilidade(MW)'][i] == 69.590):
                lista_condicao_operativa.append('NOR')
                lista_origem.append('')
            else:
                lista_condicao_operativa.append('RFO')
                lista_origem.append('GAC')
        samug_df_hdf['Condição Operativa'] = lista_condicao_operativa
        samug_df_hdf['Origem'] = lista_origem

        lista_tempo_corrigido = []
        for i in range(365 * 50):
            if Grupo[i] == '4_pas':
                valor = (1 - (samug_df_hdf['Disponibilidade(MW)'][i] / 73.290)) * samug_df_hdf['Tempo'][i]
                lista_tempo_corrigido.append(valor)
            if Grupo[i] == '5_pas':
                valor = (1 - (samug_df_hdf['Disponibilidade(MW)'][i] / 69.590)) * samug_df_hdf['Tempo'][i]
                lista_tempo_corrigido.append(valor)
        samug_df_hdf['Tempo corrigido'] = lista_tempo_corrigido

        """### Parte HDP"""

        samug_df_hdp = pd.DataFrame(columns=['Equipamento', 'Estado Operativo', 'Data Inicio Verificada',
                                             'Hora Inicio Verificada', 'Condição Operativa', 'Origem',
                                             'Disponibilidade(MW)', 'Nº ONS', 'Validação Agente', 'Tempo',
                                             'Tempo corrigido'])

        samug_df_hdp['Data Inicio Verificada'] = lista_datas_nova

        # ALIMENTANDO COLUNAS PADROZINADAS
        samug_df_hdp['Equipamento'] = Turbinas
        samug_df_hdp['Estado Operativo'] = 'LIG'
        samug_df_hdp['Hora Inicio Verificada'] = '00:00'
        samug_df_hdp['Nº ONS'] = 'SIMULACAO FID'
        samug_df_hdp['Validação Agente'] = 'NOV'
        samug_df_hdp['Tempo'] = 720.

        horas_disponivel_dia = 12 * 50
        percentual_disponibilidade_diaria = []
        for t in range(365):
            valor = 1 - (hdp_diario_df['HDP'][t] / horas_disponivel_dia)
            percentual_disponibilidade_diaria.append(valor)

        disponibilidade_diaria = []
        for t in range(365):
            for tb in range(50):
                if (lista_turbinas[tb]['Grupo'] == '4_pas'):
                    valor = percentual_disponibilidade_diaria[t] * 73.290
                    disponibilidade_diaria.append(valor)
                if (lista_turbinas[tb]['Grupo'] == '5_pas'):
                    valor = percentual_disponibilidade_diaria[t] * 69.590
                    disponibilidade_diaria.append(valor)

        samug_df_hdp['Disponibilidade(MW)'] = disponibilidade_diaria

        lista_condicao_operativa = []
        lista_origem = []
        for i in range(365 * 50):
            if (samug_df_hdp['Disponibilidade(MW)'][i] == 73.29):
                lista_condicao_operativa.append('NOR')
                lista_origem.append('')
            else:
                if (samug_df_hdp['Disponibilidade(MW)'][i] == 69.59):
                    lista_condicao_operativa.append('NOR')
                    lista_origem.append('')
                else:
                    lista_condicao_operativa.append('RPG')
                    lista_origem.append('GAC')
        samug_df_hdp['Condição Operativa'] = lista_condicao_operativa
        samug_df_hdp['Origem'] = lista_origem

        lista_tempo_corrigido = []
        for i in range(365 * 50):
            if Grupo[i] == '4_pas':
                valor = (1 - (samug_df_hdp['Disponibilidade(MW)'][i] / 73.290)) * samug_df_hdp['Tempo'][i]
                lista_tempo_corrigido.append(valor)
            if Grupo[i] == '5_pas':
                valor = (1 - (samug_df_hdp['Disponibilidade(MW)'][i] / 69.590)) * samug_df_hdp['Tempo'][i]
                lista_tempo_corrigido.append(valor)
        samug_df_hdp['Tempo corrigido'] = lista_tempo_corrigido

        samug_df = pd.concat([samug_df_hdf, samug_df_hdp], ignore_index=True)

        write_samug_df = pd.ExcelWriter("Excel_Results/samug_df.xlsx", engine='openpyxl')
        samug_df.to_excel(write_samug_df, 'samug_df', index=False)
        write_samug_df.save()

        self.samug_df = samug_df

    def buid_results_check(self,lista_turbinas, VV, VT, VAZ_AFL, HDF_mes, HDP_mes, N_Rodadas, dr_man, Agenda):
        ###################################
        ##### RESULTADOS em EXCEL #########
        ###################################
        Num_Turbinas = 50
        Num_Dias = 365
        Num_Meses = 12

        nome_turbinas = []
        for t, valor in enumerate(lista_turbinas):
            nome_turbinas.append(valor["Nome"])

        self.results_1_df = pd.DataFrame(columns=['DIA', 'VV', 'VT', 'VAZ_AFL'])
        for t in range(Num_Dias):
            self.results_1_df['DIA'] = range(Num_Dias)
            self.results_1_df['VV'] = VV
            self.results_1_df['VT'] = VT
            self.results_1_df['VAZ_AFL'] = VAZ_AFL

        self.results_2_df = pd.DataFrame(columns=['MÊS', 'HDF', 'HDP'])
        for t in range(Num_Meses):
            self.results_2_df['MÊS'] = range(Num_Meses)
            self.results_2_df['HDF'] = HDF_mes
            self.results_2_df['HDP'] = HDP_mes

        list_columns = []
        for i in range(N_Rodadas):
            txt = "DM_" + str(i + 1)
            list_columns.append(txt)
        self.results_3_df = pd.DataFrame(dr_man, columns=list_columns)
        self.results_3_df.astype(int)
        self.results_3_df.insert(0, "UG", nome_turbinas, allow_duplicates=False)

        write = pd.ExcelWriter(r"Excel_Results/Results.xlsx", engine='openpyxl')
        self.results_1_df.to_excel(write, 'results_1', index=False)
        self.results_2_df.to_excel(write, 'results_2', index=False)
        self.results_3_df.to_excel(write, 'results_3', index=False)
        write.save()

        self.agenda_manut_df = pd.DataFrame()
        for t in range(Num_Dias):
            agenda_manut = []
            for tb in range(Num_Turbinas):
                if Agenda[tb][t] == 1.:
                    aux = 'M'
                    agenda_manut.append(aux)
                else:
                    aux = int(Agenda[tb][t])
                    agenda_manut.append(aux)
            self.agenda_manut_df[t] = agenda_manut
            # agenda_manut_df.insert(t, t, agenda_manut, allow_duplicates=False)
        self.agenda_manut_df.insert(0, "UG", nome_turbinas, allow_duplicates=False)

        write = pd.ExcelWriter(r"Excel_Results/Agenda.xlsx", engine='openpyxl')
        self.agenda_manut_df.to_excel(write, 'agenda', index=False)
        write.save()

    def relatorio_manutencao(self, Agenda, path_maintenance):
        Num_Turbinas = 50
        Num_Dias = 365

        # MONTANDO LISTA COM APENAS DIAS QUE ESTÁ PROGRAMADO MANUTENÇÃO
        days_manut = []
        for tb in range(Num_Turbinas):
            list_aux = []
            for t in range(Num_Dias):
                if Agenda[tb][t] == 1:
                    posicao = t
                    list_aux.append(t)
            days_manut.append(list_aux)

        # CRIANDO RANGE PARA INDETICAR INÍCIO E FIM DE CADA MANUTENÇÃO EM CADA UG
        ranges = []
        iranges = []
        for tb in range(Num_Turbinas):
            lista = days_manut[tb]
            aux_ranges = sum((list(t) for t in zip(lista, lista[1:]) if t[0] + 1 != t[1]), [])
            aux_iranges = iter(lista[0:1] + aux_ranges + lista[-1:])
            ranges.append(aux_ranges)
            iranges.append(aux_iranges)

        # LISTA COM:
        # DIA DE INICIO E FIM DE CADA MANUTENCAO DE CADA UG
        # UG CORRESPONDENTE
        # DURAÇÃO DE CADA INTERVALO DE MANUTENÇÃO
        list_d_i_full = []
        list_d_f_full = []
        list_duration = []
        list_ug = []
        for tb in range(Num_Turbinas):
            for n in iranges[tb]:
                d_i = n
                d_f = next(iranges[tb])
                dur = d_f - d_i + 1 # ESTÁ PRECISANDO COLOCAR +1 PQ TA AGENDADO 1 DIA A MENOS
                list_d_i_full.append(d_i)
                list_d_f_full.append(d_f)
                list_duration.append(dur)
                if tb < 9:
                    txt = 'ROUHSN_13P8_UG0' + str(tb+1)
                    # txt = 'UG0' + str(tb + 1)
                    list_ug.append(txt)
                else:
                    txt = 'ROUHSN_13P8_UG' + str(tb+1)
                    # txt = 'UG' + str(tb + 1)
                    list_ug.append(txt)

        # LISTA IDENTIFICANDO QUAL DATA REPRESENTA CADA ÍNDICE
        data = date(2019, 1, 1)
        lista_ano = []
        for t in range(365):
            lista_ano.append(data)
            data = data + timedelta(days=1)

        lista_ano_nova = []
        for i in range(365):
            data = lista_ano[i]
            data = data.strftime('%d/%m/%Y')
            lista_ano_nova.append(data)

        # ALTERANDO ÍNDICE PARA DATA
        list_d_i_full_date = []
        list_d_f_full_date = []
        for i in range(len(list_d_i_full)):
            dt_i = lista_ano_nova[list_d_i_full[i]]
            dt_f = lista_ano_nova[list_d_f_full[i]]
            list_d_i_full_date.append(dt_i)
            list_d_f_full_date.append(dt_f)

        # CRIANDO RELATÓRIO
        cronogr = pd.DataFrame(columns=['UG', 'DIA INICIO', 'DIA FIM', 'DURACAO (DIAS)'])
        for i in range(len(list_ug)):
            cronogr['UG'] = list_ug
            cronogr['DIA INICIO'] = list_d_i_full_date
            cronogr['DIA FIM'] = list_d_f_full_date
            cronogr['DURACAO (DIAS)'] = list_duration

        # LENDO PLANILHA EXCEL PREENCHIDA PELO USUÁRIO COM DEMANDA DE MANUTENÇÃO
        df_dr = pd.read_excel(path_maintenance, sheet_name='DM')
        df_dr = pd.DataFrame(df_dr)
        df_dr = df_dr.drop(columns=["TRUG", "GG", "PRIORIDADE"])

        self.cronograma_manut = pd.merge(cronogr, df_dr, how='outer', on=['UG', 'DURACAO (DIAS)'])

        write = pd.ExcelWriter(r"Excel_Results/Cronograma_Sintetizado.xlsx", engine='openpyxl')
        self.cronograma_manut.to_excel(write, 'cronograma_manut', index=False)
        write.save()
