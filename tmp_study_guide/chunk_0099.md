# Recursive Bayesian Update

### **Weighted Bootstrap Method**

The weighted bootstrap method is a resampling technique used to approximate a target distribution $f(x)$ when we only have access to samples from a proposal distribution $g(x)$. This is particularly useful in Bayesian estimation when the posterior distribution is difficult to sample from directly.

**Algorithm Steps:**
1.  **Initial Sampling:** Obtain a set of $N$ samples $x_i$ from the available proposal distribution $g(x)$, where $i = 1, \dots, N$.
2.  **Weight Calculation:** For each sample, calculate the importance weight $w_i = \frac{f(x_i)}{g(x_i)}$. This weight represents how well the sample from $g(x)$ represents the target distribution $f(x)$.
3.  **Normalization:** Normalize the weights so they sum to unity: $q_i = \frac{w_i}{\sum_{j=1}^N w_j}$.
4.  **Resampling:** Generate a new set of samples by drawing from the discrete distribution defined by the pairs $\{x_i, q_i\}$. The resulting empirical distribution is:
    $$\hat{r}_N(x) = \sum_{i=1}^N q_i \delta(x - x_i)$$

**Application to Bayesian Updates:**
In a Bayesian context, if we assume a uniform prior $p(x_i) = g(x_i) = 1/N$, and our target is the posterior, the likelihood $p(y|x_i)$ effectively becomes our target function $f(x_i)$. Sampling from the normalized likelihood (the importance function) allows us to update our belief about the state $x$ based on new data $y$.

![](_page_171_Figure_13.jpeg)
<span style="display:block; text-align:center;">*Visual representation of the resampling process.*</span>

![](_page_171_Picture_14.jpeg)
![](_page_171_Picture_15.jpeg)

---

### Recursive Bayesian Update (2)

#### Kalman Filter Implementation by Weighted Bootstrap (2-Step Algorithm)
For non-linear state-space models with arbitrary noise distributions, the Particle Filter (a Sequential Monte Carlo method) implements the Bayesian recursion using the weighted bootstrap.

**Model Definition:**
- **State Equation:** $x(k+1) = f(x(k), u(k), v(k))$, where $v(k) \sim p_v(\cdot)$
- **Measurement Equation:** $y(k) = g(x(k), u(k), e(k))$, where $e(k) \sim p_e(\cdot)$

**1. Initialization:**
Set $k = 0$ and draw $N$ initial samples (particles) from the initial state distribution: $x_i \sim p(x(0)|\mathcal{D}^0)$.

**2. Time-Update Step (Prediction):**
- Sample process noise: $v_i(k) \sim p_v(v(k))$ for $i = 1, \dots, N$.
- Propagate each particle through the system dynamics:
  $$x_i(k+1|k) = f(x_i(k|k), u(k), v_i(k))$$
  This represents the predicted distribution $p(x(k+1)|\mathcal{D}^k)$.

**3. Data-Update Step (Correction):**
- Increment time $k = k + 1$ and receive the new measurement $y(k)$.
- Evaluate the likelihood $w_i = p(y(k)|x_i(k|k-1), u(k))$ for every particle.
- Normalize the weights: $q_i = \frac{w_i}{\sum_{j=1}^N w_j}$.
- **Resample:** Draw $N$ new samples from the set $\{x_i(k|k-1)\}$ with probabilities $q_i$ to obtain the filtered particles $x_i(k|k)$.

![](_page_172_Picture_17.jpeg)
![](_page_172_Picture_18.jpeg)

---

### Recursive Bayesian Update (3)

#### Kalman Filter Implementation by Weighted Bootstrap (1-Step Algorithm)
The time and data updates can be combined into a single recursive loop to improve computational efficiency.

**Combined Algorithm:**
1.  **Observe:** Get the current measurement $y(k)$.
2.  **Weight:** Evaluate and normalize the likelihoods of the existing particles:
    $$q_i = \frac{p(y(k)|x_i(k|k-1), u(k))}{\sum_{j=1}^{N} p(y(k)|x_j(k|k-1), u(k))}$$
3.  **Resample & Propagate:** 
    - Select a particle $x_j$ from the discrete distribution defined by weights $q$.
    - Draw a noise sample $v_i \sim p_v(v(k))$.
    - Generate the next state particle: $x_j(k+1|k) = f(x_j, u(k), v_j)$.

---

### Recursive Bayesian Update (4)

#### Likelihood Evaluation and State Estimation
To perform the update, we must evaluate the likelihood $p(y(k)|x_i(k|k-1), u(k))$. If the measurement noise is non-additive, we use the transformation of variables:
$$p(y(k)|x_i, u(k)) = p_e\left(g^{-1}(x_i, u(k), y(k))\right) \left| \frac{dg^{-1}(\dots)}{dy(k)} \right|$$

For the common case of **additive measurement noise** ($y(k) = g'(x(k), u(k)) + e(k)$), this simplifies to:
$$p(y(k)|x_i, u(k)) = p_e\left(y(k) - g'(x_i, u(k))\right)$$

**Resulting Estimates:**
Once the particles are updated, the state and its uncertainty can be approximated:
- **Mean (Point Estimate):** $\hat{x}(k|k-1) \approx \frac{1}{N} \sum_{i=1}^{N} x_i(k|k-1)$
- **Covariance (Uncertainty):** $P(k|k-1) \approx \frac{1}{N-1} \sum_{i=1}^{N} (x_i - \hat{x})(x_i - \hat{x})^T$

![](_page_174_Picture_10.jpeg)
![](_page_174_Picture_11.jpeg)

---

### Kalman Filter Implementation Summary

#### Bayesian Description - Functional Recursion
The particle filter is a discrete approximation of the following continuous functional recursions:

1.  **Data-Update Step:**
    $$p(x(t)|\mathcal{D}^{t}) = \frac{p(y(t)|x(t), u(t))}{p(y(t)|\mathcal{D}^{t-1}, u(t))} \times p(x(t)|\mathcal{D}^{t-1})$$
2.  **Time-Update Step:**
    $$p(x(t+1)|\mathcal{D}^t) = \int p(x(t+1)|x(t), u(t)) p(x(t)|\mathcal{D}^t) dx(t)$$
3.  **Smoothing Step (Backward Run):**
    $$\rho(x(t)|\mathcal{D}^{t_f}) = \rho(x(t)|\mathcal{D}^t) \times \int \rho(x(t+1)|x(t), u(t)) \frac{\rho(x(t+1)|\mathcal{D}^{t_f})}{\rho(x(t+1)|\mathcal{D}^t)} dx(t+1)$$
    The smoothing step allows for better estimation of past states using all data up to the final time $t_f$.

![](_page_175_Figure_11.jpeg)
![](_page_175_Picture_12.jpeg)
![](_page_175_Picture_13.jpeg)