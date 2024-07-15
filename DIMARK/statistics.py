#DIMARK/statistics.py

import pandas as pd
import statsmodels.api as sm


def multivariate_regression(df, dependent_variable):
    """
    Performs a multivariate regression and returns the regression parameters.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing the data.
    dependent_variable (str): The column name of the dependent variable.

    Returns:
    pd.Series: A Series containing the regression parameters (coefficients).
    """
    # Dependent variable (Y)
    Y = df[dependent_variable]
    
    # Independent variables (X)
    X = df.drop(columns=[dependent_variable])
    
    # Add constant (intercept) to the independent variables
    X = sm.add_constant(X)
    
    # Linear regression model
    model = sm.OLS(Y, X).fit()
    
    # Regression parameters
    params = model.params
    
    return params

def test_durbin_watson(residuals):
    """
    Calculate the Durbin-Watson statistic to test for autocorrelation in residuals.
    
    Parameters:
    residuals (list): A list of residuals from a regression model.
    
    Returns:
    float: The Durbin-Watson statistic, which ranges from 0 to 4.
           A value around 2 indicates no autocorrelation, 
           values < 2 indicate positive autocorrelation,
           and values > 2 indicate negative autocorrelation.
    """
    mn = 0.0
    lc = 0.0
    for r in residuals:
        mn += r * r
    for i in range(1, len(residuals)):
        lc += (residuals[i] - residuals[i - 1]) * (residuals[i] - residuals[i - 1])
    dw_statistic = lc / mn
    return dw_statistic
