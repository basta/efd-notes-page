# Normal (Gaussian) distribution (3)

### The Maximum Entropy Principle

In estimation and information theory, the **Entropy** $H(x)$ serves as a quantitative measure of the uncertainty or "randomness" associated with a given probability density function (p.d.f.) $f(x)$. It is defined as:

$$H(x) = -\int f(x) \ln f(x) \, dx$$

The **Maximum Entropy Principle** states that if we only know certain moments of a distribution (such as the mean or variance), the most "honest" p.d.f. to assume is the one that maximizes entropy. This distribution contains the minimum amount of "added" or subjective information beyond the given constraints.

For a set of given moment constraints $\mathcal{E}\{g_i(x)\} = \int g_i(x)f(x)dx$ for $i = 1, \ldots, n$, the p.d.f. that maximizes entropy takes the exponential form:

$$f(x) = K \exp \left(-\sum_{i=1}^{n} \lambda_i g_i(x)\right)$$

#### Example: Why the Normal Distribution?
The Gaussian distribution is the maximum entropy distribution for a specified mean and variance.
*   **Case 1:** If we only know the second raw moment $\mathcal{E}\{x^{2}\} = M_{2}$, the maximum entropy p.d.f. is $f(x) = K e^{-\lambda_{1}x^{2}}$, which is a zero-mean Normal distribution $\mathcal{N}(0, M_{2})$.
*   **Case 2:** If we know the variance (second central moment) $\mathcal{E}\{(x - \mu)^{2}\} = C_{2}$, the resulting p.d.f. is $f(x) = K e^{-\lambda_{1}(x - \mu)^{2}}$, which is the general Normal distribution $\mathcal{N}(\mu, C_{2})$.

![](_page_12_Picture_11.jpeg)

---

### Multivariable Gaussian Bell Function

When dealing with a vector of random variables $X \in \mathbb{R}^n$, the multivariable normal p.d.f. is defined by the mean vector $\hat{x}$ and the covariance matrix $P$:

$$p(x) = \frac{1}{(2\pi)^{n/2} \sqrt{\det P}} \exp\left\{-\frac{1}{2}(x-\hat{x})^T P^{-1}(x-\hat{x})\right\}$$

#### The Covariance Ellipsoid
The surfaces of constant probability density are defined by the quadratic form in the exponent. We define the **covariance ellipsoid** $E_{\alpha}$ as the set:

$$E_{\alpha} = \left\{ x \mid (x - \hat{x})^{T} P^{-1} (x - \hat{x}) \leq \alpha \right\}$$

The scalar random variable $y = (x-\hat{x})^T P^{-1}(x-\hat{x})$ follows a **Chi-square distribution** with $n$ degrees of freedom ($\chi_n^2$). 

**Proof Sketch:**
1. Transform the variable: Let $y = P^{-1/2}(x - \hat{x})$. Since $x$ is Gaussian, $y$ is also Gaussian.
2. Calculate the covariance of $y$:
   $$\text{cov}\{y\} = \mathcal{E} \left\{ P^{-1/2} (x - \hat{x}) (x - \hat{x})^T P^{-T/2} \right\} = P^{-1/2} P P^{-1/2} = I_n$$
3. Thus, $y \sim \mathcal{N}(0, I_n)$, meaning $y$ consists of independent standard normal variables.
4. The sum of squares $y^T y = \sum_{i=1}^n y_i^2$ by definition follows the $\chi_n^2$ distribution.

#### Probability Content
The probability that a realization of the random vector $x$ falls within the ellipsoid $E_{\alpha}$ is given by the cumulative distribution function (CDF) of the Chi-square distribution:

$$Pr\left\{x\in E_{\alpha}\right\} = F_{\chi_{n}^{2}}(\alpha)$$

For the specific case of $n=2$ (bivariate Gaussian), the $\chi_2^2$ p.d.f. simplifies to an exponential form:
$$\chi_2^2(y) = \frac{1}{2} e^{-\frac{y}{2}}$$

<span style="display:block;text-align:center;">
![](_page_13_Figure_12.jpeg)
![](_page_13_Picture_13.jpeg)
![](_page_13_Picture_14.jpeg)
</span>