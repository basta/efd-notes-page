# State estimation for non-linear stochastic systems

In real-world engineering applications, systems are rarely perfectly linear. To apply Kalman filtering techniques to non-linear systems, we must employ approximation methods. This section explores how to handle non-linearity using Taylor series expansions and the resulting Extended Kalman Filter (EKF) and Unscented Kalman Filter (UKF).

### **Taylor series expansion for random variables**

When a random variable $x$ undergoes a non-linear transformation, its resulting distribution is generally no longer Gaussian. However, we can approximate the moments (mean and covariance) of the transformed variable.

Consider a normal random variable $x \sim \mathcal{N}(\hat{x}, P_x)$ transformed by a non-linear mapping:
$$y = g(x)$$

We can approximate $y$ by expanding $g(x)$ in a Taylor series around the mean $\hat{x}$, where $\tilde{x} = x - \hat{x}$:
$$y = g(x) = g(\hat{x} + \tilde{x}) \approx g(\hat{x}) + \frac{\partial g}{\partial x}^T \tilde{x} + \frac{1}{2} \sum_{i} \tilde{x}^T \frac{\partial^2 g_i}{\partial x^2} \tilde{x} e_i + \cdots$$

#### **Linear Approximation (1st Order)**
By taking the expectation of the first-order expansion, we derive the linear approximations used in the standard EKF:
*   **Mean:** $\mathcal{E} \{ y \} \approx \mathcal{E} \left\{ g(\hat{x}) + \frac{\partial g}{\partial x}^T \tilde{x} \right\} = g(\hat{x})$
*   **Covariance:** $\operatorname{cov} \{ y \} \approx \mathcal{E} \left\{ \left(\frac{\partial g}{\partial x}^T \tilde{x}\right) \left(\tilde{x}^T \frac{\partial g}{\partial x}\right) \right\} = \frac{\partial g}{\partial x}^T P_x \frac{\partial g}{\partial x}$

#### **Second-order Approximation (Scalar Case)**
For higher accuracy, the second-order term accounts for the "bias" introduced by curvature:
$$\mathcal{E}\left\{y\right\} \approx g\left(\hat{x}\right) + \frac{1}{2}\frac{\partial^{2}g}{\partial x^{2}}P_{x}$$

![](_page_124_Picture_12.jpeg)
![](_page_124_Picture_13.jpeg)

---

### **Extended Kalman Filter (EKF)**

The EKF applies the linear approximation locally at each time step. Consider a non-linear discrete-time stochastic system:
$$x(t+1) = f(x(t), u(t), v(t)), \quad \text{cov} \{v(t)\} = Q$$
$$y(t) = g(x(t), u(t), e(t)), \quad \text{cov} \{e(t)\} = R$$

#### **EKF Data Update Step**
Given the predicted state $\hat{x}(t|t-1)$ and covariance $P(t|t-1)$, we linearize the measurement equation $g(\cdot)$ around the best available estimate:
$$y(t) \approx g(\hat{x}(t|t-1), u(t), 0) + C(t)(x(t)-\hat{x}(t|t-1)) + \Gamma_e(t)e(t)$$

The Jacobian matrices are defined as:
$$C(t) = \left. \frac{\partial g}{\partial x} \right|_{\hat{x}(t|t-1), u(t), 0}, \qquad \Gamma_e(t) = \left. \frac{\partial g}{\partial e} \right|_{\hat{x}(t|t-1), u(t), 0}$$

**Kalman Gain Calculation:**
$$L(t) = P(t|t-1)C^{T}(t) \left(C(t)P(t|t-1)C^{T}(t) + \Gamma_{e}(t)R\Gamma_{e}^{T}(t)\right)^{-1}$$

**State and Covariance Update:**
$$\hat{x}(t|t) = \hat{x}(t|t-1) + L(t)(y(t) - g(\hat{x}(t|t-1), u(t), 0))$$
$$P(t|t) = P(t|t-1) - L(t) \left( C(t)P(t|t-1)C^{T}(t) + \Gamma_{e}(t)R\Gamma_{e}^{T}(t) \right) L^{T}(t)$$

#### **EKF Time-Update Step**
We project the state forward by linearizing the transition function $f(\cdot)$ around the filtered estimate $\hat{x}(t|t)$:
$$A(t) = \left. \frac{\partial f}{\partial x} \right|_{\hat{x}(t|t), u(t), 0}, \qquad \Gamma_v(t) = \left. \frac{\partial f}{\partial v} \right|_{\hat{x}(t|t), u(t), 0}$$

**Mean and Covariance Projection:**
$$\hat{x}(t+1|t) = f\left(\hat{x}(t|t), u(t), 0\right)$$
$$P(t+1|t) = A(t)P(t|t)A^{T}(t) + \Gamma_{v}(t)Q\Gamma_{v}^{T}(t)$$

![](_page_126_Picture_14.jpeg)
![](_page_126_Picture_15.jpeg)

---

### **Iterated EKF (IEKF)**

The IEKF improves the data update step by iteratively re-linearizing the measurement equation. This is essentially a Gauss-Newton optimization to find the Maximum A Posteriori (MAP) estimate.

**Iteration Process:**
1.  Initialize $\hat{x}^{(0)}(t) = \hat{x}(t|t-1)$.
2.  Calculate Jacobian $G^{(i)}(t)$ and Gain $K^{(i)}(t)$ at the current iteration $\hat{x}^{(i)}(t)$.
3.  Update the estimate $\hat{x}^{(i+1)}(t)$ until convergence.
4.  Set $\hat{x}(t|t) = \hat{x}^{(final)}(t)$ and update $P(t|t)$.

![](_page_127_Picture_14.jpeg)
![](_page_127_Picture_15.jpeg)

---

### **Unscented Kalman Filter (UKF)**

The UKF addresses the flaws of linearization by using the **Unscented Transformation**. Instead of approximating the non-linear function, it approximates the probability distribution using a minimal set of chosen sample points, called **sigma-points**.

#### **Sigma-Point Definition**
For a state vector of dimension $n_x$, we generate $2n_x + 1$ sigma-points:
*   **Mean point:** $x_0 = \hat{x}$ with weight $w_0 = \frac{k}{n_x + k}$
*   **Spread points:** $x_i = \hat{x} \pm S_i$ with weights $w_i = \frac{1}{2(n_x + k)}$

Where $S_i$ are columns of the matrix square root (Cholesky factor) of $(n_x + k)P_{xx}$. The parameter $k$ scales the distance of points from the mean.

#### **UKF Data-Update Step**
The sigma-points are propagated through the non-linear measurement function $y_i(t) = g(x_i^\sigma)$. The predicted measurement $\hat{y}^A(t)$ and the cross-covariance $P_{xy}^A(t)$ are then calculated via weighted sums:
$$\hat{y}^{A}(t) = \sum w_{i}y_{i}(t)$$
$$P_{yy}^{A}(t) = \sum w_{i} (y_{i} - \hat{y}^{A}) (y_{i} - \hat{y}^{A})^{T} + R$$
$$P_{xy}^{A}(t) = \sum w_{i} (x_{i}^{\sigma} - \hat{x}) (y_{i} - \hat{y}^{A})^{T}$$

The update then follows the standard Linear Minimum Square (LMS) logic:
$$\hat{x}(t|t) = \hat{x} + P_{xy}P_{yy}^{-1}(y - \hat{y})$$

![](_page_128_Picture_10.jpeg)
![](_page_129_Picture_12.jpeg)