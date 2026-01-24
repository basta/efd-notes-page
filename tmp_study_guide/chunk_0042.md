# ARX model estimation - order selection (3)

### **How to evaluate resulting model quality (contd.)?**

Beyond the Akaike Information Criterion (AIC) and the residual sum of squares, several statistical tools allow us to assess whether a chosen model order is appropriate or if the model is capturing the underlying system dynamics effectively.

#### **1. Prediction Error Covariance Function**
One of the primary indicators of a "good" model is that the residuals (prediction errors) should behave like white noise. If the model has captured all the systematic information in the data, the remaining error $e(t)$ should be uncorrelated with its own past values. We evaluate this using the autocovariance function of the residuals:

$$R_{e,e}(k) = \mathcal{E}\left\{e(t)e(t+k)\right\} \approx \frac{1}{T-k}\sum_{t=1}^{T-k}e(t)e(t+k)$$

Where:
*   **$T$** is the total number of data points.
*   **$k$** is the lag (typically $k < K \ll T$).
*   If $R_{e,e}(k)$ is significantly non-zero for $k > 0$, it suggests that the model order is too low (underfitting), as there is still predictable structure left in the residuals.

#### **2. Parameter Significance and Confidence Intervals**
We must also determine if the estimated parameters $\hat{\theta}_i$ are statistically significant or if they are essentially zero (meaning the corresponding regressor does not contribute to the model). This is done by analyzing the parameter covariance matrix.

*   **Information Matrix:** $P_{\theta} = (Z^T Z)^{-1}$ reflects the geometry of the data.
*   **Scaled Covariance:** $P_{\theta \mid \sigma^2} = \sigma^2 (Z^T Z)^{-1}$ provides the theoretical variance of the estimates.
*   **Estimated Variance:** In practice, we use the estimated noise variance $s^2$ to approximate the variance of individual parameters:
    $$\text{cov } \{\theta_i\} \approx s^2 P_{\theta i, i}$$
    where $P_{\theta i, i}$ is the $i$-th diagonal element of $(Z^T Z)^{-1}$. If the estimate $\hat{\theta}_i$ is small relative to its standard deviation $\sqrt{\text{cov}\{\theta_i\}}$, the parameter may be redundant.

#### **3. Comparison: 2nd Order vs. 6th Order Models**
Comparing models of different complexities helps visualize the trade-off between bias and variance. A 2nd-order model might be too simple to capture the system's peaks (high bias), while a 6th-order model might begin to fit the noise (high variance/overfitting).

The following figures illustrate these diagnostic comparisons, including residual analysis and pole-zero maps for different model orders:

![](_page_71_Figure_7.jpeg)

![](_page_71_Figure_8.jpeg)

![](_page_71_Figure_9.jpeg)

![](_page_71_Picture_11.jpeg)

By examining the residual plots and the parameter significance, we can identify the "elbow" point where increasing the model order no longer yields a significant improvement in the residual white-noise properties, indicating the optimal order.