# Generators of (pseudo)random numbers (2)

While uniform random number generators serve as the foundation for stochastic simulations, many applications in control theory and estimation require samples from a **Normal (Gaussian) distribution**, $\mathcal{N}(0,1)$. Since the inverse cumulative distribution function of a Gaussian does not have a closed-form expression, we employ specific transformation techniques.

### The Box-Muller Method

The Box-Muller transform is an efficient algorithm used to generate pairs of independent, standard normally distributed random numbers from a source of uniformly distributed numbers.

1.  **Generate Uniform Samples**: Obtain two independent samples $u_1, u_2$ from a uniform distribution $U(0, 1)$.
2.  **Transformation**: Calculate two independent samples $x_1, x_2 \sim \mathcal{N}(0, 1)$ using the following polar coordinate transformation:
    $$x_1 = \sqrt{-2 \ln u_1} \cos(2\pi u_2)$$
    $$x_2 = \sqrt{-2 \ln u_1} \sin(2\pi u_2)$$

This method is mathematically exact; if $u_1$ and $u_2$ are truly uniform and independent, $x_1$ and $x_2$ will be perfectly Gaussian.

### Application of the Central Limit Theorem (CLT)

An alternative approach relies on the **Central Limit Theorem**, which states that the sum of a large number of independent and identically distributed (i.i.d.) random variables tends toward a normal distribution, regardless of the original distribution.

For a set of i.i.d. samples $x_i$ with mean $\mu$ and variance $\sigma^2$, the normalized sum $y_n$ converges to a standard normal distribution:
$$y_n = \frac{\sum_{i=1}^n x_i - n\mu}{\sigma\sqrt{n}} \longrightarrow \mathcal{N}(0,1)$$

#### Practical Implementation: The $n=12$ Rule
A common "quick" approximation uses $n=12$ samples from a uniform distribution $u \sim U(0,1)$. For a uniform distribution on $[0,1]$, the mean is $\mu = \frac{1}{2}$ and the variance is $\sigma^2 = \frac{1}{12}$. Substituting these into the CLT formula:

$$y_{12} = \frac{\sum_{i=1}^{12} x_i - 12 \left(\frac{1}{2}\right)}{\sqrt{\frac{1}{12}} \sqrt{12}} = \sum_{i=1}^{12} x_i - 6 \longrightarrow \mathcal{N}(0,1)$$

**Characteristics of the CLT Approximation:**
*   **Simplicity**: The formula is extremely simple to implement, requiring only 12 additions and one subtraction.
*   **Finite Support**: Unlike a true Gaussian distribution, this approximation has truncated tails. Since the maximum value of $\sum x_i$ is 12 and the minimum is 0, the resulting $y_{12}$ is strictly bounded within $[-6, 6]$.
*   **Accuracy**: While the tails are missing, the probability of a true standard normal variable exceeding $|y| > 6$ is less than $10^{-8}$, making this approximation sufficient for many practical engineering applications.

![](_page_165_Picture_13.jpeg)

![](_page_165_Picture_14.jpeg)