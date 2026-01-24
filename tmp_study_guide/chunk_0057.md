# Numerical implementation of bayesian estimation algorithms (4)

In the practical implementation of Bayesian estimation, especially for real-time applications, we focus on updating the statistics of the parameter distribution as new data arrives. This process is divided into the **Data Update**, where we incorporate new observations, and the **Time Update**, where we account for parameter evolution or uncertainty growth over time.

#### **Data update step**

The data update incorporates the information from the current measurement $y(t)$ to refine our parameter estimates.

*   **Parameter Covariance Factors**:
    To ensure numerical stability and maintain the positive-definiteness of the covariance matrix, we store and update the LD-factors rather than the full matrix $P(t|t)$.
    $$P(t|t) = L(t|t)D(t|t)L^T(t|t) = |d(t|t); L^T(t|t)|$$
    where $L$ is a monic lower triangular matrix and $D$ is a diagonal matrix of weights $d$.

*   **Parameter Mean Value**:
    The point estimate of the parameters, $\hat{\theta}$, is updated using the innovation $\varepsilon(t|t-1)$ and the Kalman gain $k(t)$ derived from the LD-factorization process.
    $$\hat{\theta}(t|t) = \hat{\theta}(t|t-1) + k(t)\varepsilon(t|t-1)$$

*   **Degrees of Freedom and Residuals**:
    The scalar statistics related to the noise variance estimation are also updated. The number of degrees of freedom $\nu$ increases by one with each new data point:
    $$\nu(t|t) = \nu(t|t-1) + 1$$
    The sum of residual squares is updated by adding the weighted squared innovation:
    $$\nu(t|t)s^{2}(t|t) = \nu(t|t-1)s^{2}(t|t-1) + \frac{\varepsilon^{2}(t|t-1)}{d_{y}(t)}$$
    where $d_y(t)$ represents the normalized output variance.

### **Time update step – exponential forgetting**

When parameters are expected to vary over time, we use a forgetting factor $\varphi \in (0, 1]$ to reduce the weight of older data, effectively increasing the uncertainty of our current estimate.

*   **Covariance Matrix**:
    In standard exponential forgetting, the entire covariance matrix is scaled, which corresponds to a direct scaling of the diagonal $D$ factors:
    $$P(t+1|t) = \frac{1}{\varphi}P(t|t) \qquad \rightarrow \qquad d(t+1|t) = \frac{1}{\varphi}d(t|t)$$

*   **Other Statistics**:
    The parameter mean is assumed to remain constant during the time update (random walk model with zero mean drift):
    $$\hat{\theta}(t+1|t) = \hat{\theta}(t|t)$$
    The statistics governing the noise variance are also scaled by $\varphi$. This prevents the degrees of freedom from growing to infinity, allowing the estimator to remain "alert" to changes in noise characteristics:
    $$\nu(t+1|t) + n + 1 = \varphi(\nu(t|t) + n + 1)$$
    $$\nu(t+1|t)s^{2}(t+1|t) = \varphi(\nu(t|t)s^{2}(t|t))$$

![](_page_93_Picture_15.jpeg)

![](_page_93_Picture_16.jpeg)