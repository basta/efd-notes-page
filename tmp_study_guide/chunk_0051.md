# ARX model – tracking of time-varying parameters (3)

In practical applications, system parameters are rarely constant. To track changes in the system dynamics over time, we must move beyond the "naive" recursive model (where parameters are assumed static) and introduce a mechanism that allows the model to adapt.

### Time Update – Conceptual Solution

The transition from the estimate at time $t$ to the prediction at time $t+1$ is governed by the **time update step**. Conceptually, this is solved using the Chapman-Kolmogorov equation, which propagates the posterior probability density function (p.d.f.) through a parameter development model:

$$p\left( \theta(t+1)|\mathcal{D}^t \right) = \int p\left( \theta(t+1)|\theta(t),\mathcal{D}^t \right) \; p\left( \theta(t)|\mathcal{D}^t \right) \; d \theta(t)$$

Here, the conditional p.d.f. $p\left(\theta(t+1)|\theta(t),\mathcal{D}^t\right)$ defines how we expect the parameters to evolve (e.g., as a random walk). The result of this convolution integral is typically an **increase in parameter uncertainty**, as we are essentially "blurring" our current knowledge to account for potential drift.

---

### Linear Forgetting

One specific way to model this parameter evolution is through **Linear Forgetting**, which assumes the parameters follow a random walk process.

#### Model of Parameter Drift
We assume the parameter vector $\theta$ changes by adding a zero-mean Gaussian noise term $\nu(t)$:

$$\theta(t+1) = \theta(t) + \nu(t), \qquad \nu(t) \sim \mathcal{N}\left(0; \sigma_e^2 V(t)\right)$$

#### Time Update of the Covariance Matrix
Under this model, the mean estimate remains the same, but the uncertainty (covariance) increases additively:

$$P(t+1|t) = P(t|t) + V(t)$$

**Key Characteristics:**
- **Directional Tracking:** If we have prior knowledge about which parameters are likely to change (or in which directions), we can incorporate this into the matrix $V(t)$.
- **Limitations:** This basic linear forgetting model typically assumes a constant noise variance $\sigma_e^2$; it does not inherently account for time-varying noise in the observation process.

![](_page_81_Picture_13.jpeg)

*The figure above illustrates the conceptual widening of the probability distribution during the time update, reflecting the loss of information as we project the estimate into the future.*