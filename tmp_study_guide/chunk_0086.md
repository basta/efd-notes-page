# HMM probability evaluation (4)

In complex Hidden Markov Models (HMM), a single measurement at time $t$ may not provide sufficient information to distinguish between different system modes. To improve detection accuracy, we can utilize a "look-ahead" strategy that incorporates future data before making a definitive decision about the system state at time $t$.

### **Accumulation of information from "future" data**

To handle uncertainty in mode transitions, we construct a **trajectory tree** of alternative mode sequences. Instead of evaluating a single mode $m(t)$, we consider a sequence of modes over a window of length $k$:

$$\mathcal{M}^{k}(t) = \{m(t), m(t+1), \ldots, m(t+k)\}$$

In this framework, $k$ represents the **decision delay** or the depth of the tree. By waiting for $k$ additional observations, we can more reliably identify which trajectory the system is following. We evaluate the posterior probabilities $P(\mathcal{M}^{k}(t) | \mathcal{D}^{t+k})$ for all possible mode trajectories within the tree.

#### **Data-update step**

The update process follows Bayes' rule to incorporate the latest measurement $y(t+k)$ into the trajectory probability. The posterior probability is proportional to the likelihood of the new observation given the trajectory, multiplied by our prior belief:

$$P\left(\mathcal{M}^{k}(t) \middle| \mathcal{D}^{t+k}\right) \propto p\left(y(t+k) \middle| \mathcal{D}^{t+k-1}, u(t+k), \mathcal{M}^{k}(t)\right) \times P\left(\mathcal{M}^{k}(t) \middle| \mathcal{D}^{t+k-1}\right)$$

#### **Predictive c.p.d.f. of output**

The likelihood term, or the predictive conditional probability density function (c.p.d.f.) of the output, is calculated by marginalizing over the state $x(t+k)$:

$$p\left(y(t+k)\middle|\mathcal{D}^{t+k-1},u(t+k),\mathcal{M}^{k}(t)\right) = \int p\left(y(t+k)|x(t+k),u(t+k),m(t+k)\right) \times p\left(x(t+k)\middle|\mathcal{D}^{t+k-1},\mathcal{M}^{k-1}(t)\right) dx(t+k)$$

This calculation relies on a **bank of Kalman filters** running in parallel, where each filter corresponds to a specific path (mode trajectory) in the tree. Each filter provides a state estimate and covariance:

$$p\left(x(t+k)\left|\mathcal{D}^{t+k-1},\mathcal{M}^{k-1}(t)\right.\right)=\mathcal{N}\left(\hat{x}\left(t+k|t+k-1,\mathcal{M}^{k-1}(t)\right); P\left(t+k|t+k-1,\mathcal{M}^{k-1}(t)\right)\right)$$

As the tree grows, each branch represents a unique hypothesis of how the system dynamics have evolved, allowing for a robust, albeit computationally intensive, evaluation of the most likely system mode.

![](_page_153_Picture_13.jpeg)

![](_page_153_Picture_14.jpeg)