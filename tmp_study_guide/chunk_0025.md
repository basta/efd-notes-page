# Sufficient statistics

In Bayesian estimation, we are often interested in how data informs our knowledge of unknown parameters. The concept of sufficient statistics allows us to compress large datasets into a small set of values without losing any information relevant to the estimation of those parameters.

#### **The Likelihood Principle**

The Likelihood Principle states that all the information about the unknown parameter $\theta$ contained within the data $y$ is provided by the likelihood function $l(\theta|y)$. In the Bayesian framework, the data affects the posterior distribution only through this likelihood:

$$p(\theta|y) \propto l(\theta|y) p(\theta)$$

This implies that if two different datasets yield proportional likelihood functions, they will result in the same posterior distribution for any given prior.

#### **Sufficient Statistics for the Normal Distribution**

When dealing with normally distributed data, we can identify specific summaries of the data that capture all necessary information for estimation.

1.  **Estimate of $\mu$ for a known $\sigma$:**
    If the variance $\sigma^2$ is known, the likelihood function for the mean $\mu$ is:
    $$l(\mu|\sigma,y) \propto \exp\left(-\frac{(\mu-\overline{y})^2}{2\sigma^2/n}\right)$$
    Here, the **sufficient statistics** for $\mu$ are the pair $\{\overline{y}, n\}$ (the sample mean and the number of observations). Any dataset with the same mean and size will result in the same estimate for $\mu$.

2.  **Simultaneous estimate of $\mu$ and $\sigma$:**
    When both parameters are unknown, the joint likelihood function is:
    $$l(\mu,\sigma|\,y) \propto \sigma^{-(n+1)} \exp\left(-\frac{(\mu-\overline{y})^2}{2\sigma^2/n} - \frac{(n-1)s^2}{2\sigma^2}\right)$$
    In this case, the **sufficient statistics** for the pair $\{\mu, \sigma\}$ are the triple $\{\overline{y}, s^2, n\}$, where $s^2$ is the sample variance.

**Key Properties:**
*   **Minimal Sufficient Statistic:** This is the statistic with the smallest possible dimension that still captures all information from the data.
*   **Finite Sufficient Statistics:** The existence of finite sufficient statistics is crucial for real-time estimation. It allows for the **accumulation of information** from an ever-growing stream of data within a limited memory space. This concept is mathematically analogous to the "state" of a dynamic system, where the current state summarizes all past inputs necessary to predict the future.

---

### Informative prior for $\sigma$

In many practical scenarios, we possess prior knowledge about the noise or variance of a system before observing new data. We can model this using an informative prior.

#### **A Thought Experiment**
Imagine we define our prior distribution $p(\sigma)$ based on a previous auxiliary dataset $y_a = [y_{a1}, \ldots, y_{a_{n_a}}]^T$. The posterior derived from that auxiliary data becomes our informative prior for the current experiment:

$$p(\sigma) = p(\sigma | y_a) \propto \sigma^{-(\nu_a + 1)} \exp\left(-\frac{\nu_a s_a^2}{2\sigma^2}\right)$$

#### **Updating with Actual Data**
When we combine this informative prior with new observed data $y$ (characterized by $\nu$ and $s^2$), the resulting posterior distribution for $\sigma$ maintains the same functional form:

$$p(\sigma|y) \propto \sigma^{-(\nu_a + \nu + 1)} \exp\left(-\frac{\nu_a s_a^2 + \nu s^2}{2\sigma^2}\right) = \sigma^{-(\overline{\nu} + 1)} \exp\left(-\frac{\overline{\nu} \, \overline{s}^2}{2\sigma^2}\right)$$

The updated parameters of the distribution are calculated as follows:
*   **Updated Degrees of Freedom:** $\overline{\nu} = \nu_a + \nu$
*   **Updated Combined Variance:** $\overline{\nu}\,\overline{s}^2 = \nu_a s_a^2 + \nu s^2$

Note that while the marginal distribution for $\sigma$ is updated, the functional form of the conditional distribution $p(\mu | \sigma, y)$ remains a normal distribution centered at the sample mean.

**Interpretation of Initial Statistics:**
*   $\nu_a$: Represents the **prior accuracy** or the "weight" given to prior knowledge, expressed in terms of an equivalent sample size.
*   $s_a^2$: Represents the **prior information** regarding the expected value of the variance $\sigma^2$.

![](_page_46_Picture_14.jpeg)