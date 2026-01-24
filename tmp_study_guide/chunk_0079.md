# Detection algorithms (1)

In practical control and monitoring systems, we often need to implement "on-line" recursive algorithms that can detect changes in real-time. While the standard Likelihood Ratio (LR) test provides a foundation, specific windowing or weighting techniques are used to balance detection speed against noise sensitivity.

### **GMA algorithm** (Geometric Moving Average)

The Geometric Moving Average (GMA) algorithm, also known as an Exponentially Weighted Moving Average (EWMA), is designed to give more importance to recent observations while gradually "forgetting" older data. This is particularly useful for detecting shifts in non-stationary environments.

*   **Exponentially weighted data**: The influence of a specific sample $s_{k-i}$ decays exponentially as time progresses, governed by the forgetting factor $\varphi \in [0, 1)$.
*   **Cumulative statistic**: The statistic $S_k$ is calculated as a weighted sum of all past log-likelihood ratios:
    $$S_k = (1 - \varphi) \sum_{i=0}^{\infty} \varphi^{i} s_{k-i}$$
    This can be efficiently implemented using a first-order recursive filter:
    $$S_k = \varphi S_{k-1} + (1 - \varphi) s_k$$
    where $s_k$ is the current log-likelihood ratio $\ln \frac{p(y_k|\theta_1)}{p(y_k|\theta_0)}$.

*   **Critical function**: The decision rule is based on comparing the smoothed statistic against a threshold $\lambda$:
    $$g_k = 1 \text{ for } S_k \geq \lambda, \qquad g_k = 0 \text{ for } S_k < \lambda$$

### **FMA algorithm** (Finite Moving Average)

The Finite Moving Average (FMA) algorithm uses a "sliding window" approach. It considers only the most recent $N$ samples, completely discarding any information older than the window length.

*   **Finite window based data**: This method ensures that the statistic does not have "infinite memory," making it robust against very old outliers or biases.
*   **Cumulative statistics**: The statistic is the sum of the log-likelihood ratios within the window:
    $$S_k = \sum_{i=0}^{N-1} s_{k-i}$$
    To avoid re-summing the entire window at every step, it is updated recursively by adding the newest sample and subtracting the oldest:
    $$S_k = S_{k-1} + s_k - s_{k-N}$$

*   **Critical function**: Similar to the GMA, a detection is triggered when the sum exceeds the threshold:
    $$g_k = 1 \text{ for } S_k \geq \lambda, \qquad g_k = 0 \text{ for } S_k < \lambda$$

![](_page_144_Picture_13.jpeg)

![](_page_144_Picture_14.jpeg)

**Comparison Note**: While the FMA provides a sharp cutoff of old data, the GMA is often preferred in embedded systems due to its lower memory requirements (it only needs to store $S_{k-1}$, whereas FMA must store a buffer of $N$ previous samples).