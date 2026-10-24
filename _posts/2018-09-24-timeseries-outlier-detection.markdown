---
title: "Multivariate Time Series Outlier Detection"
date: 2018-09-24 21:10
pillar: academic
series: projects
topic: time series
summary: "Finding and classifying outliers in vector ARIMA models, with R code built on the MTS package."
tags: ["time series", "intervention analysis", "R"]
---

Let $$x_t =(x_{1t}, \cdots, x_{kt})'$$ be a k-dimensional time series that follows a vector autoregressive integrated moving-average (ARIMA) model

$$\Phi(B) x_t = c + \Theta(B)\varepsilon_t,$$

where 

$$\Phi(B) = I - \sum_{i=1}^p \Phi_iB^p, \Theta(B) = I - \sum_{i=1}^p \Theta_iB^p$$ 

are $$k \times k$$ matrix polynomials of finite degrees $$p$$ and $$q$$, $$B$$ is the backshift operator such that $$Bx_t = x_{t-1}$$, $$c$$ is a $$k$$-dimensional constant vector, and $$\{\varepsilon = (\varepsilon_{1t}, \cdots, \varepsilon_{kt})'\}$$ is a sequence of independent and identically distributed Gaussian random vectors with zero mean and positive-definite covariance matrix $$\Sigma$$. We assume that $$\Phi(B)$$ and $$\Theta(B)$$ are left coprime and that all of the zeros of the determinants $$\vert\Phi(B)\vert$$ and $$\vert\Theta(B)\vert$$ are on or outside the unit circle.  

Define the autoregressive representation as

$$\Pi(B)x_t = c_0 +\varepsilon_t$$ 

where 

$$\Pi(B) = I - \sum_{i=1}^{\infty} \Pi_i B^i = \{\Theta(B)\}^{-1}\Phi(B)$$

Define the moving-average representation as 

$$x_t = c^* +\Psi(B) \varepsilon_t$$

where 

$$\Psi(B) = I - \sum_{i=1}^{\infty} \Psi_i B^i = \{\Phi(B)\}^{-1}\Theta(B)$$

Before describing the algorithm, we need a few more definitions. Denote the observed time series by $$y_t =(y_{1t}, \cdots, y_{kt})'$$ and let $$\omega = (\omega_1, \cdots, \omega_k)'$$ be the size of the initial impact of an outlier on the series $$x_t$$. The four types of univariate outliers generalize to the multivariate case as

$$y_t = x_t + \alpha(B) \omega \xi_t^{(h)},$$

where 

$$\begin{array}{c|c} 
\alpha(B) & \textbf{Type} \\\
\Psi (B) & \text{multivariate innovational outlier} \\\
I & \text{multivariate additive outlier} \\\
(I - B)^{-1} & \text{multivariate level shift} \\\
{D(\delta)}^{-1} & \text{multivariate temporary change} \\\
\end{array}$$

Here, $$\Psi$$ is the MA representation of the VARMA model. Multiplying the above equation by $$\Pi(B)$$ and subtracting the constant term from both sides gives

$$a_t = \varepsilon_t + \Pi(B)\alpha(B)\omega \xi_t^{(h)}$$

We write $$\Pi(B)\alpha(B)$$ as $$\Pi^*(B)$$. If $$\hat{a}_t$$ are the estimated residuals and $$\hat{\Pi}_i$$ are the estimated coefficients of the autoregressive representation, then

$$\hat{a}_t =\left(I - \sum_{i=1}^{\infty} \hat{\Pi^*}_i B^i\right)\xi_t^{(h)}\omega + \varepsilon_t = \left(\xi_t^{(h)} - \sum_{i=1}^{\infty} \hat{\Pi^*}_i \xi_{t-i}^{(h)}\right)\omega + \varepsilon_t$$

where $$\varepsilon_t \sim N(0, \Sigma)$$, and the estimator of $$\omega$$ is

$$\hat{\omega}_{i, h} = -\left(\sum_{i=0}^{n - h} \hat{\Pi^*}'_i \Sigma^{-1}\hat{\Pi^*}\right)^{-1}\sum_{i=0}^{n - h} \hat{\Pi^*}'_i \Sigma^{-1}\hat{a}_{h+i}$$

where $$\Pi_0 = -I$$ and $$i = I, A, L, T$$.

We obtain $$\Pi^*$$ by calculating the coefficients of $$\Pi(B)\alpha(B)$$. Because additive outliers and level shifts are special cases of a temporary change, we consider only the temporary change:

$$I - \sum_{i=1}^{\infty} \Pi^*_i B^i = \left(I - \sum_{i=1}^{\infty} \Pi_i B^i)(I - \delta B\right)^{-1}$$

This is a simple polynomial division. In general, consider three polynomials

$$\Pi(B) = I - \sum_{i=1}^{\infty} \Pi_i B^i,$$ $$\Phi(B) = I - \sum_{i=1}^{p} \Phi_i B^i$$ and $$\Theta(B)= I - \sum_{i=1}^{q} \Theta_i B^i$$ 

where

$$\Pi(B) = \Theta(B)^{-1}\Phi(B)$$

Then 

$$\Pi_i = \Phi_i + \sum_{j = 1}^{i} \Theta_j\Pi_{i-j}$$ 

where $$\Pi_{i - j} = -I$$ if $$i = j$$, $$\Phi_i = 0$$ if $$i > p$$, and $$\Theta_j = 0$$ if $$j > q$$. We use this recursive relation to obtain the polynomial representation of a temporary change.

The covariance matrix of the estimator is $$\Sigma_{i, h} = \left(\sum_{i=0}^{n-h} \hat{\Pi^*}'_i\Sigma^{-1}\hat{\Pi^*}_i\right)^{-1}$$. To remove the effect of a detected outlier, we adjust the series:

$$x_t = y_t - \alpha(B) \omega \xi_t^{(h)}$$ 

where $$x_t$$ is the adjusted series and $$y_t$$ is the original series.


### Algorithm

Suppose the observed time series has no outliers and follows an $$ARMA(p, q)$$ model.

__Step 1__: Estimate $$\Phi, \Theta$$ and $$\Sigma$$ by maximum likelihood.

__Step 2__: Use these estimates to compute the residuals, $$\hat{a}_t$$, and the AR representation, $$\hat{\Pi}_i$$.

__Step 3__: Obtain $$\omega_{i, h}$$ and its covariance estimator for all $$h$$, where the subscript $$i$$ indicates the outlier type ($$i = I, A, L, S$$).

__Step 4__: To test for a multivariate outlier at time index h, we test the null hypothesis $$H_0:\omega= 0$$ against the alternative $$H_a: \omega\neq 0$$ with two statistics:
* $$J_{i,h} = \hat{\omega}_{i, h}'\Sigma_{i, h}^{-1}\hat{\omega}_{i, h}$$ where $$i = I, A, L \text{ or } T$$, a chi-square random variable with $$k$$ degrees of freedom
* The maximum $$z$$-statistic
        
$$C_{i, h} =\frac{\max_{1 \leq j \leq k} \vert\hat{\omega}_{j, i, h}\vert}{\sqrt{\sigma_{j, i, h}}}$$

where $$\hat{\omega}_{j, i, h}$$ and $$\sigma_{j, i, h}$$ are the $$n$$th element of $$\hat{\omega}_{i, h}$$ and the $$(j, j)$$th element of $$\Sigma_{i, h}$$, respectively.

We define the overall test statistics as

$$J_{\max}(i, h_i) = \max_h J_{i, h}, C_{\max}(i, h_{i}^*) = \max_h C_{i, h}, (i = I, A, L, T)$$

where $$h_i$$ denotes the time index when the maximum of the test statistics $$J_{i, h}$$ occurs and $$h_{i}^*$$ denotes the time index when the maximum of $$C_{i, h}$$ occurs.

If several joint test statistics are significant, we identify the outlier type by the test with the smallest empirical p-value. If no $$J_{\max}$$ is significant, we test $$C_{\max}$$; if it is not significant either, the procedure ends.

__Step 5__: Once we detect an outlier, we adjust the original series by subtracting $$\alpha(B)\omega \varepsilon_t^{(h)}$$ and return to Step 1.

---

## Code Walkthrough

The `outlier_detection.R` code is available [here](https://github.com/WizardKingZ/time_series_outlier_detection). Before running it, install the MTS package. We use the gas furnace data as an example. First, we load the data:

```R 
rate <- gas.furnace$InputGasRate
co2 <- gas.furnace$CO2
```
We then run the detection loop:

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

The procedure identifies the following outliers (MTC, MIO, and MLS denote a multivariate temporary change, innovational outlier, and level shift):

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

### References

* Tsay, R., Pena, D., Pankratz, A. E., 2000. Outliers in multivariate time series. Biometrika 87, 789-804.
