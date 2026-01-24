# Linear stochastic system (3)

### **Asynchronous sampling scheme**

In practical control systems, sampling may not always be perfectly synchronized. We consider a relative delay $\varepsilon = (T_s - T_c) / T_s$, where $T_s$ is the sampling period and $T_c$ relates to the continuous-time dynamics (as discussed in the sampling schemes of Chapter 4).

#### **Deterministic part of the model**
The discrete-time state-space matrices $(A, B, C, D)$ are derived from their continuous-time counterparts $(A_c, B_c, C_c)$ as follows:

$$A = e^{A_c T_s}, \qquad B = \int_0^{T_s} e^{A_c \nu} d\nu B_c$$

$$C = C_c e^{A_c \varepsilon T_s}, \qquad D = C_c \int_0^{\varepsilon T_s} e^{A_c \nu} d\nu B_c$$

#### **Stochastic part of the model**
The discretization of continuous-time white noise results in discrete-time noise processes. A critical observation here is that for $\varepsilon > 0$, the process noise and measurement noise become correlated ($S \neq 0$):

$$Q = \int_0^{T_s} e^{A_c \nu} Q_c e^{A_c^T \nu} d\nu$$

$$S = \int_0^{\varepsilon T_s} e^{A_c \nu} Q_c e^{A_c^T \nu} C_c^T d\nu$$

$$R = \int_0^{\varepsilon T_s} C_c e^{A_c \nu} Q_c e^{A_c^T \nu} C_c^T d\nu + R_c$$

![](_page_107_Picture_8.jpeg)
![](_page_107_Picture_9.jpeg)

---

### Kalman filter – conceptual solution

The Kalman filter provides an optimal estimate of the system state by combining a model-based prediction with real-time measurement data.

#### **System state estimate based on input and output data**
*   **Deterministic approach:** Uses a state observer where the error dynamics are governed by the matrix $(A - KC)$.
*   **Stochastic approach:** The Kalman filter treats the state as a random variable, where the estimate is defined by the conditional probability density function (c.p.d.f.) $p(x(t) | \mathcal{D}^t)$.

#### **State of stochastic system – probabilistic definition**
The system state $x(t)$ is a sufficient statistic; it contains all information from the past required to predict the future. This is expressed through the Markov property:
$$\rho(x(t+1), y(t) \mid x(t), u(t), \mathcal{D}^{t-1}) = \rho(x(t+1), y(t) \mid x(t), u(t))$$

1.  **Output equation (Marginal p.d.f.):**
    $$p(y(t)|x(t), u(t)) = \int p(x(t+1), y(t)|x(t), u(t)) dx(t+1)$$
2.  **State transition equation (Conditioned p.d.f.):**
    $$p(x(t+1)|x(t), u(t), y(t)) = \frac{p(x(t+1), y(t)|x(t), u(t))}{p(y(t)|x(t), u(t))}$$

![](_page_108_Picture_12.jpeg)
![](_page_108_Picture_13.jpeg)

---

### Kalman filter – conceptual solution (2)

#### **Model of a dynamic system - review**
The single-step predictor for the output $y(t)$ is calculated by marginalizing over the state $x(t)$:
$$\begin{split} \rho(y(t)|\,u(t), \mathcal{D}^{t-1}) &= \int \rho(y(t)\,|\,x(t), u(t), \mathcal{D}^{t-1})\,\rho(x(t)\,|\,u(t), \mathcal{D}^{t-1})\,dx(t) \\ &= \int \rho(y(t)|\,x(t), u(t))\rho(x(t)\,|\,\mathcal{D}^{t-1})\,dx(t) \end{split}$$

**Natural Condition of Control (N.C.C.):**
We assume $p(x(t) \mid \mathcal{D}^{t-1}, u(t)) = p(x(t) \mid \mathcal{D}^{t-1})$, meaning the choice of current input $u(t)$ does not provide additional information about the *current* state $x(t)$. This assumption is violated if the controller has access to more information than the filter (e.g., direct state feedback $u(t) = -k^T x(t)$).

![](_page_109_Picture_10.jpeg)

---

### Kalman filter – conceptual solution (3)

#### **State estimate development (uncorrelated noise)**
The estimation process follows a recursive two-step cycle:

1.  **Data-update (Filtration) step:**
    Updates the prior estimate $p(x(t) | \mathcal{D}^{t-1})$ using the new measurement $y(t)$. Using Bayes' rule and the N.C.C.:
    $$\rho(x(t) \mid \mathcal{D}^{t}) \propto \rho(y(t) \mid x(t), u(t)) \rho(x(t) \mid \mathcal{D}^{t-1})$$

2.  **Time-update (Prediction) step:**
    Projects the current estimate forward in time using the state transition model:
    $$p(x(t+1) \mid \mathcal{D}^{t}) = \int p(x(t+1) \mid x(t), u(t), y(t)) p(x(t) \mid \mathcal{D}^{t}) dx(t)$$

![](_page_110_Picture_11.jpeg)
![](_page_110_Picture_12.jpeg)

---

### Kalman filter algorithm

#### **Assumption**
We assume process noise $v(t)$ and measurement noise $e(t)$ are uncorrelated ($S=0$), allowing the data-update and time-update steps to be derived independently.

#### **Data-update step**
We consider the joint c.p.d.f. of the state and output. Under Gaussian assumptions:
$$\rho\left(\begin{bmatrix}x(t)\\y(t)\end{bmatrix}\middle|\mathcal{D}^{t-1}\right) = \mathcal{N}\left(\begin{bmatrix}\hat{x}(t|t-1)\\\hat{y}(t|t-1)\end{bmatrix};\begin{bmatrix}P(t|t-1)&P(t|t-1)C^T\\CP(t|t-1)&CP(t|t-1)C^T+R\end{bmatrix}\right)$$

The updated mean (state estimate) and covariance are found using the properties of conditional Gaussians:
*   **Updated State:** $\hat{x}(t|t) = \hat{x}(t|t-1) + L(t)(y(t) - C\hat{x}(t|t-1) - Du(t))$
*   **Kalman Gain:** $L(t) = P(t|t-1)C^{T} (CP(t|t-1)C^{T} + R)^{-1}$
*   **Updated Covariance:** $P(t|t) = P(t|t-1) - P(t|t-1)C^{T} (CP(t|t-1)C^{T} + R)^{-1} CP(t|t-1)$

![](_page_111_Picture_13.jpeg)