# DIMARK/mathematics.py
import numpy as np

def functionvalue(a, x, functiontype="poly"):
    """
    Compute function values at given arguments using coefficients.

    Args:
    - a (list): List of coefficients representing the function.
    - x (list): List of values at which the function should be evaluated.
    - functiontype (str, optional): Type of function (default is "poly").

    Returns:
    - list: List of computed function values corresponding to each x.

    Description:
    This function computes the function values based on the coefficients `a`.
    It assumes `a` represents coefficients of a polynomial unless specified otherwise.
    For each `xi` in `x`, it calculates `yi` using the formula:
    yi = sum(coef * xi**power for power, coef in enumerate(a))
    """
    y = []
    for xi in x:
        yi = sum(coef * xi**power for power, coef in enumerate(a))
        y.append(yi)
    return y


    
def integrate_poly(a, x0, x1):
    """
    Integrate a polynomial defined by its coefficients over the interval [x0, x1].

    Args:
    - a (list): Coefficients of the polynomial in ascending order of degree.
    - x0 (float): Lower bound of integration.
    - x1 (float): Upper bound of integration.

    Returns:
    - float: Definite integral of the polynomial over [x0, x1].

    Description:
    This function computes the definite integral of a polynomial defined by its coefficients `a`
    over the interval [x0, x1]. The coefficients `a` are assumed to be in ascending order of degree.
    It first adjusts the coefficients to account for integration, computes the values of the integrated
    polynomial at `x0` and `x1` using `functionvalue`, and returns the difference between these two values.
    """
    a.insert(0, 0)  # Insert a_0 = 0 to handle integration constant
    for i in range(1, len(a)):
        a[i] = a[i] / i  # Divide each coefficient by its degree to integrate

    y = functionvalue(a, [x0, x1], "poly")  # Compute function values at x0 and x1
    return y[1] - y[0]  # Return the difference to get the definite integral

    

def estimate_poly(x, y, n):
    """
    Estimate polynomial coefficients and Mean Squared Error (MSE) using least squares fit.

    Args:
    - x (list or numpy array): Array of x-coordinates.
    - y (list or numpy array): Array of y-coordinates.
    - n (int): Degree of the polynomial to be fitted.

    Returns:
    - tuple: Coefficients of the polynomial of degree n and the Mean Squared Error (MSE).

    Description:
    This function computes the coefficients of the polynomial of degree n
    that best fits the given points (x, y) using the method of least squares.
    It also calculates the Mean Squared Error (MSE) to evaluate the quality of the fit.
    """
    # Ensure x and y are numpy arrays for numerical operations
    x = np.array(x)
    y = np.array(y)

    # Create the Vandermonde matrix
    A = np.vander(x, n + 1, increasing=True)

    # Solve the least squares problem
    coefficients = np.linalg.lstsq(A, y, rcond=None)[0]

    # Calculate predicted y values
    y_pred = np.dot(A, coefficients)

    # Calculate MSE
    mse = np.mean((y - y_pred)**2)

    return coefficients, mse
