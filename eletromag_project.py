import numpy as np 

PERMISSIVIDADE_DO_VACUO = 8.8541878176 * (10**(-12))
K = [[1, -1],[-1, 1]]

def main():
    L = float(input("Comprimento e Largura das placas do capacitor: (cm)"))
    v0 = float(input("Potencial eletrostatico da placa superior: (V)"))
    er1 = float(input("Constante dieletrica do dieletrico 1: "))
    er2 = float(input("Constante dieletrica do dieletrico 2: "))
    n1, n2 = float(input("Qtd de elementos finitos no meio 1 e no meio 2:").split())
    d1, d2 = float(input("Comprimento dos dieletricos 1 e 2: (mm)").split())

    d = d1 + d2
    n = n1 + n2 
    e1 = er1 * PERMISSIVIDADE_DO_VACUO
    e2 = er2 * PERMISSIVIDADE_DO_VACUO 
    l1 = d1/n1 # Comprimento do Elemento Finito no dieletrico 1
    l2 = d2/n2 # Comprimento do Elemento Finito no dieletrico 2

    # Montagem da Matriz de Coeficientes Global
    numero_nos = n1 + n2 + 1
    matriz_global = [[0 for j in range(0, numero_nos)] for i in range(0, numero_nos)]

    # Matriz de Coeficientes do Elemento no dieletrico 1
    K1 = (e1/l1) * K 
    # Matriz de Coeficientes do Elemento no dieletrico 2
    K2 = (e2/l2) * K 




    return


main()
