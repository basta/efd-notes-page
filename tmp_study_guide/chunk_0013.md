# Linear Mean Square Estimate (3)

#### **Interpretation of the LMS Formula**
The Linear Mean Square (LMS) estimate can be viewed as the prior mean $\mu_x$ adjusted by a correction term. This correction is proportional to the innovation (the difference between the observed data $y$ and its expected value $\mu_y$).

$$\hat{x}_{\mathsf{LMS}}(y) = \mu_{\mathsf{x}} + P_{\mathsf{x}\mathsf{y}}P_{\mathsf{y}\mathsf{y}}^{-1}\left(y - \mu_{\mathsf{y}}\right)$$

Alternatively, we can express this in terms of the deviation from the mean:
$$\hat{x}_{\mathsf{LMS}}(y) - \mu_{\mathsf{x}} = P_{\mathsf{x}\mathsf{y}}P_{\mathsf{y}\mathsf{y}}^{-1}\left(y - \mu_{\mathsf{y}}\right)$$

The term $P_{xy}P_{yy}^{-1}$ acts as a **correction gain** (often referred to as the gain matrix), which determines how much the observation $y$ should influence the estimate of $x$ based on the cross-covariance between them.

### **LMS Error Covariance**
A critical property of the LMS estimate is that the error covariance matrix $P_{\tilde{x}_{LMS}}$ is independent of the actual realized value of the data $y$. It depends only on the prior second-order moments of the joint distribution.

The error is defined as $\tilde{x} = x - \hat{x}_{LMS}(y)$. Substituting the LMS formula:
$$P_{\tilde{x}_{LMS}} = \mathcal{E}\left\{ (x - \hat{x}_{LMS}(y)) (x - \hat{x}_{LMS}(y))^{T} \right\}$$
$$= \mathcal{E}\left\{ \left( (x - \mu_{x}) - P_{xy}P_{yy}^{-1}(y - \mu_{y}) \right) \left( (x - \mu_{x}) - P_{xy}P_{yy}^{-1}(y - \mu_{y}) \right)^{T} \right\}$$

Expanding this expectation and simplifying yields the Schur complement of $P_{yy}$ in the joint covariance matrix:
$$P_{\tilde{x}_{LMS}} = P_{xx} - P_{xy}P_{yy}^{-1}P_{yx}$$

#### **Orthogonality Principle for LMS Estimate**
In the context of linear estimation, the orthogonality principle states that the estimation error is orthogonal to any **linear** function of the observed data, $g(y) = Ay + b$. This implies that the error contains no linear information that could be further extracted from $y$.

Specifically, the error is orthogonal to a constant (ensuring the estimate is unbiased):
$$\operatorname{tr} \mathcal{E} \left\{ 1 \times \left( x - \hat{x}_{\mathsf{LMS}}(y) \right)^T \right\} = 0$$

And the error is orthogonal to the data $y$ itself:
$$\operatorname{tr} \mathcal{E} \left\{ y \left( x - \hat{x}_{\mathsf{LMS}}(y) \right)^T \right\} = 0$$

![](_page_20_Picture_10.jpeg)
![](_page_20_Picture_11.jpeg)

---

### MS and LMS Estimate for Normally Distributed Variables

When the variables $x$ and $y$ are jointly Gaussian (normally distributed), the relationship between the MS and LMS estimates becomes particularly elegant.

**Joint Normal p.d.f.**
Consider $y$ and $x$ as vectors with $n_y$ and $n_x$ elements respectively:
$$p\left(\begin{bmatrix} y \\ x \end{bmatrix}\right) = \mathcal{N}\left(\begin{bmatrix} \mu_y \\ \mu_x \end{bmatrix}; \begin{bmatrix} P_{yy} & P_{yx} \\ P_{xy} & P_{xx} \end{bmatrix}\right)$$

The full probability density function is given by:
$$p\left(\begin{bmatrix} y \\ x \end{bmatrix}\right) = (2\pi)^{-\frac{n_y+n_x}{2}} \det \begin{bmatrix} P_{yy} & P_{yx} \\ P_{xy} & P_{xx} \end{bmatrix}^{-\frac{1}{2}} \exp \left\{-\frac{1}{2} \begin{bmatrix} y - \mu_y \\ x - \mu_x \end{bmatrix}^T \begin{bmatrix} P_{yy} & P_{yx} \\ P_{xy} & P_{xx} \end{bmatrix}^{-1} \begin{bmatrix} y - \mu_y \\ x - \mu_x \end{bmatrix}\right\}$$

