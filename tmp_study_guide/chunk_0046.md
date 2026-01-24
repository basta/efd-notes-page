# Supplementary reading

## ARX model estimation (recursive data processing) (2)

In the Bayesian framework for recursive estimation, we update our knowledge of the parameters as each new data point arrives. By applying the Bayes formula and focusing on the exponents of the probability density functions, we can derive the recursive update laws for our statistics.

### Comparison of Parameter Functions

To find the update for the parameter vector $\theta$, we equate the terms in the exponent of the posterior distribution at time $t$ with the sum of the log-likelihood of the new observation and the prior distribution from time $t-1$. This leads to the following identity:

$$\begin{split} \nu(t) \, s^2(t) + \left(\theta - \hat{\theta}(t)\right)^T & P(t)^{-1} \left(\theta - \hat{\theta}(t)\right) = \\ & = \quad \nu(t-1) \, s^2(t-1) + \left(y(t) - z^T(t)\theta\right)^2 + \left(\theta - \hat{\theta}(t-1)\right)^T & P(t-1)^{-1} \left(\theta - \hat{\theta}(t-1)\right) \end{split}$$

This equation balances the residual sum of squares and the weighted quadratic distance of the parameters from their estimates.

### Updating the Normalized Covariance Matrix

The precision matrix (the inverse of the normalized covariance matrix $P$) is updated by adding the outer product of the current regressor vector $z(t)$:

$$P(t)^{-1} = P(t-1)^{-1} + z(t)z^{T}(t)$$

To avoid the computationally expensive operation of matrix inversion at every time step, we utilize the **Matrix Inversion Lemma (MIL)**, also known as the Woodbury matrix identity:

$$(A + BCD)^{-1} = A^{-1} - A^{-1}B(C^{-1} + DA^{-1}B)^{-1}DA^{-1}$$

By substituting $A = P(t-1)^{-1}$, $B = z(t)$, $C = 1$, and $D = z^T(t)$, we obtain the recursive formula for $P(t)$:

$$P(t) = P(t-1) - \frac{P(t-1)z(t)z^{T}(t)P(t-1)}{1 + z^{T}(t)P(t-1)z(t)}$$

This allows us to update the covariance matrix using only matrix-vector multiplications and scalar division.

### Updating the Parameter Mean Value

The estimate of the parameter vector $\hat{\theta}(t)$ is updated by correcting the previous estimate $\hat{\theta}(t-1)$ with the new information contained in the prediction error $(y(t) - z^{T}(t)\hat{\theta}(t-1))$. The update can be expressed in two equivalent forms:

$$\hat{\theta}(t) = \hat{\theta}(t-1) + P(t)z(t)(y(t) - z^{T}(t)\hat{\theta}(t-1))$$

By substituting the MIL expression for $P(t)$, we arrive at the standard Recursive Least Squares (RLS) update form:

$$\hat{\theta}(t) = \hat{\theta}(t-1) + \frac{P(t-1)z(t)}{1 + z^{T}(t)P(t-1)z(t)} (y(t) - z^{T}(t)\hat{\theta}(t-1))$$

Here, the term $\frac{P(t-1)z(t)}{1 + z^{T}(t)P(t-1)z(t)}$ acts as the estimator gain, determining how much the new prediction error influences the updated parameter estimate.

![](_page_76_Picture_11.jpeg)