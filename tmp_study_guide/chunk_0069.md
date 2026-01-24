# Continuous-time Kalman filter with discrete output measurement (2)

In many practical engineering applications, the physical system evolves continuously in time, while measurements are acquired at discrete intervals (e.g., via a digital sensor). This requires a hybrid approach to the Kalman filter.

#### **Covariance Matrix Dynamics**

To derive the evolution of the estimation error covariance $P(\tau)$ in continuous time, we examine the error dynamics over an infinitesimal time step $d\tau$. The state error at time $\tau + d\tau$ is given by:

$$P(\tau + d\tau) = \mathcal{E}\left\{\tilde{x}(\tau + d\tau)\tilde{x}^{T}(\tau + d\tau)\right\}$$

Substituting the error dynamics $d\tilde{x}(\tau) = A\tilde{x}(\tau)d\tau + dw(\tau)$, we expand the product:

$$= \mathcal{E}\left\{\left(\tilde{x}(\tau) + A\tilde{x}(\tau)d\tau + dw(\tau)\right)\left(\tilde{x}(\tau) + A\tilde{x}(\tau)d\tau + dw(\tau)\right)^{T}\right\}$$

Expanding this expression and keeping terms up to first order (noting that $\mathcal{E}\{dw dw^T\} = Qd\tau$ and that $\tilde{x}$ and $dw$ are uncorrelated):

$$= P(\tau) + AP(\tau)d\tau + P(\tau)A^{T}d\tau + Qd\tau + AP(\tau)A^{T}(d\tau)^{2}$$

By taking the limit as $d\tau \to 0$, the higher-order term $(d\tau)^2$ vanishes, resulting in the **Continuous-time Lyapunov Equation** for the covariance evolution:

$$\frac{dP(\tau)}{d\tau} = \lim_{d\tau \to 0} \frac{P(\tau + d\tau) - P(\tau)}{d\tau} = AP(\tau) + P(\tau)A^{T} + Q$$

#### **Kalman Filter Steps**

The hybrid Kalman filter alternates between continuous integration (Time-update) and discrete jumps (Data-update).

▶ **Data-update (Correction Step)**
When a discrete measurement $y(k)$ becomes available at time $t = kT_s$, we perform a standard discrete-time Kalman update. The predicted values are taken from the end of the continuous integration:

$$\hat{x}(k+1|k) = \hat{x}(\tau)|_{\tau = (k+1)T_S}, \qquad P(k+1|k) = P(\tau)|_{\tau = (k+1)T_S}$$

The update is based on the discrete-time observation model:

$$y(k) = C_c x(k) + e(k), \qquad x(k) = x(\tau)|_{\tau = kT_s}$$

▶ **Time-update (Prediction Step)**
Between measurements, the filter propagates the state estimate and covariance by solving the continuous-time differential equations. The initial conditions for this integration are the "filtered" estimates from the previous data-update:

$$\hat{x}(\tau)|_{\tau=kT_s} = \hat{x}(k|k), \qquad P(\tau)|_{\tau=kT_s} = P(k|k)$$

The state estimate evolves according to the system dynamics $\dot{\hat{x}} = A_c\hat{x} + B_cu$, while the covariance evolves according to the Lyapunov equation derived above.

![](_page_121_Picture_12.jpeg)