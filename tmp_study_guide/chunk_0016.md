# Properties of ML estimate (2)

In the frequentist framework, the Maximum Likelihood (ML) estimate possesses several desirable asymptotic and finite-sample properties. Two of the most critical properties are efficiency and consistency.

### **Efficiency and the Cramér-Rao Bound**
An estimate is said to be **efficient** if its error covariance reaches the theoretical lower bound defined by the inverse of the Fisher Information Matrix.
*   **Efficiency**: $P_{\tilde{x}} = F^{-1}$
    
This implies that no other unbiased estimator can have a lower variance than the ML estimate in these conditions.

### **Consistency**
An estimate is **consistent** if it converges in probability to the true value of the parameter as the number of observations $n$ increases to infinity.
*   **Consistency**: $P(\|x - \hat{x}(y_1, \dots, y_n)\| > \varepsilon) \to 0 \text{ for } n \to \infty$

---

### **Example: Repeated Measurement with Gaussian Noise (contd.)**

To illustrate these properties, we return to the linear measurement model with Gaussian noise.

#### **1. Calculating the Fisher Information Matrix**
Recall the log-likelihood function for the Gaussian case:
$$\ln I(x|y) = -\frac{1}{2}(y - Cx)^{T}R^{-1}(y - Cx) - \frac{n_{y}}{2}\ln(2\pi) - \frac{1}{2}\ln|R|$$

To find the Fisher Information, we examine the sensitivity of the log-likelihood with respect to the parameter $x$. The first derivative (the score function) is:
$$\frac{\partial \ln I(x|y)}{\partial x} = C^{T}R^{-1}(y - Cx)$$

The second derivative (the Hessian) represents the curvature of the log-likelihood:
$$\frac{\partial^{2}\ln I(x|y)}{\partial x^{2}} = -C^{T}R^{-1}C$$

The Fisher Information Matrix $F$ is defined as the negative expectation of the Hessian. Since the Hessian here is deterministic (independent of $y$), we have:
$$F = -\mathcal{E}\left\{ \frac{\partial^2 \ln I(x|y)}{\partial x^2} \right\} = C^T R^{-1} C$$

**Conclusion 1:** Since we previously derived that the ML error covariance is $P_{\tilde{x}_{ML}} = (C^T R^{-1} C)^{-1}$, it follows that $P_{\tilde{x}_{ML}} = F^{-1}$. Therefore, the ML estimate for this linear Gaussian model is **efficient**.

#### **2. Analyzing Convergence**
Consider a scalar case where we take $n$ independent measurements with variances $\sigma_i^2$. The total Fisher Information is the sum of the individual precisions:
$$F = P_{\tilde{\mathbf{x}}_{\mathsf{ML}}}^{-1} = \boldsymbol{C}^T \boldsymbol{R}^{-1} \boldsymbol{C} = \sum_{i=1}^{n} \frac{1}{\sigma_i^2}$$

As $n \to \infty$, provided the sum of precisions diverges (i.e., the measurements are not becoming infinitely noisy), the information $F$ grows to infinity.
$$\text{Therefore: } P_{\tilde{\mathbf{x}}_{\mathsf{ML}}} = \frac{1}{F} \to 0$$

**Conclusion 2:** As the error covariance vanishes with increasing data, the estimate $\hat{x}_{ML}(y)$ converges to the true value, proving the estimate is **consistent**.

![](_page_28_Picture_13.jpeg)

![](_page_28_Picture_14.jpeg)