# Normal (Gaussian) distribution (2)

The Normal distribution is the cornerstone of classical estimation theory. Its prevalence in both natural phenomena and engineering applications is not accidental; it is supported by empirical observation and rigorous mathematical theory.

### Why is the Normal Distribution Ubiquitous?
*   **Empirical Evidence:** Many physical processes, measurement errors, and biological traits naturally follow a "bell curve" distribution.
*   **Central Limit Theorem (CLT):** This is the primary theoretical justification. It states that the sum of many independent random variables tends toward a Normal distribution, regardless of the original distribution of the individual variables.

---

### The Central Limit Theorem (CLT)

The CLT explains why the Gaussian distribution appears so frequently in systems where multiple small, independent effects contribute to a final observed outcome.

#### **Theorem (Lindeberg/Lévy) – Continuous Random Variables**
Let $\{X_1, X_2, \dots, X_n\}$ be a sequence of independent and identically distributed (i.i.d.) random variables with a finite mean $E\{X_i\} = \mu$ and a finite variance $\text{cov}\{X_i\} = \sigma^2$. 

As the sample size $n$ increases ($n \to \infty$), the normalized sum $Y_n$ converges in distribution to a standard normal distribution:
$$Y_n = \frac{1}{\sqrt{n}} \sum_{i=1}^n \frac{X_i - \mu}{\sigma} \rightarrow \mathcal{N}(0,1)$$

Alternatively, the sum of these variables converges to a normal distribution scaled by the number of samples:
$$\sum_{i=1}^n X_i \rightarrow \mathcal{N}\left(n\mu, n\sigma^2\right)$$

#### **Theorem (Moivre/Laplace) – Discrete Random Variables**
This is a special case of the CLT applied to Bernoulli trials (discrete outcomes). Let $\{X_1, X_2, \dots, X_n\}$ be i.i.d. random variables following an alternative (Bernoulli) distribution where:
*   $P\{X_i = 1\} = q$ (Success)
*   $P\{X_i = 0\} = 1 - q$ (Failure)
*   $E\{X_i\} = q$
*   $\text{cov}\{X_i\} = q(1 - q)$

As $n \to \infty$, the standardized sum $Y_n$ converges to:
$$Y_n = \frac{1}{\sqrt{n}} \sum_{i=1}^n \frac{X_i - q}{\sqrt{q(1-q)}} \rightarrow \mathcal{N}(0,1)$$

Or, expressed as the sum of successes:
$$\sum_{i=1}^n X_i \rightarrow \mathcal{N}\left( nq, nq(1-q) \right)$$

This theorem justifies using the Normal distribution to approximate the Binomial distribution when the number of trials is large.