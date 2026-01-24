# ARX model estimation (batch data processing)

In system identification, **batch processing** refers to the estimation of model parameters using a fixed, pre-collected set of data. This is in contrast to recursive estimation, where parameters are updated as each new data point arrives. For the ARX (Auto-Regressive with eXternal input) model, batch estimation typically relies on the Least Squares (LS) framework.

### **Batch Data Representation**

We begin with a set of observed data collected over a time horizon $T$:
$$\mathcal{D}_1^T = \{u(1), y(1), \dots, u(T), y(T)\}$$
*Note: Initial conditions (data prior to $t=1$) are required to populate the first few regressors but are generally treated as fixed constants in this notation.*

The ARX model assumes that the current output $y(t)$ is a linear combination of past outputs, current/past inputs, and a stochastic noise term:
$$y(t) = z^{T}(t)\theta + e(t), \quad e(t) \sim \mathcal{N}(0, \sigma_e^2), \quad \theta \in \mathcal{R}^n$$

Where:
*   $z(t)$ is the **regressor vector** containing past data.
*   $\theta$ is the **parameter vector** to be estimated.
*   $e(t)$ is the **equation error**, assumed here to be Gaussian white noise.

### **Compact Matrix Notation**

To solve for $\theta$ using the entire batch of data simultaneously, we stack the individual observations into a matrix-vector form:
$$Y = Z\theta + E$$

This compact notation is defined as follows:

1.  **Output Vector ($Y$):** A $T \times 1$ vector containing all observed outputs.
    $$Y = [y(1), y(2), \dots, y(T)]^T$$

2.  **Regressor (Data) Matrix ($Z$):** A $T \times n$ matrix where each row corresponds to the regressor vector at a specific time step.
    $$Z = \begin{bmatrix} z^T(1) \\ z^T(2) \\ \vdots \\ z^T(T) \end{bmatrix}$$
    In an ARX context, this matrix contains the lagged values of $y$ and $u$. Because it contains lagged outputs, $Z$ is often referred to as the "design matrix."

3.  **Prediction Error Vector ($E$):** A $T \times 1$ vector of the latent noise terms or residuals.
    $$E = [e(1), e(2), \dots, e(T)]^T$$

By formulating the problem this way, the task of parameter estimation becomes a search for the vector $\theta$ that best explains the observed $Y$ given the data $Z$, typically by minimizing the norm of the error vector $E$.