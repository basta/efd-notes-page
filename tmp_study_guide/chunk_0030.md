# Model structure and parameters (2)

In the context of system identification for adaptive control, we must define the relationship between the system parameters, the observed data, and the control actions. A fundamental concept in this framework is the "Natural Condition of Control."

#### **Natural Condition of Control**

The natural condition of control is a formal assumption regarding the independence of our parameter knowledge from the current control input. It is expressed mathematically as:

$$p\left(\theta \middle| u(t), \mathcal{D}^{t-1}\right) = p\left(\theta \middle| \mathcal{D}^{t-1}\right)$$

This identity states that the conditional probability density function (c.p.d.f.) of the parameters $\theta$, given the past data $\mathcal{D}^{t-1}$ and the current input $u(t)$, is identical to the c.p.d.f. based solely on the past data.

#### **Interpretation and Implications**

This condition carries significant weight in how we design and analyze adaptive controllers:

1.  **Independence of Parameter Knowledge**: The calculation or selection of the new input $u(t)$ does not provide additional information about the internal parameters $\theta$ of the system. 
    *   This is typically **valid** for an LQG (Linear Quadratic Gaussian) controller operating with incomplete state information, where the controller relies on the estimated state and parameters derived from past observations.
    *   This is generally **not true** for LQ control with complete state information if the control law is designed to be "dual"—meaning the control action is specifically chosen to excite the system to improve parameter estimation (probing).

2.  **Symmetry in Information**: The natural condition of control also implies that the control law does not depend on the true (unknown) parameters $\theta$ beyond what has already been learned from the data:
    $$p\left(u(t)\middle|\theta,\mathcal{D}^{t-1}\right)=p\left(u(t)\middle|\mathcal{D}^{t-1}\right)$$
    This suggests that the controller uses the available data $\mathcal{D}^{t-1}$ to form its strategy, and knowing $\theta$ directly (which is impossible in practice) would not change the distribution of the control law if the law is strictly based on the history of observations.

#### **Factorization of the Joint P.D.F.**

To understand the flow of information, we can look at two ways to factorize the joint probability density of the parameters and the current input:

$$\begin{split} \rho\left(\theta, u(t) \middle| \mathcal{D}^{t-1}\right) &= \rho\left(\theta \middle| u(t), \mathcal{D}^{t-1}\right) \rho\left(u(t) \middle| \mathcal{D}^{t-1}\right) \\ &= \rho\left(u(t) \middle| \theta, \mathcal{D}^{t-1}\right) \rho\left(\theta \middle| \mathcal{D}^{t-1}\right) \end{split}$$

Under the Natural Condition of Control, these factorizations simplify to:

$$\rho\left(\theta, u(t) \middle| \mathcal{D}^{t-1}\right) = \rho\left(\theta \middle| \mathcal{D}^{t-1}\right) \rho\left(u(t) \middle| \mathcal{D}^{t-1}\right)$$

This result confirms that, given the history $\mathcal{D}^{t-1}$, the current control input $u(t)$ and the parameters $\theta$ are conditionally independent. Consequently, all information relevant for the design of the control law is contained entirely within the observed data history $\mathcal{D}^{t-1}$.