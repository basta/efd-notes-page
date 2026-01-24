# Frequently used structures of input-output models (2)

To design an effective controller, we require a **system model for control** that provides a predictive conditional probability density function (c.p.d.f.) $p(y(t) | u(t), \mathcal{D}^{t-1}, \theta)$. This model allows us to anticipate future outputs based on current inputs and historical data.

### **Equivalent "Data Generator" and "Predictor"**

The relationship between the physical data generator and the mathematical predictor is established through the properties of the noise shaping filter $H(d)$.

*   **Spectral Factorization**: By performing spectral factorization on the output power spectral density $S_{yy}(z)$, we can ensure that $H(d)$ is **stable** and **minimum phase**. This property is crucial because it guarantees that the inverse filter $H^{-1}(d)$ is also stable, allowing us to reconstruct the noise sequence from observed data.
*   **Noise Reconstruction**: If the model parameters $\theta$ are known, the white noise sequence $e(t)$ can be recovered from the input-output data:
    $$e(t) = H^{-1}(d) \Big( y(t) - G(d)u(t) \Big)$$

### **Output Prediction**
To predict the output $y(t)$, we decompose the system equation to separate the "past" information from the "new" stochastic innovation:

$$y(t) = G(d)u(t) + (H(d) - I)e(t) + e(t)$$

This can be rewritten in the form of a predictor plus an error term:
$$y(t) = \hat{y}(t | \mathcal{D}^{t-1}, u(t), \theta) + e(t)$$

In this formulation:
1.  The term $\hat{y}(t | \mathcal{D}^{t-1}, u(t), \theta)$ represents the **optimal prediction**.
2.  The term $(H(d) - I)e(t)$ depends strictly on past data $\mathcal{D}^{t-1}$ because $H(d)$ is monic (its first term is $I$), meaning $H(d)-I$ starts with a delay:
    $$(H(d) - I)e(t) = H_1e(t-1) + H_2e(t-2) + \cdots$$

For brevity, we often use the simplified notation:
$$\hat{y}(t | \mathcal{D}^{t-1}, u(t), \theta) = \hat{y}(t | t-1, u(t))$$

<span style="display:block; text-align:center;">
![](_page_54_Picture_12.jpeg)
</span>

<span style="display:block; text-align:center;">
![](_page_54_Picture_13.jpeg)
</span>