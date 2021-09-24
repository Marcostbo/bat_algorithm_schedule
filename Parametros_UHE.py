import numpy as np
import pandas as pd
import random
import datetime
import matplotlib.pyplot as plt


class Leitura(object):

    def __init__(self, path_vazao, path_manutencao, path_rfo, path_pdf, calendario_def, year_array):
        self.vaz_afl = None
        self.vaz_hist = None
        self.dr_man = None
        self.rfo_pdf = None
        self.rfo_mes = None
        self.rfo_dia = None
        self.manut_def = None
        self.lista_turbinas = None
        self.year_array = year_array

        self.ler_turbinas()
        self.ler_vaz_afl(path_vazao, year_array)
        self.ler_dr_man(path_manutencao)
        self.ler_rfo_pdf(path_rfo, path_pdf, year_array)
        self.ler_manut_def_array(calendario_def)

    def ler_turbinas(self):
        lista_turbinas = []
        turbina = {"Nome": "ROUHSN_13P8_UG01", "Grupo": "5_pas", }
        lista_turbinas.append(turbina)  # 0
        turbina = {"Nome": "ROUHSN_13P8_UG02", "Grupo": "5_pas", }
        lista_turbinas.append(turbina)  # 1
        turbina = {"Nome": "ROUHSN_13P8_UG03", "Grupo": "5_pas", }
        lista_turbinas.append(turbina)  # 2
        turbina = {"Nome": "ROUHSN_13P8_UG04", "Grupo": "5_pas", }
        lista_turbinas.append(turbina)  # 3
        turbina = {"Nome": "ROUHSN_13P8_UG05", "Grupo": "5_pas", }
        lista_turbinas.append(turbina)  # 4
        turbina = {"Nome": "ROUHSN_13P8_UG06", "Grupo": "5_pas", }
        lista_turbinas.append(turbina)  # 5
        turbina = {"Nome": "ROUHSN_13P8_UG07", "Grupo": "5_pas", }
        lista_turbinas.append(turbina)  # 6
        turbina = {"Nome": "ROUHSN_13P8_UG08", "Grupo": "5_pas", }
        lista_turbinas.append(turbina)  # 7
        turbina = {"Nome": "ROUHSN_13P8_UG09", "Grupo": "5_pas", }
        lista_turbinas.append(turbina)  # 8
        turbina = {"Nome": "ROUHSN_13P8_UG10", "Grupo": "5_pas", }
        lista_turbinas.append(turbina)  # 9
        turbina = {"Nome": "ROUHSN_13P8_UG11", "Grupo": "5_pas", }
        lista_turbinas.append(turbina)  # 10
        turbina = {"Nome": "ROUHSN_13P8_UG12", "Grupo": "5_pas", }
        lista_turbinas.append(turbina)  # 11
        turbina = {"Nome": "ROUHSN_13P8_UG13", "Grupo": "4_pas", }
        lista_turbinas.append(turbina)  # 12
        turbina = {"Nome": "ROUHSN_13P8_UG14", "Grupo": "4_pas", }
        lista_turbinas.append(turbina)  # 13
        turbina = {"Nome": "ROUHSN_13P8_UG15", "Grupo": "4_pas", }
        lista_turbinas.append(turbina)  # 14
        turbina = {"Nome": "ROUHSN_13P8_UG16", "Grupo": "4_pas", }
        lista_turbinas.append(turbina)  # 15
        turbina = {"Nome": "ROUHSN_13P8_UG17", "Grupo": "4_pas", }
        lista_turbinas.append(turbina)  # 16
        turbina = {"Nome": "ROUHSN_13P8_UG18", "Grupo": "4_pas", }
        lista_turbinas.append(turbina)  # 17
        turbina = {"Nome": "ROUHSN_13P8_UG19", "Grupo": "4_pas", }
        lista_turbinas.append(turbina)  # 18
        turbina = {"Nome": "ROUHSN_13P8_UG20", "Grupo": "4_pas", }
        lista_turbinas.append(turbina)  # 19
        turbina = {"Nome": "ROUHSN_13P8_UG21", "Grupo": "5_pas", }
        lista_turbinas.append(turbina)  # 20
        turbina = {"Nome": "ROUHSN_13P8_UG22", "Grupo": "5_pas", }
        lista_turbinas.append(turbina)  # 21
        turbina = {"Nome": "ROUHSN_13P8_UG23", "Grupo": "4_pas", }
        lista_turbinas.append(turbina)  # 21
        turbina = {"Nome": "ROUHSN_13P8_UG24", "Grupo": "4_pas", }
        lista_turbinas.append(turbina)  # 23
        turbina = {"Nome": "ROUHSN_13P8_UG25", "Grupo": "4_pas", }
        lista_turbinas.append(turbina)  # 24
        turbina = {"Nome": "ROUHSN_13P8_UG26", "Grupo": "4_pas", }
        lista_turbinas.append(turbina)  # 25
        turbina = {"Nome": "ROUHSN_13P8_UG27", "Grupo": "4_pas", }
        lista_turbinas.append(turbina)  # 26
        turbina = {"Nome": "ROUHSN_13P8_UG28", "Grupo": "4_pas", }
        lista_turbinas.append(turbina)  # 27
        turbina = {"Nome": "ROUHSN_13P8_UG29", "Grupo": "4_pas", }
        lista_turbinas.append(turbina)  # 28
        turbina = {"Nome": "ROUHSN_13P8_UG30", "Grupo": "4_pas", }
        lista_turbinas.append(turbina)  # 29
        turbina = {"Nome": "ROUHSN_13P8_UG31", "Grupo": "5_pas", }
        lista_turbinas.append(turbina)  # 30
        turbina = {"Nome": "ROUHSN_13P8_UG32", "Grupo": "5_pas", }
        lista_turbinas.append(turbina)  # 31
        turbina = {"Nome": "ROUHSN_13P8_UG33", "Grupo": "5_pas", }
        lista_turbinas.append(turbina)  # 32
        turbina = {"Nome": "ROUHSN_13P8_UG34", "Grupo": "5_pas", }
        lista_turbinas.append(turbina)  # 33
        turbina = {"Nome": "ROUHSN_13P8_UG35", "Grupo": "5_pas", }
        lista_turbinas.append(turbina)  # 34
        turbina = {"Nome": "ROUHSN_13P8_UG36", "Grupo": "5_pas", }
        lista_turbinas.append(turbina)  # 35
        turbina = {"Nome": "ROUHSN_13P8_UG37", "Grupo": "4_pas", }
        lista_turbinas.append(turbina)  # 36
        turbina = {"Nome": "ROUHSN_13P8_UG38", "Grupo": "4_pas", }
        lista_turbinas.append(turbina)  # 37
        turbina = {"Nome": "ROUHSN_13P8_UG39", "Grupo": "4_pas", }
        lista_turbinas.append(turbina)  # 38
        turbina = {"Nome": "ROUHSN_13P8_UG40", "Grupo": "4_pas", }
        lista_turbinas.append(turbina)  # 39
        turbina = {"Nome": "ROUHSN_13P8_UG41", "Grupo": "4_pas", }
        lista_turbinas.append(turbina)  # 40
        turbina = {"Nome": "ROUHSN_13P8_UG42", "Grupo": "4_pas", }
        lista_turbinas.append(turbina)  # 41
        turbina = {"Nome": "ROUHSN_13P8_UG43", "Grupo": "4_pas", }
        lista_turbinas.append(turbina)  # 42
        turbina = {"Nome": "ROUHSN_13P8_UG44", "Grupo": "4_pas", }
        lista_turbinas.append(turbina)  # 43
        turbina = {"Nome": "ROUHSN_13P8_UG45", "Grupo": "5_pas", }
        lista_turbinas.append(turbina)  # 44
        turbina = {"Nome": "ROUHSN_13P8_UG46", "Grupo": "5_pas", }
        lista_turbinas.append(turbina)  # 45
        turbina = {"Nome": "ROUHSN_13P8_UG47", "Grupo": "5_pas", }
        lista_turbinas.append(turbina)  # 46
        turbina = {"Nome": "ROUHSN_13P8_UG48", "Grupo": "5_pas", }
        lista_turbinas.append(turbina)  # 47
        turbina = {"Nome": "ROUHSN_13P8_UG49", "Grupo": "5_pas", }
        lista_turbinas.append(turbina)  # 48
        turbina = {"Nome": "ROUHSN_13P8_UG50", "Grupo": "5_pas", }
        lista_turbinas.append(turbina)  # 49

        self.lista_turbinas = lista_turbinas

    def ler_vaz_afl(self, path, year_array):

        df = pd.read_excel(path, sheet_name='VazaoDados')

        mapa = {'Ano': '1967',
                'Vazao PVH': 'Dia/Mes',
                'Unnamed: 55': 'Media'}

        ano_ini = 1968
        ano_fim = 2019
        nanos = ano_fim - ano_ini + 1

        for k in range(nanos):
            ano = 1968 + k
            txt = 'Unnamed: %i' % (k + 2)
            mapa[txt] = ano

        df = df.rename(columns=mapa)
        df = df.drop(columns=["Unnamed: 54", "Unnamed: 56", "Unnamed: 57",
                              "Unnamed: 58", "Unnamed: 59", "Unnamed: 60", "1967"], axis=1)

        for k in np.arange(366):
            a = df['Dia/Mes'][k + 1]
            df.loc[k + 1, 'Dia/Mes'] = str(a.day) + "/" + str(a.month)

        df = df.drop(labels=[0, 60, 367])  # Remove primeira linha e linha final
        df = df.interpolate()  # Interpolação

        self.vaz_hist = df
        vaz_afl = []
        vaz_afl_yearly = df['Media'].values
        for day in year_array:
            current_vaz = vaz_afl_yearly[day]
            vaz_afl.append(current_vaz)

        self.vaz_afl = vaz_afl

    def ler_dr_man(self, path):
        Num_Turbinas = 50
        df = pd.read_excel(path, sheet_name='DM')
        n_max = 0  # max number of maintenance
        for ug in range(Num_Turbinas):
            UG = ug + 1
            if UG < 10:
                txt = 'ROUHSN_13P8_UG0' + str(UG)
            else:
                txt = 'ROUHSN_13P8_UG' + str(UG)

            df_ug = df.loc[df['UG'] == txt]
            n = len(df_ug)
            if n > n_max:
                n_max = n

        DM = np.zeros(shape=(50, n_max))
        for ug in range(50):
            UG = ug + 1
            if UG < 10:
                txt = 'ROUHSN_13P8_UG0' + str(UG)
            else:
                txt = 'ROUHSN_13P8_UG' + str(UG)

            df_ug = df.loc[df['UG'] == txt]
            N = len(df_ug)
            dm = df_ug['DURACAO (DIAS)'].values
            NaNs = np.isnan(dm)
            dm[NaNs] = 0

            for n in range(N):
                DM[ug, n] = dm[n]

        duracao_manutencao = DM
        a = np.sort(duracao_manutencao)

        dm_sort = np.zeros(shape=(50, n_max))

        for im in range(n_max):
            for it in range(50):
                dm_sort[it, im] = int(a[it, n_max - im - 1])

        self.dr_man = dm_sort

    @staticmethod
    def build_rfo_pdf(path_pdf):
        path_samug = path_pdf

        df = pd.read_excel(path_samug, sheet_name='RFO + DFO')

        mapa = {'Equipamento': 'UG',
                'Data Inicio Verificada': 'Data_Ini',
                'Data Fim Corrigida': 'Data_Fim'}

        df = df.rename(columns=mapa)

        # Ajustes no DataFrame

        Num_Turbinas = 50
        Num_Mes = 12
        Num_Even = len(df['UG'])

        retira = []
        continua = []
        anos = [2017, 2018, 2019, 2020]

        for i in range(Num_Even):
            ano = int(df['Data_Ini'][i].year)
            if ano in anos:
                continua.append(i)
            else:
                retira.append(i)

        df = df.drop(labels=retira)

        datas = []
        datas_df = pd.DatetimeIndex(df['Data_Ini'].values)

        for n in range(len(datas_df)):
            datas.append(datas_df[n].month)

        df['Mes'] = datas

        # Seleciona Dias de Ocorrência de RFO + DFO #

        dados_gerais = []

        for t in range(Num_Turbinas):
            dados = {}
            Turbina = t + 1
            if t < 9:
                txt = 'ROUHSN_13P8_UG0' + str(Turbina)
            else:
                txt = 'ROUHSN_13P8_UG' + str(Turbina)

            df_tur = df.loc[df['UG'] == txt]
            N = len(df_tur)
            for m in range(Num_Mes):
                dados_m = []
                mes = m + 1
                df_tur_mes = df_tur.loc[df_tur['Mes'] == mes]
                N = len(df_tur_mes)
                d_ini = pd.DatetimeIndex(df_tur_mes['Data_Ini'])
                d_fim = pd.DatetimeIndex(df_tur_mes['Data_Fim'])
                for n in range(N):
                    d_i = d_ini[n].day
                    d_f = d_fim[n].day

                    if d_i == d_f:
                        dados_m.append(d_i)
                    else:
                        d_i = d_ini[n].day
                        d_f = d_fim[n].day
                        dias = np.arange(d_i, d_f + 1, 1)
                        dados_m.extend(dias)

                dados[m] = dados_m

                dados_m.append(99999)
                list_aux = []
                for i in range(len(dados_m) - 1):
                    if dados_m[i] != dados_m[i + 1]:
                        list_aux.append(int(dados_m[i]))
                dados[m] = list_aux

            dados_gerais.append(dados)

        return dados_gerais

    def ler_rfo_pdf(self, path_rfo, path_pdf, year_array):

        rfo_pdf = self.build_rfo_pdf(path_pdf)
        self.rfo_pdf = rfo_pdf
        planilha = path_rfo
        dias_RFO = pd.read_excel(planilha, sheet_name="MANUT. FORÇADA - 2017 À 2020")
        self.rfo_mes = dias_RFO

        fim_dias_mes = [31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]
        num_dias_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        Num_Turbinas = 50
        Num_Meses = 12

        matriz_ano = np.zeros(shape=(Num_Turbinas, sum(num_dias_mes)))
        for tb in range(Num_Turbinas):
            for mes in range(Num_Meses):
                D = np.asarray(rfo_pdf[tb][mes])
                N = len(D)
                sorteios_mes = []
                mu, sigma = dias_RFO[mes][tb], dias_RFO[mes][tb] * 0.0
                s = np.random.normal(mu, sigma, 1)
                aux_RFO = abs(int(s))
                if mes == 0:
                    aux = int(dias_RFO[mes][tb])
                    if N > 0:
                        for i in range(aux_RFO):
                            num_sorteado = random.randrange(0, N)
                            dia_sorteado = D[num_sorteado]
                            sorteios_mes.append(dia_sorteado)
                            matriz_ano[tb, dia_sorteado] = 1
                else:
                    aux = int(dias_RFO[mes][tb])
                    if N > 0:
                        for i in range(aux_RFO):
                            num_sorteado = random.randrange(0, N)
                            dia_sorteado = D[num_sorteado]
                            sorteios_mes.append(dia_sorteado)
                            dia_mes = dia_sorteado + fim_dias_mes[mes - 1] - 1
                            matriz_ano[tb, dia_mes] = 1

        final_matrix_ano = np.zeros(shape=(Num_Turbinas, len(year_array)))
        for d, day in enumerate(year_array):
            final_matrix_ano[:, d] = matriz_ano[:, day]

        self.rfo_dia = final_matrix_ano

    def ler_manut_def_array(self, Agenda_def):
        self.manut_def = Agenda_def

    def parameters_plot(self, vt_UG):

        # Vazão Afluente e Vazão Máxima #
        plt.figure()
        x = np.arange(1, 365 + 1, 1)
        x_plot = np.arange(15, 365, 30)
        txt = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        plt.plot(x, self.vaz_afl, linewidth=3)
        plt.xlabel('Meses', fontsize=14)
        plt.ylabel('Vazão Afluente [$m^3/s$]', fontsize=14)
        plt.xticks(x_plot, txt, fontsize=12)
        plt.yticks(fontsize=12)
        plt.show()

        plt.figure()
        plt.plot(x, vt_UG[0], label='4 Pás')
        plt.plot(x, vt_UG[24], label='5 Pás')
        plt.xticks(x_plot, fontsize=12)
        plt.yticks(fontsize=12)
        plt.xlabel('Dias', fontsize=14)
        plt.ylabel('Vazão Turbinada Máxima [$m^3/s$]', fontsize=14)
        plt.legend()
        plt.show()


