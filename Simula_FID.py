import numpy as np

class Calculo_Indicadores(object):

    def __init__(self, Agenda, Dados_UHE, Dados_VT):
        Num_Dias = 365
        self.HDF = None
        self.HDP = None
        self.HDF_mes = np.zeros(Num_Dias)
        self.HDP_mes = np.zeros(Num_Dias)
        self.HDF_acum = np.zeros(Num_Dias)
        self.HDP_acum = np.zeros(Num_Dias)

        self.Calc_Indic_Mes(Agenda.Agenda, Dados_UHE.rfo_dia, Dados_VT.vt_max, Dados_UHE.vaz_afl, Agenda.Turbinado, Num_Dias)

    def Calc_Indic_Mes(self, agenda_ofi, agenda_rfo, vt_UG, VAZ_AFL, VT, Num_Dias):

        # Calcula vertimento que pode ser penalizado
        Num_Turbinas = 50
        VV_pen = []  # Vertimento passível de penalização
        vt_max = np.asarray(vt_UG)

        for t in range(Num_Dias):
            vt_max_d = np.sum(vt_max[:, t])
            if vt_max_d > VAZ_AFL[t]:
                a = VAZ_AFL[t] - VT[t]
                VV_pen.append(a)
            else:  # Vazão maior que limite, penaliza só ate o limite da UHE
                a = vt_max_d - VT[t]
                VV_pen.append(a)

        # Calcula número de horas indisponíveis

        HDF = np.zeros(Num_Dias)
        HDP = np.zeros(Num_Dias)

        vt_rfo = np.zeros(Num_Dias)
        vt_man = np.zeros(Num_Dias)

        for t in range(Num_Dias):
            for tb in range(Num_Turbinas):
                vt_rfo[t] += agenda_rfo[tb, t] * vt_max[tb, t]  # Volume turbinado perdido por RFO
                vt_man[t] += agenda_ofi[tb, t] * vt_max[tb, t]  # Volume turbinado perdido por MANUTENÇÃO

        for t in range(Num_Dias):
            if vt_rfo[t] - VV_pen[t] >= 0:  # Vertimento vira HDF
                nt = VV_pen[t] / vt_max[49, t]
                HDF[t] = nt * 24

            if vt_rfo[t] - VV_pen[t] < 0:  # Vertimento vira HDF e HDP

                n = VV_pen[t] / vt_max[49, t]  # Número total de turbinas
                nt = vt_rfo[t] / vt_max[49, t]  # Número máximo para HDF
                nr = n - nt  # Resto das Turbinas vai para HDP

                HDF[t] = nt * 24
                HDP[t] = nr * 24

        self.HDF = HDF
        self.HDP = HDP

        # Agrupa mensalmente HDF e HDP

        HDF_mes = np.zeros(12)
        HDP_mes = np.zeros(12)

        num_dias_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        k = 0

        for imes in range(12):
            HDF_mes[imes] = np.sum(HDF[0 + k:num_dias_mes[imes] + k])
            HDP_mes[imes] = np.sum(HDP[0 + k:num_dias_mes[imes] + k])
            k += num_dias_mes[imes]

        self.HDF_mes = HDF_mes
        self.HDP_mes = HDP_mes

