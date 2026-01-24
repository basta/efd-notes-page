# Numerical implementation of bayesian estimation algorithms (5)

In practical recursive estimation, we must account for the fact that system parameters may change over time. This requires a "Time Update" step to increase the uncertainty (covariance) of our estimates. When using LD-factorization, we must perform these updates directly on the factors to maintain numerical stability.

#### Time Update – Linear Forgetting (Random Walk)

Linear forgetting, also known as a random walk model, assumes that the parameters $\theta$ evolve according to $\theta(t+1) = \theta(t) + v(t)$, where $v(t)$ is process noise. The covariance update is additive:

$$P(t+1|t) = P(t|t) + V(t)$$

where $V(t)$ is the covariance of the parameter drift, represented in factorized form as $V(t) = | d_v(t); L_v^T(t) |$. 

To find the new factors $| d(t+1|t); L^{T}(t+1|t) |$, we must combine the existing factors and the noise factors:

$$\left| d(t+1|t); L^{T}(t+1|t) \right| = \left| \begin{bmatrix} d(t|t) \\ d_{v}(t) \end{bmatrix}; \begin{bmatrix} L^{T}(t|t) \\ L^{T}_{v}(t) \end{bmatrix} \right|$$

**Note:** Restoring the triangularity of the resulting $L$ matrix represents a significant computational burden compared to exponential forgetting, as it requires processing an augmented matrix.

### Time Update – Restricted Forgetting

Restricted forgetting methods are designed to prevent "covariance wind-up"—a phenomenon where the covariance grows unbounded in the absence of informative data (lack of excitation).

**1. Restricted Exponential Forgetting**
This method applies exponential forgetting only to the information actually updated by the current data. The update for the LD-factors is structured as follows:

$$\left| d(t+1|t); L^T(t+1|t) \right| = \left| \begin{bmatrix} d(t|t) \\ \dfrac{(1-\varphi)d_y}{\varphi(d_y-1)} \end{bmatrix}; \begin{bmatrix} L^T(t|t) \\ k^T(t) \end{bmatrix} \right|$$

**2. Restricted Linear Forgetting**
Similar to the linear update but scaled by the normalized output variance $d_y$ to ensure the update is proportional to the innovation:

$$\left| d(t+1|t); L^T(t+1|t) \right| = \left| \left[ \begin{array}{c} d(t|t) \\ \frac{\zeta_{\nu}(t)d_y^2}{(d_{\nu}-1)^2} \end{array} \right] ; \left[ \begin{array}{c} L^T(t|t) \\ k^T(t) \end{array} \right] \right|$$

These formulations allow for a **Rank-1 update**, which is significantly more numerically efficient than a full matrix addition. By appending a row to the $L^T$ matrix and an element to the $d$ vector, we can use algorithms like dyadic reduction to return the system to its standard triangular form.

![](_page_94_Picture_12.jpeg)

![](_page_94_Picture_13.jpeg)