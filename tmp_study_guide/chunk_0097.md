# Generators of (pseudo)random numbers (4)

### Resampling Methods

In many practical control and estimation problems, we need to generate samples from a target probability density function (p.d.f.) $f(x)$ that is difficult to sample from directly. However, we may have access to a simpler "proposal" distribution $g(x)$ from which we can easily generate samples. Resampling methods allow us to transform samples from $g(x)$ into samples that effectively represent $f(x)$.

*   **Available sample:** $x_i \sim g(x)$ (the proposal distribution).
*   **Required sample:** $x_i \sim \frac{f(x)}{\int f(x) dx}$, where $f(x) \geq 0$ is the target distribution (not necessarily normalized).

### Accept-Reject Algorithm

The Accept-Reject algorithm is a fundamental technique for generating samples from a target distribution $f(x)$ by using a proposal distribution $g(x)$ and a scaling constant $M$.

**Assumption:** There exists a finite constant $M$ such that $\frac{f(x)}{g(x)} \leq M$ for all $x$ in the support of $f$. This ensures that the "envelope" $M \cdot g(x)$ always stays above $f(x)$.

**The Algorithm:**
1.  Generate a candidate sample $x$ from the proposal distribution $g(x)$.
2.  Generate a uniform random variable $u \sim U(0, 1)$.
3.  **Acceptance Criterion:** If $u \leq \frac{f(x)}{M \cdot g(x)}$, accept the sample and set $y_i = x$. Otherwise, reject $x$ and return to step (1).

#### Example: Sampling a Gaussian from a Uniform Distribution
*   **Available:** Samples $x_i \sim U(-1.5, 1.5)$.
*   **Target:** $f(x) = \exp(-x^2/2)$ (unnormalized Gaussian).
*   **Constant:** By analysis, $f(x)/g(x) \leq 3$ (setting $M=3$).
*   **Result:** Samples are accepted if $u \leq \frac{f(x)}{3 \cdot g(x)}$, effectively "carving" the Gaussian shape out of the uniform distribution.

![](_page_167_Figure_15.jpeg)
![](_page_167_Picture_16.jpeg)
![](_page_167_Picture_17.jpeg)

---

### Numerical Integration

#### Monte Carlo Quadrature - Direct Sampling
Monte Carlo integration allows us to approximate complex integrals (often representing expected values) by using random samples. To calculate the mean value of a function $f(\theta)$ where $\theta$ follows the distribution $p(\theta)$:

$$I_N(f) = \mathcal{E}\{f\} = \int f(\theta) p(\theta) d\theta$$

By using an empirical p.d.f. (representing the distribution as a sum of Dirac deltas at sample points $\theta_i$) and applying the "sifting property" of the Dirac delta, we arrive at the sample mean:

$$\hat{I}_N(f) = \frac{1}{N} \sum_{i=1}^N f(\theta_i)$$

#### Example: Estimation of $\pi$
We can estimate the value of $\pi$ by integrating the area of a unit circle. Specifically, $\pi$ can be expressed as:
$$\pi = 4 \int_0^1 \sqrt{1 - x^2} \ p(x) dx \approx \frac{4}{N} \sum_{i=1}^N \sqrt{1 - x_i^2}$$
where $x_i$ are samples drawn from a uniform distribution $U(0,1)$.

![](_page_168_Figure_10.jpeg)
![](_page_168_Figure_11.jpeg)
![](_page_168_Picture_12.jpeg)
![](_page_168_Picture_13.jpeg)

---

## Numerical Integration (2)

### Monte Carlo Quadrature – Weighted Sampling
In many cases, we cannot sample from the target distribution $p(\theta)$ directly, or $p(\theta)$ is not efficient for integration. Instead, we sample from an importance distribution $q(\theta)$ and correct the discrepancy using **importance weights**.

**Weight Definition:**
$$w_i = \frac{p(\theta_i)}{q(\theta_i)} \geq 0$$
This assumes that the support of $q(\theta)$ covers the support of $p(\theta)$ (i.e., $q(\theta) > 0$ whenever $p(\theta) > 0$).

**The Weighted Integral:**
$$I_N(f) = \int f(\theta)p(\theta)d\theta = \int f(\theta) \frac{p(\theta)}{q(\theta)} q(\theta)d\theta = \int f(\theta) w(\theta) q(\theta)d\theta$$

Using the empirical p.d.f. of the samples drawn from $q(\cdot)$, the estimate becomes:
$$\hat{I}_{N}(f) = \frac{1}{N} \sum_{i=1}^{N} w(\theta_{i})f(\theta_{i})$$

This approach is the foundation for **Importance Sampling**, which is widely used in particle filtering and Bayesian estimation when the posterior distribution is analytically intractable.

![](_page_169_Picture_10.jpeg)