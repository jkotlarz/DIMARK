# DIMARK/allocation_ras.py

"""
Created on Sat Jun 15 12:09:19 2024

@author: Jan Kotlarz
Nicolaus Copernicus University in Toruń
Faculty of Economic Sciences and Management

"""
import numpy as np

def ras_method(products, sources, tol=1e-5, max_iter=10000):
    """
    Rekonstruuje macierz na podstawie zadanych sum wierszy i kolumn za pomocą metody RAS.

    :param products: Lista lub numpy array z sumami wierszy.
    :param sources: Lista lub numpy array z sumami kolumn.
    :param tol: Tolerancja błędu przy której zatrzymuje się iteracje.
    :param max_iter: Maksymalna liczba iteracji.
    :return: Zrekonstruowana macierz numpy array.
    """
    # Inicjalizacja
    products = np.array(products)
    sources = np.array(sources)
    m, n = len(products), len(sources)
    A = np.ones((m, n))  # Początkowa macierz z wartościami równymi 1

    for iteration in range(max_iter):
        # Skaluje wiersze
        for i in range(m):
            row_sum = np.sum(A[i, :])
            if row_sum != 0:
                A[i, :] *= products[i] / row_sum
        
        # Skaluje kolumny
        for j in range(n):
            col_sum = np.sum(A[:, j])
            if col_sum != 0:
                A[:, j] *= sources[j] / col_sum
        
        # Sprawdza zbieżność
        row_sum_check = np.sum(A, axis=1)
        col_sum_check = np.sum(A, axis=0)
        if np.allclose(row_sum_check, products, atol=tol) and np.allclose(col_sum_check, sources, atol=tol):
            break
    else:
        print("Ostrzeżenie: Metoda RAS nie osiągnęła zbieżności w zadanej liczbie iteracji.")

    return A

