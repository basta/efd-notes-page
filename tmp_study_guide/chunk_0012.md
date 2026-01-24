# Linear Mean Square Estimate (2)

#### **LMS Criterion Minimization**

To find the optimal linear estimator, we must minimize the Mean Square Error (MSE) criterion $J_{LMS}$ with respect to the matrix $A$ and the vector $b$.

▶ **Properties of the Trace Operator**
The cost function can be expressed using the trace operator, which simplifies the differentiation of scalar quadratic forms involving vectors:
$$J_{LMS} = \mathcal{E}\left\{ (x - Ay - b)^{T} (x - Ay - b) \right\} = \text{tr } \mathcal{E}\left\{ (x - Ay - b) (x - Ay - b)^{T} \right\}$$

By expanding the quadratic term and taking the expectation, we obtain:
$$= \text{tr } \left[ P_{xx} + A(P_{yy} + \mu_{y}\mu_{y}^{T})A^{T} + (b - \mu_{x})(b - \mu_{x})^{T} + 2A\mu_{y}(b - \mu_{x})^{T} - 2AP_{yx} \right]$$

*Helpful hint:* To simplify the derivation, represent the random variables as the sum of their mean and zero-mean deviation, e.g., $x = \mu_x + \tilde{x}$ and $y = \mu_y + \tilde{y}$.

▶ **Formulas from Matrix Analysis**
To find the stationary points, we utilize standard matrix calculus identities:
$$\frac{\partial}{\partial Y} \operatorname{tr}(XYZ) = X^T Z^T, \qquad \frac{\partial}{\partial X} \operatorname{tr}(XYX^T) = 2XY$$

▶ **Stationary Point Conditions**
Setting the partial derivatives of $J_{LMS}$ with respect to $A$ and $b$ to zero provides the necessary conditions for a minimum:
$$\frac{\partial}{\partial A}J_{LMS} = 2A(P_{yy} + \mu_y \mu_y^T) + 2(b - \mu_x)\mu_y^T - 2P_{xy} = 0$$
$$\frac{\partial}{\partial b}J_{LMS} = 2(b - \mu_x) + 2A\mu_y = 0$$

▶ **Resulting Estimate**
Solving the system of equations above (assuming the covariance matrix $P_{yy}$ is positive definite and thus invertible), we arrive at the optimal parameters:
$$A = P_{xy}P_{yy}^{-1}, \qquad b = \mu_x - P_{xy}P_{yy}^{-1}\mu_y$$

This result is significant because the optimal linear estimate **depends only on the first and second moments** (means and covariances) of the distribution, rather than the full probability density function.

![](_page_19_Picture_12.jpeg)