# ARX Model Estimation (Recursive Data Processing)

In many real-time control and monitoring applications, it is impractical to wait for a full batch of data to arrive before estimating model parameters. Instead, we use **Recursive Least Squares (RLS)** or Bayesian recursive estimation. This approach updates our knowledge of the parameters $\theta$ and the noise variance $\sigma_e^2$ as each new data point $(y(t), u(t))$ becomes available.

### **The Conjugated Prior Distribution**

To perform recursive estimation in a Bayesian framework, we utilize a **conjugated prior distribution**. A prior is "conjugated" if the posterior distribution belongs to the same functional family as the prior. For the ARX model, the joint conditional probability density function (c.p.d.f.) of the parameters follows a Normal-Inverse-Gamma structure:

$$\rho\left(\theta, \sigma_{e} | \mathcal{D}^{t}\right) = \rho\left(\theta | \sigma_{e}, \mathcal{D}^{t}\right) \times \rho\left(\sigma_{e} | \mathcal{D}^{t}\right) = \mathcal{N}(\hat{\theta}(t), \sigma_{e}^{2} P(t)) \times \chi_{\nu(t)}^{2}\left(\frac{\nu(t) s^{2}(t)}{2\sigma_{e}^{2}}\right)$$

Where:
*   $\hat{\theta}(t)$ is the point estimate of the parameters at time $t$.
*   $P(t)$ is the normalized covariance matrix.
*   $s^2(t)$ is the estimate of the noise variance $\sigma_e^2$.
*   $\nu(t)$ represents the degrees of freedom (effectively the count of data samples processed).

### **The Data Update Step**

The transition from the previous estimate at time $t-1$ to the new estimate at time $t$ is governed by the Bayes formula. The posterior is proportional to the product of the likelihood of the new observation and the prior distribution:

$$p\left(\theta, \sigma_{e} | \mathcal{D}^{t}\right) \propto p\left(y(t) | \theta, \sigma_{e}, u(t), \mathcal{D}^{t-1}\right) p\left(\theta, \sigma_{e} | \mathcal{D}^{t-1}\right)$$

#### **Resulting Recursive Formulas**
By processing the algebra of the Bayesian update, we derive the following recursions for the model statistics:

1.  **Parameter Estimate Update:**
    $$\hat{\theta}(t) = \hat{\theta}(t-1) + \frac{P(t-1)z(t)}{1+\zeta(t)} \varepsilon(t|t-1)$$
2.  **Covariance Matrix Update:**
    $$P(t) = P(t-1) - \frac{P(t-1)z(t)z^{T}(t)P(t-1)}{1+\zeta(t)}$$
3.  **Residual Sum of Squares Update:**
    $$\nu(t)s^{2}(t) = \nu(t-1)s^{2}(t-1) + \frac{\varepsilon^{2}(t|t-1)}{1+\zeta(t)}$$
4.  **Degrees of Freedom Update:**
    $$\nu(t) = \nu(t-1) + 1$$

#### **Auxiliary Variables**
To simplify the calculation, we define the **prediction error** and the **normalized regressor norm**:
*   **Prediction Error:** $\varepsilon(t|t-1) = y(t) - z^{\mathsf{T}}(t)\hat{\theta}(t-1)$
*   **Scalar Gain Factor:** $\zeta(t) = z^{\mathsf{T}}(t)P(t-1)z(t)$

![](_page_74_Picture_10.jpeg)

![](_page_74_Picture_11.jpeg)

---

### **Mathematical Derivation of the Update**

The core of the recursive algorithm lies in the application of the Bayes formula to the likelihood function.

#### **The Likelihood Function**
The model assumes that the output $y(t)$ is normally distributed around the predicted value $z^T(t)\theta$ with variance $\sigma_e^2$:
$$\rho\left(y(t)|\theta,\sigma_e,u(t),\mathcal{D}^{t-1}\right) = \mathcal{N}(z^T(t)\theta,\sigma_e^2) \propto \sigma_e^{-1} \exp\left(-\frac{1}{2\sigma_e^2}(y(t)-z^T(t)\theta)^2\right)$$

#### **Application of Bayes Formula**
By substituting the likelihood and the prior into the Bayes relation, we obtain the functional form of the posterior:

$$\begin{split} \rho\left(\theta,\sigma_{e}|\mathcal{D}^{t}\right) &\propto \sigma_{e}^{-1}e^{-\frac{1}{2\sigma_{e}^{2}}(y(t)-z^{T}(t)\theta)^{T}(y(t)-z^{T}(t)\theta)} \\ &\times \sigma_{e}^{-\nu(t-1)} e^{-\frac{\nu(t-1)s^{2}(t-1)}{2\sigma_{e}^{2}}} \\ &\times \sigma_{e}^{-n}e^{-\frac{1}{2\sigma_{e}^{2}}(\theta-\hat{\theta}(t-1))^{T}P(t-1)^{-1}(\theta-\hat{\theta}(t-1))} \end{split}$$

By comparing the exponents of the left-hand side (the desired form at time $t$) and the right-hand side (the product of the likelihood and the prior at $t-1$), we can extract the algebraic recursions for the statistics $\hat{\theta}(t)$, $P(t)$, and $s^2(t)$.

![](_page_75_Picture_9.jpeg)