---
title: "Portfolio Optimization Library"
layout: post
library: true
date: 2018-09-25 21:10
headerImage: false
tag: 
  - Portfolio Theory
  - Optimization
  - Finance
  - Python
category: library
author: projohnewzhang
description: Portfolio Optimization Library
---

As an ongoing effort to provide more finance-related python library, I will start with the portfolio optimization library. This page documents the Hello-World version.

# Installation

If you have python 2.7 installed, you can run the following in your terminal

```unix
pip install git+https://github.com/WizardKingZ/portfolio_optimization.git
```

It is eeasy to underinstall it.

```unix
pip uinstall portfolio_optimization
```

# Get Started
## Unconstrained Portfolio
```python
## import MarkowitzPortfolio 
from portfolio_optimization import MarkowitzPortfolio

## Load the Fama-French Five Factor Dataset to calculate annualized return and covariance
res = run_query("""select date, marketExcess + riskFreeRate as Market, 
                                SMB + riskFreeRate as SMB, 
                                HML + riskFreeRate as HML, 
                                RMW + riskFreeRate as RMW, 
                                CMA + riskFreeRate as CMA from FF5FactorDaily""", 
                "dev_factor_lib")
res = res.set_index('date')
res = res/100
rts = res.mean()*252
cov = res.cov()*252

## Initialize the MarkowitzPortfolio with the expected return, covariance and asset names
port = MarkowitzPortfolio(rts.values, cov.values, rts.index, riskFreeRate=0.046)

## set the target return as 0.1 
## you can set risk aversion or target volatility as well
## we will cover constraints optimization later
configuration = {'constraints': None, 
                 'riskAversion': None, 
                 'targetReturn': 0.1, 
                 'targetVol': None}

## obtain weights allocated on each asset
weights = port.get_allocations(configuration=configuration)

## plot the efficient frontier and capital market line 
port.display_efficient_frontier(assetsAnnotation=True, 
                                specialPortfolioAnnotation=True, 
                                addTangencyLine=True, 
                                upper_bound=0.14, 
                                path="pic/efficient_frontier_with_cml.png")
```

<p align="center"> 
<img src="{{site.base_url}}/assets/images/portfolio_optimization/efficient_frontier_with_cml.png">
</p>

## Constrained Portfolio

Let's continue to use the FF-5 Factor data. However we are interested in a portfolio with the following constraints

\begin{array}{c|cc} 
\text{Asset} & \text{Lower Bound %} & \text{Upper Bound %}\\\
\hline \text{MKT} & 0 & 100 \\\
\text{HML} & 50 & 100\\\
\text{SMB} & 0 & 100 \\\
\text{RMW} & 0 & 100 \\\
\text{CMA} & -50 & 100 \\\
\end{array}

We can set up the following constraints

```python
constraints = {'MKT': [0, 1], 'HML': [0.5, 1], 'SMB': [0, 1], 'RMW': [0, 1], 'CMA': [-.5, 1]}
## obtain weights allocated on each asset
weights = port.get_allocations(configuration=configuration)
```

To provide some intuition on the $$G$$ and $$h$$ in the constraints, consider the following quadratic programming problem

\begin{align}
\min_{x} &\frac{1}{2}x'Px + q'x \\\
\text{subject to } & Gx \leq h \\\
& Ax = b \\\
\end{align}

$$G$$ in the constraints have two identity matrices stacked and $$h$$ is a stacked vector with positive of the upper constraints and negative of the lower constraints.

I will add more functionality overtime. In the next iteration, I will include the following

* Hansen-Jaganathan bound test
* Black-Litterman Model
* Factor Models for estimating Stochastic Discount Factors
