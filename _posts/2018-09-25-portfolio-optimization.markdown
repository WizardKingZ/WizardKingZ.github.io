---
title: "Portfolio Optimization Library"
date: 2018-09-27 21:10
pillar: academic
series: code
topic: Python
summary: "A pip-installable Python library for mean-variance portfolios and the efficient frontier."
tags: ["portfolio theory", "optimization", "finance", "python"]
---

As part of an ongoing effort to provide finance-related Python libraries, I will start with portfolio optimization. This page documents the library's Hello-World version.

## Installation

If you have Python 3.6+ installed, run the following in your terminal:

```unix
pip install git+https://github.com/WizardKingZ/portfolio_optimization.git
```

To uninstall it, run:

```unix
pip uninstall portfolio_optimization
```

## Getting Started

### Unconstrained Portfolio

```python
## import MarkowitzPortfolio 
from portfolio_optimization import MarkowitzPortfolio
import numpy as np

## Load the Fama-French Five Factor Dataset to calculate annualized return and covariance
rts = np.array([0.11, 0.07, 0.09, 0.08, 0.08])
cov = np.array([[ 0.0242, -0.0015, -0.0025, -0.0019, -0.0033],
                [-0.0015,  0.0067,  0.0004, -0.0013  ,  0.0001 ],
                [-0.0025,  0.0004,  0.0063, -0.0002,  0.0025],
                [-0.0019, -0.0013  , -0.0002,  0.0033,  0.0001],
                [-0.0033,  0.0001 ,  0.0025,  0.0001,  0.0033]])
ffFactorNames = ['Market', 'SMB', 'HML', 'RMW', 'CMA']

## Initialize the MarkowitzPortfolio with the expected return, covariance and asset names
## both cov and rts are numpy arrays. rts is a row vector 
## ffFactorNames should be a list
port = MarkowitzPortfolio(rts, cov, ffFactorNames, riskFreeRate=0.046)

## set the target return as 0.1 
## you can set risk aversion as well
## we will cover constraints optimization later
configuration = {'constraints': None, 
                 'riskAversion': None, 
                 'targetReturn': 0.1}

## obtain weights allocated on each asset
weights = port.get_allocations(configuration=configuration)

## plot the efficient frontier and capital market line 
port.display_efficient_frontier(assetsAnnotation=True, 
                                specialPortfolioAnnotation=True, 
                                addTangencyLine=True, 
                                upper_bound=0.14)
```

![Efficient frontier with the capital market line for the five Fama-French factors](/assets/images/portfolio_optimization/efficient_frontier_with_cml.png)

### Constrained Portfolio

Continuing with the Fama-French five-factor (FF-5) data, suppose you want a portfolio with the following constraints:

$$\begin{array}{c|c|c} 
\textbf{Asset} & \textbf{Lower Bound %} & \textbf{Upper Bound %}\\\
\text{MKT} & 0 & 100 \\\
\text{HML} & 50 & 100\\\
\text{SMB} & 0 & 100 \\\
\text{RMW} & 0 & 100 \\\
\text{CMA} & -50 & 100 \\\
\end{array}$$

Set up these constraints as follows:

```python
constraints = {'Market': [0, 1], 
               'HML': [0.5, 1], 
               'SMB': [0, 1], 
               'RMW': [0, 1], 
               'CMA': [-.5, 1]}
configuration['constraints'] = constraints
## obtain weights allocated on each asset
weights = port.get_allocations(configuration=configuration)
```

### Black-Litterman Portfolio Allocation

Investors often want to incorporate their own views when solving asset allocation problems. For example:

$$\begin{array}{c|c|c} 
\textbf{View} & \textbf{Confidence Level %} & \textbf{Plus and Minus %}\\\
\text{Market outperforms by 1%} & 95 & 5 \\\
\text{SMB beats RMW by 1%} & 90 & 5\\\
\text{A portfolio of 20% of SMB and 80% of HML beats RMW by 1%} & 99 & 1\\\
\end{array}$$

Use ```BlackLittermanPortfolio``` to incorporate these views:

```python
from portfolio_optimization import BlackLittermanPortfolio
## assetNames are ['Market', 'HML', 'SMB', 'RMW', 'CMA']
port = BlackLittermanPortfolio(modeledReturn, modeledCovariance, assetNames, riskFreeRate=0.046)
views = {'Market': {'type': 'absolute', 'scale': 0.01, 'confidence': 95, 'plusminus%': 5},
         'SMB|RMW' : {'type': 'relative', 'scale': 0.01, 'confidence': 90, 'plusminus%': 5, 'weights': [1., -1.]},
         'SMB|HML|RMW' : {'type': 'relative', 'scale': 0.01, 'confidence': 99, 'plusminus%': 1, 'weights': [.2, .8, -1.]},
         }
## second parameter is the R^2 used in estimating your modeled expected returns
port.update_views(views, 0.1)

## Let's use the same parameters
configuration = {'constraints': None, 
                 'riskAversion': None, 
                 'targetReturn': 0.1}
## you can obtain the BL weights                
weights = port.get_allocations(configuration=configuration)

## you can reset the portfolio to become a regular Markowitz portfolio
port.reset()
```

The second argument of ```update_view``` is the $$R^2$$ of your modeled returns; I will add factor modeling tools in a later iteration. As a starting point, consider the most widely used factor model, the Capital Asset Pricing Model (CAPM). CAPM-estimated returns typically have an $$R^2$$ below 15%, so set this parameter below 15% (the example above uses 10%).

---

I will add more functionality over time. The next iteration will include:

* Hansen-Jagannathan bound test
* Factor models for estimating stochastic discount factors
* Style analysis
