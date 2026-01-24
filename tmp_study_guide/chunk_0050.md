# ARX model – tracking of time-varying parameters (2)

In practical applications, system parameters are rarely truly constant. To track changes over time, we must define how the parameters evolve between observations.

### Time Update Step (The Naive Model)
The simplest assumption for parameter evolution is the **naive model** (or random walk with zero variance), which assumes the parameters do not change from one time step to the next:

$$\theta(t+1) \approx \theta(t)$$

Under this assumption, the predicted statistics for the next time step remain identical to the current filtered estimates:

$$\hat{\theta}(t+1|t) = \hat{\theta}(t|t), \quad P(t+1|t) = P(t|t)$$

### Parameter Tracking and the Kalman Gain
The ability of the recursive algorithm to adapt to new data is governed by the **Kalman gain**, $K(t)$. This gain determines how much the prediction error $\varepsilon$ influences the parameter update:

$$K(t) = \frac{P(t|t-1)z(t)}{1+\zeta(t|t-1)}$$

The gain is directly proportional to the normalized parameter covariance matrix $P(t|t-1)$. If the covariance is "large," the model is uncertain and places high weight on new data. If the covariance is "small," the model is confident in its current estimate and largely ignores new data.

### The Problem of Diminishing Excitation
For the estimator to remain "alert" and capable of tracking changes, the system must satisfy a **sufficient excitation condition**. This requires the information matrix (the inverse of the covariance matrix) to increase over time:

$$P(t|t-1)^{-1} = \sum_{\tau=1}^{t-1} z(\tau)z^{T}(\tau) > \alpha t I$$

As more data is collected ($t \to \infty$), the information matrix grows linearly with time. Consequently, the covariance matrix $P$ is upper-limited and vanishes toward zero:

$$P(t|t-1) < \frac{1}{\alpha t}I$$

**Conclusion:** In the naive model, as $t$ increases, $P(t|t-1) \to 0$. This causes the Kalman gain $K(t)$ to diminish to zero. Eventually, the algorithm "shuts down" its learning mechanism and becomes unable to track any subsequent parameter drifts. This is why the naive model is insufficient for time-varying systems.

![](_page_80_Picture_13.jpeg)