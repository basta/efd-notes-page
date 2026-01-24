# Restricted Forgetting

In the context of tracking time-varying parameters in ARX models, standard exponential forgetting can lead to "covariance wind-up" if the system is not sufficiently excited. Restricted forgetting addresses this by selectively increasing uncertainty only in directions where new information is being received.

### **Restricted Linear Forgetting**

To implement restricted forgetting, we first recall the relationship for the Kalman gain $K(t)$, which relates the prior covariance $P(t|t-1)$ to the posterior covariance $P(t|t)$:

$$P(t|t)z(t) = \frac{P(t|t-1)z(t)}{1+\zeta(t|t-1)} = K(t)$$

Here, $\zeta(t|t-1) = z^T(t)P(t|t-1)z(t)$ represents the prior uncertainty in the direction of the regressor $z(t)$. In the restricted linear forgetting (LF) framework, the drift covariance matrix $V(t|t)$ is constructed to act only in the direction of the Kalman gain:

$$V(t|t) = P(t|t)z(t) \frac{\zeta_{\nu}(t)}{\zeta^{2}(t|t)} z^{T}(t)P(t|t) = K(t)\frac{\zeta_{\nu}(t)}{\zeta^{2}(t|t)}K^{T}(t)$$

This ensures that parameter drift is only modeled in the subspace spanned by the current data, preventing the uncontrolled growth of uncertainty in unexcited directions.

### **Restricted Exponential Forgetting**

We can derive a restricted version of exponential forgetting (EF) by finding an equivalent parameter drift model. For standard EF, the drift is implicitly $V(t) = \frac{1-\varphi}{\varphi} P(t|t)$, which implies a directional uncertainty increase of:

$$\zeta_{\nu}(t) = \frac{1-\varphi}{\varphi} \zeta(t|t)$$

By substituting this specific $\zeta_{\nu}(t)$ into the restricted drift formula, we obtain the restricted drift covariance matrix for exponential forgetting:

$$V(t|t) = K(t) \frac{\frac{1-\varphi}{\varphi}\zeta(t|t)}{\zeta^2(t|t)} K^{T}(t) = K(t) \frac{1-\varphi}{\varphi\zeta(t|t)} K^{T}(t)$$

![](_page_88_Picture_11.jpeg)

### **Combined Update Step**

The time-update and data-update steps can be merged into a single recursive formula for the covariance matrix. This combined step is expressed as:

$$P(t+1|t) = P(t|t-1) - \frac{P(t|t-1)z(t)z^{T}(t)P(t|t-1)}{\alpha(t)^{-1} + \zeta(t|t-1)}$$

where the scalar $\alpha(t)$ determines the nature of the update:

$$\alpha(t) = \frac{\varphi(1+\zeta(t|t-1))-1}{\zeta(t|t-1)}$$

Using the Matrix Inversion Lemma (MIL), we can see that $\alpha(t)$ acts as the weight of the $z(t)z^T(t)$ dyad in the information matrix update:

$$P(t+1|t)^{-1} = P(t|t-1)^{-1} + \alpha(t)z(t)z^{T}(t)$$

*   **Uncertainty Increase:** If $\varphi < \frac{1}{1+\zeta}$, then $\alpha(t) < 0$, and the update increases uncertainty (forgetting).
*   **Uncertainty Reduction:** If $\varphi > \frac{1}{1+\zeta}$, then $\alpha(t) > 0$, and the update reduces uncertainty (learning).

This approach limits forgetting to a single direction. We can define an equivalent directional forgetting factor:
$$\varphi(t|t) = \frac{\zeta(t|t)}{\zeta(t|t) + \zeta_{\nu}(t)}$$
This factor is derived from the LF model but can also be applied to the statistics of the noise variance $\sigma_e^2$.

![](_page_89_Picture_13.jpeg)

## Numerical Implementation of Bayesian Estimation Algorithms

To ensure numerical stability (e.g., maintaining positive definiteness of covariance matrices), Bayesian algorithms often use factorized forms.

### **Conditioning for Gaussian Variables**

Consider a joint Gaussian distribution for the output $y$ and parameters $x$:

$$\rho\left(\left[\begin{array}{c}\mathbf{y}\\\mathbf{x}\end{array}\right]\right) = \mathcal{N}\left(\left[\begin{array}{c}\mu_{y}\\\mu_{x}\end{array}\right]; \left[\begin{array}{c}P_{yy} & P_{yx}\\P_{xy} & P_{xx}\end{array}\right]\right)$$

We perform an **LD-factorization** on the joint covariance matrix:

$$\begin{bmatrix} P_{yy} & P_{yx} \\ P_{xy} & P_{xx} \end{bmatrix} = \begin{bmatrix} L_y & 0 \\ K & L_{x|y} \end{bmatrix} \begin{bmatrix} D_y & 0 \\ 0 & D_{x|y} \end{bmatrix} \begin{bmatrix} L_y^T & K^T \\ 0 & L_{x|y}^T \end{bmatrix}$$

Where $L$ matrices are monic lower triangular and $D$ matrices are diagonal. The conditional mean $\mu_{x|y}$ and covariance $P_{x|y}$ are then given by:

$$\mu_{x|y} = \mu_x + P_{xy}P_{yy}^{-1}(y - \mu_y)$$
$$P_{x|y} = P_{xx} - P_{xy}P_{yy}^{-1}P_{yx}$$

By substituting the LD factors:
*   $P_{yy} = L_y D_y L_y^T$
*   $P_{xy} = K D_y L_y^T$
*   $P_{xx} = K D_y K^T + L_{x|y} D_{x|y} L_{x|y}^T$

This factorization allows for efficient and robust computation of the Kalman update.

![](_page_90_Picture_12.jpeg)
![](_page_90_Picture_13.jpeg)