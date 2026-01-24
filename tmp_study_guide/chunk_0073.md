# Unscented Kalman filter (3)

#### **Time-update step**

The time-update (or prediction) step in the Unscented Kalman filter (UKF) propagates the state estimate and its uncertainty from the current time $t$ to the next time step $t+1$. Unlike the Extended Kalman Filter (EKF), which linearizes the system dynamics using a Jacobian, the UKF uses the Unscented Transformation to handle the non-linearities directly.

For a given set of filtered values:
$$\hat{x}(t|t), \quad P(t|t)$$

And a non-linear state transition equation with additive noise:
$$x(t+1) = f(x(t)) + v(t), \quad \text{cov} \{v(t)\} = Q$$

The required moments of the predictive distribution are approximated by propagating the $\sigma$–points through the non-linear function $f(\cdot)$. Let $x_i^{\sigma}(t|t)$ be the sigma points generated from the filtered state $\hat{x}(t|t)$ and covariance $P(t|t)$. Each point is transformed as follows:

$$x_i(t+1) = f\left(x_i^{\sigma}(t|t)\right), \quad i = 0, \ldots, 2n_x$$

#### **Resulting formulas**

The predicted mean $\hat{x}^A(t+1)$ and the predicted covariance $P^A(t+1)$ are calculated by taking the weighted average of the transformed sigma points:

$$\hat{x}^A(t+1) = \sum_{i=0}^{2n_X} w_i x_i(t+1)$$

$$P^{A}(t+1) = \sum_{i=0}^{2n_{X}} w_{i} \left(x_{i}(t+1) - \hat{x}^{A}(t+1)\right) \left(x_{i}(t+1) - \hat{x}^{A}(t+1)\right)^{T} + Q$$

Note that the process noise covariance $Q$ is added at the end of the covariance calculation, assuming the noise is additive. These values then serve as the prior for the subsequent data update step:

$$\hat{x}(t+1|t) \approx \hat{x}^A(t+1), \quad P(t+1|t) \approx P^A(t+1)$$

This approach captures the mean and covariance accurately to the second order of the Taylor series expansion, providing better performance than the EKF for highly non-linear systems.

![](_page_130_Picture_13.jpeg)