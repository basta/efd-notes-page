# HMM probability evaluation (3)

#### Alternative Models and Decision Latency

In many practical change detection scenarios, a change in the system's internal dynamics—such as a component failure or a shift in operating mode—may not be immediately apparent in the current output measurement $y(t)$. To improve the reliability of the detection, we often employ **Alternative Models** that utilize a Bayesian approach to update the mode probability based on a window of "future" data.

Specifically, we aim to update the probability:
$$P\left(m(t) \mid \mathcal{D}^t\right)$$
by incorporating a subsequent data set (relative to the decision time $t$) defined as:
$$\mathcal{D}_{t+1}^{t+d} = \{u(t+1), y(t+1), \dots, u(t+d), y(t+d)\}$$
where $d$ represents the decision delay or look-ahead horizon.

The final decision regarding the system state at time $t$ is then based on the **posterior probability**:
$$P\left(m(t) \mid \mathcal{D}^{t+d}\right)$$
This approach allows the estimator to "wait and see" how the system evolves, as the evidence of a mode transition often accumulates in the residuals of the Kalman filters over several time steps.

#### Key Characteristics of Alternative Models

1.  **Bayesian Update**: We treat the mode $m(t)$ as a random variable and use Bayes' rule to refine its distribution as more evidence (measurements) becomes available.
2.  **Decision Delay**: By introducing a delay $d$, we trade off real-time responsiveness for increased detection accuracy. This is particularly useful when different modes have similar output signatures in the short term but diverge over time.
3.  **Observability of Changes**: This formulation acknowledges that changes in system dynamics are often latent and may only become "visible" in the output $y$ after the system's state $x$ has been driven by the new dynamics for several samples.

<span style="display:block; height: 2em;"></span>

$$\begin{array}{cccccccccccccccccccccccccccccccccccc}$$