import pyomo.environ as pyo
import numpy as np
import timeit
import pandas as pd
import random


class Otimizacao(object):

    def __init__(self, Dados_UHE, Dados_VT):

        self.Operacao = None
        self.Agenda = None
        self.Vertido = None
        self.Turbinado = None

        self.n_rodadas = None

        self.multi_rodadas(Dados_UHE.vaz_afl, Dados_UHE.dr_man, Dados_UHE.rfo_dia, Dados_VT.vt_max)

    def multi_rodadas(self, v_afl, duracao_manutencao, matriz_ano, vt_UG):
        Num_Dias = 365
        Num_Turbinas = 50

        self.n_rodadas = duracao_manutencao.shape[1]
        self.n_rodadas = 1
        N_Rodadas = self.n_rodadas

        agenda_ofi = np.zeros(shape=(Num_Turbinas, Num_Dias))
        agenda_rfo = matriz_ano

        for rodada in range(N_Rodadas):
            start = timeit.default_timer()
            agenda_aux = np.zeros(shape=(Num_Turbinas, Num_Dias))
            agenda_rfo_aux = np.zeros(shape=(Num_Turbinas, Num_Dias))

            DM = duracao_manutencao[:, rodada]

            for tb in range(Num_Turbinas):
                dm = int(DM[tb])
                for t in range(Num_Dias):
                    if agenda_ofi[tb, t] == 1:
                        agenda_aux[tb, t - dm:t] = 1

            for tb in range(Num_Turbinas):
                dm = int(DM[tb])
                for t in range(Num_Dias):
                    if agenda_rfo[tb, t] == 1:
                        if t - dm > 0:
                            agenda_rfo_aux[tb, t - dm:t + 1] = 1
                        else:
                            dm2 = t
                            agenda_rfo_aux[tb, t - dm2:t + 1] = 1

            problema = self.main_otm(DM, vt_UG, v_afl, agenda_aux, agenda_ofi, agenda_rfo_aux, agenda_rfo)

            Solver = pyo.SolverFactory('gurobi', solver_io='python')
            Solver.options['tol'] = 0.1
            Solver.solve(problema)

            for tb in range(Num_Turbinas):
                dm = int(DM[tb])
                for t in range(Num_Dias):
                    if problema.y[tb, t]() == 1:
                        agenda_aux[tb, t:t + dm] = 1
                        agenda_ofi[tb, t:t + dm] = 1

            stop = timeit.default_timer()
            time = stop - start
            print("-> Round %1.0i Completed, Time: %4.2f" % ((rodada + 1), time))

        Agenda = agenda_ofi
        Operacao = np.zeros(shape=(Num_Turbinas, Num_Dias))
        Vertido = np.zeros(Num_Dias)

        for tb in range(Num_Turbinas):
            for t in range(Num_Dias):
                Operacao[tb, t] = problema.x[tb, t]()

        where_are_NaNs = np.isnan(Operacao)
        Operacao[where_are_NaNs] = 0

        where_are_NaNs = np.isnan(Agenda)
        Agenda[where_are_NaNs] = 0

        for t in range(Num_Dias):
            Vertido[t] = problema.vv[t]()

        # Monta lista com valores

        VV = []
        VT = []
        VAZ_AFL = []

        for t in range(Num_Dias):
            VV.append(problema.vv[t]())
            VAZ_AFL.append(v_afl[t])

        for t in range(Num_Dias):
            aux = 0
            for tb in range(Num_Turbinas):
                aux += (Operacao[tb][t] * vt_UG[tb][t])
            VT.append(aux)

        A = Operacao + Agenda + agenda_rfo

        for t in range(Num_Dias):
            if VV[t] > 0:
                vt_aju = VV[t]
                for tb in range(Num_Turbinas):
                    if A[tb, t] == 0 and vt_UG[tb][t] > 0:
                        VV[t] = 0
                        Operacao[tb, t] = 1
                        A[tb, t] = 1
                        VT[t] = VT[t] + vt_aju
                        break

        self.Operacao = Operacao
        self.Agenda = Agenda
        self.Vertido = VV
        self.Turbinado = VT

    def main_otm(self, DM, vt_UG, v_afl, agenda_aux, agenda_ofi, agenda_rfo_aux, agenda_rfo):

        Num_Turbinas = 50
        Num_Dias = 365
        problema = pyo.ConcreteModel()

        TB = np.arange(Num_Turbinas)  # Turbina
        T = np.arange(Num_Dias)  # Tempo/Dia
        D = Num_Dias
        P = 1
        Y = []  # Intervalo de tempo usado na Restrição de Desjunção
        S = []  # Final do somatorio de 'x' na equacao com BigM
        W = []
        N = 0
        for tb in TB:
            M = DM[tb]  # 'M' recebe o valor da duração da manutenção provisoriamente
            Y.append(np.arange(D - M))
            S.append(np.arange(M))
            W.append(np.arange(M + N - 1))

        problema.x = pyo.Var(TB, T,
                             domain=pyo.Binary)  # Corresponde ao modo OPERATIVO da Turbina (x[t][d] = 1 -> operante)
        problema.y = pyo.Var(TB, T,
                             domain=pyo.Binary)  # Corresponde ao estágio de termpo em que a Turbina inicia a manutenção (y[t][d] = indica o primeiro dia de manutenção)
        problema.vv = pyo.Var(T, domain=pyo.NonNegativeReals)  # Volume Vertido da Usina

        # FUNÇÃO OBJETIVO
        problema.FOB = pyo.Objective(expr=sum(problema.vv[t] for t in T))

        # Restrição do número de manutenções realizada pela mesma Turbina
        problema.rest_P = pyo.ConstraintList()
        for tb in TB:
            problema.rest_P.add(expr=sum(problema.y[tb, t] for t in Y[tb]) == P)

        # Restrição de Turbinamento
        problema.turb = pyo.ConstraintList()
        for t in T:
            problema.turb.add(expr=sum(problema.x[tb, t] * vt_UG[tb][t] for tb in TB) + problema.vv[t] == v_afl[t])

        # Restrição de Disjunção - Duração Manutenção
        problema.disj = pyo.ConstraintList()
        NTD = Num_Turbinas
        for tb in range(NTD):
            M = DM[tb]
            for t in Y[tb]:
                problema.disj.add(expr=sum(problema.x[tb, t + s] for s in S[tb]) <= 9999 * (1 - problema.y[tb, t]))

        # Adiciona Valores Otimizados em Rodadas Anteriores
        problema.otim = pyo.ConstraintList()

        for tb in range(NTD):
            for t in range(D):
                t = int(t)
                if agenda_aux[tb, t] == 1:
                    problema.otim.add(expr=agenda_aux[tb, t] + problema.y[tb, t] == 1)
                if agenda_ofi[tb, t] == 1:
                    problema.otim.add(expr=agenda_ofi[tb, t] + problema.x[tb, t] == 1)

        problema.rfo = pyo.ConstraintList()

        for tb in range(NTD):
            for t in range(D):
                t = int(t)
                if agenda_rfo_aux[tb, t] == 1:
                    problema.rfo.add(expr=agenda_rfo_aux[tb, t] + problema.y[tb, t] == 1)
                if agenda_rfo[tb, t] == 1:
                    problema.rfo.add(expr=agenda_rfo[tb, t] + problema.x[tb, t] == 1)

        return problema


