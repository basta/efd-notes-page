# <span id="page-104-0"></span>**5. Kalman filter**

The Kalman filter is the optimal recursive estimator for the state of a linear dynamic system perturbed by Gaussian noise. While the Least Squares method focuses on estimating constant or slowly varying parameters, the Kalman filter is designed to track the internal states of a system in real-time by balancing the uncertainty of the system dynamics with the uncertainty of noisy measurements.

![](_page_104_Picture_1.jpeg)

### Linear stochastic system

#### State-space model
A discrete-time linear stochastic system is typically represented by two equations: the state transition equation (describing how the state evolves over time) and the observation equation (describing how the state relates to the measured output).

$$x(t+1) = Ax(t) + Bu(t) + v(t)$$
$$y(t) = Cx(t) + Du(t) + e(t)$$

Where:
*   $x(t)$ is the state vector.
*   $u(t)$ is the deterministic input.
*   $v(t)$ is the **process noise**, representing modeling errors or unmeasured disturbances.
*   $e(t)$ is the **measurement noise**, representing sensor inaccuracies.

The stochastic properties of the noise are defined by their mean and covariance:
$$\mathcal{E}\left\{ \begin{bmatrix} v(t) \\ e(t) \end{bmatrix} \right\} = 0, \quad \mathcal{E}\left\{ \begin{bmatrix} v(t_1) \\ e(t_1) \end{bmatrix}, \begin{bmatrix} v(t_2) \\ e(t_2) \end{bmatrix}^T \right\} = \begin{bmatrix} Q & S \\ S^T & R \end{bmatrix} \delta(t_1 - t_2)$$

Here, $\delta(t_1-t_2)$ is the **Kronecker delta**, implying that the noise is "white" (uncorrelated over time). $Q$ is the process noise covariance, $R$ is the measurement noise covariance, and $S$ represents the cross-covariance between process and measurement noise.

### Time evolution of state and output

To understand how uncertainty propagates through the system, we examine the mean and covariance of the state and output.

**Mean values:**
The expected values follow the deterministic part of the state-space equations:
$$\hat{x}(t+1) = A\hat{x}(t) + Bu(t)$$
$$\hat{y}(t) = C\hat{x}(t) + Du(t)$$

**Covariance matrices:**
The joint covariance of the next state and the current output is given by:
$$\operatorname{cov}\left\{\begin{bmatrix}x(t+1)\\y(t)\end{bmatrix}\right\} = \begin{bmatrix}AP_{x}(t)A^{T} + Q & AP_{x}(t)C^{T} + S\\CP_{x}(t)A^{T} + S^{T} & CP_{x}(t)C^{T} + R\end{bmatrix}$$

**Derivation Hint:**
To derive these, define the error dynamics where $\tilde{x}(t)=x(t)-\hat{x}(t)$ and $\tilde{y}(t)=y(t)-\hat{y}(t)$. Substituting these into the system equations yields:
$$\tilde{x}(t+1) = A\tilde{x}(t)+v(t)$$
$$\tilde{y}(t) = C\tilde{x}(t)+e(t)$$
The covariance is then calculated as $\mathcal{E}\{\tilde{x}\tilde{x}^T\}$.

![](_page_105_Picture_10.jpeg)
![](_page_105_Picture_11.jpeg)

### Linear stochastic system (2)

If the system matrix $A$ is stable (all eigenvalues inside the unit circle), the state covariance $P_x(t)$ will eventually converge to a constant **steady-state covariance** $P_X$.

$$P_{\scriptscriptstyle X} = \lim_{t \to \infty} P_{\scriptscriptstyle X}(t)$$

This steady-state solution satisfies the **Discrete Algebraic Lyapunov Equation**:
$$P_{x} = AP_{x}A^{T} + Q$$

**Interpretation of the Lyapunov equation:**
1.  **Stability Test:** For a deterministic system, the existence of a positive definite $P_x$ for a given $Q$ proves stability ($AP_xA^T - P_x = -Q$).
2.  **Stochastic Equilibrium:** In a stochastic context, it represents the balance where the "thinning" of uncertainty by the stable dynamics $A$ exactly offsets the "injection" of new uncertainty by the process noise $Q$.

#### Sampling of continuous-time linear stochastic system
In many practical applications, the physical process is continuous, but measurements are taken at discrete intervals $T_s$.

**Continuous-time dynamics:**
$$dx_c(\tau) = A_c x_c(\tau) d\tau + B_c u_c(\tau) d\tau + dv_c(\tau)$$
$$y_c(kT_s) = C_c x_c(kT_s) + e_c(kT_s)$$

Here, $dv_c(\tau)$ represents the increment of a **Wiener process** (Brownian motion). Its stochastic properties are defined as:
$$\mathcal{E}\left\{dv_{c}(\tau)\right\} = 0, \qquad \mathcal{E}\left\{dv_{c}(\tau) \ dv_{c}^{T}(\tau)\right\} = Q_{c}d\tau$$

When discretizing this system, the resulting discrete-time noise covariance $Q$ is not simply $Q_c$, but an integral that accounts for how the noise is filtered by the system dynamics over the sampling period.

![](_page_106_Picture_13.jpeg)