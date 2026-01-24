# HMM probability evaluation (5)

In the context of Hidden Markov Models (HMM) with multiple potential system modes, we must account for how mode trajectories evolve over time and how we can detect the currently active mode using a window of "future" data to improve decision reliability.

### **Time-Update Step**

The time-update step involves propagating the probability of a specific mode trajectory $\mathcal{M}^{k}(t)$ forward in time. By applying the **Markov property**, we assume that the probability of the next mode $m(t+k+1)$ depends only on the current mode $m(t+k)$ and is independent of the past trajectory or historical data $\mathcal{D}^{t+k}$ once the current mode is known.

The joint probability of the extended trajectory $\mathcal{M}^{k+1}(t)$ is calculated as:

$$P\left(\mathcal{M}^{k+1}(t)\middle|\mathcal{D}^{t+k}\right) = P\left(m(t+k+1)\middle|m(t+k)\right)P\left(\mathcal{M}^{k}(t)\middle|\mathcal{D}^{t+k}\right)$$

This recursive structure allows us to build a tree of possible mode sequences, where each transition is weighted by the known mode transition probabilities.

#### **Active Mode Detection**
To determine which mode was active at time $t$ given a look-ahead window of depth $d$, we calculate the **posterior marginal probability**. This is achieved by summing (marginalizing) the probabilities of all possible branches in the trajectory tree that stem from the root mode $m(t)$:

$$P\left(m(t)|\mathcal{D}^{t+d}\right) = \sum_{m(t+1),\dots,m(t+d)} P\left(\mathcal{M}^d(t)|\mathcal{D}^{t+d}\right)$$

#### **Properties and Challenges**
*   **Consistency:** This approach requires a consistent state representation across all modes to allow for meaningful comparisons.
*   **Complexity:** The primary drawback is the **exponential growth** of the trajectory tree ($M^d$ branches). To maintain real-time performance, pruning techniques (discarding low-probability branches) are often required.
*   **Prior Information:** Complexity can be mitigated by incorporating constraints, such as distinguishing between reversible and irreversible mode changes.
*   **Decision Latency:** There is an inherent trade-off between the tree depth $d$ (accuracy) and the delay in decision-making.

![](_page_154_Picture_12.jpeg)

---

### Interacting Multiple Models (IMM)

The Interacting Multiple Models (IMM) algorithm provides a computationally efficient alternative to the growing tree approach by mixing the estimates of parallel filters at each time step.

#### **Data Update Step**
For each mode $i$, we update the mode probability and the state estimate using the current observation $y(t)$:

1.  **Mode Probability Update:**
    $$P(m(t)=i | \mathcal{D}^{t}) \propto p(y(t) | \mathcal{D}^{t-1}, u(t), m(t)=i) P(m(t)=i | \mathcal{D}^{t-1})$$
2.  **State Estimate Update:**
    The posterior state density for each mode is approximated as a Gaussian distribution:
    $$p_{i}(x(t) | \mathcal{D}^{t}) \approx \mathcal{N}(\hat{x}_{i}(t|t); P_{i}(t|t))$$

### **Model Mixing**
The core innovation of IMM is the mixing step, which occurs before the next prediction cycle. This allows the filters to "exchange" information based on the likelihood of transitioning between modes.

*   **Transition Probabilities:** We define $\pi_{i|j} = P\{m(t) = i|m(t-1) = j\}$ as the probability of switching from mode $j$ to mode $i$.
*   **Mixed Mode Probability:** The predicted probability for mode $i$ considering all possible previous modes $j$:
    $$\bar{P}\left(m(t)=i\,\Big|\,\mathcal{D}^{t}\right)=\sum_{j=1}^{M}\pi_{i\,|j}\,P\left(m(t)=j\,\Big|\,\mathcal{D}^{t}\right)$$
*   **Mixed State Estimate:** We compute a conditional mixing probability $\rho_{i|j}(t)$, which represents the probability that the system was in mode $j$ at $t-1$ given it is in mode $i$ at $t$:
    $$\rho_{i|j}(t) = \frac{\pi_{i|j} P(m(t-1)=j|\mathcal{D}^{t-1})}{\sum_k \pi_{i|k} P(m(t-1)=k|\mathcal{D}^{t-1})}$$
    The mixed initial condition for the filter of mode $i$ is then:
    $$\bar{p}_i(x(t)|\mathcal{D}^t) = \sum_{j=1}^M \rho_{i|j}(t) p_j(x(t)|\mathcal{D}^t)$$

![](_page_155_Picture_11.jpeg)

![](_page_155_Picture_12.jpeg)