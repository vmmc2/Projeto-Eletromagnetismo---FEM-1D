import numpy as np 
import matplotlib.pyplot as plt

PERMISSIVIDADE_DO_VACUO = 8.8541878176 * (10**(-12))
K = [[1.0, -1.0],[-1.0, 1.0]]

def plot_graphic_V_vs_d(V_values, d_values, d_fronteira, d_total):
    plt.plot(d_values, V_values, color="black", marker="o", markersize=3)
    plt.axvspan(0.0, d_fronteira, facecolor="#FFC001")
    plt.axvspan(d_fronteira, d_total, facecolor="#FBE7C6")
    plt.xlabel('Distância - d (m)')
    plt.ylabel('Potencial Eletrostático - V (V)')
    plt.title('Gráfico V x d')
    plt.show()
    return

def calculate_approximate_charge(V_values, L, e2, l2):
    delV = (V_values[-1] - V_values[-2])
    Q = e2 * (delV/l2) * (L*L)
    return Q

def main():
    L = float(input("A medida do lado das placas do capacitor: (cm)\n"))
    v0 = float(input("Potencial eletrostatico da placa superior: (V)\n"))
    er1 = float(input("Constante dieletrica do dieletrico 1:\n"))
    er2 = float(input("Constante dieletrica do dieletrico 2:\n"))
    n1, n2 = map(float, input("Qtd de elementos finitos no meio 1 e no meio 2:\n").split())
    d1, d2 = map(float, input("Comprimento dos dieletricos 1 e 2: (mm)\n").split())
    
    # Deixando as unidades de medidas em metros (m)
    L = L/100
    d1 = d1/1000
    d2 = d2/1000

    d = d1 + d2
    n = n1 + n2 
    e1 = er1 * PERMISSIVIDADE_DO_VACUO
    e2 = er2 * PERMISSIVIDADE_DO_VACUO 
    l1 = d1/n1 # Comprimento do Elemento Finito no dieletrico 1
    l2 = d2/n2 # Comprimento do Elemento Finito no dieletrico 2

    # Criacao da Matriz de Coeficientes Global e do Vetor Global d
    numero_nos = int(n1 + n2 + 1)
    matriz_global = [[0 for j in range(0, numero_nos)] for i in range(0, numero_nos)]
    vetor_global_d = [0 for i in range(0, numero_nos)]

    # Matriz de Coeficientes do Elemento no dieletrico 1
    K1 = [[0, 0],[0, 0]]
    for i in range(0 , 2):
        for j in range(0, 2):
            K1[i][j] = (e1/l1) * K[i][j]
    # Matriz de Coeficientes do Elemento no dieletrico 2
    K2 = [[0, 0],[0, 0]]
    for i in range(0, 2):
        for j in range(0, 2):
            K2[i][j] = (e2/l2) * K[i][j]

    # Montagem da Matriz de Coeficientes Global
    i = 0
    contador_dieletrico1 = 0
    limite_dieletrico1 = n1
    while i <= (numero_nos - 2):
        if contador_dieletrico1 < limite_dieletrico1: # Usar o K1 para preencher a matriz global
            matriz_global[i][i] += K1[0][0]
            matriz_global[i + 1][i] += K1[1][0]
            matriz_global[i][i + 1] += K1[0][1]
            matriz_global[i + 1][i + 1] += K1[1][1]
            i += 1
            contador_dieletrico1 += 1
        else: # Usar o K2 para preencher a matriz global
            matriz_global[i][i] += K2[0][0]
            matriz_global[i + 1][i] += K2[1][0]
            matriz_global[i][i + 1] += K2[0][1]
            matriz_global[i + 1][i + 1] += K2[1][1]
            i += 1

    # Aplicando as condicoes de Dirichlet: Para reduzir a ordem da matriz global
    # v1 = 0
    # v(n1 + n2 + 1) = v0

    # 1) v1 = 0: Eliminar a primeira linha e primeira coluna da matriz global.
    #            Eliminar a primeira linha do vetor_global_d e fazer atualizacoes no restante das linhas.
    for i in range(0, len(matriz_global)):
        matriz_global[i].pop(0)
    matriz_global.pop(0)
    vetor_global_d.pop(0)

    # 2) v(n1 + n2 + 1) = v0: Eliminar a ultima linha e a ultima coluna da matriz global.
    #                         Eliminar a ultima linha do vetor_global_d e fazer atualizacoes no restante das linhas. 
    for i in range(0, len(vetor_global_d)):
        vetor_global_d[i] = vetor_global_d[i] - (matriz_global[i][-1]*v0)
    for i in range(0, len(matriz_global)):
        matriz_global[i].pop()
    matriz_global.pop()
    vetor_global_d.pop()

    # Resolvendo o Sistema Matricial Global de Equacoes Lineares
    A = np.array(matriz_global)
    B = np.array(vetor_global_d)
    V = np.linalg.solve(A, B)

    # Printando a solucao com os valores do potencial eletrostatico em cada nó do domínio do problema:
    print("V1 = 0")
    for i in range(0, len(V)):
        print("V" + str(i + 2) + " = " + str(V[i]))
    print("V" + str(int(n1 + n2 + 1)) + " = " + str(v0))
    
    # Plotando os resultados em um gráfico: V x d.
    V_values = [0.0]
    for i in range(0, len(V)):
        V_values.append(V[i])
    V_values.append(v0)
    d_values = []
    d_values.append(0.0)
    current = l1
    for i in range(0, int(n1)):
        d_values.append(current)
        current += l1
    current -= l1
    d_fronteira = current
    current += l2
    for i in range(0, int(n2)):
        d_values.append(current)
        current += l2
    
    plot_graphic_V_vs_d(V_values, d_values, d_fronteira, d1+d2)
    approximate_capacitance = (calculate_approximate_charge(V_values, L, e2, l2))/v0
    print("Capacitancia Aproximada (C):", approximate_capacitance, "F.")
    return

main()
