# DIMARK/allocation_matrix.py

import numpy as np
import random


def error(product, matrix):
    """
    Calculates the sum of the absolute differences between the provided product vector 
    and the column sums of a given matrix.

    Parameters:
    product (list or array-like): A list or array representing the expected values for each column in the matrix.
    matrix (list of lists or 2D array): A 2D list or array where each element matrix[s][p] corresponds to the value at row s and column p.

    Returns:
    float: The total error calculated as the sum of the absolute differences between the expected product values and the actual sums of the columns in matrix.

    Example:
    >>> import numpy as np
    >>> product = [10, 20, 30]
    >>> matrix = [
    ...     [1, 2, 3],
    ...     [4, 5, 6],
    ...     [5, 13, 21]
    ... ]
    >>> error_value = error(product, matrix)
    >>> print(error_value)
    14.0
    """
    e=0.
    for p in range(len(product)):
        v = 0.
        for s in range(len(matrix)):
            v = v + matrix[s][p]
        dv = np.abs(v-product[p])
        e = e + dv
    return e

def iteration(product,mx,s):
    """
    Performs an iteration to attempt to reduce the error between the product vector and 
    the column sums of the matrix by adjusting two non-zero elements in the specified row.

    Parameters:
    product (list or array-like): A list or array representing the expected values for each column in the matrix.
    mx (list of lists or 2D array): A 2D list or array where each element mx[s][p] corresponds to the value at row s and column p.
    s (int): The index of the row to be adjusted.

    Returns:
    list: A list containing a boolean indicating whether the error was reduced and the new matrix if the error was reduced. 
          If the error was not reduced, it returns [False].

    Example:
    >>> product = [10, 20, 30]
    >>> mx = [
    ...     [1, 2, 3],
    ...     [4, 5, 6],
    ...     [5, 13, 21]
    ... ]
    >>> result = iteration(product, mx, 1)
    >>> print(result)
    [True, [[1, 2, 3], [3.99, 5, 6.01], [5, 13, 21]]]
    """
    matrix1 = []
    for k in range(len(mx)):
        col=[]
        for j in range(len(mx[0])):
            col.append(mx[k][j])
        matrix1.append(col)
    e0 = error(product,mx)
    a = matrix1[s]
    not0 = sum(1 for x in a if x != 0)
    niezery = [i for i, x in enumerate(a) if x != 0]
    if not0 > 1:
        pozycje = random.sample(niezery, 2)
        x1 = pozycje[0]
        x2 = pozycje[1]
        dz = min(0.01,a[x1]*0.01)
        a[x1]=a[x1]-dz
        a[x2]=a[x2]+dz
    matrix1[s]=a
    e1 = error(product,matrix1)
    mret = [False]
    if e1 < e0:
        mret = [True, matrix1]
    return mret

def resolve_allocation_matrix(sources,product,matrix,maxiterations=1e4):

    """
    Resolves the allocation matrix by iteratively adjusting the matrix to minimize the error
    between the expected product values and the actual sums of the columns in the matrix.

    Parameters:
    sources (list or array-like): A list or array representing the source values for each row in the matrix.
    product (list or array-like): A list or array representing the expected values for each column in the matrix.
    matrix (list of lists or 2D array): A 2D list or array where each element matrix[s][p] corresponds to the value at row s and column p.
    maxiterations (int, optional): The maximum number of iterations to perform (default is 1e4).

    Returns:
    tuple: A tuple containing the adjusted matrix and the final error value.

    Example:
    >>> sources = [100, 200, 300]
    >>> product = [10, 20, 30]
    >>> matrix = [
    ...     [1, 2, 3],
    ...     [4, 5, 6],
    ...     [5, 13, 21]
    ... ]
    >>> adjusted_matrix, final_error = resolve_allocation_matrix(sources, product, matrix)
    >>> print(adjusted_matrix)
    >>> print(final_error)
    """    
    matrix_adjusted = []
    errors = []
    for s in range(len(sources)):
        column=[]
        n = np.sum(matrix[s])
        sn = sources[s]/n
        for j in range(len(matrix[s])):
            column.append(matrix[s][j]*sn)
        matrix_adjusted.append(column)
    matrix = matrix_adjusted
    curr_error = error(product,matrix)
    i=0
    while (curr_error > np.sum(matrix)*0.0001) and (i<maxiterations):
        result = iteration(product,matrix,i % len(matrix))
        if result[0]:
            matrix = result[1]
        curr_error = error(product,matrix)
        errors.append(curr_error)
        i = i + 1
    
    for p in range(len(product)):
        err=0.
        for s in range(len(sources)):
            err = err + matrix[s][p]
        err = product[p]-err
    return matrix,curr_error


def product_distribution(matrix, products=[]):
    p_n = len(matrix[0])
    products_sum=[]
    for p in range(p_n):
        ps=0.
        for s in range(len(matrix)):
            ps+= matrix[s][p]
        products_sum.append(ps)
        ret = [products_sum]
    if len(products) == p_n:
        diff = []
        diff2 = []
        for p in range(p_n):
            diff.append(products_sum[p]-products[p])
            diff2.append(diff[p]/products[p])
        
        ret.append(diff)
        ret.append(diff2)
    return ret


