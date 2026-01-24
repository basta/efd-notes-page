# Properties of Statistics $s(y)$ and $S_N(\mathcal{Y}^N)$

To effectively detect changes in a system, we must understand the behavior of the log-likelihood ratio (LR) statistics. This section explores the properties of the incremental statistic $s(y)$ and the cumulative statistic $S_N$ through the lens of a classic change-of-mean problem.

#### Example: Change of Mean Value
Consider a sequence of independent normal variables with a known variance $\sigma^2$. We wish to detect a change in the mean parameter $\mu$. The two hypotheses are defined by the following probability density functions:

$$p(y|\mu_0) = \frac{1}{\sqrt{2\pi}\sigma}e^{-\frac{(y-\mu_0)^2}{2\sigma^2}}, \qquad p(y|\mu_1) = \frac{1}{\sqrt{2\pi}\sigma}e^{-\frac{(y-\mu_1)^2}{2\sigma^2}}$$

The log-likelihood for a single observation $y$ given a mean $\mu$ is:
$$\ln l(\mu|y) = -\ln \sigma - \frac{1}{2} \ln 2\pi - \frac{(y-\mu)^2}{2\sigma^2}$$

The incremental statistic $s(y)$, which represents the log-likelihood ratio between the alternative hypothesis ($H_1$) and the null hypothesis ($H_0$), is derived as:
$$s(y) = \ln \frac{l(\mu_1|y)}{l(\mu_0|y)} = -\frac{(y-\mu_1)^2}{2\sigma^2} + \frac{(y-\mu_0)^2}{2\sigma^2} = \frac{\mu_1 - \mu_0}{\sigma^2} \left(y - \frac{\mu_0 + \mu_1}{2}\right)$$

##### Statistical Properties of $s(y)$
The effectiveness of the test depends on the expected value of $s(y)$ under different conditions:
*   **Under $H_0$ ($\mu = \mu_0$):**
    $$\mathcal{E}\{s(y)|\mu = \mu_0\} = \frac{\mu_1 - \mu_0}{\sigma^2} \left(\mu_0 - \frac{\mu_0 + \mu_1}{2}\right) = -\frac{(\mu_1 - \mu_0)^2}{2\sigma^2} < 0$$
*   **Under $H_1$ ($\mu = \mu_1$):**
    $$\mathcal{E}\{s(y)|\mu = \mu_1\} = \frac{\mu_1 - \mu_0}{\sigma^2} \left(\mu_1 - \frac{\mu_0 + \mu_1}{2}\right) = \frac{(\mu_1 - \mu_0)^2}{2\sigma^2} > 0$$

The difference in these expectations is proportional to the **Signal-to-Noise Ratio (SNR)**, defined here by the squared difference of the means relative to the variance.

![](_page_141_Picture_10.jpeg)
![](_page_141_Picture_11.jpeg)

#### Properties of Statistics $s(y)$ and $S_N(\mathcal{Y}^N)$ (continued)

##### Variance of $s(y)$
To understand the spread of the statistic, we calculate the variance (covariance in the scalar case). Let $\tilde{y}$ be the zero-mean noise component. The deviation of the statistic $\tilde{s}(y)$ from its mean is:
$$\tilde{s}(y) = \frac{\mu_1 - \mu_0}{\sigma^2} \tilde{y}$$
Thus, the variance is:
$$\text{var} \{s(y)|\mu = \mu_i\} = \frac{(\mu_1 - \mu_0)^2}{\sigma^4} \text{var} \{y\} = \frac{(\mu_1 - \mu_0)^2}{\sigma^2}$$

##### Properties of the Cumulative Statistic $S_N$
For a sequence of $N$ independent samples, the cumulative log-likelihood ratio $S_N(\mathcal{Y}^N) = \sum_{k=1}^N s(y(k))$ exhibits the following properties:
*   **Mean:** $\mathcal{E}\{S_N|\mu=\mu_i\} = N \cdot \mathcal{E}\{s(y)|\mu=\mu_i\}$
*   **Variance:** $\text{var}\{S_N|\mu=\mu_i\} = N \cdot \text{var}\{s(y)|\mu=\mu_i\}$

**Key Observations:**
1.  The **mean difference** between hypotheses grows linearly with $N$.
2.  The **standard deviation** (the "scale" of uncertainty) grows with $\sqrt{N}$.
3.  As the sample size $N$ increases, the separation between the distributions of $S_N$ under $H_0$ and $H_1$ becomes more distinct, leading to better discrimination and a reduced false alarm rate.

![](_page_142_Picture_8.jpeg)
![](_page_142_Picture_9.jpeg)

#### Visualizing $S_N$ Statistics for Change of Mean

The following figures illustrate how the cumulative statistic $S_N$ behaves over time under different Signal-to-Noise Ratios.

**Case 1: High Signal-to-Noise Ratio ($\frac{\Delta\mu}{\sigma} = 1$)**
When the change is large relative to the noise, $S_N$ diverges quickly after the change point, making detection straightforward with low delay.

![](_page_143_Figure_3.jpeg)
![](_page_143_Figure_4.jpeg)
![](_page_143_Figure_5.jpeg)

**Case 2: Low Signal-to-Noise Ratio ($\frac{\Delta\mu}{\sigma} = 0.5$)**
When the change is subtle, the drift in $S_N$ is slower and more obscured by stochastic fluctuations. This requires more samples (larger $N$) to reach a confident decision, increasing the detection delay.

![](_page_143_Figure_7.jpeg)
![](_page_143_Figure_8.jpeg)
![](_page_143_Figure_9.jpeg)

![](_page_143_Picture_10.jpeg)
![](_page_143_Picture_11.jpeg)