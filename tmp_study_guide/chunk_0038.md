# ARX model estimation (batch data processing) (3)

In the Bayesian framework, the joint posterior distribution of the parameters $\theta$ and the noise standard deviation $\sigma_e$ provides a complete statistical description of our uncertainty after observing the data $\mathcal{D}^T$. By analyzing this joint distribution, we can derive specific conditional and marginal distributions.

### Conditional Distribution of Parameters $\theta$

If the noise standard deviation $\sigma_e$ is assumed to be known, the conditional posterior probability density function (c.p.d.f.) of the parameter vector $\theta$ follows a **Multivariate Normal Distribution**.

$$p(\theta | \sigma_e, \mathcal{D}^T) = (\sqrt{2\pi}\sigma_e)^{-n} |P_\theta|^{-1/2} \exp\left(-\frac{1}{2\sigma_e^2} (\theta - \hat{\theta})^T P_\theta^{-1} (\theta - \hat{\theta})\right)$$

This is compactly expressed as:
$$p(\theta | \sigma_e, \mathcal{D}^T) = \mathcal{N}(\hat{\theta}, \sigma_e^2 P_\theta)$$

Where:
*   $\hat{\theta}$ is the mean (and mode) of the distribution, representing our best estimate.
*   $\sigma_e^2 P_\theta$ is the covariance matrix, where $P_\theta = (Z^T Z)^{-1}$ scales the uncertainty based on the information content of the regressor matrix $Z$.

### Posterior Distribution of Noise $\sigma_e$

The uncertainty regarding the noise level itself is captured by the marginal distribution of $\sigma_e$. This follows a specialized form related to the **$\chi$ (Chi) distribution** (specifically, an Inverse-Gamma type distribution for the variance).

$$p(\sigma_{e}|\ \mathcal{D}^{T}) = \frac{2}{\Gamma(\nu/2)} \left(\frac{\nu s^{2}}{2}\right)^{\nu/2} \sigma_{e}^{-(\nu+1)} \exp\left(-\frac{\nu s^{2}}{2\sigma_{e}^{2}}\right)$$

This can be mapped to the Chi-squared distribution:
$$p(\sigma_e | \mathcal{D}^T) = \chi_{\nu}^2 \left( \frac{\nu s^2}{2\sigma_e^2} \right)$$

The expected value for the noise variance, given the data, is represented by the sample residual variance:
$$\mathcal{E}\left\{\sigma_e^2|\mathcal{D}^T\right\} = s^2$$

### Marginal Distribution of Parameters $\theta$

In practice, $\sigma_e$ is rarely known. To find the distribution of $\theta$ independent of $\sigma_e$, we integrate (average) the joint distribution over all possible values of $\sigma_e$. This results in an **$n$-dimensional Student t-distribution** with $\nu = T - n$ degrees of freedom.

$$p(\theta | \mathcal{D}^T) \propto \left[ 1 + \frac{(\theta - \hat{\theta})^T P_{\theta}^{-1} (\theta - \hat{\theta})}{\nu s^2} \right]^{-(\nu + n)/2} = t_n \left( \hat{\theta}, s^2 P_{\theta}, \nu \right)$$

**Key Takeaway:** The Student t-distribution has "heavier tails" than the Normal distribution. This reflects the increased uncertainty in our parameter estimates because we are estimating the noise variance $s^2$ from the same finite data set used to estimate $\theta$. As the number of data points $T$ increases (and thus $\nu \to \infty$), this distribution converges to the Normal distribution.

<span style="display:block; text-align:center;">
![](_page_67_Picture_15.jpeg)
</span>