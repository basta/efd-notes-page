# ARX Model

### **The ARX Model Structure**
The **ARX model** (Auto-Regressive model with eXternal input) is one of the most fundamental structures in system identification. It describes a system using a linear difference equation combined with a stochastic noise term $e(t)$, typically assumed to be white noise with zero mean and variance $\sigma_e^2$.

The general form of the difference equation is:
$$y(t) + a_1 y(t-1) + \dots + a_{n_a} y(t-n_a) = b_0 u(t) + b_1 u(t-1) + \dots + b_{n_b} u(t-n_b) + e(t)$$

This is often referred to as an **equation error model** because the noise term $e(t)$ enters the equation directly as a residual error in the difference relationship.

#### **Polynomial Representation**
Using the delay operator $d$ (where $d \cdot y(t) = y(t-1)$), we can define the following polynomials:
*   $a(d) = 1 + a_1 d + \dots + a_{n_a} d^{n_a}$
*   $b(d) = b_0 + b_1 d + \dots + b_{n_b} d^{n_b}$

Here, $n_a$ and $n_b$ are the **structural parameters** (orders) of the model. The model can then be written compactly as:
$$a(d)y(t) = b(d)u(t) + e(t)$$

#### **Fractional Form and Transfer Functions**
By rearranging the equation, we obtain the fractional form:
$$y(t) = \frac{b(d)}{a(d)} u(t) + \frac{1}{a(d)} e(t)$$
In this structure:
*   The **deterministic transfer function** $G(d) = \frac{b(d)}{a(d)}$ can be chosen to represent the system dynamics.
*   The **noise shaping filter** $H(d) = \frac{1}{a(d)}$ is defined implicitly by the denominator of the deterministic part. This coupling is a limitation of ARX, as the noise and system dynamics share the same poles.

![](_page_56_Picture_14.jpeg)

---

### **ARX Predictor**

To use the model for control or estimation, we derive the **one-step-ahead predictor**. Starting from the generic predictor form:
$$\hat{y}(t|t-1, u(t)) = H^{-1}(d)G(d)u(t) + \left(I - H^{-1}(d)\right)y(t)$$

Substituting $G(d) = \frac{b(d)}{a(d)}$ and $H(d) = \frac{1}{a(d)}$, we get:
$$\hat{y}(t|t-1,u(t)) = (1-a(d)) y(t) + b(d) u(t)$$
Expanding the polynomials, the prediction becomes a weighted sum of past observations and current/past inputs:
$$\hat{y}(t|t-1,u(t)) = -\sum_{i=1}^{n_a} a_i y(t-i) + \sum_{i=0}^{n_b} b_i u(t-i)$$

#### **Linear Regression Form**
The predictor can be written as a scalar product of a **parameter vector** $\theta$ and a **data vector (regressor)** $z(t)$:
*   $\theta = [a_1, a_2, \dots, a_{n_a}, b_0, b_1, \dots, b_{n_b}]^T$
*   $z(t) = [-y(t-1), -y(t-2), \dots, -y(t-n_a), u(t), u(t-1), \dots, u(t-n_b)]^T$

The predicted output is thus a **linear function of the parameters**:
$$\hat{y}(t|t-1) = z^{T}(t)\theta$$

Because of this linearity, ARX parameters can be estimated efficiently using **linear regression** (Least Squares). If the noise is Gaussian $e(t) \sim \mathcal{N}(0, \sigma_e^2)$, the conditional probability density of the output is:
$$p(y(t)|u(t),\mathcal{D}^{t-1},\theta) = \mathcal{N}\left(z^T(t)\theta, \sigma_e^2\right)$$

![](_page_57_Picture_16.jpeg)
![](_page_57_Picture_17.jpeg)

---

### **ARMAX Model**

The **ARMAX model** (Auto-Regressive Moving Average model with eXternal input) extends ARX by providing a more flexible description of the stochastic part using a **Moving Average (MA)** process for the noise.

The difference equation is:
$$y(t) + a_1 y(t-1) + \dots + a_{n_a} y(t-n_a) = b_0 u(t) + \dots + b_{n_b} u(t-n_b) + e(t) + c_1 e(t-1) + \dots + c_{n_c} e(t-n_c)$$

