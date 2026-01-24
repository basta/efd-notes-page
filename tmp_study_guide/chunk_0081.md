# Detection algorithms (3)

### **Example: CUSUM $S_k$ statistics for change of mean value**

The Cumulative Sum (CUSUM) algorithm is particularly effective at detecting small, persistent shifts in the mean of a process. Unlike simple thresholding, it integrates information over time, making it sensitive to sustained changes while remaining robust against transient noise.

▶ **Signal/noise ratio analysis**
The following figures illustrate the performance of the CUSUM statistic under varying signal-to-noise conditions. As the ratio $\frac{\Delta \mu}{\sigma}$ increases, the drift in the cumulative sum becomes more pronounced, allowing for faster detection with a lower probability of false alarms.

![](_page_146_Figure_3.jpeg)

![](_page_146_Figure_4.jpeg)

---

### Change detection in state-space model

In many engineering applications, the system dynamics are not constant but switch between different regimes (e.g., normal operation vs. failure mode). To detect these changes, we utilize a framework that combines continuous state estimation with discrete mode detection.

#### Hidden Markov model (HMM)

A Hidden Markov Model in this context represents a system where the underlying "state" consists of both a continuous vector $x(t)$ and a discrete operating mode $m(t)$.

*   **Continuous State Dynamics**: The system follows a Markov process where the future state depends only on the current state.
    $$p(x(t+1)|x(t),x(t-1),...,x(1)) = p(x(t+1)|x(t))$$

*   **Multiple Operating Modes**: The system can operate in one of $M$ possible modes, denoted as $m(t) \in \{1, \dots, M\}$. Each mode $i$ defines a specific set of transition and observation probabilities:
    $$p_i(x(t+1), y(t)|x(t), u(t)) = p(x(t+1), y(t)|x(t), u(t), m(t) = i)$$

*   **The "Hidden" Nature**: In an HMM, the sequence of observations $\{y(1), y(2), \dots, y(t)\}$ is available, but the actual state $x(t)$ and the active mode $m(t)$ are hidden. We must infer them based on the data.
    *   The observations $y(t)$ are conditionally dependent on the associated Markov chains of both the continuous state $\{x(t)\}$ and the discrete mode $\{m(t)\}$.

The following diagrams visualize the dependency structure and the probabilistic flow within a switching state-space system:

![](_page_147_Figure_11.jpeg)

![](_page_147_Picture_12.jpeg)

![](_page_147_Picture_13.jpeg)