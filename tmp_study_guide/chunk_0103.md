# <span id="page-181-0"></span>**8. Gaussian process regression**

Gaussian Process Regression (GPR) is a powerful non-parametric Bayesian approach to regression. Unlike traditional regression that learns parameters for a fixed function, GPR infers a distribution over functions themselves. To understand GPR, we must first establish the foundations of random variables and random processes.

![](_page_181_Picture_1.jpeg)

### Random variable and random process

#### **Probability space**
A probability space is defined by a set of elementary events $S = \{\zeta_1, \dots, \zeta_n\}$.
*   $\mathcal{A} \subseteq \mathcal{S}$ represents an event.
*   $\mathcal{A} = \mathcal{S}$ is the **certain event**.
*   $\mathcal{A} = \emptyset$ is the **impossible event**.

The **probability of an event** $P(A)$ must satisfy the Kolmogorov axioms:
1.  $P(A) \geq 0$ (Non-negativity).
2.  $P(S) = 1$ (Normalization).
3.  If $A \cap B = \emptyset$, then $P(A \cup B) = P(A) + P(B)$ (Additivity).

### **Random variable**
A random variable is a mapping $S \mapsto \mathbb{R}$, where a real value $X(\zeta_i)$ is assigned to each outcome $\zeta_i$ of an experiment. For this mapping to be valid:
1.  The set $\{\zeta_i \mid X(\zeta_i) \leq x\}$ must be a valid event.
2.  The limits must be well-behaved: $P(\{X(\zeta_i) = -\infty\}) = 0$ and $P(\{X(\zeta_i) = \infty\}) = 1$.

**Cumulative Distribution Function (CDF) and Probability Density Function (PDF):**
The CDF describes the probability that $X$ takes a value less than or equal to $x$:
$$F_X(x) = P\{X \le x\}, \qquad f_X(x) = \frac{dF_X(x)}{dx}$$

![](_page_182_Picture_15.jpeg)

### Random variable and random process

#### **Random process**
A random process (or stochastic process) is a mapping $\mathbb{T} \times \mathcal{S} \mapsto \mathbb{R}$, assigning a time function $X(t, \zeta_i)$ to each outcome $\zeta_i$.
*   If $\mathbb{T} = \mathbb{R}$, it is a **continuous-time process**.
*   If $\mathbb{T} = \mathbb{N}$, it is a **discrete-time process**.

**Interpretations of $X(t, \zeta)$:**
1.  **Family of functions**: Both $t$ and $\zeta$ vary.
2.  **Realization (Sample Path)**: Fixed $\zeta$, variable $t$. This is a single observed trajectory.
3.  **Random Variable**: Fixed $t$, variable $\zeta$. The state of the process at a specific moment.
4.  **Number**: Fixed $t$ and fixed $\zeta$.

**Distribution Functions:**
*   **First order**: $f_X(x, t)$ describes the distribution at a single time $t$.
*   **Second order**: $f_X(x_1, x_2, t_1, t_2)$ describes the joint distribution of the process at two different times, $t_1$ and $t_2$.
*   **n-th order**: Generalizes to the joint distribution of $X(t_1), \dots, X(t_n)$.

![](_page_183_Picture_16.jpeg)
![](_page_183_Picture_17.jpeg)

### Random variable and random process

**Mean value**: The expected value of the process at time $t$:
$$\mu_X(t) = \mathcal{E}\{X(t)\} = \int x \, f_X(x,t) dx$$

**Correlation function**: Measures the linear relationship between values at different times:
$$R_X(t_1, t_2) = \mathcal{E}\{X(t_1)X(t_2)\}$$

**Covariance function**: Measures the correlation of the deviations from the mean:
$$C_X(t_1,t_2) = \mathcal{E}\{ (X(t_1) - \mu(t_1))(X(t_2) - \mu(t_2)) \}$$

### **Stationarity**
A process is **stationary** if its statistical properties do not change over time.
*   **First-order stationarity**: The mean is constant, $\mu_X(t) = \text{constant}$.
*   **Second-order (Wide-sense) stationarity**: The correlation/covariance depends only on the time lag $\tau = t_1 - t_2$, rather than absolute time.
    $$R_X(t_1, t_2) = R_X(t_1 - t_2)$$

