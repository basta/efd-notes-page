# Incorporation of prior information

In Bayesian estimation, the initialization of an algorithm is not merely a formality but an opportunity to embed existing physical knowledge or engineering intuition into the model. This section explores how prior information can be mathematically structured to improve the convergence and robustness of estimation algorithms.

### **What information can be provided during algorithm initialization?**

When initializing the estimator, we define the prior conditional probability density functions (c.p.d.f.) for the parameters $\theta$ and the noise variance $\sigma_e^2$. Based on the data $\mathcal{D}^t$ available at time $t=0$, we typically assume:

*   **Parameter Distribution**: The parameters follow a Normal distribution conditioned on the noise variance:
    $$p(\theta | \sigma_e, \mathcal{D}^t) = \mathcal{N}(\widehat{\theta}, \sigma_e^2 P)$$
*   **Noise Variance Distribution**: The noise variance follows an Inverse-Gamma distribution (often represented via a Chi-squared form):
    $$p(\sigma_e | \mathcal{D}^t) = \chi_{\nu}^2 \left( \frac{\nu s^2}{2\sigma_e^2} \right)$$
*   **Noise Variance Estimate**: The expected value of the noise variance given the prior data is:
    $$\mathcal{E}\left\{\sigma_e^2|\mathcal{D}^t\right\} = s^2$$

#### **Confidence intervals for $\theta$**
If an engineer knows that a parameter $\theta_i$ must reside within a specific physical range, this can be translated into a prior mean and covariance. Assume the parameter is bounded by:
$$\theta_i^L \leq \theta_i \leq \theta_i^H$$
This interval translates to a **prior mean value**:
$$\hat{\theta}_i(1|0) = \frac{\theta_i^H + \theta_i^L}{2}$$
And the **prior covariance matrix diagonal elements** are determined by setting the interval to represent a specific confidence level (e.g., $\pm \alpha \sigma_{\theta}$, where $\alpha = 2 \dots 3$):
$$s^{2}(1|0)P_{ii}(1|0) = \left(\frac{\theta_{i}^{H} - \theta_{i}^{L}}{2\alpha}\right)^{2}$$

![](_page_101_Picture_13.jpeg)

---

### **Parameter drift covariance "shaping"**

In non-stationary systems, parameters may change over time. This "drift" is often modeled using linear forgetting, which updates the covariance matrix as:
$$P(t+1|t) = P(t|t) + V(t)$$
where $V(t)$ is the drift covariance matrix. We can "shape" $V$ to allow for more uncertainty in specific directions while remaining confident in others.

*   **Directional Uncertainty**: Define a "significant" direction vector $l$. We want the variance in direction $l$ to be $\sigma_1$ ($l^T V l = \sigma_1 l^T l$) and the variance in all orthogonal directions $x \perp l$ to be $\sigma_0$ ($x^T V x = \sigma_0 x^T x$).
*   **Covariance Construction**: This property is satisfied by the drift covariance matrix:
    $$V = \sigma_1 \frac{ll^T}{l^T l} + \sigma_0 \left( I - \frac{ll^T}{l^T l} \right)$$
*   **Applications**: This is particularly useful for systems with a fixed steady-state gain but time-varying transport delays, or when certain physical constraints must be maintained during tracking.

---

### **Smooth impulse response**

When identifying a system's impulse response using a model of the form:
$$y(t) = \sum_{i=0}^{N} g_i u(t-i) + e(t)$$
we often expect the coefficients $g_i$ to change "smoothly" rather than abruptly. We can translate this "smoothness" into prior information on the parameter error $\tilde{g}_i = g_i - \hat{g}_i(1|0)$.

A smoothness constraint can be expressed by penalizing the second difference:
$$\Delta^2 \tilde{g}_i = \tilde{g}_{i+2} - 2\tilde{g}_{i+1} + \tilde{g}_i \quad \to \quad 0$$
In matrix notation, this becomes:
$$\Delta^2 \tilde{\mathbf{g}} = \begin{bmatrix} 1 & & & & \\ -2 & 1 & & & \\ 1 & -2 & 1 & & \\ & \ddots & \ddots & \ddots & \\ & & 1 & -2 & 1 \end{bmatrix} \begin{bmatrix} \tilde{g}_0 \\ \tilde{g}_1 \\ \vdots \\ \tilde{g}_N \end{bmatrix} = D \tilde{\mathbf{g}}$$

To initialize the covariance matrix $P(1|0)$, we assume the covariance of the second differences is small:
$$\operatorname{cov}\left\{\Delta^2 \tilde{\mathbf{g}} \mid \mathbf{0} \right\} = DPD^T \approx \sigma_{\mathbf{g}}^2 \mathbf{I}, \qquad \sigma_{\mathbf{g}} \to 0$$
Solving for $P(1|0)$ yields:
$$P(1|0) = \sigma_{g}^2 D^{-1} D^{-T}$$

**Further improvement**: One can implement a "decreasing curvature" constraint where the expected variance $\sigma_{g_i}^2$ decreases as $i$ increases, reflecting the natural decay of an impulse response.

![](_page_103_Picture_14.jpeg)

![](_page_103_Picture_15.jpeg)