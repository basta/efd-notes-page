# Adaptation vs. change detection methods

In the context of system monitoring and control, we distinguish between two primary ways a system's behavior can evolve over time. The choice of monitoring method depends heavily on the expected velocity of the change:

*   **Slow parameter drift:** When system characteristics change gradually (e.g., due to mechanical wear or environmental shifts), we typically use **parameter estimation** with **forgetting factors**. This allows the model to "adapt" continuously to the new dynamics.
*   **Abrupt changes:** When a change occurs suddenly (e.g., a sensor failure or a structural break), adaptation is often too slow. In these cases, we employ **change detection and isolation** methods to identify the exact moment and nature of the jump.

### **On-line change detection**

On-line detection is performed in real-time as data arrives. We observe a sequence of data items:
$$y(t) \sim p_{\theta}(y(t)|y(t-1),\ldots,y(1))$$

The fundamental challenge is that the **time of change ($t_0$)** is unknown. The system is characterized by:
*   For $t \leq t_0$: The parameter is $\theta = \theta^0$ (the nominal state).
*   For $t > t_0$: The parameter shifts to $\theta = \theta^1$ (the changed state).

The objective is an optimization problem: we aim to **minimize the "delay"** in detection for a given, acceptable **false alarm rate**.

### **Off-line change detection**

In off-line detection, we analyze a fixed, finite sample of data $\{y(1), \dots, y(N)\}$. We test two competing hypotheses:

*   **$H_0$ (Null Hypothesis):** No change occurred. The distribution remains constant for the entire sample:
    $$p_{\theta}(y(t)|y(t-1),\ldots,y(1)) = p_{\theta_0}(y(t)|y(t-1),\ldots,y(1)) \quad \text{for } t=1,\ldots,N$$

*   **$H_1$ (Alternative Hypothesis):** A change occurred at some time $t_0$ (where $1 \leq t_0 \leq N-1$):
    $$\begin{array}{lcl} \rho_{\theta}(y(t)|y(t-1),\ldots,y(1)) & = & \rho_{\theta_0}(y(t)|y(t-1),\ldots,y(1)) & \text{for } t=1,\ldots,t_0 \\ \rho_{\theta}(y(t)|y(t-1),\ldots,y(1)) & = & \rho_{\theta_1}(y(t)|y(t-1),\ldots,y(1)) & \text{for } t=t_0+1,\ldots,N \end{array}$$

![](_page_133_Picture_18.jpeg)

![](_page_133_Picture_19.jpeg)

### Statistical hypothesis testing

A statistical hypothesis is an assumption regarding the probability distribution of observed data. These are categorized as:

1.  **Non-parametric:** Assumptions about the *type* of distribution (e.g., testing if data is Gaussian vs. Cauchy).
2.  **Parametric:** Assumptions about the *value* of a parameter (e.g., $\mu, \sigma^2$) for a known distribution.
    *   **Simple hypothesis:** The parameter is completely specified (e.g., $\mu = 0$).
    *   **Composite hypothesis:** The parameter lies within a range or set (e.g., $\mu > 0$).

### Statistical test - decision function

A statistical test is a decision rule that maps an observed sample $\mathcal{Y}^N = \{y(1), \ldots, y(N)\}$ to one of the hypotheses.

*   **$H_0$ (Null hypothesis):** Usually represents the "status quo" or "no change."
*   **$H_1$ (Alternative hypothesis):** Represents the "change occurred" state.

The goal is to use a **test statistic** to determine if $H_0$ should be invalidated. We define a **critical function** $g: \Omega^N \to \{0,1\}$ that partitions the sample space $\Omega^N$ into two disjunctive regions:

$$\begin{array}{rcl} \Omega^N &=& \Omega_0^N \cup \Omega_1^N, \quad \text{where } \Omega_0^N \cap \Omega_1^N = \emptyset \\ \\ g(\mathcal{Y}^N) &=& 0 \quad \text{for } \mathcal{Y}^N \in \Omega_0^N \text{ (Accept } H_0) \\ \\ g(\mathcal{Y}^N) &=& 1 \quad \text{for } \mathcal{Y}^N \in \Omega_1^N \text{ (Reject } H_0 \text{ in favor of } H_1) \end{array}$$

The region $\Omega_1^N$ is known as the **critical region** of the test.

![](_page_134_Picture_13.jpeg)