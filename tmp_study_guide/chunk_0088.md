# Interacting Multiple Models (2)

![](_page_156_Picture_1.jpeg)

In the Interacting Multiple Model (IMM) framework, we face a challenge: as time progresses, the number of possible mode histories grows exponentially. To maintain a computationally feasible filter, we must approximate the Gaussian mixture resulting from the different mode hypotheses into a single representative Gaussian distribution for each mode.

#### Mixture Approximation

The goal is to approximate the mixture distribution $\bar{p}_i(\cdot|\cdot)$—which is a weighted sum of Gaussians from all possible previous modes $j$ transitioning into current mode $i$—by a single normal distribution.

$$ \bar{p}_i \Big( x(t) \, \Big| \, \mathcal{D}^t \, \Big) \approx \mathcal{N} \left( \bar{\mathbf{x}}_i(t|t); \bar{P}_i(t|t) \right) \approx \sum_{j=1}^M \rho_{i|j}(t) \; \mathcal{N} \left( \hat{\mathbf{x}}_j(t|t); P_j(t|t) \right) $$

To perform this approximation, we use **moment matching**, where we calculate the mean and covariance of the combined mixture.

**Fitting the Mean:**
The mixed mean for mode $i$ is the weighted average of the state estimates from all filters $j$ at the previous step:
$$\bar{x}_i(t|t) = \sum_{j=1}^M \rho_{i|j}(t) \; \hat{x}_j(t|t)$$

**Fitting the Covariance:**
The mixed covariance must account for both the individual filter covariances $P_j$ and the "spread" or "dispersion" caused by the differences between the individual means $\hat{x}_j$ and the new mixed mean $\bar{x}_i$:
$$\bar{P}_i(t|t) = \sum_{j=1}^M \rho_{i|j}(t) \left( P_j(t|t) + (\hat{x}_j(t|t) - \bar{x}_i(t|t)) \; (\hat{x}_j(t|t) - \bar{x}_i(t|t))^T \right)$$

![](_page_156_Picture_7.jpeg)

![](_page_156_Picture_8.jpeg)

### Interacting Multiple Models (3)

### Time Update Step

Once the models are mixed, we proceed with the standard prediction step of the filtering cycle.

**Mode Probability Prediction:**
The predicted probability of being in mode $i$ at the next time step is derived from the mixed mode probability:
$$P(m(t+1)=i \mid \mathcal{D}^t) = \bar{P}(m(t)=i \mid \mathcal{D}^t)$$

**State Prediction:**
The time update for the approximated state estimates is performed for each individual mode $i$. This involves propagating the mixed Gaussian through the system dynamics associated with that specific mode:
$$\begin{array}{lcl} \rho_i\Big(x(t+1)\Big|\mathcal{D}^t\Big) & = & \int \rho_i\Big(x(t+1)\Big|x(t),u(t)\Big) \; \bar{\rho}_i\Big(x(t)\Big|\mathcal{D}^{t}\Big) dx(t) \\ & \approx & \mathcal{N}\Big(\hat{x}_i(t+1|t);P_i(t+1|t)\Big) \end{array}$$

#### **Properties of the IMM Algorithm**

*   **Consistent State Representation**: Unlike simpler switching filters, the IMM maintains a consistent state estimate across all modes by interacting (mixing) them at each step.
*   **Fixed Complexity**: By collapsing the mixture of Gaussians back into a single Gaussian per mode at every iteration, the IMM avoids the exponential complexity growth seen in HMM decision trees.
*   **Superior Tracking**: It is widely considered one of the most effective algorithms for tracking maneuvering targets where the system dynamics change abruptly between several discrete models.