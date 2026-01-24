# ARX model estimation - recursive algorithm convergence

In the study of system identification, it is crucial to understand how recursive algorithms behave as more data becomes available. The recursive ARX (Auto-Regressive with Exogenous terms) estimation is not merely a heuristic; it is a mathematically rigorous way to update our knowledge of the system parameters.

#### **Batch vs. Recursive Results**
One of the most important properties of the recursive least squares (RLS) and Bayesian recursive estimation is that the **terminal values** of the recursive processing are mathematically equivalent to the results obtained from **batch processing**. 

If you have a fixed dataset $\mathcal{D}^T = \{y(t), u(t)\}_{t=1}^T$, the point estimate $\hat{\theta}(T)$ and the covariance matrix $P(T)$ calculated step-by-step will be identical to the estimates calculated by processing all $T$ samples at once, provided the initial conditions are consistent. This equivalence ensures that we do not lose any statistical information by choosing the computationally efficient recursive approach over the memory-intensive batch approach.

#### **Impact of Excitation**
The convergence of the parameter estimates $\hat{\theta}(t)$ to their true values depends heavily on the "richness" of the input signal, known as **Persistence of Excitation**.
- If the input $u(t)$ is sufficiently exciting, the information matrix $P(t)^{-1}$ grows with time, causing the normalized covariance matrix $P(t)$ to shrink toward zero.
- As $P(t) \to 0$, the uncertainty in our estimates vanishes, and the parameters converge to the true system values.
- If the system is poorly excited (e.g., the input is constant or zero), certain directions in the parameter space will remain uncertain, and $P(t)$ will not decrease in those directions.

#### **Uncertainty of $a_i$ vs. $b_i$ Parameters**
In an ARX model, we estimate two sets of parameters:
1.  **$a_i$ parameters**: These relate to the auto-regressive part (past outputs $y(t-i)$).
2.  **$b_i$ parameters**: These relate to the exogenous part (past inputs $u(t-i)$).

The rate of convergence and the final uncertainty levels often differ between these two sets. The uncertainty of $b_i$ is directly controlled by the experimental design (the choice of input $u(t)$). In contrast, the uncertainty of $a_i$ depends on the closed-loop behavior and the noise characteristics, as $y(t)$ is a stochastic process driven by both the input and the noise $e(t)$.

![](_page_78_Figure_5.jpeg)

<span id="_page_78_Figure_5"></span>
*The figure above typically illustrates the convergence of parameter estimates over time. Notice how the estimates stabilize as the number of samples increases, and the confidence intervals (derived from $P(t)$) narrow, representing the reduction in parameter uncertainty.*