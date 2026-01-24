# Bayesian Inference (2)

### Conjugated Priors
In Bayesian estimation, we leverage the naturally recursive character of the update rule:
$$p(\theta|y_1, y_2, \ldots, y_n) \propto l(\theta|y_n) p(\theta|y_1, y_2, \ldots, y_{n-1})$$

A **conjugated prior** is a specific choice of prior distribution such that the posterior distribution belongs to the same functional family as the prior. This property is highly desirable for several reasons:
*   **Analytic Invariance**: The mathematical form of the p.d.f. is preserved throughout the update process. For example, if we use a Normal prior with a Normal likelihood, the resulting posterior is also a Normal distribution.
*   **Computational Efficiency**: The **functional** recursion (updating the entire shape of the distribution) is reduced to a simple **algebraic** recursion on the parameters of the distribution (e.g., updating only the mean and covariance).

### The Chain Rule of Probability
The chain rule allows for the composition of uncertain information without requiring the assumption of independence between samples. This is particularly vital for time-dependent variables or dynamical systems:
$$\begin{aligned}
\rho(y_2, y_1) &= \rho(y_2|y_1) \rho(y_1) \\
\rho(y_3, y_2, y_1) &= \rho(y_3|y_2, y_1) \rho(y_2|y_1) \rho(y_1) \\
\rho(y_n, y_{n-1}, \dots, y_1) &= \prod_{k=2}^{n} \rho(y_k|y_{k-1}, \dots, y_1) \cdot \rho(y_1)
\end{aligned}$$

![](_page_38_Picture_11.jpeg)
![](_page_38_Picture_12.jpeg)

---

### Supplementary Reading: Selection of Prior p.d.f.
The core criticism of Bayesian statistics often centers on the subjectivity of the prior. However, several principles guide rational prior selection:

*   **Non-informative Priors**: These are "locally flat" relative to the likelihood function, representing a state of total ignorance.
*   **Principle of Stable Estimation**: As data accumulates, the information in the likelihood will eventually dominate the prior. If the prior continues to dominate after many samples, the experiment likely lacks sufficient informative power.
*   **Informative Priors**: These are used when prior knowledge exists (e.g., physical constraints). They can significantly improve transient properties, such as in parameter identification for adaptive control.

#### Jeffrey's Rule
To address the problem of parameterization (e.g., whether to estimate $\sigma$ or $\sigma^2$), Jeffrey proposed that the prior should be invariant to reparameterization. He suggested the prior p.d.f. be proportional to the square root of the **Fisher Information** $F(\theta)$:
$$p(\theta) \propto F(\theta)^{1/2} = \mathcal{E} \left\{ -\frac{\partial^2 \ln l(\theta|y)}{\partial \theta^2} \right\}^{1/2}$$
A prior is truly uniform only if the likelihood is "data translated" (its shape does not change with $\theta$, only its location).

### Example: Prior for a Scale Parameter
Assume we observe $y \sim \mathcal{N}(\mu, \sigma^2)$ where the mean $\mu$ is known, and we wish to estimate the scale parameter $\sigma$. The likelihood function is:
$$l(\sigma|\mu,y) \propto \sigma^{-n} e^{-\frac{ns^2}{2\sigma^2}}, \qquad s^2 = \frac{1}{n} \sum_{i=1}^{n} (y_i - \mu)^2$$
This likelihood is not "data translated" in $\sigma$. However, if we transform the coordinates to $\ln \sigma$, the likelihood $l(\ln \sigma | \mu, y)$ becomes data translated. Applying the transformation theorem:
$$p(\ln \sigma | \mu) \propto 1 \quad \to \quad p(\sigma | \mu) = p(\ln \sigma | \mu) \left| \frac{d \ln \sigma}{d\sigma} \right| \propto \sigma^{-1}$$
Thus, the non-informative prior for a scale parameter is $p(\sigma) \propto 1/\sigma$.

![](_page_40_Picture_12.jpeg)

---

## Parameters of the Normal Distribution

### Estimation of $\mu$ for known $\sigma$
**Goal:** Determine the posterior $p(\mu| \sigma, y)$ given $n$ observations from $\mathcal{N}(\mu, \sigma^2)$.

1.  **Likelihood Function**: The joint probability of the data, centered around the sample average $\overline{y}$:
    $$l(\mu|\sigma,y) \propto \exp\left(-\frac{(\mu-\overline{y})^2}{2\sigma^2/n}\right)$$
2.  **Prior**: Using a non-informative prior $p(\mu|\sigma) \propto \text{const}$.
3.  **Posterior**: Multiplying the prior and likelihood yields a Normal distribution:
    $$p(\mu|\sigma,y) = \mathcal{N}\left(\overline{y}, \frac{\sigma^2}{n}\right)$$
This result aligns with classical statistics, where the sample average $\overline{y}$ is the best estimate of the mean, and its uncertainty decreases with $1/\sqrt{n}$.

![](_page_41_Picture_11.jpeg)