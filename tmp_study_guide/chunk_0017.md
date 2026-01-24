# Comparison of MS and a ML estimate

In estimation theory, the **Minimum Square (MS)** and **Maximum Likelihood (ML)** estimators are two of the most fundamental tools. While they often yield similar results under Gaussian assumptions, they originate from different philosophical and mathematical frameworks.

#### **Linear Measurement Model**
Consider a standard linear measurement model where the observation $y$ is a linear combination of the unknown parameters $x$ and additive Gaussian noise $e$:
$$y = Cx + e, \quad e \sim \mathcal{N}(0, R)$$
Here, $C$ is the observation matrix and $R$ is the covariance matrix of the measurement noise.

---

#### **MS Estimate: Minimizing Parameter Error**
The Minimum Square (MS) estimator, often associated with Bayesian Minimum Mean Square Error (MMSE), focuses on minimizing the expected value of the squared error of the parameter itself.

*   **Objective**: Minimize the parameter error variance.
    $$J_{\mathsf{MS}} = \mathcal{E}\left\{ \left( x - \hat{x}_{\mathsf{MS}} \right)^{\mathsf{T}} \left( x - \hat{x}_{\mathsf{MS}} \right) \right\}$$
*   **Estimation Formula**:
    The MS estimate incorporates prior knowledge about $x$ (mean $\mu_x$ and covariance $P_{xx}$). The resulting posterior covariance $P_{\tilde{\mathbf{x}}_{\mathsf{MS}}}$ and the estimate $\hat{\mathbf{x}}_{\mathsf{MS}}$ are:
    $$P_{\tilde{\mathbf{x}}_{\mathsf{MS}}} = \left(P_{\mathsf{xx}}^{-1} + C^{\mathsf{T}} R^{-1} C\right)^{-1}$$
    $$\hat{\mathbf{x}}_{\mathsf{MS}} = \mu_{\mathsf{x}} + P_{\tilde{\mathbf{x}}_{\mathsf{MS}}} C^{\mathsf{T}} R^{-1} \left(y - C \mu_{\mathsf{x}}\right)$$

---

#### **ML Estimate: Minimizing Prediction Error**
The Maximum Likelihood (ML) estimator treats $x$ as a fixed but unknown constant. It seeks the value of $x$ that makes the observed data $y$ most probable.

*   **Objective**: Minimize the weighted prediction error (residual).
    $$J_{\mathsf{ML}} = \mathcal{E}\left\{ \left( y - C\hat{x}_{\mathsf{ML}} \right)^{\mathsf{T}} R^{-1} \left( y - C\hat{x}_{\mathsf{ML}} \right) \right\}$$
*   **Estimation Formula**:
    The ML estimate does not use prior information. Its covariance and state estimate are:
    $$P_{\tilde{\mathbf{x}}_{\mathsf{ML}}} = \left(C^{\mathsf{T}}R^{-1}C\right)^{-1}$$
    $$\hat{\mathbf{x}}_{\mathsf{ML}} = P_{\tilde{\mathbf{x}}_{\mathsf{ML}}}C^{\mathsf{T}}R^{-1}\mathbf{y}$$

#### **Relationship Between MS and ML**
The ML estimate can be viewed as a **limiting case of the MS estimate** when there is no prior information available (i.e., the prior uncertainty is infinite). Mathematically, this occurs when:
$$\mu_{\scriptscriptstyle \mathsf{X}} = 0, \quad P_{\scriptscriptstyle \mathsf{XX}}^{-1} = 0 \quad (\text{or } P_{\scriptscriptstyle \mathsf{XX}} \to \infty)$$

Conversely, the MS estimate can be interpreted as a **Regularized ML estimate**. By adding $P_{xx}^{-1}$ to the information matrix, we prevent numerical instability and incorporate prior beliefs:
$$P^{-1}_{\tilde{x}_{ML, reg}} = P^{-1}_{xx} + C^T R^{-1} C$$

![](_page_29_Picture_16.jpeg)

![](_page_29_Picture_17.jpeg)

---

#### **Deriving the MS Estimate Formulas**
To derive the MS covariance, we utilize the **Matrix Inversion Lemma (MIL)**:
$$(A + BCD)^{-1} = A^{-1} - A^{-1}B(C^{-1} + DA^{-1}B)^{-1}DA^{-1}$$

1.  **MS Covariance**:
    The posterior covariance can be expressed in terms of the prior $P_{xx}$ and the measurement update:
    $$P_{\tilde{x}_{MS}} = P_{xx} - P_{xy} P_{yy}^{-1} P_{yx} = P_{xx} - P_{xx} C^{T} (CP_{xx} C^{T} + R)^{-1} CP_{xx}$$
    Applying the MIL, this simplifies to the information form:
    $$P_{\tilde{x}_{MS}} = (P_{xx}^{-1} + C^{T} R^{-1} C)^{-1}$$

2.  **MS Mean**:
    The estimate is the prior mean adjusted by the innovation (the difference between actual and predicted measurements):
    $$\hat{x}_{MS} = \mu_{x} + P_{xy} P_{yy}^{-1} (y - \mu_{y}) = \mu_{x} + P_{xx} C^{T} (CP_{xx} C^{T} + R)^{-1} (y - C\mu_{x})$$
    Using the covariance relationship, this is often written as:
    $$\hat{x}_{MS} = \mu_{x} + P_{\tilde{x}_{MS}} C^{T} R^{-1} (y - C\mu_{x})$$

---

### Examples of ML estimates

#### **Alternative/Bernoulli Distribution**
Consider a coin-tossing experiment where we want to estimate the probability of success $\theta$.

*   **Model**: For a single trial $x \in \{0,1\}$, the probability mass function is:
    $$p(x|\theta) = \theta^{x}(1-\theta)^{1-x}$$
*   **Likelihood**: For $n$ independent trials, the joint likelihood is the product of individual probabilities:
    $$p_n(x|\theta) = \prod_{i=1}^n \theta^{x_i} (1-\theta)^{1-x_i}$$
*   **Log-Likelihood**:
    $$L_n(\theta) = \sum_{i=1}^n \{x_i \ln \theta + (1-x_i) \ln(1-\theta)\} = n\bar{X} \ln \theta + n(1-\bar{X}) \ln(1-\theta)$$
    where $\bar{X}$ is the sample average.
*   **Optimization**: Setting the derivative $\frac{dL_n(\theta)}{d\theta} = 0$ yields:
    $$\widehat{\theta}_{ML} = \bar{X}$$

**Conclusions**:
*   The ML estimate for a Bernoulli process is simply the **sample average**.
*   This estimate is computationally efficient and can be **updated recursively** as new data arrives.

![](_page_31_Picture_13.jpeg)