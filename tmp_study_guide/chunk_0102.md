# Markov chain MC method

The Markov Chain Monte Carlo (MCMC) method is a powerful class of algorithms used to sample from complex probability distributions. It is particularly useful when we are given a full set of conditional distributions and need to find the joint and marginal distributions that are otherwise analytically intractable.

### Analytic Foundation
In a bivariate system, the relationship between the marginal distributions $p(x)$ and $p(y)$ can be expressed through the following integral equations:

$$p(x) = \int p(x|y) p(y) dy, \qquad p(y) = \int p(y|x) p(x) dx$$

By substituting the expression for $p(y)$ into the equation for $p(x)$, we can derive a Fredholm integral equation of the second kind:

$$p(x) = \int p(x|y) \left( \int p(y|x')p(x') dx' \right) dy = \iint p(x|y)p(y|x')dy \ p(x')dx' = \int h(x,x')p(x')dx'$$

Here, $h(x, x')$ acts as a transition kernel. The solution to this equation corresponds to the steady-state (stationary) distribution of a Markov process.

### The Sampling Process
The MCMC approach solves this by simulating a chain of samples where each new sample depends only on the previous one:

1. Start with an initial sample $x^{(i)}$ from an initial guess or the prior $p(x^{(i)})$.
2. Draw a sample $y$ from the conditional distribution $p(y|x')$.
3. Draw the next sample $x^{(i+1)}$ from the conditional distribution $p(x|y)$.
4. Repeat the process until the chain converges to the target distribution.

### Generalization: The Gibbs Sampler
When dealing with $n$ variables, the **Gibbs Sampler** generalizes this logic. It updates each variable one by one, conditioned on the most recent values of all other variables. The expected value of a function $f$ over the joint distribution can be estimated using the ergodic theorem:

$$\mathcal{E}\left\{f(x_1,\ldots,x_n)\right\} = \lim_{k\to\infty} \frac{1}{k} \sum_{i=1}^k f(x_1^{(i)},\ldots,x_n^{(i)})$$

#### Estimating Marginal Distributions
To estimate the marginal probability density function $p(x_j)$, we can use the conditional density $p(x_j | X_j)$ as a kernel, where $X_j$ represents all variables except $x_j$:

$$p(x_j) \approx \frac{1}{N} \sum_{i=1}^{N} p(x_j^{(i)}|X_j^{(i)}), \quad X_j = \{x_1, \dots, x_{j-1}, x_{j+1}, \dots, x_n\}$$

This approach provides a smoother estimate of the marginal density than a simple histogram of the samples.

![](_page_180_Picture_12.jpeg)

![](_page_180_Picture_13.jpeg)