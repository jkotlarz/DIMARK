# DIMARK/market.py
import numpy as np

def functionvalue(a, x, functiontype="lin"):
    """
    Evaluates the function based on the specified function type.

    Parameters:
    a (list or array-like): A list or array of coefficients.
                           For "lin" type, it should have at least two elements [a0, a1].
                           For "poly" type, it can have multiple elements representing polynomial coefficients.
    x (list or array-like): A list or array of input values.
    functiontype (str, optional): The type of function to evaluate. Defaults to "lin".
                                  "lin" for linear function a[0] + a[1] * x.
                                  "poly" for polynomial function a[0] + a[1] * x + a[2] * x^2 + ... + a[n] * x^n.

    Returns:
    list: A list of evaluated values based on the function type.

    """
    if functiontype == "lin":
        if len(a) < 2:
            return "ERR: At least two parameters required in a array."
        else:
            y = [a[0] + a[1] * xi for xi in x]
            return y
    elif functiontype == "poly":
        y = []
        for xi in x:
            yi = sum(coef * xi**power for power, coef in enumerate(a))
            y.append(yi)
        return y
    elif functiontype == "exp":
        if len(a) < 2:
            return "ERR: At least two parameters required in a array."
        else:
            y = []
            if a[1] >=0:
                for xi in x:
                    yi = a[0]*np.power(a[1],xi)
                    y.append(yi)
                return y
            else:
                for xi in x:
                    yi = a[0]*np.power(-a[1],xi)
                    y.append(1./yi)
                return y
    elif functiontype == "expe":
        if len(a) < 1:
            return "ERR: At least two parameters required in a array."
        else:
            y = []
            for xi in x:
                yi = a[0]*np.power(np.e,xi)
                y.append(yi)
            return y    
    elif functiontype == "pow":
        if len(a) < 1:
            return "ERR: At least two parameters required in a array."
        else:
            y = []
            for xi in x:
                yi = a[0]*np.power(a[1],xi)
                y.append(yi)
            return y    
    else:
        return f"ERR: Unsupported function type '{functiontype}'. Supported types are 'lin' and 'poly'."


def market_equilibrium(supp, demd):
    """
    Finds the market equilibrium points where the supply and demand polynomials are equal.

    Parameters:
    supp (list or array): Coefficients of the supply polynomial.
    demd (list or array): Coefficients of the demand polynomial.

    Returns:
    tuple: A tuple containing:
        - real_roots (array): The x values where the supply and demand polynomials are equal.
        - supp_values (array): The values of the supply polynomial at the equilibrium points.
    """
    diff_coeffs = np.polysub(supp, demd)
    roots = np.roots(diff_coeffs[::-1])
    real_roots = roots[np.isreal(roots)].real
    supp_values = np.polyval(supp[::-1], real_roots)
    
    return real_roots, supp_values


