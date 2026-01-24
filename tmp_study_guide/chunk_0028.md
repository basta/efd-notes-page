# Model of a Dynamic System for Control (2)

In the context of Bayesian system identification and adaptive control, we define the interaction between the controller and the plant using two fundamental sets of conditional probability density functions (c.p.d.f.).

1.  **Controlled System Model**: This is defined as the set of c.p.d.f. $p\left(y(t) \mid u(t), \mathcal{D}^{t-1}\right)$. It describes the probability of observing output $y(t)$ given the current input $u(t)$ and the historical data $\mathcal{D}^{t-1}$.
2.  **Control Law**: This is defined as the set of c.p.d.f. $p\left(u(t) \mid \mathcal{D}^{t-1}\right)$. It represents the strategy used by the controller to select the input $u(t)$ based solely on the available history.

### **Sampling Scheme and Causality**

The timing of information exchange is critical for maintaining causality in a closed-loop system. The information available at time $t$ determines the action taken, but there is an inherent information delay.

![](_page_49_Figure_8.jpeg)

![](_page_49_Figure_9.jpeg)

As illustrated in the diagrams above, the **system model acts as a predictor**. It attempts to forecast the system's future output by synthesizing the accumulated history of the process with the most recent control command.

---

### Model Structure and Parameters

When defining the predictor $p\left(y(t) \mid u(t), \mathcal{D}^{t-1}\right)$, we generally choose between two modeling philosophies:

*   **Non-parametric Models**: These are frequently used in Machine Learning (ML) and Artificial Intelligence (AI). They do not rely on a fixed set of parameters but rather on the data points themselves to define the mapping.
*   **Parametric Models**: These are preferred in classical system identification. By introducing a parameter vector $\theta$, we can compress the information from the data history into a finite set of values. This is computationally efficient and often aligns better with physical laws.

In the parametric framework, the predictor is calculated by marginalizing over the unknown parameters $\theta$:

$$p\left(y(t) \mid u(t), \mathcal{D}^{t-1}\right) = \int p\left(y(t) \mid u(t), \mathcal{D}^{t-1}, \theta\right) p\left(\theta \mid u(t), \mathcal{D}^{t-1}\right) d\theta$$

This integral highlights two distinct components of our knowledge:

1.  **Model Structure**: $p\left(y(t) \mid u(t), \mathcal{D}^{t-1}, \theta\right)$ defines how the output is generated if the parameters were known perfectly.
2.  **Knowledge of Parameters**: $p\left(\theta \mid u(t), \mathcal{D}^{t-1}\right)$ represents our current uncertainty regarding the true values of $\theta$, conditioned on the observed data and the current input.