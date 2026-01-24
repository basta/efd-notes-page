# HMM probability evaluation (2)

In the context of Hidden Markov Models (HMM) for state-space systems, we often encounter scenarios where we must evaluate the likelihood of different operating modes. This section focuses on the **Parallel Model** configuration, where we assume that once the system starts in a specific mode, it remains in that mode without switching.

### Time-Update Step for Parallel Models

The time-update step for the mode probability $P(m(t)|\mathcal{D}^{t-1})$ is simplified when we assume there is no switching or interaction between the models. In this case, the transition is deterministic with respect to the identity of the mode.

Mathematically, the transition probability is defined by the Kronecker delta function $\delta(i, j)$:

$$P\{m(t) = i \mid m(t-1) = j, \mathcal{D}^{t-1}\} = \delta(i, j), \quad i, j = 1, \dots, M$$

Where:
- $\delta(i, j) = 1$ if $i = j$
- $\delta(i, j) = 0$ if $i \neq j$

This implies that the probability of being in mode $i$ at time $t$ is purely dependent on the probability of having been in mode $i$ at the previous time step, effectively treating each model as an independent hypothesis about the system's behavior.

### Complexity and Implementation

The parallel model approach is characterized by several key architectural features:

*   **Bank of Kalman Filters:** The system runs $M$ Kalman filters simultaneously in parallel. Each filter is tuned to the dynamics and measurement characteristics of a specific mode $m_i$.
*   **No Information Exchange:** Because the modes are assumed to be independent (no switching), there is no "mixing" of state estimates or covariances between the filters. Each filter evolves based solely on its own model and the incoming data stream $\mathcal{D}^t$.
*   **Structural Flexibility:** One of the primary advantages of this approach is that the state vectors $x(t)$ and the model structures (e.g., the dimensionality of the state space or the definition of the physics) do not need to be consistent across different modes. For example, Mode 1 could be a first-order kinematic model, while Mode 2 could be a complex high-order dynamic model.

![](_page_151_Figure_7.jpeg)

The figure above illustrates the parallel architecture where the input $u(t)$ and output $y(t)$ are fed into multiple independent estimators, each producing its own residual and likelihood for mode evaluation.

#### Summary of the Parallel Architecture
In this framework, we are essentially performing **Model Selection**. We monitor the innovations (residuals) of each Kalman filter; the filter that produces the smallest, most white residuals will see its posterior mode probability $P(m(t)|\mathcal{D}^t)$ increase over time, while the probabilities for mismatched models will decay.

![](_page_151_Picture_9.jpeg)