# <span id="page-158-0"></span>**7. Monte Carlo implementation of bayesian methods**

In many practical control and estimation problems, the analytical solutions provided by the Kalman Filter or simple Hidden Markov Models are insufficient, particularly when dealing with non-Gaussian noise or highly non-linear dynamics. Monte Carlo methods provide a powerful numerical framework for implementing Bayesian inference by representing probability distributions as sets of discrete samples.

![](_page_158_Picture_1.jpeg)

### Optimal decision problem

The core of Bayesian estimation is the **Optimal Decision Problem**. We seek a decision $d$ (such as a state estimate or a control action) that minimizes the expected cost based on our current knowledge of the system.

#### Decision based on observed data $y$
The optimal decision $d^*(y)$ is found by minimizing the expected loss over the posterior distribution of the unknown parameters $\theta$:

$$d^*(y) = \arg\min_{d} \int L(\theta, d) p(\theta|y) \ d\theta$$

Where:
*   **Utility/Loss Function**: We define a function $U(\theta, d)$ to maximize utility or $L(\theta, d)$ to minimize loss. This function quantifies the "cost" of making decision $d$ when the true state is $\theta$.
*   **Decision $d$**: The variable to be optimized (e.g., the estimated state $\hat{x}$).
*   **Posterior Distribution $p(\theta|y)$**: This represents our updated information about the unknown parameter $\theta$ after observing data $y$.

#### Example: Minimum Square (MS) Estimation
In parameter estimation, if we choose the decision $d$ to be our estimate $\hat{\theta}$ and use a quadratic loss function $L(\theta, \hat{\theta}) = (\theta - \hat{\theta})^2$, the optimization becomes:

$$\hat{\theta}^*(y) = \arg\min_{\hat{\theta}} \int (\theta - \hat{\theta})^2 p(\theta|y) \ d\theta = \mathcal{E}\{\theta|y\}$$

This result shows that for a Mean Square Error (MSE) criterion, the optimal Bayesian estimate is simply the **conditional expectation** (the mean) of the posterior distribution.

#### Where are the problems?
While the theory is straightforward, two major computational hurdles arise in practice:

1.  **Calculation of the posterior c.p.d.f.**: Using Bayes' formula, we know that:
    $$p(\theta|y) \propto p(y|\theta) p(\theta)$$
    To make this a valid probability density, we must calculate the normalization constant (the evidence):
    $$p(\theta|y) = \frac{p(y|\theta)p(\theta)}{\int p(y|\theta)p(\theta)d\theta}$$
2.  **Multivariate Integration**: When the dimension of $\theta$ exceeds 3 or 4, standard numerical integration (quadrature) becomes computationally prohibitive due to the "curse of dimensionality."

#### The Monte Carlo Solution
To overcome these integration challenges, we represent the continuous conditional probability density function (c.p.d.f.) by a discrete set of random samples (particles):
$$y_i \sim p(y|\mathcal{D}), \quad i = 1, \dots, N$$
By using a sufficiently large number of samples $N$, we can approximate complex integrals as simple empirical averages, allowing us to handle non-linearities and non-Gaussianities that would otherwise be intractable.

![](_page_159_Picture_15.jpeg)

![](_page_159_Picture_16.jpeg)