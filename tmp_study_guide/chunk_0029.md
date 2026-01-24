# **Update of parameter knowledge** based on new data $\{u(t), y(t)\}$

In the context of system identification and adaptive control, our knowledge of the system parameters $\theta$ is not static; it evolves as we collect more observations. This process is governed by Bayesian inference, where we update our prior beliefs about the parameters using new information from the input $u(t)$ and the resulting output $y(t)$.

The update rule is derived from Bayes' Theorem, expressing the posterior probability density function (p.d.f.) of the parameters given all data up to time $t$:

$$\rho\left(\theta \middle| \mathcal{D}^{t}\right) = \frac{\rho\left(y(t) \middle| u(t), \mathcal{D}^{t-1}, \theta\right) \rho\left(\theta \middle| u(t), \mathcal{D}^{t-1}\right)}{\rho\left(y(t) \middle| u(t), \mathcal{D}^{t-1}\right)}$$

Since the denominator $\rho(y(t) | u(t), \mathcal{D}^{t-1})$ acts as a normalizing constant (independent of $\theta$), we can express the relationship as a proportionality:

$$\rho\left(\theta \middle| \mathcal{D}^{t}\right) \propto \rho\left(y(t) \middle| u(t), \mathcal{D}^{t-1}, \theta\right) \rho\left(\theta \middle| \mathcal{D}^{t-1}\right)$$

### Components of the Update Equation

*   **Model Structure (Likelihood):** The term $\rho(y(t) | u(t), \mathcal{D}^{t-1}, \theta)$ represents the likelihood function. It defines how likely it is to observe the output $y(t)$ given the current input, the historical data, and a specific set of parameters $\theta$.
*   **Prior Knowledge:** The term $\rho(\theta | \mathcal{D}^{t-1})$ represents our knowledge of the parameters based on all information available up to the previous time step.

### The Natural Condition of Control Assumption
To simplify the recursive update, we typically employ the **Natural Condition of Control**. This assumption states that the choice of the current input $u(t)$ does not provide additional information about the internal parameters $\theta$ beyond what is already known from the past data $\mathcal{D}^{t-1}$. Mathematically, this is expressed as:

$$p\left(\theta \middle| u(t), \mathcal{D}^{t-1}\right) = p\left(\theta \middle| \mathcal{D}^{t-1}\right)$$

This assumption is crucial for separating the identification process (learning $\theta$) from the control synthesis process (choosing $u(t)$).

![](_page_50_Picture_11.jpeg)

The figure above illustrates the recursive nature of this estimation: as the system operates in a closed loop, each new data pair $\{u(t), y(t)\}$ refines the parameter distribution, ideally leading to a reduction in uncertainty and more accurate future predictions.