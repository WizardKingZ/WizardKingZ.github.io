---
title: "Project: Multivariate Time Series Outlier Detection"
layout: post
projects: true
date: 2018-09-24 21:10
headerImage: false
tag: 
  - Time Series
  - Intervention Analysis
category: projects
author: projohnewzhang
description: "Multivariate Time Series Outlier Detection"
---

Let $$x_t =(x_{1t}, \cdots, x_{kt})'$$ be a k-dimensional time series that follows a vector autoregressive integrated moving-average, ARIMA, model

$$\Phi(B) x_t = c + \Theta(B)\varepsilon_t,$$

where 

$$\Phi(B) = I - \sum_{i=1}^p \Phi_iB^p, \Theta(B) = I - \sum_{i=1}^p \Theta_iB^p$$ 

are $$k \times k$$ matrix polynomials of finite degrees $$p$$ and $$q$$, $$B$$ is the backshift operator such that $$Bx_t = x_{t-1}$$, $$c$$ is a $$k$$-dimensional constant vector, and $$\{\varepsilon = (\varepsilon_{1t}, \cdots, \varepsilon_{kt})'\}$$ is a sequence of independent and identically distributed Gaussian random vector with zero mean and positive-definite covariance matrix $$\Sigma$$. We assume that $$\Phi(B)$$ and $$\Theta(B)$$ are left caprice and that all of the zeros of the determinants $$\vert\Phi(B)\vert$$ and $$\vert\Theta(B)\vert$$ are on or outside the unit circle.  

Define the autoregressive representation as

$$\Pi(B)x_t = c_0 +\varepsilon_t$$ 

where 

$$\Pi(B) = I - \sum_{i=1}^{\infty} \Pi_i B^i = \{\Theta(B)\}^{-1}\Phi(B)$$

Define the moving-average representation as 

$$x_t = c^* +\Psi(B) \varepsilon_t$$

where 

$$\Psi(B) = I - \sum_{i=1}^{\infty} \Psi_i B^i = \{\Phi(B)\}^{-1}\Theta(B)$$

Before diving into the algorithm, we will make some more definitions. Denote the observed time series by $$y_t =(y_{1t}, \cdots, y_{kt})'$$ and let $$\omega = (\omega_1, \cdots, \omega_k)'$$ be the size of the initial impact of an outlier on the series $$x_t$$. The four types of univariate outliers can be generalized to the multivariate case

$$y_t = x_t + \alpha(B) \omega \xi_t^{(h)},$$

where 

$$\begin{array}{c|c} 
\alpha(B) & \textbf{Type} \\\
\Psi (B) & \text{multivariate innovational outlier} \\\
I & \text{multivariate additive outlier} \\\
(I - B)^{-1} & \text{multivariate level shift} \\\
{D(\delta)}^{-1} & \text{multivariate temporary change} \\\
\end{array}$$

Here, $$\Psi$$ is the MA representation of VARMA model. Next, we can multiply the above equation by $$\Pi(B)$$ and subtract a constant term from both sides, we have

$$a_t = \varepsilon_t + \Pi(B)\alpha(B)\omega \xi_t^{(h)}$$

Here let's write $$\Pi(B)\alpha(B)$$ as $$\Pi^*(B)$$. Therefore, if we suppose $$\hat{a}_t$$ is the estimated residuals and $$\hat{\Pi}_i$$ is the estimated coefficients of the autoregressive representation, we have the following

$$\hat{a}_t =\left(I - \sum_{i=1}^{\infty} \hat{\Pi^*}_i B^i\right)\xi_t^{(h)}\omega + \varepsilon_t = \left(\xi_t^{(h)} - \sum_{i=1}^{\infty} \hat{\Pi^*}_i \xi_{t-i}^{(h)}\right)\omega + \varepsilon_t$$

where $$\varepsilon_t \sim N(0, \Sigma)$$, and the estimator of $$\omega$$ is

$$\hat{\omega}_{i, h} = -\left(\sum_{i=0}^{n - h} \hat{\Pi^*}'_i \Sigma^{-1}\hat{\Pi^*}\right)^{-1}\sum_{i=0}^{n - h} \hat{\Pi^*}'_i \Sigma^{-1}\hat{a}_{h+i}$$

where $$\Pi_0 = -I$$ and $$i = I , A, L, T$$. 

For the $$\Pi^*$$, we can obtain by calculating the coefficient of $$\Pi(B)\alpha(B)$$. Here, additive outlier and level shift are a just special case of temporary change so let's only consider a temporary change at the moment. That is the following

$$I - \sum_{i=1}^{\infty} \Pi^*_i B^i = \left(I - \sum_{i=1}^{\infty} \Pi_i B^i)(I - \delta B\right)^{-1}$$

Hence, the above is just a simple polynomial division. In general, suppose three polynomials 

$$\Pi(B) = I - \sum_{i=1}^{\infty} \Pi_i B^i,$$ $$\Phi(B) = I - \sum_{i=1}^{p} \Phi_i B^i$$ and $$\Theta(B)= I - \sum_{i=1}^{q} \Theta_i B^i$$ 

where

$$\Pi(B) = \Theta(B)^{-1}\Phi(B)$$

Then 

$$\Pi_i = \Phi_i + \sum_{j = 1}^{i} \Theta_j\Pi_{i-j}$$ 

where $$i = j$$, $$\Pi_{i - j} = -I$$, if $$i > p$$, $$\Phi_i = 0$$ and if $$j > q$$, $$\Theta_j = 0$$. Therefore, we can obtain the polynomial representation for temporary change using the above reclusive relation. 

In addition, the covariance matrix of the estimator is $$\Sigma_{i, h} = \left(\sum_{i=0}^{n-h} \hat{\Pi^*}'_i\Sigma^{-1}\hat{\Pi^*}_i\right)^{-1}$$. Lastly, to reduce the effect of one particular outlier, we can proceed to the following equation 

$$x_t = y_t - \alpha(B) \omega \xi_t^{(h)}$$ 

where $$x_t$$ is the adjusted series and $$y_t$$ is the original series. 


## Algorithm

Suppose the observed time series has no outlier and provide model $$ARMA(p, q)$$

__Step 1__: Use Maximum-Likelihood estimation to estimate $$\Phi, \Theta$$ and $$\Sigma$$. 

__Step 2__:  Use resulted estimation to calculate estimated residuals, $$\hat{a}_t$$ and the estimated AR representation, $$\hat{\Pi}_i$$

__Step 3__:  Obtain $$\omega_{i, h}$$ for all $$h$$ where the subscript $$i$$ indicates type of outliers ($$i = I, A, L, S$$) and the covariance estimator. 

__Step 4__:  To test the significance of a multivariate outlier at time index h, we consider the null hypothesis $$H_0:\omega= 0$$ versus the alternative hypothesis $$H_a: \omega\neq 0$$. Two test statistics are used. 
* $$J_{i,h} = \hat{\omega}_{i, h}'\Sigma_{i, h}^{-1}\hat{\omega}_{i, h}$$ where $$i = I, A, L \text{ or } T$$.  (chi-square random variable with $$k$$ degrees of freedom)
* The maximum $$z$$-statistics
        
$$C_{i, h} =\frac{\max_{1 \leq j \leq k} \vert\hat{\omega}_{j, i, h}\vert}{\sqrt{\sigma_{j, i, h}}}$$

where $$\hat{\omega}_{j, i, h}$$ and $$\sigma_{j, i, h}$$ are the $$n$$th element of $$\hat{\omega}_{i, h}$$ and the $$(j, j)$$th element of $$\Sigma_{i, h}$$ respectively. 

We define the overall test statistics as 

$$J_{\max}(i, h_i) = \max_h J_{i, h}, C_{\max}(i, h_{i}^*) = \max_h C_{i, h}, (i = I, A, L, T)$$

where $$h_i$$ denotes the time index when the maximum of the test statistics $$J_{i, h}$$ occurs and $$h_{i}^*$$ denotes the time index when the maximum of $$C_{i, h}$$ occurs.

In the case of multiple significant joint test statistics, we identify the outlier type based on the test that has the smallest empirical p-value. If none of $$J_{\max}$$ are significant, $$C_{\max}$$ will be tested. Otherwise, our procedure ends. 

__Step 5__: Once an outlier is detected, we will adjust the original time series by subtracting $$\alpha(B)\omega \varepsilon_t^{(h)}$$ Then the process jumps back to Step 1.

---

# Code Walk Through

One can download the "outlier_detection.R" code <a href="https://github.com/WizardKingZ/time_series_outlier_detection">here</a>. Before using this program, please make sure MTS library is also installed. We will use the gas furnace data as an example. First, let's load the data

```R 
rate <- gas.furnace$InputGasRate
co2 <- gas.furnace$CO2
```
Then we will use the following blocks to get the outlier

```R
n <- length(co2)
## delta value for temporary change is normally set to be 0.7
delta <- 0.7
xt = gas.furnace

res = list()
it = 1
while (TRUE) {
  out = outlierDetect(xt, p, q, k, n, delta, critical.j, critical.c)
  
  if (out$Outlier[1, 1] == 0) {
    break;
  } else {
  
    l = list()
    l$Outlier = out$Outlier
    l$Jmax = out$Jmax
    l$Cmax = out$Cmax
  
    xt = out$xt
    print(l)
    res[[it]] = l
    it = it + 1
  }
}
##
## report returns a summary of the outlier and its statistics for each individual iteration
## each interaction takes two rows
## first row contains Jmax, Cmax value for each type of outlier, and the position of the identified outlier
## first 4 columns are for Jmax from type 1 to 4 and column 5 to 8 are for Cmax from type 1 to 4
## the 9th column is the type of the identified outlier and the 10th is the time index
## the second row contains time indexes for each Jmax and Cmax
##
report = matrix(0, length(res)*2, 10)

for (i in 1:length(res)) {
  item = res[[i]]
  index =2*i - 1
  report[index, 1:4] = item$Jmax[, 1]
  report[index+1, 1:4] = item$Jmax[, 2] 
  report[index, 5:8] = item$Cmax[, 1]
  report[index+1, 5:8] = item$Cmax[, 2]
  report[index, 9:10] =item$Outlier
}
```

Finally, you can obtain the results as follows

$$\begin{array}{c|c} 
\textbf{Time Index} & \textbf{Type} \\\
43 & \text{MTC} \\\
55 & \text{MTC} \\\
265 & \text{MIO} \\\
113 & \text{MTC} \\\
199 & \text{MTC} \\\
235 & \text{MLS} \\\
91 & \text{MTC} \\\
262 & \text{MIO} \\\
288 & \text{MLS} \\\
287 & \text{MLS} \\\
82 & \text{MLS} \\\
\end{array}$$

---
## References

* Tsay, R., Pena, D., Pankratz, A. E., 2000. Outliers in multivariate time series. Biometrika 87, 789-804.
