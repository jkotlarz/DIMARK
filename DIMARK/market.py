# DIMARK/market.py
import numpy as np

from .mathematics import functionvalue, integrate_poly

def market_equilibrium(supp, demd, maxdif=1.,maxiter=1e3):
    """
    Finds the market equilibrium points where the supply and demand polynomials are equal.

    Parameters:
    supp (list or array): Coefficients of the supply polynomial.
    demd (list or array): Coefficients of the demand polynomial.
    maxdif (float): Maximum prices difference on equilibrium.
    maxiter (int): Maximum number of iterations

    Returns:
    tuple: A tuple containing:
        - quantity in equilibrium
        - price in equilibrium
        - final iteration step
        - final difference in prices between demand and supply in returned quantity
        - number of iterations
    """

    delta = 1.
    q = [5.0]
    i=0
    sup = functionvalue(supp, q, "poly")
    dem = functionvalue(demd, q, "poly")
    
    while (np.abs(sup[0]-dem[0]) > maxdif) and (i<maxiter):
        i += 1
        q.append(q[0]+delta)
        sup = functionvalue(supp, q, "poly")
        dem = functionvalue(demd, q, "poly")
        dy = np.abs(sup[0]-dem[0])
        dy2 = np.abs(sup[1]-dem[1])
        if (dy2 < dy):
            q=[q[0]+delta]
        else:
            q=[q[0]-delta]
        if (sup[0]-dem[0])*(sup[1]-dem[1]) < 0:
            delta = delta/2

    return(q[0],(sup[0]+dem[0])*0.5,delta,np.abs(sup[0]-dem[0]),i)    

def surplus(a,equilibrium_q):
    """
    Computes the surplus by finding the difference between the area under the
    polynomial curve and the area of the rectangle formed by the equilibrium price
    and quantity.
    
    Parameters:
    a (list or array-like): Coefficients of the polynomial in increasing powers.
    equilibrium_q (float): Market equilibrium quantity.
    
    Returns:
    float: Surplus calculated as the absolute difference between the integral and the rectangle area.
    """
    equilibrium_p = functionvalue(a, [equilibrium_q])[0]
    rectangle = equilibrium_p*equilibrium_q
    integral = integrate_poly(a, 0, equilibrium_q)
    return np.abs(integral - rectangle)