# ARX model estimation (batch data processing) (4)

In the evaluation of the AutoRegressive with eXogenous input (ARX) model, a critical consideration is whether the resulting parameter estimates are biased. The statistical properties of the estimate $\hat{\theta}$ depend heavily on the relationship between the regressor matrix $Z$ and the noise vector $E$.

#### Bias of ARX model parameter estimate

To determine if the estimate is unbiased, we examine the expected value of the Least Squares estimator $\hat{\theta} = (Z^T Z)^{-1} Z^T Y$. Substituting the system equation $Y = Z\theta + E$ into the estimator formula, we obtain:

$$\mathcal{E}\left\{\hat{\theta}\middle|\theta\right\} = \mathcal{E}\left\{(Z^TZ)^{-1}Z^T(Z\theta + E)\middle|\theta\right\} = \theta + \mathcal{E}\left\{(Z^TZ)^{-1}Z^TE\right\}$$

The estimate is considered **unbiased** if $\mathcal{E}\left\{(Z^TZ)^{-1}Z^TE\right\} = 0$. This condition is satisfied if the data matrix $Z$ is not correlated with the noise vector $E$.

**1. Finite Impulse Response (FIR) Models**
For an FIR model, the output is defined solely by past inputs and the current noise:
$$y(t) = \sum_{i=1}^{n_b} b_i u(t-i) + e(t)$$
In this case, the regressor vector $z(t)$ contains only input values $u(t-i)$. Since the inputs are typically assumed to be independent of the measurement noise $e(t)$, the regressor matrix $Z$ and the noise vector $E$ are uncorrelated. Consequently, the FIR model provides an **unbiased** estimate of $\theta$.

**2. General ARX Models**
In a general ARX model, the regressor vector $z(t)$ includes lagged versions of the output $y(t-1), y(t-2), \dots$. Because the output $y$ is itself a function of past noise terms, the data matrix $Z$ inevitably contains elements that are correlated with the noise vector $E$. Specifically:
$$\mathcal{E}\left\{ \left(Z^{T}Z\right)^{-1}Z^{T}E\right\} \neq 0$$
This correlation introduces a bias in finite samples. While the ARX estimate is often **consistent** (meaning the bias vanishes as the number of observations $T \to \infty$ under certain conditions), it is technically biased for small or batch data sets because the regressors are not strictly exogenous.