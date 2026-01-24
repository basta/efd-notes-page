# <span id="page-47-0"></span>**4. Parameter estimation**

![](_page_47_Picture_1.jpeg)

# Model of a dynamic system for control

In the context of control theory, the primary objective of system identification is to build a mathematical representation of a system that enables optimal or adaptive control. This process relies on observing the relationship between the system's inputs and outputs over time.

#### **Objective: System Identification for Optimal Control**
We aim to design a control law that minimizes a specific cost criterion based on the data observed up to the current time $t$. The data set available at time $t$, denoted as $\mathcal{D}^{t}$, consists of the history of all input variables $u$ and output variables $y$:

$$\mathcal{D}^{t} = \{u(0), y(0), \dots, u(t), y(t)\}$$

#### **Problem Formulation: The Optimal Control Law**
When designing a controller over a $T$-step future horizon, we seek to minimize an expected cost criterion $\mathcal{J}$. Because the future data $\mathcal{D}_{t+1}^{t+T}$ is unknown, we must evaluate the expectation of the cost function $J$ conditioned on our current knowledge $\mathcal{D}^{t}$:

$$\mathcal{J} = \mathcal{E}\left\{J\left(\mathcal{D}_{t+1}^{t+T}\right) \middle| \mathcal{D}^{t}\right\} = \int J\left(\mathcal{D}_{t+1}^{t+T}\right) \rho\left(\mathcal{D}_{t+1}^{t+T} \middle| \mathcal{D}^{t}\right) d\mathcal{D}_{t+1}^{t+T}$$

To solve this integral, we require the joint probability density function (p.d.f.) of all future inputs and outputs.

#### **Evaluating the Joint P.D.F. via the Chain Rule**
The joint p.d.f. $\rho\left(\mathcal{D}_{t+1}^{t+T} \middle| \mathcal{D}^{t}\right)$ can be decomposed using the chain rule of probability. This decomposition separates the system's behavior (the output given the input and history) from the controller's behavior (the input given the history):

$$
\begin{split} 
\rho\left( \left. \mathcal{D}_{t+1}^{t+T} \right| \mathcal{D}^{t} \right) &= \rho \left( y(t+T) | u(t+T), \mathcal{D}^{t+T-1} \right) \rho \left( u(t+T) | \mathcal{D}^{t+T-1} \right) \\ 
&\times \dots \\ 
&\times \rho \left( y(t+2) | u(t+2), \mathcal{D}^{t+1} \right) \rho \left( u(t+2) | \mathcal{D}^{t+1} \right) \\ 
&\times \rho \left( y(t+1) | u(t+1), \mathcal{D}^{t} \right) \rho \left( u(t+1) | \mathcal{D}^{t} \right) 
\end{split}
$$

In this product:
*   **$\rho(y(\cdot) | u(\cdot), \mathcal{D}^{(\cdot)})$**: Represents the **System Model**, describing how the system generates an output given the current input and past data.
*   **$\rho(u(\cdot) | \mathcal{D}^{(\cdot)})$**: Represents the **Control Law**, describing how the controller chooses an input based on the available history.

This probabilistic framework allows us to account for uncertainties in both the system dynamics and the future control actions when calculating the optimal control strategy.