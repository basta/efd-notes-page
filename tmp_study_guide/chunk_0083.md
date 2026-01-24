# HMM probability evaluation

In the context of Hidden Markov Models (HMM) for change detection, we often utilize a **bank of filters** to evaluate the likelihood of different system modes. This section focuses on the evaluation of probabilities when multiple models are running in parallel.

#### **Parallel Models**

When we assume the system operates in one of $M$ possible modes and does not switch between them during the observation period (or we are testing which model best fits the data), we use parallel filtering.

1.  **Initialization**:
    We begin by assigning prior probabilities to each model in the set. If no prior information is available, we typically assume a uniform distribution:
    $$P_{m_i}(0) \approx 1/M, \qquad i=1,\ldots,M$$

2.  **Data Update Step**:
    As new data $\mathcal{D}^t = \{y(t), u(t), \mathcal{D}^{t-1}\}$ arrives, we update the posterior probability of each mode $m(t)$ using Bayes' rule. The posterior is proportional to the product of the predictive likelihood of the current observation and the previous belief:
    $$P(m(t)|\mathcal{D}^t) \propto p(y(t)|\mathcal{D}^{t-1}, u(t), m(t)) P(m(t)|\mathcal{D}^{t-1})$$

3.  **Predictive Likelihood of Output**:
    The term $p(y(t)|\mathcal{D}^{t-1}, u(t), m(t))$ represents how well the $i$-th model predicts the current measurement $y(t)$. This is calculated by marginalizing over the hidden state $x(t)$:
    $$p(y(t)|\mathcal{D}^{t-1}, u(t), m(t)) = \int p(y(t)|x(t), u(t), m(t)) \ p(x(t)|\mathcal{D}^{t-1}, m(t)) \ dx$$

#### **Implementation via Kalman Filtering**

In a linear Gaussian framework, each mode $i$ is represented by a specific state-space realization $(A_i, B_i, C_i, D_i)$ and noise covariances $(Q_i, R_i)$. The components of the integral above are defined as follows:

*   **Measurement Model**: The likelihood of the observation given the state for mode $i$:
    $$p(y(t)|x(t),u(t),m(t)=i) = p_i(y(t)|x(t),u(t)) = \mathcal{N}(C_i\hat{x}_i(t|t-1) + D_iu(t), C_iP_i(t|t-1)C_i^T + R_i)$$
    This corresponds to the innovation covariance in a Kalman Filter.

*   **State Estimate**: The predicted state distribution based on previous data for mode $i$:
    $$p(x(t)|\mathcal{D}^{t-1}, m(t)=i) = p_i(x(t)|\mathcal{D}^{t-1}) = \mathcal{N}(\hat{x}_i(t|t-1), P_i(t|t-1))$$

By monitoring the residuals (innovations) of each Kalman filter in the bank, we can dynamically update the probability that a specific model $m_i$ is the "active" mode. A model that consistently produces small residuals relative to its predicted covariance will see its posterior probability $P(m(t)|\mathcal{D}^t)$ increase.

![](_page_150_Picture_12.jpeg)