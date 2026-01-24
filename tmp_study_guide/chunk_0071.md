# Kalman smoother (Rauch-Tung-Striebel)

The Kalman filter is inherently a recursive algorithm that provides the best estimate of the current state based on past and present measurements (filtering). However, in many applications—such as post-processing experimental data or trajectory reconstruction—we have access to the entire dataset $\mathcal{D}^{T_f}$ up to a final time $T_f$. The **Kalman Smoother**, specifically the Rauch-Tung-Striebel (RTS) form, allows us to improve the estimates of past states by incorporating "future" information through a backward pass.

### **Transform functional recursion to parametric recursion**

To implement the smoother, we first perform a standard forward pass using the Kalman filter to generate and store the necessary statistics.

#### **Statistics from the forward run of the Kalman filter**
During the forward pass, for each time step $t$, we compute and store:
*   **Data update step (Filtering):** The conditional probability density function (c.p.d.f.) of the state given all data up to time $t$.
    $$p(x(t)|\mathcal{D}^t) = \mathcal{N}(\hat{x}(t|t), P(t|t))$$
*   **Time-update step (Prediction):** The predictive c.p.d.f. for the next state given data up to time $t$.
    $$p(x(t+1)|\mathcal{D}^t) = \mathcal{N}(\hat{x}(t+1|t), P(t+1|t))$$

#### **Backward (smoothing) run of the Kalman filter**
Once the forward pass reaches the final time $T_f$, we begin the backward recursion. We initialize the smoother with the final filtered state: $\hat{x}(T_f|T_f)$ and $P(T_f|T_f)$.

*   **Smoothing step:** We seek the c.p.d.f. of the state at time $t$ given the full dataset $\mathcal{D}^{T_f}$.
    $$p(x(t)|\mathcal{D}^{T_f}) = \mathcal{N}(\hat{x}(t|T_f), P(t|T_f))$$

*   **Kalman gain (Smoothing Gain):**
    The smoothing gain $F(t)$ determines how much the "future" residual (the difference between the smoothed future state and the predicted future state) should correct the current filtered estimate.
    $$F(t) = P(t|t)A^{T}P^{-1}(t+1|t)$$

*   **State update:**
    The smoothed state estimate is calculated by adjusting the filtered estimate $\hat{x}(t|t)$ using the smoothing gain and the information from the next smoothed time step.
    $$\hat{x}(t|T_f) = \hat{x}(t|t) + F(t)(\hat{x}(t+1|T_f) - \hat{x}(t+1|t))$$

*   **Covariance update:**
    The uncertainty is similarly reduced by incorporating the future information.
    $$P(t|T_f) = P(t|t) - F(t) \Big( P(t+1|t) - P(t+1|T_f) \Big) F^{T}(t)$$

**Key Insight:** The backward run does not require the raw measurement data $y(t)$ again. It relies entirely on the statistics (means and covariances) saved during the forward Kalman filter pass!

![](_page_123_Picture_17.jpeg)

![](_page_123_Picture_18.jpeg)