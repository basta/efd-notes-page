# Numerical implementation of bayesian estimation algorithms (2)

#### Conditioning for Gaussian variables – Results

When performing Bayesian estimation, we often need to derive the conditional distribution of parameters given new data. For Gaussian variables, the $LD$-factorization of the joint covariance matrix provides a numerically robust way to extract both marginal and conditional statistics.

Starting with the joint $LD$-factors:
$$\left| \left[ \begin{array}{c} d_y \\ d_{x|y} \end{array} \right]; \left[ \begin{array}{cc} L_y^T & K^T \\ 0 & L_{x|y}^T \end{array} \right] \right|$$

We can identify the following components:

*   **Factors of the marginal covariance matrix $P_y$:**
    The uncertainty regarding the output $y$ (before observing its actual value) is captured by:
    $$P_{y} = L_{y}D_{y}L_{y}^{T} = \left| d_{y}; L_{y}^{T} \right|$$

*   **Factors of the conditional covariance matrix $P_{x|y}$:**
    After observing $y$, the remaining uncertainty in $x$ (the parameters) is represented by the conditional covariance. The $LD$-factors are directly available from the lower block of the joint factorization:
    $$P_{x|y} = L_{x|y} D_{x|y} L_{x|y}^T = |d_{x|y}; L_{x|y}^T|$$

*   **Conditioned Mean $\mu_{x|y}$:**
    The updated estimate (mean) of $x$ given the observation $y$ is calculated as:
    $$\mu_{x|y} = \mu_x + KL_y^{-1}\varepsilon$$
    where $\varepsilon = y - \mu_y$ represents the **prediction error** or innovation.

#### Practical Implementation Notes

In the **scalar case** (where $y$ is a single measurement), the term $L_y$ simplifies to $1$. Consequently, the term $KL_y^{-1}$ simplifies directly to $K$, which corresponds to the **Kalman Gain**. 

The primary advantage of this approach is numerical stability. Rather than performing a full $LD$-factorization at every time step—which is computationally expensive—we implement a **direct update of the $LD$-factors**. This ensures that the covariance matrix remains positive-definite even in the presence of round-off errors, a common failure point in standard Kalman Filter implementations.

![](_page_91_Picture_13.jpeg)