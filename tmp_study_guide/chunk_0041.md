# ARX model estimation - order selection (2)

In the process of system identification, selecting the appropriate model order is a critical step. If the order is too low (underfitting), the model will fail to capture the underlying dynamics of the system. If the order is too high (overfitting), the model will begin to fit the stochastic noise in the data, leading to poor generalization on new datasets.

### **How to evaluate resulting model quality?**

To determine the optimal order for an ARX model, we utilize several statistical metrics that balance the fit of the model against its complexity.

#### 1. Residual Sum of Squares and Estimated Noise Variance
The most fundamental measure of fit is the residual sum of squares. Once the parameter estimate $\hat{\theta}$ is obtained, we can calculate the estimated noise variance, $s^2$. This value represents the portion of the output signal that the model cannot explain.

$$\sigma_e^2 \approx s^2 = \frac{1}{T-n} \left( Y - Z\hat{\theta} \right)^T \left( Y - Z\hat{\theta} \right)$$

Where:
*   $T$ is the number of data samples.
*   $n$ is the number of estimated parameters (model order).
*   $Y$ is the vector of observed outputs.
*   $Z\hat{\theta}$ represents the predicted outputs based on the estimated parameters.

As the model order $n$ increases, the residual variance $s^2$ typically decreases. However, a decreasing $s^2$ does not always mean a better model, as it may indicate overfitting.

#### 2. Akaike Information Criterion (AIC)
To prevent overfitting, we use the **Akaike Information Criterion (AIC)**. The AIC introduces a penalty term that increases with the number of parameters, effectively "penalizing" model complexity. The goal is to find the model order that minimizes the AIC value.

$$AIC = T\log(s^2) + 2n$$

In this formula:
*   $T\log(s^2)$ represents the log-likelihood of the model (how well the model fits the data).
*   $2n$ is the penalty term for the number of parameters $n$.

By minimizing the AIC, we seek a balance where the model is complex enough to capture the system dynamics but simple enough to remain robust.

![](_page_70_Figure_6.jpeg)

![](_page_70_Figure_7.jpeg)

The figures above illustrate the trade-off between the fit (residual error) and the model order. Typically, you will observe that while the error $s^2$ continues to drop as the order increases, the AIC curve will reach a minimum and then begin to rise, indicating the point where additional parameters no longer provide a statistically significant improvement in model quality.