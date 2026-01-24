# Kernel function

In Gaussian Process Regression, the **kernel function** $k(t_1, t_2)$ (also known as the covariance function) is the fundamental building block that defines the properties of the functions we are modeling. It encodes our prior assumptions about the relationship between points in the input space, such as smoothness, periodicity, or decay.

#### **Linear Model**

Consider a simple linear model where the state $x(t)$ is a linear combination of the input vector $z(t)$:
$$x(t) = z^{T}(t)\theta$$
We assume a prior distribution for the parameters $\theta \sim \mathcal{N}(0, \Sigma)$. In the simplest case, where parameters are independent and identically distributed, $\Sigma = \sigma^{2}I_{n}$.

*   **Mean Value**: Since the expected value of the parameters is zero, the mean of the process is also zero:
    $$\mathcal{E}\{x(t)\} = \mathcal{E}\{z^{T}(t)\theta\} = z^{T}(t)\mathcal{E}\{\theta\} = 0$$
*   **Kernel Function**: The covariance between the process values at two different times $t_1$ and $t_2$ is derived as:
    $$k(t_1, t_2) = \mathcal{E} \{ x(t_1)x(t_2) \} = \mathcal{E} \{ z^{T}(t_1)\theta\theta^{T}z(t_2) \}$$
    By moving the expectation inside, we see that the kernel depends on the parameter covariance $\Sigma$:
    $$k(t_1, t_2) = z^{T}(t_1)\Sigma z(t_2) = \sigma^2 z^{T}(t_1)z(t_2)$$
    This demonstrates that the covariance between output values is strictly a function of the input values.

#### **Linear-in-Parameters Model**

We can extend this concept to non-linear mappings by using a **basis function space**. Here, the state is defined as:
$$x(t) = \Phi^{T}(t)\theta$$
where $\Phi(t)$ is an $m$-dimensional vector of basis functions $\varphi$ acting on the inputs $z(t)$:
$$\Phi(t) = \left(\varphi_1(z(t)), \dots, \varphi_m(z(t))\right)^T$$
Assuming the same prior distribution $\theta \sim \mathcal{N}(0, \sigma^{2}I_{m})$, we find:

*   **Mean Value**: The process remains zero-mean:
    $$\mathcal{E}\{x(t)\} = \mathcal{E}\{\Phi^{T}(t)\theta\} = 0$$
*   **Kernel Function**: The covariance is now defined by the inner product of the basis functions:
    $$k(t_1, t_2) = \mathcal{E}\{x(t_1)x(t_2)\} = \mathcal{E}\{\Phi^T(t_1)\theta\theta^T\Phi(t_2)\}$$
    $$k(t_1, t_2) = \Phi^T(t_1)\Sigma\Phi(t_2) = \sigma^2\Phi^T(t_1)\Phi(t_2)$$

This formulation is powerful because it allows us to model complex non-linear behaviors while maintaining the analytical tractability of the Gaussian framework. By choosing different basis functions (polynomials, radial basis functions, etc.), we can change the "shape" of the functions the Gaussian Process can represent.

![](_page_189_Picture_16.jpeg)

![](_page_189_Picture_17.jpeg)