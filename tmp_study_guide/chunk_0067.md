# Kalman filter for coloured noise (2)

In many practical applications, the assumption that measurement noise is "white" (uncorrelated in time) is violated. When the measurement noise exhibits spectral characteristics—meaning it is "coloured"—we must adapt the Kalman filter to maintain optimality.

#### **Kalman filter for coloured measurement noise**

Consider a standard linear stochastic process model where the measurement noise $e(t)$ is not white:

$$x(t+1) = Ax(t) + Bu(t) + v(t)$$
$$y(t) = Cx(t) + Du(t) + e(t)$$

To handle the coloured noise $e(t)$, we model it as the output of a **noise shaping filter** driven by a white noise source $e'(t)$. This allows us to describe the noise dynamics within a state-space framework:

$$x_e(t+1) = A_e x_e(t) + B_e e'(t)$$
$$e(t) = C_e x_e(t) + D_e e'(t)$$

The frequency characteristics of this noise are defined by its power spectrum density $S_{ee}(z)$:

$$S_{ee}(z) = \left(C_e(zI - A_e)^{-1}B_e + D_e\right)\left(C_e(z^{-1}I - A_e)^{-1}B_e + D_e\right)^T$$

#### **Augmented state space model**

To apply the standard Kalman filter equations, we augment the original system state $x(t)$ with the noise filter state $x_e(t)$. This results in a new, higher-dimensional system where the driving noise sources are white:

$$\begin{bmatrix} x(t+1) \\ x_e(t+1) \\ y(t) \end{bmatrix} = \begin{bmatrix} A & 0 \\ 0 & A_e \\ C & C_e \end{bmatrix} \begin{bmatrix} x(t) \\ x_e(t) \end{bmatrix} + \begin{bmatrix} B \\ 0 \\ D \end{bmatrix} u(t) + \begin{bmatrix} I & 0 \\ 0 & B_e \\ 0 & D_e \end{bmatrix} \begin{bmatrix} v(t) \\ e'(t) \end{bmatrix}$$

By defining the augmented state vector $x_{aug} = [x^T, x_e^T]^T$, we can proceed with the standard filter derivation. Note that in this formulation, the process noise and measurement noise in the augmented system may become correlated if $D_e \neq 0$, requiring the use of the correlated noise version of the Kalman filter equations.

#### **Key Considerations**

*   **Combined Noise Modeling**: If both process noise and measurement noise are coloured, the two augmentation methods (from this and the previous section) are combined. The state vector is expanded to include both $x_v$ and $x_e$.
*   **Engineering Perspective**: From a frequency-domain viewpoint, modeling coloured noise effectively modifies the frequency response of the Kalman filter. The transfer function from the output $y$ to the state estimate $\hat{x}$ is adjusted to "de-emphasize" frequency bands where the measurement noise power is high.

![](_page_119_Picture_13.jpeg)

![](_page_119_Picture_14.jpeg)