### Conditional p.d.f.
Using the chain rule $p(x, y) = p(y) p(x|y)$, we can factor the joint Gaussian distribution into the marginal distribution of $y$ and the conditional distribution of $x$ given $y$:
$$p\left(\begin{bmatrix} y \\ x \end{bmatrix}\right) = \mathcal{N}(y; \mu_y, P_{yy}) \times \mathcal{N}(x; \mu_{x|y}, P_{x|y})$$

Where the conditional parameters are:
$$\mu_{x|y} = \mu_x + P_{xy}P_{yy}^{-1}(y - \mu_y), \qquad P_{x|y} = P_{xx} - P_{xy}P_{yy}^{-1}P_{yx}$$

**Conclusion:** For Gaussian distributions, the conditional mean (the MS estimate) is a linear function of the data. Therefore, the optimal Mean Square estimate and the optimal Linear Mean Square estimate are identical:
$$\hat{x}_{\mathsf{MS}}(y) = \hat{x}_{\mathsf{LMS}}(y)$$

![](_page_21_Picture_10.jpeg)

#### **How to Factorize the Joint p.d.f.?**
To derive the conditional distribution, we factor the joint covariance matrix using a triangular transformation:
$$\begin{bmatrix} P_{yy} & P_{yx} \\ P_{xy} & P_{xx} \end{bmatrix} \begin{bmatrix} I & -P_{yy}^{-1}P_{yx} \\ 0 & I \end{bmatrix} = \begin{bmatrix} P_{yy} & 0 \\ P_{xy} & P_{xx} - P_{xy}P_{yy}^{-1}P_{yx} \end{bmatrix}$$

Because the transformation matrix has a unit determinant, the joint determinant factors as:
$$\det \begin{bmatrix} P_{yy} & P_{yx} \\ P_{xy} & P_{xx} \end{bmatrix} = \det (P_{yy}) \det (P_{xx} - P_{xy}P_{yy}^{-1}P_{yx})$$

The inverse of the joint covariance matrix can also be partitioned:
$$\begin{bmatrix} P_{yy} & P_{yx} \\ P_{xy} & P_{xx} \end{bmatrix}^{-1} = \begin{bmatrix} P_{yy}^{-1} + P_{yy}^{-1} P_{yx} P_{x|y}^{-1} P_{xy} P_{yy}^{-1} & -P_{yy}^{-1} P_{yx} P_{x|y}^{-1} \\ -P_{x|y}^{-1} P_{xy} P_{yy}^{-1} & P_{x|y}^{-1} \end{bmatrix}$$

This allows us to factor the quadratic form in the exponent:
$$\begin{bmatrix} y - \mu_y \\ x - \mu_x \end{bmatrix}^T \begin{bmatrix} P_{yy} & P_{yx} \\ P_{xy} & P_{xx} \end{bmatrix}^{-1} \begin{bmatrix} y - \mu_y \\ x - \mu_x \end{bmatrix} = (y - \mu_y)^T P_{yy}^{-1} (y - \mu_y) + (x - \mu_{x|y})^T P_{x|y}^{-1} (x - \mu_{x|y})$$

![](_page_22_Picture_11.jpeg)

---

### Maximum Likelihood Estimate

### **Classical (Frequentist) Approach**
In the frequentist framework, the parameter $x$ is treated as a **deterministic but unknown constant**, rather than a random variable. Consequently, there is no prior distribution $p(x)$, and the conditional probability $p(x|y)$ is not defined in the Bayesian sense. Instead, we rely on the probability of the observed data given the parameter:
$$y \sim p(y|x)$$

#### **Likelihood Function**
The likelihood function $l(x|y)$ is simply the conditional p.d.f. $p(y|x)$ viewed as a function of the unknown parameter $x$ for a fixed set of observed data $y$:
$$l(x|y) = p(y|x)$$

### **Maximum Likelihood (ML) Estimate**
The goal of ML estimation is to find the value of $x$ that makes the observed data $y$ "most likely":
$$\hat{x}_{\mathsf{ML}}(y) = \arg\max_{x} l(x|y)$$

Since the natural logarithm is a monotonically increasing function, maximizing the likelihood is equivalent to maximizing the **log-likelihood**. The estimate is found by solving the likelihood equation:
$$\left. \frac{\partial \ln l(x|y)}{\partial x} \right|_{x = \hat{x}_{\text{ML}}} = 0$$

![](_page_23_Picture_14.jpeg)
![](_page_23_Picture_15.jpeg)