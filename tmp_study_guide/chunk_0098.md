# Numerical integration (3)

### **Example: Posterior mean (importance sampling)**

In Bayesian estimation, we often need to compute the posterior mean of a function $f(\theta)$. When the posterior distribution $p(\theta|y)$ is complex, we can use **Importance Sampling**. This technique allows us to estimate properties of a target distribution by using samples generated from a different, simpler distribution (the proposal or prior distribution).

To calculate the posterior mean using samples $\theta_i$ drawn from the prior distribution $p(\theta)$, we use the following derivation:

$$\hat{I}_{N}(f) = \mathcal{E}\left\{f(\theta)|y\right\} = \int f(\theta)p(\theta|y) \ d\theta = \int f(\theta) \frac{p(\theta|y)}{p(\theta)} \ p(\theta) \ d\theta \approx \frac{1}{N} \sum_{i=1}^{N} w_{i} \ f(\theta_{i})$$

#### Deriving the Weights
The ratio between the posterior and the prior can be simplified using Bayes' rule. We define the unnormalized weights $\omega_i$ based on the likelihood:

$$w_i = \frac{p(\theta_i|y)}{p(\theta_i)} = \frac{p(y|\theta_i)}{p(y)}$$

Since the evidence $p(y)$ is often unknown or difficult to calculate, we normalize the estimate by expressing $p(y)$ as an integral over the parameter space:

$$\hat{I}_{N}(f) = \int f(\theta) \frac{p(y|\theta)}{p(y)} p(\theta) d\theta = \frac{\int f(\theta)p(y|\theta)p(\theta) d\theta}{p(y)} = \frac{\int f(\theta)p(y|\theta)p(\theta) d\theta}{\int p(y|\theta)p(\theta) d\theta}$$

By applying the Monte Carlo approximation to both the numerator and the denominator, the constant $1/N$ cancels out:

$$\hat{I}_{N}(f) = \frac{\frac{1}{N} \sum_{i=1}^{N} \omega_{i}f(\theta_{i})}{\frac{1}{N} \sum_{i=1}^{N} \omega_{i}} = \sum_{i=1}^{N} w_{i}f(\theta_{i})$$

#### Resulting weights: Normalized Likelihood (Importance Function)
The final normalized weights $w_i$ represent the relative "importance" of each sample. They are calculated by dividing the likelihood of each sample by the sum of the likelihoods of all samples:

$$w_i = \frac{\omega_i}{\sum_{j=1}^N \omega_j} = \frac{p(y|\theta_i)}{\sum_j p(y|\theta_j)}$$

In this framework, the **samples** $\theta^i$ are provided by the prior $p(\theta)$, while the **weights** are determined by the likelihood $p(y|\theta)$. This effectively "shifts" the prior samples to represent the posterior distribution.

![](_page_170_Picture_11.jpeg)

![](_page_170_Picture_12.jpeg)