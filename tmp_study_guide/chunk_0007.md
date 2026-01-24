# Some well-known statistics (2)

In statistical estimation, we distinguish between the theoretical parameters of a population and the statistics calculated from a finite sample. Two of the most critical statistics are those used to estimate the variance ($\sigma^2$) of a distribution.

### Sample Moments and Variance

#### Sample 2nd Central Moment
The sample second central moment, denoted as $C_2$, is a measure of the spread of the data around the sample mean $\bar{X}$. It is defined as:

$$C_2 = \frac{1}{n} \sum_{i=1}^{n} (X_i - \bar{X})^2$$

While intuitive, $C_2$ is a **biased estimate** of the true population variance $\sigma^2$. Specifically, its expected value is:
$$\mathcal{E}\left\{C_2\right\} = \frac{n-1}{n} \sigma^2$$
As $n \to \infty$, the bias disappears, making it asymptotically unbiased.

#### Sample Variance
To obtain an **unbiased estimate** of the population variance $\sigma^2$, we use the sample variance $s^2$. This version applies Bessel's correction by dividing by $n-1$ instead of $n$:

$$s^{2} = \frac{1}{n-1} \sum_{i=1}^{n} (X_{i} - \bar{X})^{2}$$

The expected value of this statistic is exactly the population variance:
$$\mathcal{E}\left\{s^{2}\right\} = \sigma^{2}$$

#### Useful Identity
A helpful algebraic identity for deriving these properties relates the deviations from the sample mean to the deviations from the true population mean $\mu$:

$$\sum_{i=1}^{n} (X_i - \bar{X})^2 = \sum_{i=1}^{n} (X_i - \mu)^2 - n(\bar{X} - \mu)^2$$

This is analogous to the **Huygens-Steiner parallel axis theorem** in classical mechanics, where $\bar{X}$ represents the center of gravity of the data points.

---

### Normal (Gaussian) Distribution

The Normal distribution is the cornerstone of classical control theory and estimation due to its unique mathematical properties.

#### Normal Probability Density Function (PDF)
If a random variable $X_i$ follows a normal distribution with mean $\mu$ and variance $\sigma^2$, its PDF is given by:

$$X_i \sim \mathcal{N}\left(\mu, \sigma^2\right) \quad \rightarrow \quad p(x) = \frac{1}{\sqrt{2\pi} \, \sigma} \, e^{-\frac{(x-\mu)^2}{2\sigma^2}}$$

The distribution is entirely characterized by its first two moments: the mean $\mu$ (location) and the variance $\sigma^2$ (scale).

#### Why is it so frequently used?
1.  **Mathematical Convenience**: The Gaussian distribution is closed under linear operations. For example, the sum of independent Gaussian variables is also Gaussian:
    $$\sum_{i=1}^{n} X_{i} \sim \mathcal{N}\left(n\mu, n\sigma^{2}\right)$$
    The sample mean likewise follows a Gaussian distribution:
    $$\bar{X} \sim \mathcal{N}\left(\mu, \sigma^{2}/n\right)$$

2.  **Foundation for Other Distributions**: Many other important statistical distributions are derived from Gaussian variables. For instance, if $X_i$ are independent standard normal variables $\mathcal{N}(0,1)$, the sum of their squares follows a **Chi-square distribution** with $n$ degrees of freedom:
    $$X_i \sim \mathcal{N}(0,1) \rightarrow \sum_{i=1}^{n} X_i^2 \sim \chi_n^2(x) = \frac{1}{2^{\frac{n}{2}} \Gamma(\frac{n}{2})} x^{\frac{n}{2}-1} e^{-\frac{x}{2}}$$
    Other derived distributions include the Student's T-distribution and the Fisher F-distribution, which are essential for hypothesis testing.

![](_page_10_Picture_9.jpeg)