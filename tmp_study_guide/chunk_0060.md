# Numerical implementation of bayesian estimation algorithms (7)

### MATLAB function LDFIL

The following MATLAB function, `ldfil`, provides a robust implementation of the ARX (Auto-Regressive with Exogenous variables) identification algorithm. It utilizes the **LD factorization** of the covariance matrix to ensure numerical stability, preventing the covariance matrix from losing its positive-definite property due to rounding errors.

```matlab
function [stheta_out, ssigma_out, k, eps, dy] ...
         = ldfil(stheta, ssigma, data, phi)
% =========================================================
% LDFIL - ARX identification with LD factorized covariance
% =========================================================
% stheta = [theta, d, L^T] : Parameter estimates and factors
% ssigma = [nu, nus2]      : Degrees of freedom and residual sum
% data   = [z^T, y]        : Regressor vector and current output
% phi    = forgetting coefficient (exponential forgetting)
% =========================================================

% Unpack input dimensions and vectors
n = length(data) - 1;
z = data(1:n)';
y = data(n+1);
theta = stheta(:,1);
dth = stheta(:,2);
ltht = stheta(:,3:n+2);

% Validate and bound the forgetting factor
if nargin < 4,
  phi = 1;
else
  phi = min(phi,1);
  phi = max(phi,.01);
end

% Update covariance structure
% Construct the extended M and D matrices for the dyadic reduction
m = [1, zeros(1,n); ltht*z, ltht ];
d = [1; dth ];

% Perform Dyadic Reduction (dydr) for i=1
% This loop transforms the factors to maintain triangularity
for j = n+1:-1:2,
  mji = m(j,1);
  di = d(1) + mji*mji*d(j);
  mu = mji*d(j)/di;
  d(j) = d(j)*d(1)/di;
  d(1) = di;
  m(j,:) = m(j,:) - mji*m(1,:);
  m(1,:) = m(1,:) + mu*m(j,:);
end

% Decompose the results back into standard statistics
dy = d(1);                         % Output variance factor
dth = d(2:n+1)/phi;                % Updated parameter variance factors
ltht = m(2:n+1,2:n+1);             % Updated L factor
k = m(1,2:n+1)';                   % Gain vector

% Update parameter mean (theta)
eps = y - z'*theta;                % Prediction error
theta = theta + k*eps;             % Parameter update
stheta_out = [theta, dth, ltht];

% Update noise statistics (sigma)
if ~isempty(ssigma)
  nu = ssigma(1);
  nus2 = ssigma(2);
  nu = phi*(nu+1);                 % Update degrees of freedom
  nus2 = phi*(nus2 + eps*eps/dy);  % Update sum of squares
  ssigma_out = [nu, nus2];
else
  ssigma_out = [];
end
```

*Note: This implementation uses exponential forgetting. To adapt this function for **restricted linear** or **restricted exponential** forgetting, the update logic for $d(t+1|t)$ and $L(t+1|t)$ must be modified to incorporate the specific rank-1 update rules discussed in previous sections.*

![](_page_96_Picture_5.jpeg)

![](_page_96_Picture_6.jpeg)

---

### Convergence of the Least-Square method

The convergence of the Recursive Least Squares (RLS) estimator is a critical property for ensuring that the identified parameters eventually reach their "true" values.

#### Convergence vs. Experiment Design
Consider a data generator defined by:
$$y(t) = z^{T}(t)\theta^{*}$$
where $\theta^{*}$ represents the true parameter vector. If the system is not perfectly described by this structure, the "true" value is not well-defined.

The parameter error is defined as $\tilde{\theta}(t) = \theta^* - \hat{\theta}(t)$. We say the estimator converges if $\tilde{\theta}(t) \longrightarrow 0$ as $t \to \infty$. This convergence is guaranteed under the **Sufficient Excitation** condition:
$$\sum_{\tau=1}^t z(\tau) z^{T}(\tau) > \alpha I t$$
This condition implies that the input signals must be "rich" enough to excite all modes of the system, ensuring the information matrix is non-singular and grows linearly with time.

*   **Experiment Design:** To ensure high-quality data, one should test the eigenvalues of the information matrix $\sum_{\tau=1}^{t} z(\tau)z^{T}(\tau)$.
*   **Tracking Time-Varying Parameters:** For systems where parameters drift, we require **Persistent Excitation**, meaning the signal must be sufficiently exciting within every finite time window $T_p$:
    $$\alpha_1 I > \sum_{\tau=t}^{t+T_p} z(\tau) z^{T}(\tau) > \alpha_2 I$$

![](_page_97_Picture_13.jpeg)

![](_page_97_Picture_14.jpeg)

---

### Stability of Parameter Error (Lyapunov Method)

We can analyze the stability of the estimation process by treating the parameter error $\tilde{\theta}(t)$ as the state of a dynamic system.

**1. Error Dynamics:**
During the data update step, the error evolves as:
$$\tilde{\theta}(t) = \left(I - \frac{P(t-1)z(t)z^T(t)}{1+\zeta(t)}\right)\tilde{\theta}(t-1)$$
By substituting the identity $I - \frac{P(t-1)zz^T}{1+\zeta} = P(t)P^{-1}(t-1)$, we obtain the simplified linear dynamics:
$$\tilde{\theta}(t) = P(t)P^{-1}(t-1)\tilde{\theta}(t-1)$$

**2. Lyapunov Function Candidate:**
To prove stability, we define a Lyapunov function using the positive definite precision matrix $P^{-1}(t)$:
$$V(t) = \tilde{\theta}^{T}(t)P^{-1}(t)\tilde{\theta}(t)$$

**3. Stability Conclusion:**
It can be shown that this Lyapunov function is non-increasing ($\Delta V(t) \leq 0$). This implies that the parameter error is **Lyapunov-stable**, meaning the error will not grow over time, and under conditions of sufficient excitation, it will converge to zero.