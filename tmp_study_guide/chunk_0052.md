# ARX model – tracking of time-varying parameters (4)

In the previous sections, we explored how a naive model fails to track parameters because the influence of new data diminishes over time. To maintain the estimator's sensitivity, we must introduce a mechanism to "forget" old information.

### **Exponential Forgetting**

Exponential forgetting is a technique that directly increases the uncertainty of both the parameter vector $\theta$ and the noise variance $\sigma_e^2$. This is achieved by flattening the posterior probability density function (pdf) from the previous step.

The conceptual time update step is defined as:
$$p\left( \theta(t+1)|\mathcal{D}^t \right) \propto p^\varphi\left( \theta(t)|\mathcal{D}^t \right), \qquad \varphi \in (0,\,1]$$

Where $\varphi$ is the **forgetting factor**. When $\varphi = 1$, we retain all information (standard RLS). When $\varphi < 1$, the exponentiation "spreads" the distribution, representing a loss of information.

#### **Resulting Statistics**
Applying this operation to the Gaussian-Inverse-Gamma distribution results in the following updates for the statistics:

1.  **Covariance Matrix:** $P(t+1|t) = \frac{1}{\varphi}P(t|t)$
    *   Since $\frac{1}{\varphi} \geq 1$, the uncertainty in $\theta$ increases by a multiplicative factor.
2.  **Parameter Estimate:** $\hat{\theta}(t+1|t) = \hat{\theta}(t|t)$
    *   The point estimate remains the same; only the confidence in it decreases.
3.  **Degrees of Freedom:** $\nu(t+1|t) + n + 1 = \varphi (\nu(t|t) + n + 1)$
    *   The "effective" number of observations is reduced.
4.  **Residual Sum of Squares:** $\nu(t+1|t)s^{2}(t+1|t) = \varphi \nu(t|t)s^{2}(t|t)$

#### **Properties and Selection of $\varphi$**
The forgetting factor determines the "memory" of the estimator. We can define an **effective sample size** ($t_{eff}$), which represents the length of the sliding data window the algorithm considers:
$$t_{eff} = \varphi(t_{eff} + 1) \implies t_{eff} = \frac{1}{1-\varphi}$$

*   **Example:** If $\varphi = 0.99$, the estimator effectively uses the last 100 data points.
*   **Trade-off:** A smaller $\varphi$ allows for faster tracking of rapidly changing parameters but makes the estimates more sensitive to noise (higher variance).

![](_page_82_Picture_12.jpeg)

---

#### **Exponential Forgetting Formulas**

To derive the specific updates, we look at the conceptual solution for the joint time-update of parameters and noise variance:

$$p\left( \theta(t+1), \sigma_{\text{e}}(t+1)|\mathcal{D}^{t} \right) \propto \left. \rho^{\varphi}\left( \theta(t), \sigma_{\text{e}}(t)|\mathcal{D}^{t} \right) \right|_{\theta(t) = \theta(t+1), \ \sigma_{\text{e}}(t) = \sigma_{\text{e}}(t+1)}$$

By substituting the functional form of the Normal-Inverse-Gamma distribution, we compare the terms on both sides of the proportionality:

$$\sigma_e^{-(\nu(t+1|t)+1)}(t+1) e^{-\frac{\nu(t+1|t)s^2(t+1|t)}{2\sigma_e^2(t+1)}} \times \sigma_e^{-n}(t+1)e^{-\frac{1}{2\sigma_e^2(t+1)}}(\theta(t+1)-\hat{\theta}(t+1|t))^T P(t+1|t)^{-1}(\theta(t+1)-\hat{\theta}(t+1|t))$$
$$\propto \sigma_e^{-(\nu(t|t)+1)\varphi}(t+1) e^{-\frac{\nu(t|t)s^2(t|t)\varphi}{2\sigma_e^2(t+1)}} \times \sigma_e^{-n\varphi}(t+1)e^{-\frac{1}{2\sigma_e^2(t+1)}}(\theta(t+1)-\hat{\theta}(t|t))^T P(t|t)^{-1}\varphi(\theta(t+1)-\hat{\theta}(t|t))$$

By matching the quadratic forms in the exponents, we can extract the update for the inverse covariance matrix:
$$\theta^{T}(t+1) P(t+1|t)^{-1} \theta(t+1) = \theta^{T}(t+1) P(t|t)^{-1} \varphi \theta(t+1)$$
This confirms that $P(t+1|t)^{-1} = \varphi P(t|t)^{-1}$, or equivalently, $P(t+1|t) = \frac{1}{\varphi}P(t|t)$.