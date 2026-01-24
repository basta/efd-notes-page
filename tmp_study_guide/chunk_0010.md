# Multivariable Gaussian bell function (2)

In the multivariate case, the Gaussian distribution is not just a "bell curve" but a "bell surface" in higher dimensions. Understanding the geometry of this distribution is critical for estimation and control tasks.

### Covariance Ellipsoid Shape

The level sets (contours of constant probability density) of a multivariate normal distribution form ellipsoids. For a given threshold $\alpha$, the covariance ellipsoid $E_\alpha$ is defined by:

*   **Center:** The ellipsoid is centered at the mean vector $\hat{x}$.
*   **Semi-axes Size and Direction:** The geometry of the ellipsoid is governed by the spectral decomposition of the covariance matrix $P$.
    *   The **directions** of the semi-axes are given by the unit eigenvectors $v_i$ of $P$.
    *   The **lengths** of the semi-axes are proportional to $\sqrt{\alpha \lambda_i}$, where $\lambda_i$ are the corresponding eigenvalues.

#### **Example: Visualizing Correlation**

1.  **Uncorrelated Noise Data:**
    Consider a zero-mean process $\hat{x} = [0, 0]^T$ with identity covariance:
    $$P = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}, \ \lambda = \begin{bmatrix} 1.0 \\ 1.0 \end{bmatrix}, \ V = \begin{bmatrix} 1.0 & 0.0 \\ 0.0 & 1.0 \end{bmatrix}$$
    Because the eigenvalues are equal and the off-diagonal elements are zero, the contours are perfect circles (or spheres in 3D), indicating no correlation between variables.
    ![](_page_14_Figure_9.jpeg)

2.  **Correlated Noise Data:**
    Consider a zero-mean process $\hat{x} = [0, 0]^T$ where variables influence each other:
    $$P = \begin{bmatrix} 2 & 1 \\ 1 & 1 \end{bmatrix}, \ \lambda = \begin{bmatrix} 2.6 \\ 0.4 \end{bmatrix}, \ V = \begin{bmatrix} 0.8 & 0.5 \\ 0.5 & -0.8 \end{bmatrix}$$
    Here, the unequal eigenvalues stretch the circle into an ellipse. The eigenvectors show that the principal axis of uncertainty is rotated, reflecting the correlation between the components of $x$.
    ![](_page_14_Figure_12.jpeg)

![](_page_14_Picture_14.jpeg)

---

### Mean Square Estimate (MSE)

The Mean Square (MS) estimation problem is a fundamental pillar of estimation theory, aiming to find an estimate that minimizes the expected squared error.

#### **MS Problem Formulation**
*   **Objective:** Find an optimal estimator function $\hat{x}_{MS}(y)$.
*   **Variables:** Let $x$ be the hidden random vector to be estimated and $y$ be the vector of observable data.
*   **Information:** We assume knowledge of the joint probability density function $p(x, y)$.
*   **Criterion:** Minimize the Mean Square Error (MSE) $J_{MS}$:
    $$J_{MS} = \int \int (x - \hat{x}_{MS}(y))^{T} (x - \hat{x}_{MS}(y)) p(x, y) \, dx \, dy$$

#### **Minimization Strategy**
To solve this, we use the property of conditional probability $p(x, y) = p(x|y) p(y)$:
$$J_{MS} = \int \left[ \int (x - \hat{x}_{MS}(y))^T (x - \hat{x}_{MS}(y)) p(x|y) \, dx \right] p(y) \, dy$$

Since the marginal density $p(y)$ is always non-negative, minimizing the total integral $J_{MS}$ is equivalent to minimizing the inner integral for every possible realization of $y$:
$$J'_{MS}(y) = \int (x - \hat{x}_{MS}(y))^T (x - \hat{x}_{MS}(y)) p(x|y) \, dx$$

This inner integral represents the conditional mean square error. As we will see in the following section, the solution to this minimization is the **conditional mean**, $\mathcal{E}\{x|y\}$.

![](_page_15_Picture_12.jpeg)