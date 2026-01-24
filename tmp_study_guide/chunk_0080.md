# Detection algorithms (2)

### **CUSUM algorithm** (Cumulative Sum)

The Cumulative Sum (CUSUM) algorithm is a powerful technique for detecting changes in the parameters of a stochastic process. It is particularly effective at identifying a shift from a known baseline state ($\theta_0$) to an alternative state ($\theta_1$).

Recall the fundamental properties of the log-likelihood ratio statistic $s_k$:
$$\mathcal{E}\left\{s_k|\theta=\theta_0\right\}<0,\qquad \mathcal{E}\left\{s_k|\theta=\theta_1\right\}>0$$

Under the null hypothesis ($H_0$), the cumulative statistic $S_k = \sum_{i=1}^k s_i$ exhibits a negative drift, meaning it decreases over time. When a change occurs ($H_1$), the drift becomes positive, and the statistic begins to increase.

#### **The Decision Logic**
To detect the change, we focus on the growth of the statistic relative to its historical minimum. We define the running minimum as:
$$m_k = \min_{i=0,\ldots,k} S_i$$

The detection is based on the difference between the current cumulative sum and this minimum. The critical function is defined as:
- $g_k = 1$ (Change detected) if $S_k - m_k \ge \lambda$
- $g_k = 0$ (No change) if $S_k - m_k < \lambda$

This approach uses an **adaptive thresholding** mechanism. By measuring the "rise from the bottom," the algorithm ensures that the detection delay remains relatively independent of how long the process has been running in the $H_0$ state.

#### **CUSUM interpreted as a repeated SLR test**
The CUSUM method can be viewed as a sequence of Sequential Likelihood Ratio (SLR) tests. If the statistic $S_k$ drops too low (e.g., $S_k < -\epsilon$), it indicates that the evidence for $H_1$ is non-existent, and we restart the cycle.

In the limit where the lower boundary $\epsilon \to 0$, the statistics update can be simplified. We prevent the cumulative sum from becoming negative, effectively "resetting" the search for a change whenever the evidence points strongly toward $H_0$:
- $S_k = S_{k-1} + s_k$ if $S_{k-1} + s_k > 0$
- $S_k = 0$ if $S_{k-1} + s_k \le 0$

This is expressed in the following **compact notation**:
$$S_k = \left(S_{k-1} + s_k\right)^+$$
where $(x)^+ = \max(0, x)$.

![](_page_145_Picture_16.jpeg)

![](_page_145_Picture_17.jpeg)

*The figures above illustrate the behavior of the CUSUM statistic. The first plot shows the raw log-likelihood ratio with negative drift, while the second plot demonstrates the rectified CUSUM statistic $S_k$ rising toward the threshold $\lambda$ once a change in the mean occurs.*