# ARX model estimation - order selection (4)

### **Textbook example results**

In this section, we examine the practical application of order selection criteria using a controlled "textbook" scenario. In such examples, the true system structure is known, allowing us to validate how effectively our estimation tools—such as the **Akaike Information Criterion (AIC)** and **Residual Variance ($s^2$)**—identify the correct model order.

The data generator used for this demonstration follows a pure ARX (Auto-Regressive with eXogenous input) structure. Because the underlying system matches the model structure being tested, we expect the statistical metrics to behave predictably as the assumed model order $n$ increases.

![](_page_72_Figure_3.jpeg)

The figure above illustrates the typical behavior of the selection criteria:
1.  **Estimated Noise Variance ($s^2$):** As the model order increases, the residual sum of squares generally decreases. However, once the true order is reached, the decrease in $s^2$ becomes marginal, as the model begins to fit the stochastic noise rather than the underlying system dynamics.
2.  **AIC Curve:** The AIC introduces a penalty term $2n$ for model complexity. In this textbook case, the AIC curve typically shows a distinct minimum at the true order of the system. This "elbow" or minimum point provides a clear, objective justification for selecting a specific order, balancing the trade-off between bias (underfitting) and variance (overfitting).

![](_page_72_Picture_5.jpeg)

The secondary visualization provides a comparison of the estimated parameters against the true coefficients of the data generator. In a textbook ARX example, when the correct order is selected, the parameter estimates $\hat{\theta}$ should converge closely to the true values, and the prediction errors should resemble white noise with a variance approximately equal to $\sigma_e^2$. 

These results confirm that for systems where the ARX assumption holds, the combination of residual analysis and information criteria provides a robust framework for system identification.