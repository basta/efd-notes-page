# Parameters of normal distribution (3)

### **Marginal c.p.d.f. of** $\mu$ **for unknown** $\sigma$

In many practical scenarios, we are primarily interested in estimating the mean $\mu$, while the variance $\sigma^2$ is unknown. In Bayesian statistics, $\sigma$ is treated as a **nuisance parameter**—a variable that is necessary for the model but not the primary object of inference. To obtain the distribution of $\mu$ alone, we must "marginalize out" the uncertainty regarding $\sigma$.

The marginal posterior probability density function (p.d.f.) for $\mu$ is calculated by integrating the joint posterior $p(\mu, \sigma | y)$ over all possible values of $\sigma$:

$$p(\mu|y) = \int_0^\infty p(\mu|\sigma, y) p(\sigma|y) d\sigma$$

By substituting the normal conditional distribution for $\mu$ and the inverse-chi-squared marginal distribution for $\sigma$ (derived in the previous section) and applying the standard integral identities, we arrive at the normalized posterior for $\mu$:

#### **Normalized Posterior of** $\mu$

$$p(\mu|y) = \left(\frac{n}{\nu s^2}\right)^{1/2} \frac{\Gamma((\nu+1)/2)}{\Gamma(\nu/2)\Gamma(1/2)} \left[1 + \frac{n(\mu-\overline{y})^2}{\nu s^2}\right]^{-\frac{\nu+1}{2}}$$

This expression reveals that the uncertainty in $\mu$ follows a **Student t-distribution**. Specifically, the transformed variable $t$ follows a standard Student t-distribution with $\nu = n-1$ degrees of freedom:

$$t = \frac{\mu - \overline{y}}{s / \sqrt{n}} \sim \text{Student } t(\nu)$$

The p.d.f. of this $t$ variable is defined as:

$$p(t) = t\left(\overline{y}, s^2/n, \nu\right) = \left(\frac{1}{\nu}\right)^{1/2} \frac{\Gamma\left((\nu+1)/2\right)}{\Gamma(\nu/2)\Gamma(1/2)} \left[1 + \frac{t^2}{\nu}\right]^{-\frac{\nu+1}{2}}$$

### **Properties and Approximations**

The Student t-distribution is characterized by "heavier tails" than the normal distribution, reflecting the added uncertainty caused by not knowing the true variance $\sigma^2$. 

- **Convergence to Normal:** As the number of observations increases, our estimate of the variance becomes more precise. For large $\nu$ (typically $\nu > 10$), the Student t-distribution can be closely approximated by a normal distribution.
- **Mathematical Limit:** This relationship is rooted in the fundamental limit:
  $$e^{x} = \lim_{n \to \infty} \left( 1 + \frac{x}{n} \right)^{n}$$
  As $\nu \to \infty$, the term $[1 + \frac{t^2}{\nu}]^{-\frac{\nu+1}{2}}$ approaches the exponential form of the Gaussian kernel $e^{-t^2/2}$.

![](_page_44_Picture_11.jpeg)

![](_page_44_Picture_12.jpeg)