class Optimize_Operation(object):

    def __init__(self, Dados_UHE, Dados_VT, calendar, previous_calendar, n_days, n_ug):

        self.Operacao = None
        self.Agenda = None
        self.Vertido = None
        self.Turbinado = None
        self.full_operation = None
        self.flag_out = 0
        self.n_days = n_days
        self.n_ug = n_ug

        self.optimize(Dados_UHE, Dados_VT.vt_max, calendar=calendar, previous_calendar=previous_calendar)

    @staticmethod
    def update_rfo(Parametros_UHE, path_rfo):

        rfo_pdf = Parametros_UHE.rfo_pdf
        planilha = path_rfo
        dias_RFO = pd.read_excel(planilha, sheet_name="MANUT. FORÇADA - 2017 À 2020")

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
                mu, sigma = dias_RFO[mes][tb], dias_RFO[mes][tb] * 0.3
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

        Parametros_UHE.rfo_dia = matriz_ano

        return Parametros_UHE

    def optimize(self, Dados_UHE, vt_UG, calendar, previous_calendar):
        Num_Dias = self.n_days
        Num_Turbinas = self.n_ug

        v_afl = Dados_UHE.vaz_afl
        agenda_ofi = calendar
        agenda_rfo = Dados_UHE.rfo_dia
        agenda_prev = previous_calendar

        problema = self.main_otm(vt_UG, v_afl, agenda_ofi, agenda_rfo, agenda_prev)

        # Solver = pyo.SolverFactory('gurobi', solver_io='python')
        # Solver.options['tol'] = 0.1

        solver = 'cbc'
        Solver = pyo.SolverFactory(solver)

        Solver.solve(problema)

        if problema.vv[0]() is None:
            self.flag_out = 1

        if self.flag_out == 0:
            Agenda = agenda_ofi
            Operacao = np.zeros(shape=(Num_Turbinas, Num_Dias))
            Vertido = np.zeros(Num_Dias)

            for tb in range(Num_Turbinas):
                for t in range(Num_Dias):
                    Operacao[tb, t] = problema.x[tb, t]()

            where_are_NaNs = np.isnan(Operacao)
            Operacao[where_are_NaNs] = 0

            for t in range(Num_Dias):
                Vertido[t] = problema.vv[t]()

            # Monta lista com valores

            VV = []
            VT = []
            VAZ_AFL = []

            for t in range(Num_Dias):
                VV.append(problema.vv[t]())
                VAZ_AFL.append(v_afl[t])

            for t in range(Num_Dias):
                aux = 0
                for tb in range(Num_Turbinas):
                    aux += (Operacao[tb][t] * vt_UG[tb][t])
                VT.append(aux)

            A = Operacao + Agenda + agenda_rfo

            for t in range(Num_Dias):
                if VV[t] > 0:
                    vt_aju = VV[t]
                    for tb in range(Num_Turbinas):
                        if A[tb, t] == 0 and vt_UG[tb][t] > 0:
                            VV[t] = 0
                            Operacao[tb, t] = 1
                            A[tb, t] = 1
                            VT[t] = VT[t] + vt_aju
                            break
            self.full_operation = A
            self.Operacao = Operacao
            self.Agenda = Agenda
            self.Vertido = VV
            self.Turbinado = VT

    def main_otm(self, vt_UG, v_afl, agenda_def, agenda_rfo, agenda_prev):

        # T = Número de Dias
        # NT = Número de Turbinas

        problema = pyo.ConcreteModel()
        Num_Turbinas = self.n_ug
        Num_Dias = self.n_days
        TB = np.arange(Num_Turbinas)  # Turbina
        T = np.arange(Num_Dias)  # Tempo/Dia

        problema.x = pyo.Var(TB, T,
                             domain=pyo.Binary)  # Corresponde ao modo OPERATIVO da Turbina (x[t][d] = 1 -> operante)
        problema.vv = pyo.Var(T, domain=pyo.NonNegativeReals)  # Volume Vertido da Usina

        # FUNÇÃO OBJETIVO
        problema.FOB = pyo.Objective(expr=sum(problema.vv[t] for t in T))

        # Restrição de Turbinamento
        problema.turb = pyo.ConstraintList()
        for t in T:
            problema.turb.add(expr=sum(problema.x[tb, t] * vt_UG[tb][t] for tb in TB) + problema.vv[t] == v_afl[t])

        # Adiciona Limitação de Operação - Agenda do Bat Atual
        # Adiciona Limitação de Operação - RFO + DFO
        # Adiciona Limitação de Operação - Agenda dos Bats Passados

        problema.otim_ag = pyo.ConstraintList()
        problema.otim_prev = pyo.ConstraintList()
        problema.otim_rfo = pyo.ConstraintList()

        for tb in TB:
            for t in T:
                t = int(t)
                if int(agenda_def[tb, t]) == 1:
                    problema.otim_ag.add(expr=int(agenda_def[tb, t]) + problema.x[tb, t] == 1)

                if agenda_prev[tb, t] == 1:
                    problema.otim_prev.add(expr=agenda_prev[tb, t] + problema.x[tb, t] == 1)

                if agenda_rfo[tb, t] == 1:
                    problema.otim_rfo.add(expr=agenda_rfo[tb, t] + problema.x[tb, t] == 1)

        return problema