# Non-parametric estimate of p.d.f. (3)

While histograms provide a basic visualization of data distribution, they are sensitive to bin placement and suffer from discontinuities. A more sophisticated approach is the **Kernel Density Estimate (KDE)**, which provides a smooth, continuous approximation of the underlying probability density function.

#### Kernel estimate

The kernel density estimator for a sample of $n$ observations $\{y_1, \dots, y_n\}$ is defined as:

$$k_{n,h}(y) = \frac{1}{nh} \sum_{i=1}^{n} K\left(\frac{y-y_i}{h}\right)$$

In this formulation, $K(\cdot)$ is the **kernel function**—a symmetric function that integrates to one—and $h$ is the **bandwidth** (or smoothing parameter). Effectively, the KDE places a small "bump" of probability mass (the kernel) at each data point $y_i$ and sums them to create a global estimate.

**Frequently used kernels:**
*   **Normal (Gaussian) kernel:** $K(y) = \frac{1}{\sqrt{2\pi}} \exp\left(-y^2/2\right)$. This is the most common choice due to its smooth analytical properties.
*   **Tukey (Biweight) kernel:** $K(y) = \frac{15}{16} (1 - y^2)^2$ for $|y| \le 1$, and $0$ otherwise. This kernel has finite support, meaning it only considers data points within a specific distance.

#### Bandwidth Selection: The Smoothing Tradeoff

The choice of the kernel width $h$ is critical. A small $h$ leads to an "undersmoothed" estimate with high variance (showing spurious peaks), while a large $h$ leads to an "oversmoothed" estimate with high bias (obscuring the true structure of the data).

**Globally optimal width:**
If the true underlying density $p(y)$ were known, the optimal bandwidth $h$ that minimizes the Mean Integrated Square Error (MISE) is given by:

$$h = \left[ \frac{\int K^2(y) \ dy}{\int y^2 K^2(y) \ dy} \right]^{1/5} \left[ n \int \left(\frac{d^2 p(y)}{d y^2}\right)^2 \ dy \right]^{-1/5}$$

**Practical Implementation:**
1.  **Iterative Approach:** Since $p(y)$ is unknown, we can start with an initial guess $h^{(i)}$, estimate the density $k_{n,h^{(i)}}(y)$, use that estimate to calculate a refined $h^{(i+1)}$, and repeat until convergence:
    $$h^{(i)} \rightarrow p(y) \approx k_{n,h^{(i)}}(y) \rightarrow h^{(i+1)} \rightarrow p(y) \approx k_{n,h^{(i+1)}}(y) \dots$$
2.  **Variable Bandwidth (k-Nearest Neighbor):** Instead of a global $h$, we can use a local approximation where the bandwidth depends on the distance to the $k$-th nearest neighbor, $d_k(y)$. This allows for more smoothing in sparse regions and less smoothing in dense regions:
    $$k_n(y) = \sum_{i=1}^n \frac{K\left(\frac{y-y_i}{d_k(y)}\right)}{nd_k(y)}$$

![](_page_162_Picture_13.jpeg)

![](_page_162_Picture_14.jpeg)