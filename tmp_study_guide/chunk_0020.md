# Bayesian Inference: The Unfair Coin Example

In Bayesian statistics, we treat parameters not as fixed unknown constants, but as random variables characterized by probability distributions. This example demonstrates how we update our belief about a parameter $\theta$ as we collect data from a series of Bernoulli trials (coin tosses).

#### **1. The Application of the Bayesian Formula**

Consider an experiment where the outcome $y$ is binary, $y \in \{0, 1\}$, representing a "tail" or a "head."

*   **The Model (Likelihood):** 
    The probability of observing a specific outcome $y$ given the parameter $\theta$ (the probability of heads) is defined by the Bernoulli distribution:
    $$P\{Y=1\} = \theta, \quad P\{Y=0\} = 1-\theta \implies p(y|\theta) = \theta^{y}(1-\theta)^{1-y}$$

*   **The Prior PDF:**
    Before observing any data, we assume a **non-informative prior**. If we have no reason to favor any specific value of $\theta$, we use a uniform distribution over the valid range $[0, 1]$:
    $$p(\theta) = 1 \quad \text{for } \theta \in [0, 1], \quad \text{otherwise } p(\theta) = 0$$

*   **The Recursive Update:**
    As we perform the $n$-th independent trial, we update our posterior distribution using Bayes' Rule. The posterior distribution after $n$ trials is proportional to the likelihood of the current observation multiplied by the previous posterior (which acts as the new prior):
    $$p(\theta|y_1,\dots,y_n) \propto \theta^{y_n} (1-\theta)^{1-y_n} p(\theta|y_1,\dots,y_{n-1})$$

#### **2. Evolution of the Posterior Distribution**

The following figures illustrate the evolution of the conditional probability density function (c.p.d.f.) for $\theta$ as the number of trials $n$ increases. In this simulation, the true underlying value is $\theta = 0.35$.

![](_page_37_Figure_8.jpeg)
*Initial state: With $n=0$, the distribution is flat (Uniform prior).*

![](_page_37_Figure_9.jpeg)
![](_page_37_Figure_10.jpeg)
*Early trials ($n=1, 3, 5$): The distribution is wide, reflecting high uncertainty. The peak (mode) begins to shift toward the observed frequency of heads.*

![](_page_37_Figure_11.jpeg)
![](_page_37_Figure_12.jpeg)
*Large sample sizes ($n=10, 40$): As more data is collected, the posterior distribution becomes narrower and taller. This indicates that our uncertainty is decreasing and the estimate is converging toward the true value of $0.35$.*

#### **3. Key Observations**

*   **Information Accumulation:** Each new data point $y_i$ "sharpens" the distribution. The variance of the posterior distribution decreases as $n \to \infty$.
*   **Dominance of Data:** While the prior reflects our initial guess, its influence diminishes as the number of observations increases. Eventually, the likelihood term dominates the posterior.
*   **Recursive Nature:** Bayesian inference is naturally suited for real-time estimation because the current posterior contains all the information from past data needed to process the next observation.

![](_page_37_Picture_13.jpeg)

![](_page_37_Picture_14.jpeg)