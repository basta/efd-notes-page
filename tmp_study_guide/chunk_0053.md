# ARX Model with Forgetting: Combined Time-Update and Data-Update Step

When implementing recursive estimation for time-varying systems, it is often convenient to combine the **time-update** (which accounts for parameter drift/uncertainty increase) and the **data-update** (which incorporates new measurements) into a single step. However, one must be cautious with time indices to distinguish between predicted (a priori) and filtered (a posteriori) estimates.

### Combined Recursion for Predicted Values
These formulas update the prediction at the next time step $t+1$ based on information available at time $t$.

$$
\hat{\theta}(t+1|t) = \hat{\theta}(t|t-1) + \frac{P(t|t-1)z(t)}{1+\zeta(t|t-1)} \varepsilon(t|t-1)
$$
$$
P(t+1|t) = \frac{1}{\varphi} \left( P(t|t-1) - \frac{P(t|t-1)z(t)z^{T}(t)P(t|t-1)}{1+\zeta(t|t-1)} \right)
$$

### Combined Recursion for Filtered Values
These formulas provide the current estimate $\hat{\theta}(t|t)$ by updating the previous filtered estimate from $t-1$. Note the inclusion of the forgetting factor $\varphi$ within the denominator of the gain.

$$
\hat{\theta}(t|t) = \hat{\theta}(t-1|t-1) + \frac{P(t-1|t-1)z(t)}{\varphi + z^{T}(t)P(t-1|t-1)z(t)} \varepsilon(t|t-1)
$$
$$
P(t|t) = \frac{1}{\varphi} \left( P(t-1|t-1) - \frac{P(t-1|t-1)z(t)z^{T}(t)P(t-1|t-1)}{\varphi + z^{T}(t)P(t-1|t-1)z(t)} \right)
$$

#### Key Definitions
*   **Normalized Innovation Variance:** $\zeta(t|t-1) = z^{T}(t)P(t|t-1)z(t)$
*   **Posterior Variance Projection:** $\zeta(t|t) = z^{T}(t)P(t|t)z(t)$
*   **Prediction Error (Innovation):** $\varepsilon(t|t-1) = y(t) - z^{T}(t)\hat{\theta}(t|t-1)$
*   **Filtering Error:** $\varepsilon(t|t) = y(t) - z^{T}(t)\hat{\theta}(t|t)$

![](_page_84_Picture_8.jpeg)
![](_page_84_Picture_9.jpeg)

---

### Problems with Parameter Tracking

While exponential forgetting allows the model to adapt to changes, it introduces specific numerical and structural risks:

#### 1. Poor System Excitation
If the input signal does not sufficiently "excite" the system (e.g., in closed-loop control where the input is linearly dependent on the output), the regressor $z(t)$ may lack information in certain directions.
*   **Covariance Wind-up:** Information subject to forgetting is not replaced by new data. This leads to the unlimited growth of eigenvalues in the covariance matrix $P$ in "unexcited" directions, making the estimator extremely sensitive to noise.

#### 2. Possible Solutions
*   **Optimal Experiment Design:** Using external excitation signals to ensure the regressor spans the parameter space.
*   **Varying Forgetting Factor:** Adjusting $\varphi$ dynamically. For example, Fortesque (1981) proposed keeping the "information content" constant:
    $$\varphi(t) = 1 - \alpha \frac{\varepsilon^2(t|t-1)}{1 + \zeta(t|t-1)}$$
*   **Restricted Forgetting:** A concept introduced by Kulhavý (1987) where forgetting is applied only to the directions in the parameter space where new information is actually being received.

---

## Restricted Forgetting

Restricted forgetting aims to prevent covariance wind-up by only increasing uncertainty in directions where the data update has recently reduced it.

#### **Data Update Analysis**
To understand restricted forgetting, we analyze how the covariance matrix $P$ changes during a standard update:
1.  **Parameter Uncertainty:** Defined as $\tilde{\theta}(t|t-1) = \theta(t) - \hat{\theta}(t|t-1)$.
2.  **Directional Uncertainty:** The uncertainty of a scalar product $x^T\theta$ is given by $x^T P x$.
3.  **Covariance Update:** 
    $$P(t|t) = P(t|t-1) - \frac{P(t|t-1)z(t)z^{T}(t)P(t|t-1)}{1 + \zeta(t|t-1)}$$

*   **In the direction of the regressor $z(t)$:** The uncertainty is reduced by the factor $1/(1 + \zeta(t|t-1))$.
*   **In orthogonal directions $x(t) \perp_P z(t)$:** Where $x^T(t)P(t|t-1)z(t) = 0$, the uncertainty remains unchanged: $x^T(t)P(t|t)x(t) = x^T(t)P(t|t-1)x(t)$.

![](_page_86_Picture_14.jpeg)
![](_page_86_Picture_15.jpeg)

---

### Restricted Forgetting (2): Time Update

In the time update step, we apply a selective uncertainty increase. We only allow the parameters to "drift" in the direction of the current regressor $z(t)$.

**1. Direction of Regressor $z(t)$:**
We follow a drift model where the variance increases by $\zeta_{\nu}(t)$:
$$z^{T}(t)P(t+1|t)z(t) = \zeta(t|t) + \zeta_{\nu}(t)$$
where $\zeta_{\nu}(t) = z^{T}(t)V(t)z(t)$.

**2. Orthogonal Directions:**
We ensure no uncertainty increase: $x^{T}(t)P(t+1|t)x(t) = x^{T}(t)P(t|t)x(t)$.

**3. Restricted Drift Covariance Matrix:**
This selective increase is achieved by constructing the drift covariance matrix $V(t|t)$ as:
$$V(t|t) = \frac{\zeta_{\nu}(t)}{\zeta^{2}(t|t)} P(t|t) z(t) z^{T}(t) P(t|t)$$

**Validation:**
*   Multiplying by $z^T$ and $z$ yields exactly $\zeta_{\nu}(t)$.
*   Multiplying by an orthogonal vector $x^T$ (where $x^T P z = 0$) yields $0$, confirming that uncertainty is preserved in all other directions.

![](_page_87_Picture_14.jpeg)
![](_page_87_Picture_15.jpeg)