# Maximum Likelihood Estimate – example

To better understand the application of the Maximum Likelihood (ML) method, let us consider a classic problem in estimation theory: estimating a constant parameter from noisy measurements.

### **Example: Repeated Measurement with Gaussian Noise**

Consider a scenario where we observe a vector of measurements $\mathbf{y}$ related to an unknown deterministic parameter $\mathbf{x}$ through a linear model:
$$\mathbf{y} = \mathbf{C}\mathbf{x} + \mathbf{e}$$
In this model, $\mathbf{C}$ is a known observation matrix and $\mathbf{e}$ represents the measurement noise. We assume the noise follows a zero-mean Gaussian distribution with a known covariance matrix $\mathbf{R}$:
$$p_e(\mathbf{e}) = (2\pi)^{-n_y/2} |\mathbf{R}|^{-1/2} \exp\left\{-\frac{1}{2}\mathbf{e}^T\mathbf{R}^{-1}\mathbf{e}\right\}$$

#### **1. Deriving the Conditional Density**
For a fixed (given) value of $\mathbf{x}$, the measurement $\mathbf{y}$ is simply a linear transformation of the random variable $\mathbf{e}$. Using the transformation theorem for random variables:
$$\mathbf{y} = \mathbf{Ie} + \mathbf{Cx} \implies \mathbf{e} = \mathbf{y} - \mathbf{Cx}$$
Since the Jacobian of this transformation is the identity matrix, the conditional probability density $p(\mathbf{y}|\mathbf{x})$ is equivalent to the noise density shifted by the mean $\mathbf{Cx}$:
$$p(\mathbf{y}|\mathbf{x}) = p_e(\mathbf{y} - \mathbf{Cx})$$

#### **2. The Likelihood Function**
The likelihood function $l(\mathbf{x}|\mathbf{y})$ is defined as the conditional density $p(\mathbf{y}|\mathbf{x})$ viewed as a function of the unknown parameter $\mathbf{x}$:
$$l(\mathbf{x}|\mathbf{y}) = (2\pi)^{-n_y/2} |\mathbf{R}|^{-1/2} \exp\left\{-\frac{1}{2}(\mathbf{y} - \mathbf{Cx})^T \mathbf{R}^{-1}(\mathbf{y} - \mathbf{Cx})\right\}$$

#### **3. Log-Likelihood and Optimization**
To find the maximum, it is mathematically convenient to work with the natural logarithm of the likelihood (the log-likelihood), as the logarithm is a monotonic function and does not change the location of the maximum:
$$\ln l(\mathbf{x}|\mathbf{y}) = -\frac{1}{2}(\mathbf{y} - \mathbf{Cx})^{T}\mathbf{R}^{-1}(\mathbf{y} - \mathbf{Cx}) - \frac{n_{y}}{2}\ln(2\pi) - \frac{1}{2}\ln|\mathbf{R}|$$
To find the stationary point, we take the partial derivative with respect to $\mathbf{x}$ and set it to zero. This is known as the **likelihood equation**:
$$\frac{\partial \ln l(\mathbf{x}|\mathbf{y})}{\partial \mathbf{x}} = \mathbf{C}^{T} \mathbf{R}^{-1} (\mathbf{y} - \mathbf{Cx}) = 0$$

Solving this equation yields the ML estimate. Note that for Gaussian noise, maximizing the likelihood is equivalent to minimizing the weighted squared error $(\mathbf{y} - \mathbf{Cx})^T \mathbf{R}^{-1}(\mathbf{y} - \mathbf{Cx})$, which is the basis for the Weighted Least Squares method.

![](_page_24_Picture_13.jpeg)

![](_page_24_Picture_14.jpeg)