from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np

mpl.rcParams["legend.loc"] = 'upper right'
mpl.rcParams['figure.figsize'] = (10, 6)
mpl.rcParams['font.size'] = 14

class plota_Agenda(object):

    def __init__(self, VT, VV, VAZ_AFL, Operacao, Agenda, Agenda_rfo, vert_turb, ug_op_man, vert_n_turb, calendario):
        Num_Dias = 365
        Num_Turbinas = 50

        x_plot = np.arange(0, Num_Dias + 1, 30)
        x_plot[0] = 1

        x = np.arange(1, Num_Dias + 1)

        if vert_turb:
            Y0 = np.zeros(Num_Dias)
            Y1 = np.array(VT, dtype=float)
            Y2 = np.array(VAZ_AFL, dtype=float)

            plt.figure()
            x = np.arange(1, Num_Dias + 1)
            plt.plot(x, Y2, 'darkblue', linewidth=1, label='Vazão Afluente')
            plt.fill_between(x, Y0, Y1, label='Vazão Turbinada', color='palegreen')
            plt.fill_between(x, Y1, Y2, label='Vazão Vertida', color='orange')
            plt.xticks(x_plot, fontsize=12)
            plt.yticks(fontsize=12)
            plt.xlabel('Dias', fontsize=12)
            plt.ylabel('Vazão [$m^3/s$]', fontsize=12)
            plt.title('Vazão Diária: Turbinada e Vertida')
            plt.legend()
            plt.show()

        if ug_op_man:
            n_oper = []
            n_foper = []
            n_rfo = []
            n_rfo_plot = []
            n_manut = []
            n_manut_plot = []
            x = np.arange(1, Num_Dias + 1)

            for t in range(Num_Dias):
                no = sum(Operacao[:, t])  # Operação
                nr = sum(Agenda_rfo[:, t])  # RFO
                nm = sum(Agenda[:, t])  # Manutenção

                if int(no + nr + nm) > 50:
                    diff = int(no + nr + nm) - 50
                    nr = nr - diff

                nf = Num_Turbinas - no - nr - nm  # Fora de Operação

                npp = no + nm  # Manutenção para Plot Fill Between
                nrr = npp + nr  # RFO para Plot Fill Between

                n_oper.append(no)
                n_rfo.append(nr)
                n_foper.append(nf)
                n_manut.append(nm)

                n_rfo_plot.append(nrr)
                n_manut_plot.append(npp)

            Y0 = np.zeros(Num_Dias)
            Y1 = n_oper
            Y2 = n_manut_plot
            Y3 = n_rfo_plot
            Y4 = np.ones(Num_Dias) * Num_Turbinas

            plt.figure()
            plt.plot(x, Y4, 'k', linewidth=1.5)

            plt.fill_between(x, Y0, Y1, label='Ativas', color='palegreen')
            plt.fill_between(x, Y1, Y2, label='Manutenção', color='orange')
            plt.fill_between(x, Y2, Y3, label='RFO', color='red')
            plt.fill_between(x, Y3, Y4, label='Inativas', color='royalblue')
            plt.xticks(x_plot, fontsize=12)
            plt.yticks(fontsize=12)
            plt.xlabel('Dias', fontsize=14)
            plt.ylabel('Número de Unidades Geradoras', fontsize=14)
            plt.title('Estado Operativo das UGs')
            plt.legend()
            plt.show()

            plt.figure()
            plt.bar(x, n_manut)
            plt.xticks(x_plot, fontsize=12)
            plt.yticks(fontsize=12)
            plt.xlabel('Dias', fontsize=14)
            plt.ylabel('Número de Unidades Geradoras', fontsize=14)
            plt.title('Número de Unidades Geradoras em Manutenção')
            plt.show()

        if vert_n_turb:
            fig, ax1 = plt.subplots()

            color = 'red'
            ax1.set_xlabel('Dias', fontsize=14)
            ax1.set_ylabel('Vazão Vertida [$m^3/s$]', color=color, fontsize=14)
            ax1.plot(x, VV, color=color)
            ax1.tick_params(axis='y', labelcolor=color)

            ax2 = ax1.twinx()
            n_oper = []
            for t in range(Num_Dias):
                no = sum(Operacao[:, t])  # Operação
                n_oper.append(no)

            color = 'tab:blue'
            ax2.set_ylabel('Número de Unidades Geradoras', color=color, fontsize=14)
            ax2.plot(x, n_oper, color=color)
            ax2.tick_params(axis='y', labelcolor=color)
            fig.tight_layout()
            plt.xticks(x_plot, fontsize=12)
            plt.yticks(fontsize=12)
            plt.show()

        if calendario:
            plt.figure()
            for tb in range(Num_Turbinas):
                for d in range(Num_Dias):
                    p = Agenda[tb, d] * d
                    if p > 0:
                        plt.plot(p, tb, '.', color='blue')

            plt.xlabel('Dias')
            plt.ylabel('Unidade Geradora')
            plt.grid(True)
            plt.show()