#### **Polynomial and Fractional Form**
Defining the monic polynomial $c(d) = 1 + c_1 d + \dots + c_{n_c} d^{n_c}$, the model is:
$$a(d)y(t) = b(d)u(t) + c(d)e(t) \quad \implies \quad y(t) = \frac{b(d)}{a(d)} u(t) + \frac{c(d)}{a(d)} e(t)$$
Unlike ARX, ARMAX allows for **independent properties** of the deterministic part $G(d)$ and the stochastic part $H(d) = \frac{c(d)}{a(d)}$, thanks to the additional $c(d)$ polynomial.

#### **ARMAX Predictor**
Using the generic predictor formula, the ARMAX predictor is:
$$\hat{y}(t|t-1) = \left(1 - a(d)\right)y(t) + b(d)u(t) + \left(c(d) - 1\right)\left(y(t) - \hat{y}(t|t-1)\right)$$
Note that the prediction now depends on previous **prediction errors** $\varepsilon(t-i) = y(t-i) - \hat{y}(t-i|t-i-1)$.

![](_page_58_Picture_16.jpeg)
![](_page_58_Picture_17.jpeg)

---

### **ARMAX Estimation and State-Space Equivalence**

#### **Pseudolinear Regression**
In ARMAX, the regressor $z(t)$ includes past prediction errors:
$$z(t) = [-y(t-1), \dots, -y(t-n_a), u(t), \dots, u(t-n_b), \varepsilon(t-1|t-2), \dots, \varepsilon(t-n_c|t-n_c-1)]^T$$
Since $\varepsilon$ depends on the parameters $\theta$, the prediction $\hat{y}(t|t-1) = z^T(t, \theta)\theta$ is **not a linear function of the parameters**. This requires **pseudolinear regression** or iterative optimization.

#### **State-Space Equivalence**
An ARMAX model can be represented in **observer canonical form**. By defining states to represent delayed terms, we can map the difference equation into:
$$x(t+1) = Ax(t) + Bu(t) + Ke(t)$$
$$y(t) = Cx(t) + Du(t) + e(t)$$
This highlights that ARMAX is essentially a state-space model where the noise enters through a specific gain $K$ (the Kalman gain in steady state).

![](_page_60_Figure_6.jpeg)
![](_page_60_Picture_7.jpeg)

---

### **Output Error (OE) Model**

The **OE model** assumes that the stochastic component is simply measurement noise $e(t)$ added to the "true" output $x(t)$ of a deterministic system:
$$x(t) = \frac{b(d)}{a(d)} u(t), \quad y(t) = x(t) + e(t)$$
This results in $H(d) = 1$. The predictor is purely a simulation of the deterministic system:
$$\hat{y}(t|t-1) = \frac{b(d)}{a(d)} u(t) = b(d)u(t) + (1 - a(d))\hat{y}(t|t-1)$$
Like ARMAX, the OE predictor is non-linear in parameters because the regressor $z(t)$ contains past **predicted** values $\hat{y}$ rather than past **observed** values $y$.

![](_page_61_Picture_12.jpeg)

---

### **Incremental Models**

In many industrial applications, disturbances are not white noise but rather piecewise constant. This is modeled by assuming the noise is a **random walk**: $v(t) = v(t-1) + e(t)$.
By differencing the ARX equation, we obtain the **incremental model**:
$$\Delta y(t) + a_1 \Delta y(t-1) + \dots = b_0 \Delta u(t) + b_1 \Delta u(t-1) + \dots + e(t)$$
where $\Delta y(t) = y(t) - y(t-1)$. These models are crucial for control because they naturally lead to **integral action**, allowing the controller to compensate for constant load disturbances.

---

### **The Least Squares Method**

The history of parameter estimation is rooted in the **Least Squares (LS)** method, first applied by Gauss in 1795 to predict the orbit of Ceres. The goal is to minimize the sum of squared residuals:
$$V(\theta) = \sum e_k^2$$
In the context of system identification, this provides the foundation for batch processing of data to find the optimal $\theta$ that fits the observed input-output behavior.

![](_page_64_Figure_9.jpeg)
![](_page_64_Figure_10.jpeg)