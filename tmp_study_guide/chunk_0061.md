# Supplementary reading

### Convergence of the Least-Squares method (2)

To analyze the convergence of the parameter error $\tilde{\theta}(t) = \theta^* - \hat{\theta}(t)$, we utilize the Lyapunov stability theory. By examining the behavior of a scalar energy-like function, we can determine if the estimation error diminishes over time.

#### Increment of the Lyapunov function
We define the Lyapunov function using the positive definite precision matrix $P^{-1}(t)$:
$$V(t) = \tilde{\theta}^{T}(t)P^{-1}(t)\tilde{\theta}(t)$$

The change in this function between two consecutive time steps, $\Delta V(t)$, is derived as follows:
$$\Delta V(t) = \tilde{\theta}^{T}(t)P^{-1}(t)\tilde{\theta}(t) - \tilde{\theta}^{T}(t-1)P^{-1}(t-1)\tilde{\theta}(t-1)$$

Substituting the error dynamics $\tilde{\theta}(t) = P(t)P^{-1}(t-1)\tilde{\theta}(t-1)$, we obtain:
$$\Delta V(t) = \tilde{\theta}^{T}(t)P^{-1}(t)\left(P(t)P^{-1}(t-1)\tilde{\theta}(t-1)\right) - \tilde{\theta}^{T}(t-1)P^{-1}(t-1)\tilde{\theta}(t-1)$$
$$\Delta V(t) = \tilde{\theta}^{T}(t)P^{-1}(t-1)\tilde{\theta}(t-1) - \tilde{\theta}^{T}(t-1)P^{-1}(t-1)\tilde{\theta}(t-1)$$
$$\Delta V(t) = \left(\tilde{\theta}(t) - \tilde{\theta}(t-1)\right)^{T}P^{-1}(t-1)\tilde{\theta}(t-1)$$

By further substituting the relationship $\tilde{\theta}(t) - \tilde{\theta}(t-1) = \left(P(t)P^{-1}(t-1) - I\right)\tilde{\theta}(t-1)$, the formula becomes:
$$\Delta V(t) = \tilde{\theta}^{T}(t-1) \left( P^{-1}(t-1)P(t) - I \right) P^{-1}(t-1)\tilde{\theta}(t-1)$$

Using the Riccati-like update for the covariance matrix $P(t) = P(t-1) - \frac{P(t-1)z(t)z^{T}(t)P(t-1)}{1+\zeta(t)}$, we arrive at the final expression:
$$\Delta V(t) = -\tilde{\theta}^{T}(t-1) \frac{z(t)z^{T}(t)}{1+\zeta(t)} \tilde{\theta}(t-1)$$

**Conclusion:** Since the term is a negative quadratic form, the Lyapunov function is non-increasing:
$$\Delta V(t) \leq 0$$

![](_page_99_Picture_10.jpeg)

### Conditions for Parameter Convergence
While $\Delta V(t) \leq 0$ ensures stability (the error does not grow), it does not guarantee that the error converges to zero. For convergence, we look at the relationship between the Lyapunov function and the norm of the parameter error:

$$V(t) = \| \tilde{\theta}(t) \|_{P^{-1}(t)}^{2} \geq \lambda_{\min} \left( P^{-1}(t) \right) \| \tilde{\theta}(t) \|^2$$

#### Minimum eigenvalue of the precision matrix
The precision matrix (inverse covariance) evolves as:
$$P^{-1}(t) = P^{-1}(t-1) + z(t)z^T(t)$$
This implies that $\lambda_{\min}(P^{-1}(t)) \geq \lambda_{\min}(P^{-1}(t-1))$, meaning the "information" in the system is non-decreasing.

#### Sufficient Excitation
If the system satisfies the **sufficient excitation condition**, the minimum eigenvalue grows indefinitely:
$$\lim_{t \to \infty} \lambda_{\min} \left( P^{-1}(t) \right) = \lim_{t \to \infty} \lambda_{\min} \left( \sum_{\tau=1}^t z(\tau) z^T(\tau) \right) = \infty$$

Under this condition, since $V(t)$ is bounded (non-increasing from a finite initial value), the only way for the inequality to hold is for the parameter error to vanish:
$$\lambda_{\min}\left(P^{-1}(t)\right) \| \tilde{\theta}(t) \|^2 \leq V(t) < \infty \quad \longrightarrow \quad \lim_{t \to \infty} \tilde{\theta}(t) = 0$$