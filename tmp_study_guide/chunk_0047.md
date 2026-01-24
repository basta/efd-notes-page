# Supplementary reading

## ARX model estimation (recursive data processing) (3)

In the previous sections, we derived the recursive updates for the parameter vector $\hat{\theta}(t)$ and the normalized covariance matrix $P(t)$. To complete the Bayesian estimation framework, we must also update our knowledge regarding the noise variance $\sigma_e^2$.

### Updating Noise Statistics

By comparing the functions of the noise variance $\sigma_e$ in the posterior distribution, we derive the recursions for the degrees of freedom and the residual sum of squares.

*   **Degrees of Freedom ($\nu$):**
    The parameter $\nu(t)$ represents the "strength" of our evidence or the number of effective data samples processed. With each new observation, the degrees of freedom increase linearly:
    $$\nu(t) = \nu(t-1) + 1$$

*   **Residual Sum of Squares ($s^2$):**
    The point estimate of the noise variance, $s^2(t)$, is updated by incorporating the new prediction error. The update formula is:
    $$\nu(t)s^{2}(t) = \nu(t-1)s^{2}(t-1) + \frac{\varepsilon^{2}(t|t-1)}{1+z^{T}(t)P(t-1)z(t)}$$
    Here, $\varepsilon(t|t-1) = y(t) - z^T(t)\hat{\theta}(t-1)$ is the innovation (prediction error). The denominator $1+z^{T}(t)P(t-1)z(t)$ acts as a scaling factor that accounts for the uncertainty in the current parameter estimates.

**Note on Prediction Error Variance:**
It is useful to compare the update term with the expected value of the squared prediction error. Given the noise variance $\sigma_e^2$, the variance of the innovation is:
$$\mathcal{E}\left\{\left.\varepsilon^{2}(t|t-1)\right|\,\sigma_{e}\right\}=\sigma_{e}^{2}\left(1+z^{T}(t)P(t-1)z(t)\right)$$
This shows that the innovation variance is composed of the inherent system noise $\sigma_e^2$ and the additional uncertainty stemming from the estimation error of $\theta$.

### Initialization of Recursions

To begin the recursive process at $t=0$, we must define the prior hyperparameters. These reflect our initial knowledge (or lack thereof) before any data is observed:

*   **$s^2(0)$**: The prior estimate of the noise variance $\sigma_e^2$.
*   **$\nu(0)$**: The weight assigned to the prior variance, often interpreted as the size of a "virtual" auxiliary data sample.
*   **$\hat{\theta}(0)$**: The initial guess for the system parameters.
*   **$P(0)$**: The prior estimate of the parameter covariance matrix (normalized by $s^2(0)$). A large $P(0)$ (e.g., $10^3 I$) indicates high uncertainty, effectively making the estimator rely more on incoming data.

### The Stationary Assumption

In this standard ARX recursive formulation, we assume a **constant parameter model**:
$$\theta(t) = \theta = \text{constant}$$
Because the parameters are assumed not to change over time, a **Time Update Step** (common in Kalman Filtering) is not needed. We only perform the **Data Update Step** to refine our estimate of the fixed unknown constants.