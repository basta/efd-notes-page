# <span id="page-47-0"></span>**4. Parameter estimation**

In the previous sections, we explored the theoretical foundations of the normal distribution and the role of sufficient statistics. We now transition into the core of Bayesian inference: **Parameter Estimation**.

Parameter estimation is the process of using observed data to refine our knowledge of the internal constants (parameters) that govern a system's behavior. In a Bayesian framework, we do not treat parameters as fixed, unknown constants, but rather as random variables characterized by probability distributions.

### **The Estimation Workflow**

The estimation process typically follows a recursive or batch logic:
1.  **Prior Knowledge**: We begin with an initial belief about the parameters, represented by the prior distribution $p(\theta)$.
2.  **Data Collection**: We observe a set of measurements or data points $y$.
3.  **Likelihood Evaluation**: We determine how likely the observed data is, given specific parameter values, using the model $p(y|\theta)$.
4.  **Posterior Update**: Using Bayes' Rule, we combine the prior and the likelihood to form the posterior distribution $p(\theta|y)$, which represents our updated knowledge.

![](_page_47_Picture_1.jpeg)

As we move forward into dynamic systems, this estimation process becomes the engine for **System Identification**. By continuously updating our parameter estimates as new inputs $u(t)$ and outputs $y(t)$ arrive, we can build adaptive models that "learn" the characteristics of a plant in real-time, providing the necessary information for optimal control laws.