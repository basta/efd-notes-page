# Numerical implementation of bayesian estimation algorithms (3)

In practical control and estimation applications, maintaining numerical stability is paramount. Standard Kalman filter updates for the covariance matrix $P$ can become numerically unstable, potentially leading to non-positive definite matrices due to rounding errors. To mitigate this, we use the **LD-factorization** (also known as $LDL^T$ decomposition), where the covariance matrix is represented by a monic lower triangular matrix $L$ and a diagonal matrix $D$ with non-negative entries.

#### Linear regression with LD-factorized covariance matrix

The goal is to perform the Bayesian update directly on the factors of the covariance matrix.

**1. Algorithm Input:**
We start with the factorized prior covariance matrix at time $t$ given data up to $t-1$:
$$P(t|t-1) = L(t|t-1)D(t|t-1)L^{T}(t|t-1) = \left| d(t|t-1); L^{T}(t|t-1) \right|$$
Here, $d(t|t-1)$ represents the vector of diagonal elements of $D$.

**2. Joint Covariance Construction:**
To update our estimate based on a new observation $y(t) = z^{T}(t)\theta(t) + e(t)$, we consider the joint covariance matrix of the output $y(t)$ and the parameter vector $\theta(t)$. This joint structure can be represented in factorized form as:
$$\left| \begin{bmatrix} 1 \\ d(t|t-1) \end{bmatrix}; \begin{bmatrix} 1 & 0 \cdots 0 \\ L^{T}(t|t-1)z(t) & L^{T}(t|t-1) \end{bmatrix} \right|$$
*Exercise: Verify this by multiplying out the factors to show it reconstructs the joint covariance matrix.*

**3. Factor Transformation:**
The matrix above is not yet in the standard lower-triangular form required for the posterior factors. We apply a transformation—typically a **dyadic reduction algorithm** (such as the Bierman or Thornton updates)—to zero out the elements in the first row (except for the diagonal). This process effectively "pushes" the information from the observation into the parameter covariance.

$$\begin{bmatrix} 1 & 0 & 0 & \cdots & 0 & 0 \\ x & 1 & x & \cdots & x & x \\ x & 0 & 1 & \cdots & x & x \\ \vdots & & & \ddots & & \\ x & & & & 1 & x \\ x & & & & & 1 \end{bmatrix} \longrightarrow \begin{bmatrix} 1 & x & x & \cdots & x & x \\ 0 & 1 & x & \cdots & x & x \\ 0 & & 1 & \cdots & x & x \\ \vdots & & & \ddots & & \\ \vdots & & & \ddots & & \\ 0 & & & & & 1 & x \\ \vdots & & & & \ddots & \\ 0 & & & & & & 1 \end{bmatrix}$$

**4. Algorithm Output:**
After the transformation, we obtain the LD-factors of the joint distribution:
$$\left| \begin{bmatrix} d_{y}(t) \\ d(t|t) \end{bmatrix}; \begin{bmatrix} 1 & k^{T}(t) \\ 0 & L^{T}(t|t) \end{bmatrix} \right|$$

From this result, we can directly extract:
*   **$k(t)$**: The Kalman gain vector used to update the parameter mean.
*   **$d_{y}(t) = 1 + \zeta(t|t-1)$**: The normalized output variance (innovation covariance).
*   **$d(t|t), L(t|t)$**: The LD-factors of the posterior parameter covariance matrix $P(t|t)$.

![](_page_92_Picture_13.jpeg)

![](_page_92_Picture_14.jpeg)