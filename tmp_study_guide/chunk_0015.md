# Maximum Likelihood Estimate – example (2)

#### Resulting ML estimate
In a well-designed experiment, the observation matrix $C$ has full rank, ensuring that the system is observable and a unique solution exists. Under the assumption of Gaussian noise, the Maximum Likelihood (ML) estimate is given by the weighted least squares solution:

$$\hat{\mathbf{x}}_{\mathsf{ML}} = \left( C^{\mathsf{T}} R^{-1} C \right)^{-1} C^{\mathsf{T}} R^{-1} \mathbf{y}$$

#### Model of $n$ independent samples with various precision
Consider a scalar parameter $x$ observed through $n$ independent measurements, where each measurement $y_i$ has a different noise variance $\sigma_i^2$. This is modeled as:

$$C = \begin{bmatrix} 1 \\ \vdots \\ 1 \end{bmatrix}, \quad e \sim \mathcal{N} \left( \begin{bmatrix} 0 \\ \vdots \\ 0 \end{bmatrix}, \begin{bmatrix} \sigma_1^2 & & 0 \\ & \ddots & \\ 0 & & \sigma_n^2 \end{bmatrix} \right)$$

▶ **ML estimate – weighted average**
The ML estimate for this case simplifies to a weighted average, where the weights are inversely proportional to the variances (precisions $1/\sigma_i^2$):

$$\hat{x}_{\mathsf{ML}} = \frac{\frac{y_1}{\sigma_1^2} + \dots + \frac{y_n}{\sigma_n^2}}{\frac{1}{\sigma_1^2} + \dots + \frac{1}{\sigma_n^2}}$$

▶ **For samples with equal precision – arithmetic average**
If all measurements have the same variance ($\sigma_1^2 = \dots = \sigma_n^2$), the weights cancel out, and the ML estimate becomes the standard arithmetic mean:

$$\hat{x}_{ML} = \frac{y_1 + \dots + y_n}{n} = \bar{y}$$

![](_page_25_Picture_12.jpeg)

### Properties of ML estimate

#### Linear measurement model
Given the model $y = Cx + e$, we can evaluate the statistical properties of the ML estimator.

**1. Unbiasedness**
An estimator is unbiased if its expected value equals the true parameter value. For the linear ML estimate:
$$\mathcal{E}\left\{\hat{\mathbf{x}}_{\mathsf{ML}}|\mathbf{x}\right\} = \mathcal{E}\left\{\left.\left(\mathbf{C}^{\mathsf{T}}\mathbf{R}^{-1}\mathbf{C}\right)^{-1}\mathbf{C}^{\mathsf{T}}\mathbf{R}^{-1}(\mathbf{C}\mathbf{x} + \mathbf{e})\right|\mathbf{x}\right\} = \mathbf{x}$$
Since $\mathcal{E}\{e\} = 0$, the term involving noise vanishes, proving the ML estimate is unbiased.

**2. Estimation error covariance matrix**
The covariance matrix $P_{\tilde{\mathbf{x}}_{\mathsf{ML}}}$ represents the uncertainty of our estimate:
$$P_{\tilde{\mathbf{x}}_{\mathsf{ML}}} = \mathcal{E}\left\{ \left( \mathbf{x} - \hat{\mathbf{x}}_{\mathsf{ML}} \right) \left( \mathbf{x} - \hat{\mathbf{x}}_{\mathsf{ML}} \right)^{T} \middle| \mathbf{x} \right\} = \mathcal{E}\left\{ \tilde{\mathbf{x}}_{\mathsf{ML}} \tilde{\mathbf{x}}_{\mathsf{ML}}^{T} \middle| \mathbf{x} \right\}$$
Substituting the error expression and simplifying:
$$= \left( C^{T} R^{-1} C \right)^{-1} C^{T} R^{-1} \mathcal{E}\left\{ e e^{T} \middle| \mathbf{x} \right\} R^{-1} C \left( C^{T} R^{-1} C \right)^{-1} = \left( C^{T} R^{-1} C \right)^{-1}$$

#### Theorem (Cramér–Rao)
The Cramér–Rao bound provides a lower limit on the variance of any unbiased estimator. Let $\hat{x}(y)$ be an unbiased estimate of parameter $x$. Then the covariance matrix is bounded by the inverse of the **Fisher Information Matrix** $F(x)$:
$$P_{\tilde{x}} \geq F^{-1}(x)$$

The Fisher Information Matrix is defined as:
$$F(x) = \mathcal{E}\left\{ \left( \frac{\partial \ln I(x|y)}{\partial x} \right) \left( \frac{\partial \ln I(x|y)}{\partial x} \right)^T \right\} = -\mathcal{E}\left\{ \frac{\partial^2 \ln I(x|y)}{\partial x^2} \right\}$$
Equality (efficiency) applies if and only if the score function is linear in the estimation error: $\frac{\partial \ln I(x|y)}{\partial x} = k(x)(x - \hat{x})$.

![](_page_26_Picture_12.jpeg)
![](_page_26_Picture_13.jpeg)

#### **Proof: Estimate is unbiased**
By the definition of unbiasedness:
$$\mathcal{E}\left\{\hat{x}(y) - x \mid x\right\} = \int (\hat{x}(y) - x) \, p(y \mid x) dy = 0$$

Taking the derivative with respect to $x$:
$$\frac{\partial}{\partial x} \int (\hat{x}(y) - x) \, p(y|x) dy = -\int p(y|x) dy + \int (\hat{x}(y) - x) \, \frac{\partial p(y|x)}{\partial x} \, dy = 0$$
The first term $\int p(y|x)dy = 1$. Using the log-derivative identity $\frac{\partial p}{\partial x} = p \frac{\partial \ln p}{\partial x}$, we obtain:
$$\int (\hat{x}(y) - x) \frac{\partial \ln I(x|y)}{\partial x} p(y|x) dy = 1$$

Applying the **Schwarz inequality** $\mathcal{E}\{f(y)g(y)\}^2 \leq \mathcal{E}\{f^2(y)\}\mathcal{E}\{g^2(y)\}$ to this result yields:
$$\int (\hat{x}(y)-x)^2 \, p(y|x) \, dy \times \int \left\{ \frac{\partial \ln I(x|y)}{\partial x} \right\}^2 p(y|x) \, dy = \sigma_{\tilde{x}}^2 \, F(x) \ge 1$$

**Interpretation:** The Fisher Information represents the "sharpness" or mean curvature of the log-likelihood function. A more curved likelihood function implies more information and thus a lower possible estimation error variance.

![](_page_27_Picture_13.jpeg)