class Volume_Turbinado(object):

    def __init__(self, vazao, lista_turbinas):

        self.vt_max = None
        self.vt_individual(vazao, lista_turbinas)

    def vt_individual(self, vaz_afl, lista_turbinas):
        Num_Dias = 365
        vt_individual_max = []
        for t, valor in enumerate(lista_turbinas):
            lista_aux_vaz = []
            if valor["Grupo"] == "4_pas":
                for d in range(Num_Dias):
                    lista_aux_vaz.append(
                        int(self.vaz_max_ug(4, vaz_afl[d], self.queda_bruta(vaz_afl[d])))
                        if self.vaz_max_ug(4, vaz_afl[d], self.queda_bruta(vaz_afl[d])) > 0 else 0)
            if valor["Grupo"] == "5_pas":
                for d in range(Num_Dias):
                    lista_aux_vaz.append(int(self.vaz_max_ug(5, vaz_afl[d], self.queda_bruta(vaz_afl[d]))))
            vt_individual_max.append(lista_aux_vaz)

        self.vt_max = vt_individual_max

    def poli(self, indice, x):
        elem = len(indice)
        y = 0
        for ii in range(0, elem):
            y += indice[ii] * (x ** ii)
        return y

    def n_jus(self, vazao):
        indice = [[44.00162, 0.0006307992, -0.00000000376748, -8.808463 * 10 ** -14, 1.013894 * 10 ** -18],
                  [51.6258, 0.0002688642, -0.000000001945816, 8.526341 * 10 ** -15, -1.562465 * 10 ** -20]]
        return self.poli(indice[0], vazao) if vazao <= 61560.5 else self.poli(indice[1], vazao)

    def n_mon(self, vazao):
        if vazao < 36000:
            mon = 71.30
        elif vazao < 38500:
            mon = 71.30 + (vazao - 36000) * (70.50 - 71.30) / (38500 - 36000)
        elif vazao < 47000:
            mon = 70.50
        elif vazao < 54000:
            mon = 70.5 + (vazao - 47000) * (68.50 - 70.50) / (54000 - 47000)
        else:
            mon = 68.5
        return self.n_jus(vazao) if self.n_jus(vazao) > mon else mon

    def queda_bruta(self, vazao):
        qb = self.n_mon(vazao) - self.n_jus(vazao)
        return round(qb, 3)

    def v_turb(self, turb, queda_b, ger):
        g_1 = []
        g_2 = []
        if turb == 5:
            pot = [20, 40, 60, 75.55, 80, 100]
            indice = [[1542.1068502734, -363.168666397843, 43.8877985376981, -3.01694006908378,
                       0.119796859361409 - 2.56895854388342 * 10 ** -3, 2.30898328016118 * 10 ** -5],
                      [4815.83005888612, -1274.65999242747, 156.945430870228, -10.5483338523214, 0.399467336279488,
                       -8.01705485760964 * 10 ** -3, 6.63874869426332 * 10 ** -5],
                      [5404.59016564035, -1195.27116201434, 126.620708775267, -7.46925397809458, 0.252092738757319,
                       -4.56405994865629 * 10 ** -3, 3.44280095893734 * 10 ** -5],
                      [4549.58355790069, -724.875702518667, 50.9501283794821, -1.54049618733722,
                       1.90152611909298 * 10 ** -3, 9.16523445703766 * 10 ** -4, -1.46173765679596 * 10 ** -5],
                      [13548.8358999023, -3422.90282415623, 388.215314752655, -23.9169925089663, 0.832011244028366,
                       -1.54063084579256 * 10 ** -2, 1.1831173356133 * 10 ** -4],
                      [35494.6581071653, -9079.70966758283, 999.035249434716, -58.9857114050143, 1.95900442299092,
                       -0.034619368852737, 2.54062271784836 * 10 ** -4]]
        else:
            pot = [20, 30, 40, 50, 60, 70, 75.55]
            indice = [[-68391.5287073856, 38431.8719424059, -8896.96858105448, 1092.57285917684, -75.1659492051471,
                       2.74835841936084, -4.17385453330366 * 10 ** -2],
                      [1986.36775975162, -358.996197502942, 21.6523931917652, 0.737003079693346, -0.155171915406742,
                       7.06303255783142 * 10 ** -3, -1.08811747320316 * 10 ** -4],
                      [12106.5630375655, -4280.88772401832, 661.047984415047, -54.6877405437234, 2.53172807467736,
                       -6.19710145261558 * 10 ** -2, 6.25831558310555 * 10 ** -4],
                      [12873.7403582906, -4101.77457654, 574.12051984435, -43.216425184913, 1.82604156203266,
                       -4.09058816407132 * 10 ** -2, 3.78980180968533 * 10 ** -4],
                      [7455.86131566893, -1666.34276281295, 157.711117068013, -7.01665412505839, 0.113792054402741,
                       1.19316278786076 * 10 ** -3, -4.33857790091163 * 10 ** -5],
                      [34669.8566353205, -11232.1744856617, 1567.45153876544, -117.783324026687, 4.99465177211563,
                       -0.112986926687405, 1.06335625109526 * 10 ** -3],
                      [122054.791844751, -40889.0930169186, 5746.47394888225, -430.434202220977, 18.0885047039821,
                       -0.404006920172422, 3.74504708434931 * 10 ** -3]]
        j = len(indice)
        l = len(pot) - 1
        for i in range(0, j):
            g_1.append(self.poli(indice[i], queda_b))
        for i in range(0, l):
            g_2.append((g_1[i + 1] - g_1[i]) / (pot[i + 1] - pot[i]))
        if ger < pot[0]:
            return g_1[0] + g_2[0] * (ger - pot[0])
        elif ger > pot[l]:
            return 0
        else:
            x = 0
            while ger > pot[x]:
                x += 1
            return g_1[x] if ger == pot[x] else g_1[x - 1] + g_2[x - 1] * (ger - pot[x - 1])

    @staticmethod
    def p_carga(vazao):
        return 0.00000028664 * vazao ** 2 + 0.00000063375 * vazao ** 2

    def p_e_max(self, turb, queda_l):
        if turb == 5:
            indice = [[8509.94503415321, -4642.59302425164, 1046.23601140887, -124.499349432213, 8.26448435245188,
                       -0.290315086950096, 4.21989717071968 * 10 ** -3],
                      [35494.6581071653, -9079.70966758283, 999.035249434716, -58.9857114050143, 1.95900442299092,
                       -0.034619368852737, 2.54062271784836 * 10 ** -4]]
            if queda_l < 8.8:
                aux = 0
            elif queda_l < 15.52:
                aux = self.poli(indice[0], queda_l)
            elif queda_l < 28:
                aux = self.poli(indice[1], queda_l)
            else:
                aux = 0
        else:
            indice = [[-23188.0314624648, 7923.86045536461, -765.736964295095, -10.2072788716934, 4.45108187570693,
                       -8.93564135240482 * 10 ** -2, -4.79253408319384 * 10 ** -3],
                      [123510.594671818, -62635.7535259461, 13195.9680627112, -1478.13480444296, 92.8627206993978,
                       -3.10261045319629, 0.043070692445689],
                      [-16377.004905732, 3715.49597870386, -183.507597935879, -18.7801452395411, 2.51293787024037,
                       -0.104175349143223, 1.51762645364382 * 10 ** -3]]
            if queda_l < 8.8:
                aux = 0
            elif queda_l < 9.881:
                aux = self.poli(indice[0], queda_l)
            elif queda_l < 13.951:
                aux = self.poli(indice[1], queda_l)
            elif queda_l < 16.48:
                aux = self.poli(indice[2], queda_l)
            elif queda_l < 22:
                aux = 75.55
            else:
                aux = 0
        return 75.55 if aux > 75.55 else aux

    def p_eixo_max(self, turb, queda_b):
        delta = 0.3
        intera = 0
        while abs(self.p_carga(self.v_turb(turb, queda_b - delta,
                                           self.p_e_max(turb, queda_b - delta))) - delta) > 0.00001 \
                and queda_b - delta >= 8.8 and intera < 10000:
            delta = self.p_carga(self.v_turb(turb, queda_b - delta, self.p_e_max(turb, queda_b - delta)))
            intera += 1
        return self.p_e_max(turb, queda_b - delta)

    def vaz_max_ug(self, turb, vazao, queda_bruta):
        potencia_max_UG = self.p_e_max(turb, queda_bruta)
        vt_individual_max = self.v_turb(turb, queda_bruta, potencia_max_UG)
        return vt_individual_max