![](_page_184_Picture_13.jpeg)

## Gaussian process

### **Definition**
A process $X(t)$ is **Gaussian** if any finite collection of random variables $X(t_1), \dots, X(t_n)$ has a jointly normal distribution.

#### **Properties**
For a stationary Gaussian process, the joint distribution is entirely defined by the mean $\mu$ and the covariance function $C_X(t_i - t_j)$.

**Conditioning Property**:
If $x$ and $y$ are jointly Gaussian:
$$p\left(\left[\begin{array}{c} y\\x\end{array}\right]\right) = \mathcal{N}\left(\left[\begin{array}{c} \mu_y\\\mu_x\end{array}\right]; \left[\begin{array}{cc} P_{yy} & P_{yx}\\P_{xy} & P_{xx}\end{array}\right]\right)$$
The conditional distribution $p(x|y)$ is also Gaussian:
$$\mu_{x|y} = \mu_{x} + P_{xy} P_{yy}^{-1} (y - \mu_{y}), \quad P_{x|y} = P_{xx} - P_{xy} P_{yy}^{-1} P_{yx}$$

![](_page_185_Picture_10.jpeg)

### Regression - functional space view

#### **GPR Model**
In GPR, we assume the underlying function $x(t)$ follows a Gaussian Process, and we observe noisy versions $y(t)$:
$$y(t) = x(t) + e(t), \quad e(t) \sim \mathcal{N}(0, \sigma_e^2)$$
The GP is defined by its mean function $\mu(t)$ and covariance (kernel) function $k(t_1, t_2)$:
$$x(t) \sim \mathcal{GP}(\mu(t), k(t_1, t_2))$$

The covariance matrix for a set of observations is constructed using the kernel:
$$\operatorname{cov}\{y\} = K(Z, Z) + \sigma_e^2 I$$
where $K(Z, Z)$ is the kernel matrix with entries $K_{ij} = k(t_i, t_j)$.

![](_page_186_Picture_11.jpeg)

### Regression - functional space view: Example
Consider a linear model $y = z\theta + e$ with a prior $\theta \sim \mathcal{N}(0, \sigma_\theta^2)$.
*   **Prediction**: To predict $x(t)$ at a new point given data $y$, we use the joint covariance matrix:
    $$\operatorname{cov}\left\{\begin{array}{c} x(t) \\ y \end{array}\right\} = \left[\begin{array}{cc} P_{xx} & P_{xy} \\ P_{yx} & P_{yy} \end{array}\right]$$
*   **Conditional Mean**: The prediction is a weighted sum of kernels:
    $$\mu_{x|y} = \sum_{j=1}^n w_j k(t, t_j)$$
    where the weights $d_y = P_{yy}^{-1}y$ can be precalculated from the training data.

![](_page_187_Picture_12.jpeg)
![](_page_187_Picture_13.jpeg)

### Generic prediction formula

#### **Noise-free observations**
If we observe the function exactly ($x_i$), the joint distribution of observed $X$ and predicted $X^*$ is:
$$\begin{bmatrix} X \\ X^* \end{bmatrix} \sim \mathcal{N} \left\{ 0, \begin{bmatrix} K(Z,Z) & K(Z,Z^*) \\ K(Z^*,Z) & K(Z^*,Z^*) \end{bmatrix} \right\}$$
The predictor is:
$$\mathcal{E}\{X^*|X\} = K(Z^*,Z)K^{-1}(Z,Z)X$$

#### **Noisy observations**
When observations $Y$ include noise $\sigma_e^2$, the predictor accounts for the uncertainty:
$$\mathcal{E}\{X^*|Y\} = K(Z^*, Z)\left(K(Z, Z) + \sigma_e^2 I\right)^{-1} Y$$
$$\text{cov}\{X^*|Y\} = K(Z^*, Z^*) - K(Z^*, Z) (K(Z, Z) + \sigma_e^2 I)^{-1} K(Z, Z^*)$$
The term $(K(Z, Z) + \sigma_e^2 I)^{-1}$ effectively regularizes the inversion, handling the noise in the training data.

![](_page_188_Picture_15.jpeg)
![](_page_188_Picture_16.jpeg)