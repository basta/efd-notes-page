# Dynamic system identification via GPR

Gaussian Process Regression (GPR) provides a powerful framework for identifying dynamic systems by treating the system's impulse response as a realization of a stochastic process. This approach allows us to incorporate prior knowledge about system stability and smoothness directly into the identification process.

### **Impulse response / FIR model**

Consider a linear time-invariant (LTI) system represented by a Finite Impulse Response (FIR) model. Our goal is to estimate the impulse response function $g(\cdot)$ using observed input data $u(t)$ and output data $y(t)$:

$$y(t) = \sum_{\tau=0}^{T} g(\tau)u(t-\tau) + e(t)$$

where $e(t)$ represents measurement noise. In the GPR framework, we place a Gaussian Process prior on the impulse response $g(t)$.

#### **Prior information on $g(t)$**
To ensure the identified model is physically meaningful, we use kernels that encode specific properties:

*   **Non-stationary SE kernel with exponential decay**: This kernel combines the smoothness of the Squared-Exponential (SE) kernel with an exponential decay term to enforce stability (ensuring the impulse response vanishes as $t \to \infty$).
    $$k(t_1, t_2) = \sigma^2 \exp\left(-\frac{(t_1 - t_2)^2}{2\lambda^2}\right) \exp\left(-\frac{t_1 + t_2}{\tau}\right)$$
    Here, $\lambda$ controls the smoothness (length-scale) and $\tau$ represents the time constant of the decay.

*   **Stable Spline Kernels**: Specifically designed for system identification (e.g., Pillonetto et al., 2014), these kernels encode exponential stability. A first-order stable spline kernel is defined as:
    $$k(t_1, t_2) = \sigma^2 \exp\left(-\frac{\max(t_1, t_2)}{\tau}\right)$$
    A more complex second-order version is given by:
    $$k(t_1, t_2) = \frac{\sigma^2}{2} \exp\left(-\frac{(t_1 + t_2 + \max(t_1, t_2))}{\tau}\right) - \frac{\sigma^2}{6} \exp\left(-\frac{3\max(t_1, t_2)}{\tau}\right)$$

#### **Prediction and Covariance Structure**
To predict the vector of impulse response coefficients $g = [g(0), \dots, g(T)]^T$ from the observed output vector $y = [y(t_1), \dots, y(t_n)]^T$ (where $t_1 \geq T$), we utilize the joint Gaussian distribution of the weights and the observations:

$$\operatorname{cov}\left\{\begin{array}{c}g\\y\end{array}\right\} = \left[\begin{array}{cc}P_{gg} & P_{gy}\\P_{yg} & P_{yy}\end{array}\right]$$

In this block matrix:
- $P_{gg}$ is the prior covariance of the impulse response derived directly from the kernel $k(t_1, t_2)$.
- $P_{gy}$ and $P_{yy}$ are cross-covariances that account for the filtering operation of the input signal $u(t)$.

![](_page_193_Picture_11.jpeg)

![](_page_193_Picture_12.jpeg)