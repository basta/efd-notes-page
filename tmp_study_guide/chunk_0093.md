# Non-parametric estimate of p.d.f. (4)

#### Kernel width for normally distributed data

In kernel density estimation (KDE), the selection of the bandwidth $h$ is critical. A bandwidth that is too small leads to an undersmoothed estimate with high variance (showing spurious artifacts), while a bandwidth that is too large leads to an oversmoothed estimate that masks the underlying structure of the data.

When the underlying distribution $p(y)$ is known, we can derive an **optimal kernel width** that minimizes the Mean Integrated Square Error (MISE). The general theoretical formula for the optimal bandwidth is:

$$h = \left[ \frac{\int K^2(y) \ dy}{\int y^2 K^2(y) \ dy} \right]^{1/5} \left[ n \int \left( \frac{d^2 p(y)}{d \ y^2} \right)^2 \ dy \right]^{-1/5}$$

For the specific case where the data is assumed to be normally distributed, $y \sim \mathcal{N}(\mu, \sigma^2)$, and a Gaussian kernel is used, this expression simplifies significantly. This is often referred to as **Silverman's Rule of Thumb**:

$$h \approx 1.06 \ \sigma n^{-1/5}$$

where:
*   $\sigma$ is the standard deviation of the samples.
*   $n$ is the total number of observations in the sample set $\mathcal{Y}^n$.

#### Practical Example: Small Sample Size
Consider a kernel estimate based on a small sample of $n=20$ observations drawn from a standard normal distribution $\mathcal{N}(0,1)$. Applying the rule of thumb:

$$h \approx 1.06 \cdot (1) \cdot (20)^{-1/5} \approx 0.58\,\sigma$$

This bandwidth provides a balance between capturing the bell-shaped curve of the normal distribution and responding to the specific data points provided in the sample.

![](_page_163_Figure_5.jpeg)

*Figure 5: Comparison of different bandwidths on a sample set, illustrating the effect of smoothing.*

![](_page_163_Figure_6.jpeg)

*Figure 6: The resulting kernel density estimate versus the true underlying Gaussian distribution.*

![](_page_163_Picture_8.jpeg)

*Note: In practice, if $\sigma$ is unknown, it is often estimated using the sample standard deviation or the interquartile range (IQR) to make the bandwidth selection robust to outliers.*