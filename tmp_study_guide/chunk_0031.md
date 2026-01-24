# Model structure and parameters (3)

In real-world control applications, systems are rarely perfectly stationary. Environmental changes, mechanical wear, or shifts in operating points mean that the parameters governing the system dynamics may evolve over time.

#### **Time-Varying Systems**

When the parameter vector $\theta$ is (slowly) time-varying, we denote it as $\theta(t)$. The predictive conditional probability density function (c.p.d.f.) must account for this uncertainty by integrating over the possible values of the current parameter state:

$$p\left(y(t) \mid u(t), \mathcal{D}^{t-1}\right) = \int p\left(y(t) \mid u(t), \mathcal{D}^{t-1}, \theta(t)\right) p\left(\theta(t) \mid u(t), \mathcal{D}^{t-1}\right) d\theta(t)$$

This formulation shows that the prediction of the output $y(t)$ depends on both the model structure (the first term in the integral) and our current estimate of the time-varying parameters (the second term).

---

#### **Update of Parameter c.p.d.f. in Two Steps**

To track time-varying parameters, we employ a recursive estimation strategy similar to the Kalman Filter, consisting of a **Data Update** and a **Time Update**.

**1. Data Update Step (Filtering)**
In this step, we incorporate the most recent observation $\{u(t), y(t)\}$ to refine our knowledge of the parameter $\theta(t)$. Using Bayes' formula:

$$\rho\left(\theta(t) \mid \mathcal{D}^{t-1}\right) \to \rho\left(\theta(t) \mid \mathcal{D}^{t}\right)$$

The posterior distribution is proportional to the product of the likelihood and the prior:
$$\rho\left(\theta(t) \mid \mathcal{D}^{t}\right) \propto \rho\left(y(t) \mid u(t), \mathcal{D}^{t-1}, \theta(t)\right) \rho\left(\theta(t) \mid \mathcal{D}^{t-1}\right)$$

**2. Time Update Step (Prediction)**
This step projects our parameter knowledge forward to the next time step $t+1$. It accounts for the fact that the parameters may have changed between observations:

$$p\left(\theta(t+1) \mid \mathcal{D}^t\right) = \int p\left(\theta(t+1) \mid \theta(t), \mathcal{D}^t\right) p\left(\theta(t) \mid \mathcal{D}^t\right) d\theta(t)$$

#### **Parameter Development Model**
In many practical scenarios, the exact physical law governing how $\theta(t)$ changes (the transition model $p(\theta(t+1) \mid \theta(t), \mathcal{D}^t)$) is unknown. In such cases, we replace the formal transition model with **heuristics**, such as **exponential forgetting**. This technique gives more weight to recent data and allows the estimator to "forget" obsolete information, effectively widening the distribution $p(\theta(t+1) \mid \mathcal{D}^t)$ to account for increased uncertainty.

![](_page_52_Picture_11.jpeg)

![](_page_52_Picture_12.jpeg)