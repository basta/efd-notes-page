# ARX model estimation (batch data processing) (2)

In the context of system identification, the Bayesian approach allows us to treat the model parameters as random variables. By combining prior knowledge with the observed data, we can derive the posterior distribution of the parameters.

#### **Bayesian estimate**

The starting point for the estimation is the **Likelihood function**. Given the ARX model structure $Y = Z\theta + E$ and assuming the noise $e(t)$ follows a Gaussian distribution $\mathcal{N}(0, \sigma_e^2)$, the likelihood of observing the data $Y$ for a given set of parameters $\theta$ and noise standard deviation $\sigma_e$ is:

$$l(\theta, \sigma_e | Y) \propto \sigma_e^{-T} \exp \left(-\frac{1}{2\sigma_e^2} (Y - Z\theta)^T (Y - Z\theta)\right)$$

where $T$ is the number of observations.

#### **Rearranging the Quadratic Form**
To find the most likely parameters, we decompose the quadratic term in the exponent. This algebraic manipulation separates the error into a part that depends on the parameter estimate and a part that represents the minimum achievable residual:

$$(Y-Z\theta)^T(Y-Z\theta) = (Y-\hat{Y})^T(Y-\hat{Y}) + (\theta-\hat{\theta})^TZ^TZ(\theta-\hat{\theta})$$

From this decomposition, we identify two critical components:

1.  **Parameter Estimate ($\hat{\theta}$):** The value that minimizes the quadratic form is the standard Least Squares solution:
    $$\hat{\theta} = (Z^T Z)^{-1} Z^T Y = P_{\theta} Z^T Y$$
    Here, $P_{\theta} = (Z^T Z)^{-1}$ is often related to the covariance of the estimate.

2.  **Output Prediction ($\hat{Y}$):** The predicted output vector based on the estimated parameters:
    $$\hat{Y} = Z\hat{\theta}$$

#### **Residual Sum of Squares and Degrees of Freedom**
The quality of the fit is measured by the variance of the residuals. We define the estimated noise variance $s^2$ as:

$$s^2 = \frac{1}{\nu} (Y - \hat{Y})^T (Y - \hat{Y}), \qquad \nu = T - n$$

where $\nu$ represents the **degrees of freedom**, calculated as the number of observations $T$ minus the number of estimated parameters $n$.

#### **Posterior Distribution**
By applying Bayes' rule with a non-informative (flat) prior, we obtain the **Posterior conditional probability density function (c.p.d.f.)** for the parameters $\theta$ and the noise standard deviation $\sigma_e$:

$$p(\theta, \sigma_e | \mathcal{D}^T) \propto \sigma_e^{-(T+1)} \exp\left(-\frac{\nu s^2}{2\sigma_e^2} - \frac{1}{2\sigma_e^2}(\theta - \hat{\theta})^T P_\theta^{-1}(\theta - \hat{\theta})\right)$$

This joint distribution provides a complete probabilistic description of our uncertainty regarding the model. The first term in the exponent relates to the noise variance (leading to an Inverse-Gamma or Chi-squared type distribution), while the second term shows that, for a fixed $\sigma_e$, the parameters $\theta$ follow a Gaussian distribution centered at $\hat{\theta}$.

![](_page_66_Picture_14.jpeg)

![](_page_66_Picture_15.jpeg)