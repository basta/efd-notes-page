# Change detection in state-space model (2)

In complex dynamical systems, the system behavior often shifts between different regimes or "modes." To model these transitions mathematically, we treat the active mode as a stochastic process.

#### Active mode dynamics

The active mode $m(t)$ is modeled as a Markov process with a discrete state space $m(t) \in \{1, \dots, M\}$. The evolution of these modes over time is governed by transition probabilities, which define the likelihood of moving from one mode to another.

The transition probability from mode $i$ at time $t$ to mode $j$ at time $t+1$ is defined as:
$$\pi_{i,j}(t) = P\left\{m(t+1)=j\mid m(t)=i\right\}$$

For a **stationary Markov process**, these probabilities remain constant over time, allowing us to represent the system using a constant transition matrix $\Pi$. The probability distribution across all possible modes at time $t$ is represented by the vector:
$$P_m(t) = (P\{m(t) = 1\}, \dots, P\{m(t) = N\})^T$$

The distribution evolves according to the following time update and reaches a stationary distribution proportional to the left eigenvector associated with the eigenvalue $\lambda_\Pi=1$:
$$P_m(t+1) = \Pi^T P_m(t), \qquad P_m^T(\infty) = P_m^T(\infty) \Pi$$

**Example: Transition Matrix and Weighted Graph Representation**
Consider a three-mode system with the transition matrix $\Pi$:
$$\Pi = \begin{pmatrix} 0.6 & 0.3 & 0.1 \\ 0.0 & 0.4 & 0.6 \\ 0.4 & 0.2 & 0.4 \end{pmatrix}$$
Starting from an initial state where the system is certainly in Mode 1 ($P_m(0) = [1, 0, 0]^T$), the distribution converges over time toward a steady-state equilibrium:
- $P_m(1) = (0.600, 0.300, 0.100)^T$
- $P_m(2) = (0.400, 0.320, 0.270)^T$
- $P_m(\infty) = (0.353, 0.294, 0.353)^T$

![](_page_148_Picture_12.jpeg)
![](_page_148_Picture_13.jpeg)
![](_page_148_Picture_14.jpeg)

---

### Use of bank of models

When the system mode is hidden, we employ a "bank" of filters or models running in parallel, each corresponding to a specific hypothesis about the current mode $m(t)$.

#### Multiple models of state-transition
These models account for changes in the internal dynamics of the system or changes in external disturbances (often used in unknown input observers):
$$p_i(x(t+1)|x(t), u(t), y(t)) = p(x(t+1)|x(t), u(t), y(t), m(t) = i)$$

#### Multiple models of output measurement
These models are designed to detect issues related to the observation process, such as:
- **Sensor faults:** Increased noise levels or constant biases.
- **Communication loss:** "Frozen" sensors where the output remains static.
- **Range limitations:** Clipping or saturation of sensor data.

The measurement model for mode $i$ is expressed as:
$$p_i(y(t)|x(t), u(t)) = p(y(t)|x(t), u(t), m(t) = i)$$

#### Markov model of transitions (Problem Formulations)
Depending on how the transitions between models are handled, we categorize the detection problem into three main structures:

1.  **Parallel models:** Used for **structure selection**. Each model may have a completely different state representation or mathematical structure.
2.  **Alternative models:** Used for **change/fault detection**. These share a consistent structure and state representation. They can model reversible changes (switching back and forth) or irreversible changes (permanent faults).
3.  **Interacting models:** Used for **dimensionality reduction** in hybrid systems. These maintain a consistent structure but allow for complex interactions between modes while keeping computational complexity fixed.

![](_page_149_Picture_21.jpeg)
![](_page_149_Picture_22.jpeg)
![](_page_149_Picture_23.jpeg)
![](_page_149_Picture_24.jpeg)
![](_page_149_Picture_25.jpeg)
![](_page_149_Picture_26.jpeg)