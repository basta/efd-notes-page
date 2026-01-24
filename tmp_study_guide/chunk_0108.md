# Dynamic system identification via GPR

In Gaussian Process Regression (GPR), identifying a dynamic system involves estimating the impulse response $g(\tau)$. When we model the output $y(t)$ as a convolution of the input $u(t)$ and the impulse response $g(\tau)$, the covariance properties of the output are directly inherited from the kernel $k(t_1, t_2)$ assigned to $g$.

#### **Covariance function derivation**

To perform inference, we must determine the cross-covariance between the impulse response and the observed output, as well as the auto-covariance of the output itself.

1.  **Cross-covariance between $g(t_1)$ and $y(t_2)$**:
    By applying the expectation operator to the convolution sum, we find that the covariance between a specific point of the impulse response and a measured output is a filtered version of the kernel:
    $$cov \{g(t_1), y(t_2)\} = cov \left\{g(t_1), \sum_{\tau=0}^{T} g(\tau)u(t_2 - \tau)\right\} = \sum_{\tau=0}^{T} k(t_1, \tau)u(t_2 - \tau)$$

2.  **Auto-covariance of the output $y$**:
    The covariance between two output measurements at different times $t_1$ and $t_2$ involves a double summation (or double integral in continuous time) over the kernel, weighted by the input signals:
    $$cov \{y(t_1), y(t_2)\} = cov \left\{\sum_{\tau_1=0}^{T} g(\tau_1)u(t_1 - \tau_1), \sum_{\tau_2=0}^{T} g(\tau_2)u(t_2 - \tau_2)\right\} = \sum_{\tau_1=0}^{T} \sum_{\tau_2=0}^{T} k(\tau_1, \tau_2)u(t_1 - \tau_1)u(t_2 - \tau_2)$$

### **Example: Impulse Response Estimation**

Consider a continuous-time system with a sampling period $T_s = 1s$ and measurement noise $e_i \sim \mathcal{N}(0, 1)$. The true impulse response is given by:
$$g(t) = \exp(-t/15)\sin(2\pi t/20)$$

By utilizing GPR with optimized hyperparameters ($\lambda, \tau$), we can achieve significantly better reconstruction of the system dynamics compared to traditional ARX or FIR models, especially when data is sparse or noisy.

![](_page_194_Figure_7.jpeg)
![](_page_194_Figure_8.jpeg)
![](_page_194_Figure_9.jpeg)
![](_page_194_Picture_10.jpeg)
![](_page_194_Picture_11.jpeg)

---

### Non-parametric function approximation

#### **Greedy algorithm for Sparse GP**
When dealing with large datasets ($n$), the computational cost of GP (which scales $O(n^3)$) becomes prohibitive. Greedy algorithms are used to select a subset of $m$ points ($m \ll n$) to approximate the full process.

*   **Selection Criteria**:
    *   **Prediction Error**: Selecting points where $\varepsilon_i = y_i - \hat{x}_i$ is largest. This requires knowing the target values $y_i$.
    *   **Predictive Variance**: Selecting points where the model is most uncertain. This only depends on the inputs $z_i$, allowing for active learning.
*   **Practical Insight**: In practice, the predictive variance is a measure of "information gain" but does not always correlate perfectly with the actual bias or residual error.

#### **Example: 2D Surface Approximation**
In approximating complex 2D non-linear functions, the choice of kernel is critical. A greedy algorithm might select points in high-variance regions first. If the function has different behaviors in different regions, stationary kernels may struggle unless the hyperparameters are carefully tuned.

![](_page_195_Figure_12.jpeg)
![](_page_195_Picture_13.jpeg)
![](_page_195_Picture_14.jpeg)

---

## Non-parametric function approximation

### **Can we estimate also function derivatives?**
Because differentiation is a linear operator, and Gaussian Processes are closed under linear operations, the derivative of a GP is also a GP. This allows us to project the relationship of the data directly onto the kernels.

*   **Kernel for the function $x(z)$**:
    $$cov \{x(z(t_1)), x(z(t_2))\} = k(z(t_1), z(t_2))$$

*   **Cross-covariance (Derivative vs. Value)**:
    If we wish to estimate the derivative $\frac{dx}{dz}$ from observed values $x(z)$, we use the derivative of the kernel with respect to the first argument:
    $$\operatorname{cov}\left\{\frac{\partial x(z(t_1))}{\partial z(t_1)}, x(z(t_2))\right\} = \frac{\partial k(z(t_1), z(t_2))}{\partial z(t_1)}$$

*   **Auto-covariance of the Derivative**:
    To find the covariance between derivatives at two different points, we take the second partial derivative of the kernel:
    $$\mathsf{cov}\left\{\frac{\partial x(z(t_1))}{\partial z(t_1)}, \frac{\partial x(z(t_2))}{\partial z(t_2)}\right\} = \frac{\partial^2 k(z(t_1), z(t_2))}{\partial z(t_1) \ \partial z(t_2)}$$

This framework is bi-directional: one can use function values to infer derivatives or use observed derivatives (e.g., from an accelerometer) to infer function values (e.g., position).

![](_page_196_Picture_15.jpeg)
![](_page_196_Picture_16.jpeg)

---

## Non-parametric function approximation

#### **Example: Derivatives of the Squared-Exponential (SE) Kernel**
Using the SE kernel $k(x_1, x_2) = \exp\left(-\frac{(x_1 - x_2)^2}{2r}\right)$, the derivatives (calculated via symbolic tools) are:

*   **First Derivatives**:
    $$ \frac{\partial k}{\partial x_1} = -\frac{k(x_1, x_2) \cdot (2x_1 - 2x_2)}{2r} $$
    $$ \frac{\partial k}{\partial x_2} = +\frac{k(x_1, x_2) \cdot (2x_1 - 2x_2)}{2r} $$

*   **Second Derivatives**:
    $$ \frac{\partial^2 k}{\partial x_1 \partial x_2} = \frac{k(x_1, x_2)}{r} - \frac{k(x_1, x_2) \cdot (2x_1 - 2x_2)^2}{4r^2} $$

#### **Summary**
*   **GPR** is a robust framework for non-parametric approximation, providing both mean estimates and uncertainty bounds.
*   **Kernel Design** is the "art" of the process, allowing engineers to encode prior physical knowledge (e.g., stability, periodicity, smoothness).
*   **Hyperparameter Optimization** (usually via Maximum Likelihood Estimation) is essential for model accuracy.
*   GPR acts as a **bridge** between classical control theory (system ID) and modern AI/Machine Learning (Kernel methods and SVMs).

![](_page_197_Picture_9.jpeg)