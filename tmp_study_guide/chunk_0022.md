# Parameters of normal distribution (2)

In this section, we extend the Bayesian framework to the case where both the mean $\mu$ and the standard deviation $\sigma$ of a normal distribution are unknown and must be estimated simultaneously.

### **Simultaneous estimate of $\mu$ and $\sigma$**

**Goal:** Our objective is to determine the joint posterior probability density function (p.d.f.) $p(\mu, \sigma | y)$ given a set of observations $y = [y_1, \dots, y_n]^T$.

#### **The Likelihood Function**
Assuming the data points $y_i$ are independent and identically distributed (i.i.d.) according to a normal distribution $\mathcal{N}(\mu, \sigma^2)$, the likelihood function is the product of the individual densities:

$$l(\mu, \sigma | y) = \prod_{i=1}^{n} \frac{1}{\sqrt{2\pi}\sigma} \exp\left(-\frac{(y_i - \mu)^2}{2\sigma^2}\right) \propto \sigma^{-n} \exp\left(-\frac{1}{2\sigma^2} \sum_{i=1}^{n} (y_i - \mu)^2\right)$$

To make this expression more manageable for Bayesian updating, we decompose the sum of squares in the exponent. By adding and subtracting the sample mean $\overline{y}$, we can rewrite the sum as:

$$\sum_{i=1}^{n} (y_i - \mu)^2 = \sum_{i=1}^{n} (y_i - \overline{y})^2 + n(\overline{y} - \mu)^2 = \nu s^2 + n(\overline{y} - \mu)^2$$

Here, we define the **sufficient statistics** that capture all the necessary information from the data:
*   **Sample Average:** $\overline{y} = \frac{1}{n} \sum_{i=1}^{n} y_i$
*   **Degrees of Freedom:** $\nu = n-1$
*   **Sample Variance:** $s^2 = \frac{1}{\nu} \sum_{i=1}^{n} (y_i - \overline{y})^2$

#### **Resulting Likelihood Form**
Substituting these statistics back into the likelihood expression, we obtain a form that clearly separates the influence of the mean and the variance:

$$l(\mu, \sigma | y) \propto \sigma^{-n} \exp\left(-\frac{1}{2} \frac{(\mu - \overline{y})^2}{\sigma^2/n} - \frac{\nu s^2}{2\sigma^2}\right)$$

This structure is particularly useful because the first term in the exponent resembles a normal distribution for $\mu$ (conditioned on $\sigma$), while the second term relates to the Inverse-Gamma distribution family for $\sigma^2$.

#### **Prior Selection**
To perform Bayesian inference without incorporating external subjective information, we use a **non-informative prior**. Following the logic of Jeffrey's rule for location and scale parameters:
*   For the location parameter $\mu$, we assume a flat prior: $p(\mu | \sigma) \propto \text{const}$.
*   For the scale parameter $\sigma$, we assume a prior proportional to its reciprocal: $p(\sigma) \propto \sigma^{-1}$.

Combining these, the joint prior is $p(\mu, \sigma) \propto \sigma^{-1}$. This choice ensures that the posterior is dominated by the data rather than the initial assumptions.

![](_page_42_Picture_12.jpeg)

![](_page_42_Picture_13.jpeg)