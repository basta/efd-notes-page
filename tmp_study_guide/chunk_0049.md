# ARX model – tracking of time-varying parameters

In many practical control applications, the assumption that system parameters are constant over time is unrealistic. Systems may undergo changes due to wear and tear, varying environmental conditions, or shifts in operating points. To account for this, we transition from static parameters $\theta$ and $\sigma_e$ to time-varying notations $\theta(t)$ and $\sigma_e(t)$.

### **Slowly time-varying parameters**

When parameters change slowly relative to the sampling rate, we can adapt the recursive estimation framework to "track" these changes. This process is fundamentally divided into a **Data Update** step (incorporating new information) and a **Time Update** step (modeling how parameters evolve between samples).

#### **Data Update Step**
The data update is based on Bayes' rule. The posterior distribution of the parameters at time $t$, given all data up to that point $\mathcal{D}^t$, is proportional to the likelihood of the current observation $y(t)$ multiplied by the prior distribution (which is the prediction from the previous step):

$$\rho\left(\theta(t), \sigma_e(t)|\mathcal{D}^t\right) \propto \rho\left(y(t)|\theta(t), \sigma_e(t), u(t), \mathcal{D}^{t-1}\right) \rho\left(\theta(t), \sigma_e(t)|\mathcal{D}^{t-1}\right)$$

In this recursive framework, our knowledge of the system is encapsulated in four primary statistics that evolve from their predicted values (denoted by $t|t-1$) to their updated values (denoted by $t|t$):
$$\hat{\theta}(t|t-1), P(t|t-1), s^2(t|t-1), \nu(t|t-1) \rightarrow \hat{\theta}(t|t), P(t|t), s^2(t|t), \nu(t|t)$$

#### **Resulting Formulas for Statistics**
The recursive update equations for the ARX model parameters are derived as follows:

1.  **Mean Parameter Estimate:**
    $$\hat{\theta}(t|t) = \hat{\theta}(t|t-1) + \frac{P(t|t-1)z(t)}{1+\zeta(t|t-1)} \varepsilon(t|t-1)$$
    The new estimate is the old estimate plus a correction term weighted by the Kalman-like gain.

2.  **Normalized Covariance Matrix:**
    $$P(t|t) = P(t|t-1) - \frac{P(t|t-1)z(t)z^{T}(t)P(t|t-1)}{1+\zeta(t|t-1)}$$
    This update reduces the uncertainty in the parameter estimates as more data is processed.

3.  **Residual Sum of Squares and Degrees of Freedom:**
    $$\nu(t|t)s^{2}(t|t) = \nu(t|t-1)s^{2}(t|t-1) + \frac{\varepsilon^{2}(t|t-1)}{1+\zeta(t|t-1)}$$
    $$\nu(t|t) = \nu(t|t-1) + 1$$
    The degrees of freedom $\nu$ increment with every new data point, while the weighted residual variance $s^2$ is updated based on the prediction error.

#### **Auxiliary Variables**
To simplify the notation, we define the **prediction error** $\varepsilon$ and the **normalized regressor norm** $\zeta$:
*   **Prediction Error:** $\varepsilon(t|t-1) = y(t) - z^{T}(t)\hat{\theta}(t|t-1)$
    (The difference between the actual observed output and the output predicted by the previous model).
*   **Regressor Norm:** $\zeta(t|t-1) = z^{T}(t)P(t|t-1)z(t)$
    (A measure of the "informativeness" or "strength" of the current regressor $z(t)$ relative to the current parameter uncertainty).

![](_page_79_Picture_10.jpeg)

![](_page_79_Picture_11.jpeg)

The figures above illustrate the dynamic nature of the estimation. As new data arrives, the probability density functions (PDFs) for the parameters shift and sharpen, allowing the model to converge toward the true (though potentially moving) parameter values.