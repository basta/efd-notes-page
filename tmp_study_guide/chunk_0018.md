# Examples of ML estimates (2)

#### Uniform Distribution
Consider a scenario where the data $x$ is drawn from a uniform distribution $U_{\theta}(x)$ centered at zero with an unknown boundary parameter $\theta$.

**Probability Density Function (PDF):**
The PDF for a single observation is defined as:
$$p(x|\theta) = \begin{cases} \frac{1}{2\theta} & \text{for } x \in [-\theta, \theta] \\ 0 & \text{otherwise} \end{cases}$$

**Likelihood Function:**
For $n$ independent and identically distributed (i.i.d.) observations $x_1, \dots, x_n$, the joint likelihood is the product of individual densities:
$$l_n(\theta) = p_n(x|\theta) = \left(\frac{1}{2\theta}\right)^n$$
This expression holds true only if **all** observed samples fall within the range $[-\theta, \theta]$. If even one sample $|x_i| > \theta$, the likelihood drops to zero.

**Conclusions:**
To maximize the likelihood $l_n(\theta)$, we need to choose the smallest possible $\theta$ that still satisfies the condition $|x_i| \leq \theta$ for all $i$.
*   **ML Estimate:** The estimate is defined by the maximum absolute value in the sample set:
    $$\widehat{\theta}_{\text{ML}} = \max_{i} |x_i|$$
*   **Recursive Update:** This estimate is easily updated as new data arrives: $\widehat{\theta}_{n} = \max(|\widehat{\theta}_{n-1}|, |x_n|)$.

![](_page_32_Picture_11.jpeg)

---

### Examples of ML estimates (3)

#### Cauchy Distribution
The Cauchy distribution is a symmetric distribution similar in shape to the Normal distribution but with "heavy tails." It is frequently used in robustness analysis because it is more likely to produce extreme outliers than a Gaussian model.

**Probability Density Function:**
The PDF for a single observation with location parameter $\theta$ is:
$$C_{\theta}(x) = \frac{1}{\pi \left(1 + (x - \theta)^2\right)}$$
For $n$ independent samples, the joint PDF is:
$$p_n(x|\theta) = \frac{1}{\pi^n} \prod_{i=1}^n \frac{1}{1+(x_i-\theta)^2}$$

**Log-Likelihood:**
To find the ML estimate, we take the natural logarithm to simplify the product into a sum:
$$L_n(\theta) = \ln p_n(x|\theta) = -n \ln \pi - \sum_{i=1}^n \ln \left(1 + (x_i - \theta)^2\right)$$
Maximizing $L_n(\theta)$ is equivalent to minimizing the summation term:
$$f(\theta) = \sum_{i=1}^n \ln \left(1 + (x_i - \theta)^2\right)$$

**Conclusions:**
*   **Numerical Solution:** Unlike the Gaussian case, the derivative of $f(\theta)$ results in a high-order polynomial. Consequently, there is no closed-form analytical solution; the estimate must be found using numerical optimization.
*   **Sufficient Statistics:** There are no "smaller" statistics (like the mean or variance) that can summarize the data. To compute the ML estimate, the entire raw dataset must be preserved.

![](_page_33_Figure_13.jpeg)
![](_page_33_Figure_14.jpeg)
![](_page_33_Picture_15.jpeg)
![](_page_33_Picture_16.jpeg)