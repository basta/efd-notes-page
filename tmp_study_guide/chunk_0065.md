# Kalman filter algorithm (2)

The Kalman filter operates through a recursive cycle of two main stages: the **Time-update** (prediction) and the **Data-update** (correction). While the data-update incorporates new measurements, the time-update projects the current state estimate forward in time using the system dynamics.

#### **Time-update step**

In this step, we project the state and the uncertainty (covariance) from time $t$ to $t+1$ based on our knowledge of the system physics, before the next measurement $y(t+1)$ is actually recorded.

▶ **Conditional mean – prediction**
The predicted state $\hat{x}(t+1|t)$ is calculated by applying the state transition matrix $A$ to the previous corrected estimate and adding the effect of the known control input $u(t)$:
$$\hat{x}(t+1|t) = A\hat{x}(t|t) + Bu(t)$$

▶ **Conditional covariance matrix – prediction**
The uncertainty grows during the prediction step because of the process noise $Q$. The predicted covariance $P(t+1|t)$ is:
$$P(t+1|t) = AP(t|t)A^{T} + Q$$

#### **Combined data-update and time-update step**

For implementation efficiency, these two steps can be merged into a single recursive equation that updates the prediction for the next step directly from the current prediction and the new measurement.

▶ **Conditional mean**
By substituting the data-update equation into the time-update, we obtain the one-step ahead predictor:
$$\begin{aligned} \hat{x}(t+1|t) &= A(\hat{x}(t|t-1) + L(t)(y(t) - C\hat{x}(t|t-1) - Du(t))) + Bu(t) \\ &= (A - AL(t)C)\hat{x}(t|t-1) + (B - AL(t)D)u(t) + AL(t)y(t) \end{aligned}$$

▶ **Conditional covariance matrix**
Similarly, the covariance update can be expressed in a single step. Under the assumption that process and measurement noise are uncorrelated ($S=0$), this results in the standard discrete-time **Riccati equation**:
$$P(t+1|t) = AP(t|t-1)A^{T} - AP(t|t-1)C^{T} \left(CP(t|t-1)C^{T} + R\right)^{-1}CP(t|t-1)A^{T} + Q$$

![](_page_112_Picture_12.jpeg)

---

### Supplementary reading: Kalman filter with correlated noise

In many practical scenarios, such as systems with high-frequency sampling or shared sensors, the assumption that process noise $v(t)$ and measurement noise $e(t)$ are independent ($S=0$) does not hold.

### **Assumption**
- The process and measurement noises are correlated: $\mathcal{E}\{v(t)e^T(t)\} = S \neq 0$.
- In this case, the data-update and time-update steps become coupled and cannot be performed independently in their standard form.

#### **Update algorithm 1 – Recovering separated steps**
We can "de-correlate" the system by transforming the equations. We use the fact that if $y(t)$ is known, it provides information about the measurement noise $e(t)$, which in turn provides information about the process noise $v(t)$ due to their correlation.

The conditioned process noise properties, given the measurement, are:
$$\hat{v}(t|t) = SR^{-1} \Big( y(t) - Cx(t) - Du(t) \Big)$$
$$Q(t|t) = Q - SR^{-1}S^{T}$$

![](_page_113_Picture_12.jpeg)

▶ **De-correlated state transition equation**
We define a new system where the noise $v'(t)$ is uncorrelated with $e(t)$:
$$x(t+1) = A'x(t) + B'u(t) + SR^{-1}y(t) + v'(t)$$
where:
$$A' = A - SR^{-1}C, \quad B' = B - SR^{-1}D$$

The resulting noise covariance matrix is now block-diagonal, allowing for standard filtering techniques:
$$\mathcal{E}\left\{ \left[ \begin{array}{c} v'(t) \\ e(t) \end{array} \right] \cdot \left[ \begin{array}{c} v'(t) \\ e(t) \end{array} \right]^T \right\} = \left[ \begin{array}{cc} Q - SR^{-1}S^T & 0 \\ 0 & R \end{array} \right] = \left[ \begin{array}{cc} Q' & 0 \\ 0 & R \end{array} \right]$$

#### **Update algorithm 2 - Combined Bayesian solution**
Alternatively, we can derive the filter directly from the joint conditional probability density function (c.p.d.f.) of the state and output.

▶ **Joint c.p.d.f. of state $x(t+1)$ and output $y(t)$**
$$\rho\bigg(\begin{bmatrix} x(t+1) \\ y(t) \end{bmatrix} \bigg| \, \mathcal{D}^{t-1} \bigg) = \mathcal{N}\bigg(\begin{bmatrix} \hat{x}(t+1|t-1) \\ \hat{y}(t|t-1) \end{bmatrix}; \begin{bmatrix} AP(t|t-1)A^T + Q & AP(t|t-1)C^T + S \\ CP(t|t-1)A^T + S^T & CP(t|t-1)C^T + R \end{bmatrix} \bigg)$$

Using the properties of conditional Gaussian distributions, the updated mean and covariance are:
$$\hat{x}(t+1|t) = A\hat{x}(t|t-1) + Bu(t) + K(t)(y(t) - C\hat{x}(t|t-1) - Du(t))$$
$$K(t) = (AP(t|t-1)C^{T} + S)(CP(t|t-1)C^{T} + R)^{-1}$$
$$P(t+1|t) = AP(t|t-1)A^{T} - (AP(t|t-1)C^{T} + S)(CP(t|t-1)C^{T} + R)^{-1}(CP(t|t-1)A^{T} + S^{T}) + Q$$

![](_page_115_Picture_11.jpeg)
![](_page_115_Picture_12.jpeg)

---

### Stochastic properties of Kalman filter

The Kalman filter is the optimal estimator in the sense that it minimizes the mean square error. This optimality leads to specific stochastic properties in the resulting residuals.

#### **Stochastic properties not affected by deterministic input**
For a linear system, the deterministic control input $u(t)$ shifts the mean but does not change the covariance or the whiteness of the error. We analyze the **prediction error sequence** (also known as the innovation):
$$\varepsilon(t|t-1) = y(t) - \hat{y}(t|t-1)$$

By the **orthogonality principle**, the optimal estimate ensures that the prediction error is orthogonal to all past data. This implies:
1. The error has zero mean: $\mathcal{E}\{\varepsilon(t|t-1)\} = 0$.
2. The error is uncorrelated with past outputs: $\mathcal{E}\{\varepsilon(t|t-1)y^T(t-\tau)\} = 0$.
3. The error sequence is **white noise**: $\mathcal{E}\{\varepsilon^T(t|t-1)\varepsilon(t-\tau|t-\tau-1)\} = 0$ for $\tau \neq 0$.

**Conclusion:** If the Kalman filter is correctly tuned to the system's true $A, C, Q, R$ matrices, the innovation sequence $\varepsilon(t|t-1)$ must be white. This can be validated in practice using the sample autocovariance function:
$$R_{\varepsilon\varepsilon}(\tau) = \frac{1}{T-\tau} \sum_{t=\tau}^{T} \varepsilon(t|t-1) \varepsilon^{T}(t-\tau|t-\tau-1)$$

![](_page_116_Picture_12.jpeg)
![](_page_116_Picture_13.jpeg)