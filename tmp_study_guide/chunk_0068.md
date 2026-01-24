# Continuous-time Kalman filter with discrete output measurement

In many practical engineering applications, the physical system evolves continuously in time, while the sensors provide measurements only at specific discrete intervals. To handle this, we utilize a hybrid approach: a continuous-time model for the state evolution (time-update) and a discrete-time model for the measurement incorporation (data-update).

#### **Continuous-time stochastic system**

In continuous time, we must be careful with how we define noise. Strictly speaking, **continuous-time white noise does not exist** in a physical sense because it would require infinite power (having a constant spectral density across all frequencies to infinity). Instead, we describe the system using stochastic differential equations (SDEs).

**State development**
The evolution of the state $x(\tau)$ is modeled as:
$$dx(\tau) = A_c x(\tau) d\tau + B_c u(\tau) d\tau + dw(\tau)$$

Here, the uncertainty is represented by $dw(\tau)$, which is the increment of a **Wiener process** (Brownian motion). The stochastic properties of these increments are defined as:
- $\mathcal{E}\{dw(\tau)\} = 0$ (Zero mean)
- $\mathcal{E}\{dw(\tau) dw^{T}(\tau)\} = Q d\tau$ (Covariance proportional to the infinitesimal time step)

Note that the expectation operator changes the order of the infinitesimally small terms, allowing us to treat the variance as a rate $Q$ over the interval $d\tau$.

**Mean value dynamics**
To find the expected trajectory of the state (the prediction), we take the expectation of the SDE. Since the noise increment has a zero mean, the dynamics of the conditional mean $\hat{x}(\tau)$ follow:
$$d\hat{x}(\tau) = A_c\hat{x}(\tau)d\tau + B_cu(\tau)d\tau$$
Dividing by $d\tau$, we obtain the standard ordinary differential equation (ODE) for the state estimate:
$$\frac{d\hat{x}(\tau)}{d\tau} = A_c\hat{x}(\tau) + B_cu(\tau)$$

**Estimation error dynamics**
The estimation error is defined as $\tilde{x}(\tau) = x(\tau) - \hat{x}(\tau)$. By subtracting the mean dynamics from the state development equation, we find that the error evolves according to the system matrix and the process noise:
$$d\tilde{x}(\tau) = A_c\tilde{x}(\tau)d\tau + dw(\tau)$$

![](_page_120_Picture_15.jpeg)

This formulation allows us to propagate the state estimate and its uncertainty (covariance) between measurement samples by solving these differential equations. In the next section, we will derive how the covariance matrix $P(\tau)$ evolves over time.