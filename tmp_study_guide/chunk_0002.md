# EFD course approach

The core objective of the Estimation, Filtering, and Detection (EFD) course is the **extraction of information about "hidden" variables** within stochastic dynamic systems. In real-world engineering, we rarely have direct access to the internal variables or the exact parameters governing a system's behavior. Instead, we must infer these values from noisy measurements and incomplete data.

### **System Parameters**

When we focus on the underlying constants or slowly varying properties of a system, we are dealing with **System Identification**. This typically involves Input/Output (I/O) models such as ARX (Auto-Regressive with Exogenous variables) or ARMAX models.

![](_page_3_Picture_4.jpeg)

The process of identification is broken down into several critical steps:
*   **Structure Determination:** Selecting the mathematical form of the model (e.g., the order of the differential or difference equations).
*   **Parameter Estimation:** Calculating the numerical values of the coefficients within that structure.
*   **Algorithm Selection:** Choosing between **batch algorithms** (processing all data at once) or **recursive algorithms** (updating estimates as new data arrives in real-time).

### **System State**

While parameters define the "rules" of the system, the **System State** represents the internal variables that change over time (e.g., position, velocity, or temperature). These are modeled using **state-space representations**.

![](_page_3_Picture_11.jpeg)

State estimation is categorized based on the relationship between the time of the estimate and the time of the available measurements:
*   **Filtering:** Estimating the current state based on measurements up to the present time.
*   **Prediction:** Estimating a future state based on current and past data.
*   **Smoothing:** Estimating a past state using data collected after that point in time (non-real-time).

### **Unifying Framework: The Bayesian Approach**

This course utilizes the **Bayesian method** as a rigorous mathematical framework to unify parameter estimation, state estimation, and detection. The fundamental shift is moving from a likelihood—the probability of observing data given a parameter—to a posterior distribution—the probability of the parameter given the observed data.

The general transformation is expressed as:
$$p(y|\theta, \ldots) \Rightarrow p(\theta|y, \ldots)$$

This logic applies across all domains of the course:
*   **For Parameters ($\theta$):** $p(y|\theta,\ldots) \Rightarrow p(\theta|y,\ldots)$
*   **For States ($x$):** $p(y|x,\ldots) \Rightarrow p(x|y,\ldots)$
*   **For Models/Modes ($m$):** $p(y|m,\ldots) \Rightarrow p(m|y,\ldots)$

### **System Mode**

In many complex scenarios, a system may operate in different "modes" (e.g., a sensor failure, a change in flight regime, or a mechanical break). This is handled by a **bank of multiple models**, where each model represents a different operating condition.

![](_page_3_Picture_21.jpeg)

**Fault Detection and Isolation (FDI)** relies on:
*   **System Mode Probability:** Calculating which model currently best explains the observed data.
*   **Mode Switching:** Modeling the transitions between modes as a **Hidden Markov Process**.

The Bayesian inference for detection is represented as:
$$p(y|m, \ldots) \Rightarrow p(m|y, \ldots)$$

![](_page_3_Picture_26.jpeg)

![](_page_3_Picture_27.jpeg)