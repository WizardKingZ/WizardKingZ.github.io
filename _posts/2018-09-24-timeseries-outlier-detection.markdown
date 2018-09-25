---
title: "Multi-Variate Time Series Outlier Detection"
layout: post
date: 2018-09-24 21:10
tag: 
  - Time Series
  - Intervention Analysis
headerImage: true
projects: true
hidden: true # don't count this post in blog pagination
description: Multi-Variate Time Series Outlier Detection
category: project
author: projohnewzhang
externalLink: false
---

Let $$x_t =(x_{1t}, \cdots, x_{kt})'$$ be a k-dimensional time series that follows a vector autoregressive integrated moving-average, ARIMA, model

$$\Phi(B) x_t = c + \Theta(B)\epsilon_t,$$

where 

$$\Phi(B) = I - \sum_{i=1}^p \Phi_iB^p, \Theta(B) = I - \sum_{i=1}^p \Theta_iB^p$$ 

are $$k \times k$$ matrix polynomials of finite degrees $$p$$ and $$q$$, $$B$$ is the backshift operator such that $$Bx_t = x_{t-1}$$, $$c$$ is a k-dimensional constant vector, and $$\{\varepsilon = (\varepsilon_{1t}, \cdots, \varepsilon_{kt})'\}$$ is a sequence of independent and identically distributed Gaussian random vector with zero mean and positive-definite covariance matrix $$\Sigma$$. We assume that $$\Phi(B)$$ and $$\Theta(B)$$ are left caprice and that all of the zeros of the determinants $$\vert\Phi(B)\vert$$ and $$\vert\Theta(B)\vert$$ are on or outside the unit circle.  

Define the autoregressive representation as

$$\Pi(B)x_t = c_0 +\varepsilon_t$$ 

where 

$$\Pi(B) = I - \sum_{i=1}^{\infty} \Pi_i B^i = \{\Theta(B)\}^{-1}\Phi(B)$$

Define the moving-average representation as 

$$x_t = c^* +\Psi(B) \varepsilon_t$$

where 

$$\Psi(B) = I - \sum_{i=1}^{\infty} \Psi_i B^i = \{\Phi(B)\}^{-1}\Theta(B)$$

Before diving into the algorithm, we will make some more definitions. Denote the observed time series by $$y_t =(y_{1t}, \cdots, y_{kt})'$$ and let $$\omega = (\omega_1, \cdots, \omega_k)'$$ be the size of the initial impact of an outlier on the series $$x_t$$. The four types of univariate outlier can be generalized to the multivariate case

$$y_t = x_t + \alpha(B) \omega \xi_t^{(h)},$$

where 

| $$\alpha(B)$$ | Type | 
| ------------- | ----- |
| $$\Psi (B)$$ | multivariate innovational outlier |
| $$I$$ | multivariate additive outlier |
| $$(I - B)^{-1}$$  | multivariate level shift |
| $$\{D(\delta)\}^{-1}$$ | multivariate temporary change |


Here, $$\Psi$$ is the MA representation of VARMA model. Next, we can multiply above equation by $$\Pi(B)$$ and subtract a constant term from both sides, we have

$$a_t = \epsilon_t + \Pi(B)\alpha(B)\omega \xi_t^{(h)}$$

Here let's write $$\Pi(B)\alpha(B)$$ as $$\Pi^*(B)$$. Therefore, if we suppose $$\hat{a}_t$$ is the estimated residuals and $$\hat{\Pi}_i$$ is the estimated coefficients of the autoregressive representation, we have the following

$$\hat{a}_t =\left(I - \sum_{i=1}^{\infty} \hat{\Pi^*}_i B^i\right)\xi_t^{(h)}\omega + \varepsilon_t = \left(\xi_t^{(h)} - \sum_{i=1}^{\infty} \hat{\Pi^*}_i \xi_{t-i}^{(h)}\right)\omega + \varepsilon_t$$

where $$\varepsilon_t \sim N(0, \Sigma)$$, and the estimator of $$\omega$$ is

$$\hat{\omega}_{i, h} = -\left(\sum_{i=0}^{n - h} \hat{\Pi^*}'_i \Sigma^{-1}\hat{\Pi^*}\right)^{-1}\sum_{i=0}^{n - h} \hat{\Pi^*}'_i \Sigma^{-1}\hat{a}_{h+i}$$

where $$\Pi_0 = -I$$ and $$i = I , A, L, T$$. 

For the $$\Pi^*$$, we can obtain by calculating the coefficient of $$\Pi(B)\alpha(B)$$. Here, additive outlier and level shift are a just special case of temporary change so let's only consider a temporary change at the moment. That is the following

$$I - \sum_{i=1}^{\infty} \Pi^*_i B^i = \left(I - \sum_{i=1}^{\infty} \Pi_i B^i)(I - \delta B\right)^{-1}$$

Hence, above is just a simple polynomial division. In general, suppose three polynomials 

$$\Pi(B) = I - \sum_{i=1}^{\infty} \Pi_i B^i,$$ $$\Phi(B) = I - \sum_{i=1}^{p} \Phi_i B^i$$ and $$\Theta(B)= I - \sum_{i=1}^{q} \Theta_i B^i$$ 

where

$$\Pi(B) = \Theta(B)^{-1}\Phi(B)$$

Then 

$$\Pi_i = \Phi_i + \sum_{j = 1}^{i} \Theta_j\Pi_{i-j}$$ 

where $$i = j$$, $$\Pi_{i - j} = -I$$, if $$i > p$$, $$\Phi_i = 0$$ and if $$j > q$$, $$\Theta_j = 0$$. Therefore, use the above reclusive relation, we can obtain the polynomial representation for temporary change. 

In addition, the covariance matrix of the estimator is $$\Sigma_{i, h} = \left(\sum_{i=0}^{n-h} \hat{\Pi^*}'_i\Sigma^{-1}\hat{\Pi^*}_i\right)^{-1}$$. Lastly, to reduce the effect of one particular outlier, we can just proceed to the following equation 

$$x_t = y_t - \alpha(B) \omega \xi_t^{(h)}$$ 

where $$x_t$$ is the adjusted series and $$y_t$$ is the original series. 


## Algorithm

Suppose observed time series has no outlier and provide model $$ARMA(p, q)$$

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

where $$h_i$$ denotes the time index when the maximum of the test statistics $$J_{i, h}$$ occurs and $$h_{i}^*$$ denotes the time index when the maximum f $$C_{i, h}$$ occurs.

In case of multiple significant joint test statistics, we identify the outlier type based on the test that has the smallest empirical p-value. If none of $$J_{\max}$$ are significant, $$C_{\max}$$ will be tested. Otherwise, our procedure end. 

__Step 5__: Once an outlier is detected, we will adjust the original time series by subtracting $$\alpha(B)\omega \varepsilon_t^{(h)}$$ Then the process jumps back to Step 1.

---

My code is available <a href="https://github.com/WizardKingZ/time_series_outlier_detection">here</a>.

---
## References

* Tsay, R., Pena, D., Pankratz, A. E., 2000. Outliers in multivariate time series. Biometrika 87, 789-804.
