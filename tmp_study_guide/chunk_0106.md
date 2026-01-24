# Kernel functions

In Gaussian Process Regression, the kernel function (or covariance function) $k(z_1, z_2)$ is the fundamental building block that defines the properties of the functions we are modeling. It encodes our prior assumptions about the smoothness, periodicity, and general behavior of the underlying process.

### **Some other kernels**

Beyond the standard Squared-Exponential (SE) kernel, several other kernels allow us to model specific functional behaviors:

*   **Affine Kernel**: This kernel represents the space of all linear (affine) functions. It is defined as:
    $$k(z_1, z_2) = \sigma^2 (1 + z_1 z_2)$$
    Using this kernel in GPR is equivalent to performing Bayesian linear regression with a prior on the intercept and slope.

*   **Brownian Kernel**: This kernel describes a random walk process (Wiener process), where the value at a certain point is the integral of white noise. For a discrete process $x_k = \sum_{i=0}^{k} e_i$, the covariance is determined by the "overlap" in time:
    $$k(z_1, z_2) = \sigma^2 \min(z_1, z_2)$$

*   **Mixed Kernels**: In practice, real-world data often exhibits both global trends and local variations. We can combine kernels to capture these complex behaviors. For example, combining an Affine kernel (global linear trend) with an SE kernel (local non-linearities) allows the model to capture a general slope while remaining flexible enough to fit local deviations.

![](_page_192_Figure_7.jpeg)
![](_page_192_Figure_8.jpeg)
![](_page_192_Figure_9.jpeg)

### **Fundamental kernel property**

To be a valid kernel, a function must satisfy specific mathematical criteria:

1.  **Positive Semi-Definiteness**: For any set of input points $\{z_1, \dots, z_n\}$, the resulting covariance matrix $K$ (where $K_{ij} = k(z_i, z_j)$) must be positive semi-definite. This ensures that the variance of any linear combination of the random variables is non-negative.
2.  **Closure Properties**: Kernels are highly modular. The sum of two kernels, the product of two kernels, or an affine transformation of a kernel also results in a valid kernel. This allows for the construction of sophisticated models by layering simple prior information.

The process of selecting a kernel and then tuning its parameters (such as $\sigma^2$ or length-scales) is known as **hyperparameter optimization**, typically achieved by maximizing the marginal likelihood of the observed data.

<span id="page-192-13"></span>
![](_page_192_Picture_13.jpeg)