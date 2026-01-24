# Frequently used structures of input-output models (3)

In the previous sections, we established that the noise sequence $e(t)$ can be recovered from observed data if the noise-shaping filter $H(d)$ is stable and minimum phase. We now extend this to derive the formal predictor equations used in control and estimation.

#### **The Predictor Equation**

The goal of a predictor is to determine the mean value of the output $y(t)$ given all information up to the previous time step $\mathcal{D}^{t-1}$ and the current input $u(t)$. This predicted mean value depends fundamentally on the noise properties of the system.

The general form of the predictor is given by:
$$\hat{y}(t|t-1, u(t)) = H^{-1}(d)G(d)u(t) + \left(I - H^{-1}(d)\right)y(t)$$

To understand the relationship between the **predictor dynamics** and the **data generator dynamics**, we can substitute the data generator equation $y(t) = G(d)u(t) + H(d)e(t)$ into the predictor formula:

$$\begin{aligned} \hat{y}(t|t-1, u(t)) &= H^{-1}(d)G(d)u(t) + (I-H^{-1}(d))(G(d)u(t) + H(d)e(t)) \\ &= G(d)u(t) + (H(d)-I)e(t) \end{aligned}$$

This derivation confirms that the prediction consists of the deterministic response to the input $u(t)$ plus a weighted sum of past noise terms (since $H(d)$ is monic, $H(d)-I$ contains only terms with delays $d, d^2, \dots$).

#### **Probabilistic Description**

From a probabilistic perspective, the actual output $y(t)$ is the sum of our best prediction and a stochastic innovation term $e(t)$:

$$y(t) = \hat{y}(t|t-1, u(t)) + e(t), \quad e(t) \sim p_e(\cdot)$$

Because $\hat{y}$ is a deterministic function of past data and the current input, the conditional probability density function (c.p.d.f.) of the output is simply a shifted version of the noise distribution. By applying the transformation of random variables, we obtain:

$$p(y(t)|u(t), \mathcal{D}^{t-1}, \theta) = p_{e}\left(y(t) - \hat{y}\left(t|t-1, u(t)\right)\right)$$

This result is powerful: it implies that if the noise $e(t)$ is Gaussian, the predictive distribution of the output is also Gaussian, centered at $\hat{y}$ with a variance equal to the noise variance $\sigma_e^2$. This forms the basis for Maximum Likelihood and Bayesian estimation methods.