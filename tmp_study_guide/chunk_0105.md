# Kernel function

### **Polynomial model**

In a polynomial regression framework, the latent function $x(t)$ is modeled as a linear combination of polynomial basis functions. We assume a linear-in-parameters structure:

$$x(t) = \Phi^{T}(t)\theta$$

where the parameters $\theta$ follow a prior distribution $\theta \sim \mathcal{N}(0, \Sigma) = \mathcal{N}(0, \sigma^{2}I_{m})$.

▶ **m-dimensional basis-function space**
The feature vector $\Phi(t)$ maps the input $z(t)$ into a higher-dimensional space of polynomials:
$$\Phi(t) = \left(1, z(t), z^2(t), \ldots\right)^T$$

*   **Mean value**: Since the prior mean of $\theta$ is zero, the expected value of the process is $\mathcal{E}\{x(t)\} = \Phi^T(t)\mathcal{E}\{\theta\} = 0$.
*   **Kernel function**: The covariance between the process at two different times $t_1$ and $t_2$ is derived as:
$$k(t_1,t_2) = \sigma^2 \left(1, z(t_1), z^2(t_1), \ldots\right) \left(1, z(t_2), z^2(t_2), \ldots\right)^T = \sigma^2 \left(1 + z(t_1)z(t_2) + z^2(t_1)z^2(t_2) + \ldots\right)$$

#### **Kernel functions in a Hilbert space**

The "Kernel Trick" allows us to define the covariance directly through a scalar product of regressors in a feature space, which does not necessarily need to be finite-dimensional.

$$k(t_1, t_2) = \sigma^2 \Phi^T(t_1) \Phi(t_2) = \sigma^2 \langle \Phi(t_1), \Phi(t_2) \rangle$$

▶ **$l^2$ space**: If we consider square-summable sequences $\Phi(t) = \{\varphi_1(t), \varphi_2(t), \ldots\}$, the scalar product is well-defined provided that:
$$\sum_{i=1}^{\infty} \varphi_i^2(t) < \infty \implies k(t_1,t_2) = \sigma^2 \langle \Phi(t_1), \Phi(t_2) \rangle = \sigma^2 \sum_{i=1}^{\infty} \varphi_i(t_1) \varphi_i(t_2)$$

▶ **Kernel trick**: This approach is powerful because we can compute the similarity between points in an infinite-dimensional space using a simple kernel function, even when a parametric view (explicitly defining $\Phi$) is not computationally feasible.

![](_page_190_Picture_14.jpeg)

![](_page_190_Picture_15.jpeg)

### Squared-exponential (SE) kernel

The Squared-Exponential kernel (also known as the Radial Basis Function or Gaussian kernel) is the most widely used kernel in Gaussian Process Regression due to its smoothness properties.

#### Scalar model
Consider the model $y_i = x(z_i) + e_i$. When no explicit parametric representation is available, we assume a prior $x(\cdot) = 0$ and define the covariance between any two points $x_i$ and $x_j$ as:

$$\operatorname{cov}\{x_i, x_j\} = k(z_i, z_j) = \sigma^2 \exp\left(-\frac{1}{2\lambda^2} \|z_i - z_j\|^2\right)$$

*   **Length-scale parameter ($\lambda$)**: This determines the "similarity" or correlation between points. A large $\lambda$ results in a very smooth function (global character), while a small $\lambda$ allows the function to change rapidly (local character).

![](_page_191_Figure_6.jpeg)

#### Multivariable model
For inputs $z$ in higher dimensions, the kernel can be generalized to account for different scales in different input dimensions:

*   **Kernel function**: $k(z_i,z_j) = \sigma^2 \exp\left(-\frac{1}{2}\left(z_i-z_j\right)^T\Lambda^{-1}\left(z_i-z_j\right)\right)$, where $\Lambda = \text{diag}(\lambda_1^2, \dots, \lambda_n^2)$.
*   **Hyperparameters**: 
    *   $\sigma^2$: Represents the overall variance (amplitude) of the function $x(\cdot)$.
    *   $\lambda_1, \ldots, \lambda_n$: These are characteristic length-scales. This "Automatic Relevance Determination" (ARD) structure allows the model to be directionally sensitive, effectively ignoring inputs with very large $\lambda$ values.
*   **Connection**: This structure is mathematically related to Radial Basis Function (RBF) Neural Networks.

![](_page_191_Picture_11.jpeg)