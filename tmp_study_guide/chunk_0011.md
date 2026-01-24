# Mean Square Estimate (2)

In the previous section, we formulated the Mean Square (MS) estimation problem by minimizing the expected value of the squared error. We determined that to find the optimal estimate $\hat{x}_{\text{MS}}(y)$, it is sufficient to minimize the inner integral of the cost function for every observed value $y$.

### Minimizing the Inner Integral

The inner integral of the MS criterion, denoted as $J_{\text{MS}}'(y)$, represents the conditional mean square error. By expanding the quadratic term $(x - \hat{x}_{\text{MS}})^T(x - \hat{x}_{\text{MS}})$, we obtain:

$$J_{\mathsf{MS}}'(y) = \mathcal{E}\left\{\boldsymbol{x}^T\boldsymbol{x}|\boldsymbol{y}\right\} - \mathcal{E}\left\{\boldsymbol{x}|\boldsymbol{y}\right\}^T\hat{\boldsymbol{x}}_{\mathsf{MS}}(y) - \hat{\boldsymbol{x}}_{\mathsf{MS}}^T(y)\mathcal{E}\left\{\boldsymbol{x}|\boldsymbol{y}\right\} + \hat{\boldsymbol{x}}_{\mathsf{MS}}^T(y)\hat{\boldsymbol{x}}_{\mathsf{MS}}(y)$$

To find the stationary point, we take the partial derivative with respect to the estimate $\hat{\mathbf{x}}_{\text{MS}}(y)$ and set it to zero:

$$\frac{\partial J_{\rm MS}'}{\partial \hat{\mathbf{x}}_{\rm MS}(y)} = -2\mathcal{E}\left\{x|y\right\} + 2\hat{\mathbf{x}}_{\rm MS}(y) = 0 \quad \rightarrow \quad \hat{\mathbf{x}}_{\rm MS}(y) = \mathcal{E}\left\{x|y\right\}$$

**Conclusion:** The optimal Mean Square estimate is simply the **conditional mean value** of the hidden state $x$ given the observed data $y$.

### Measure of Quality: Estimation Error Covariance

The performance of the MS estimator is characterized by the estimation error $\tilde{\mathbf{x}}(y) = \mathbf{x} - \hat{\mathbf{x}}_{\text{MS}}(y)$. Since the estimate is the conditional mean, the expected error is zero ($\mathcal{E}\{\tilde{\mathbf{x}}\} = 0$). The quality is quantified by the error covariance matrix:

$$P_{\tilde{\mathbf{x}}_{\mathsf{MS}}} = \mathcal{E}\left\{\tilde{\mathbf{x}}(y)\tilde{\mathbf{x}}^{\mathsf{T}}(y)\right\}$$

This can be expressed by integrating over the joint distribution:
$$P_{\tilde{x}_{\mathsf{MS}}} = \int \int \tilde{x}(y) \tilde{x}^{\mathsf{T}}(y) p(x|y) \ dx \ p(y) \ dy = \int P_{x|y}(y) p(y) \ dy = P_{x|y}$$

Where:
- $P_{x|y}(y)$ is the covariance matrix of the estimation error for a specific observation $y$.
- $P_{x|y}$ is the mean covariance matrix, which represents the average uncertainty across all possible observations.

The original scalar criterion function $J_{\text{MS}}$ is equivalent to the trace of this error covariance matrix:
$$J_{\mathsf{MS}} = \mathcal{E}\left\{\tilde{x}^{\mathsf{T}}\tilde{x}\right\} = \mathcal{E}\left\{\mathsf{tr}\;\tilde{x}^{\mathsf{T}}\tilde{x}\right\} = \mathcal{E}\left\{\mathsf{tr}\;\tilde{x}\tilde{x}^{\mathsf{T}}\right\} = \mathsf{tr}\;P_{\tilde{x}_{\mathsf{MS}}}$$

![](_page_16_Picture_13.jpeg)

![](_page_16_Picture_14.jpeg)

---

### Orthogonality Principle

The orthogonality principle is a fundamental concept in estimation theory. Two random variables are considered **orthogonal** if their inner product's expectation is zero:
$$\mathcal{E}\left\{x^{T}y\right\} = \int\int x^{T}y \ p(x,y) \ dxdy = 0$$

**The Principle for MS Estimation:**
The estimation error $(x - \mathcal{E}\{x|y\})$ is orthogonal to any function $g(y)$ of the observed data. Mathematically:
$$\mathcal{E}\left\{g(y)^{T}\left(x-\mathcal{E}\left\{x|y\right\}\right)\right\}=0$$

**Key Implications:**
1. The MS error is orthogonal to all possible functions (linear or non-linear) of the observed data.
2. The MS estimate is the "best" possible estimate in terms of the Euclidean norm:
   $$\mathcal{E}\{\|x - \mathcal{E}\{x|y\}\|\} \le \mathcal{E}\{\|x - g(y)\|\}$$
   where $\|x\| = \sqrt{x^T x}$.

![](_page_17_Picture_11.jpeg)

---

### Linear Mean Square Estimate

While the MS estimate (conditional mean) is theoretically optimal, it has practical drawbacks:
- It requires full knowledge of the joint probability density function $p(x, y)$, which is often unknown.
- Calculating the conditional mean can be analytically or computationally intractable for complex distributions.

#### LMS Problem Formulation
To overcome these issues, we restrict the estimator to be a **linear function** of the observed data:
$$\hat{x}_{\mathsf{LMS}}(y) = Ay + b$$

**Requirements and Goals:**
- **Information:** We only require the first and second moments (means and covariances) of $x$ and $y$, rather than the full p.d.f.
- **Optimality Criterion:** Minimize the Linear Mean Square (LMS) error:
$$J_{\text{LMS}} = \int \int \left(x - \hat{x}_{\text{LMS}}(y)\right)^{T} \left(x - \hat{x}_{\text{LMS}}(y)\right) p(x, y) \ dx \ dy$$