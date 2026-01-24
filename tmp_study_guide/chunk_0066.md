# Stochastic properties of Kalman filter (2)

#### **Prediction error – innovation**

The prediction error, often denoted as $\varepsilon(t|t-1)$, represents the difference between the actual observed output and the output predicted by the filter based on information up to the previous time step. Mathematically, it is defined as:

$$\varepsilon(t|t-1) = y(t) - \hat{y}(t|t-1) = Cx(t) + e(t) - C\hat{x}(t|t-1) = C\tilde{x}(t|t-1) + e(t)$$

where $\tilde{x}(t|t-1)$ is the state estimation error. Because the filter is still converging, the variance of this error is time-varying. It only reaches a steady state once the state error covariance $P(t|t-1)$ converges to its steady-state value $P$. The conditional covariance of the innovation is given by:

$$\mathcal{E}\left\{\varepsilon(t|t-1)\varepsilon^{T}(t|t-1)\middle|\mathcal{D}^{t-1}\right\} = CP(t|t-1)C^{T} + R$$

#### **Kalman filter and innovation**

The Kalman filter can be viewed through two dual perspectives regarding signal processing:

1.  **As a noise shaping filter**: In this view, the filter takes the white noise innovation sequence $\varepsilon(t|t-1)$ and "shapes" it through the system dynamics to reconstruct the output $y(t)$, which is a random process with a specific spectral density $S_{yy}(z)$.
    $$\hat{x}(t+1|t) = A\hat{x}(t|t-1) + L(t)\varepsilon(t|t-1)$$
    $$y(t) = C\hat{x}(t|t-1) + \varepsilon(t|t-1)$$

2.  **As a whitening filter**: Conversely, the filter can be seen as a system that takes the correlated output signal $y(t)$ and extracts the "new" information, resulting in the white noise innovation sequence $\varepsilon(t|t-1)$.
    $$\hat{x}(t+1|t) = (A-L(t)C)\hat{x}(t|t-1)+L(t)y(t)$$
    $$\varepsilon(t|t-1) = y(t) - C\hat{x}(t|t-1)$$

![](_page_117_Picture_13.jpeg)
![](_page_117_Picture_14.jpeg)
![](_page_117_Picture_15.jpeg)
![](_page_117_Picture_16.jpeg)

## Kalman filter for coloured noise

#### **Terminology**
The term "coloured noise" is an analogy to optics. While **white noise** contains all frequencies with uniform power (like white light), **coloured noise** has a non-uniform power spectrum, meaning certain frequencies are more dominant than others.

### **Kalman filter for coloured process noise**

When the process noise $v(t)$ is not white, we cannot apply the standard Kalman filter directly. Instead, we model the coloured noise as the output of a **noise shaping filter** driven by a white noise source $v'(t)$.

**Process model with coloured noise:**
$$x(t+1) = Ax(t) + Bu(t) + v(t)$$
$$y(t) = Cx(t) + Du(t) + e(t)$$

**Noise shaping filter dynamics:**
$$x_{\nu}(t+1) = A_{\nu}x_{\nu}(t) + B_{\nu}v'(t)$$
$$v(t) = C_{\nu}x_{\nu}(t) + D_{\nu}v'(t)$$

The power spectrum density of the resulting coloured noise is:
$$S_{vv}(z) = \left(C_v(zI - A_v)^{-1}B_v + D_v\right)\left(C_v(z^{-1}I - A_v)^{-1}B_v + D_v\right)^T$$

#### **Augmented state space model**
To solve this, we augment the original state $x(t)$ with the noise filter state $x_\nu(t)$. This creates a larger system where the inputs are once again white noise, allowing us to use the standard Kalman filter derivation:

$$\begin{bmatrix} x(t+1) \\ x_{v}(t+1) \\ y(t) \end{bmatrix} = \begin{bmatrix} A & C_{v} \\ 0 & A_{v} \\ C & 0 \end{bmatrix} \begin{bmatrix} x(t) \\ x_{v}(t) \end{bmatrix} + \begin{bmatrix} B \\ 0 \\ D \end{bmatrix} u(t) + \begin{bmatrix} D_{v} \\ B_{v} \\ 0 \end{bmatrix} v'(t) + \begin{bmatrix} 0 \\ 0 \\ I \end{bmatrix} e(t)$$

By estimating this augmented state, the filter simultaneously estimates the system state and the underlying "state" of the noise process.

![](_page_118_Picture_13.jpeg)
![](_page_118_Picture_14.jpeg)