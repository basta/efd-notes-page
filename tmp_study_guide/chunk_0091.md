# Non-parametric estimate of p.d.f. (2)

In practical estimation, we often encounter data where the underlying distribution is unknown or too complex to be modeled by standard parametric families (like the Gaussian distribution). In such cases, we rely on non-parametric methods to estimate the probability density function (p.d.f.) directly from the observed data.

### Histogram normalization

The histogram is the most fundamental non-parametric tool. Given a sample set $\mathcal{Y}^n = \{y_1, \dots, y_n\}$, we divide the range of data into $m$ bins, each of width $h$. To ensure the histogram serves as a valid statistical tool, several normalization schemes are used, often corresponding to standard software implementations like those found in MATLAB.

#### 1. Bin Counts and Probabilities
For each bin $j$, we define:
*   **Bin count** $n_b(j)$: The number of observations falling into the $j$-th bin.
*   **Bin probability** $p_b(j) = \frac{n_b(j)}{n}$: The relative frequency of observations in that bin.

#### 2. Normalization Types
Depending on the objective, the histogram can be scaled in different ways:

*   **Normalized Count (Matlab 'count'):**
    The sum of the heights of all bins equals the total number of samples (or is normalized to 1 in some contexts to show proportions).
    $$\sum_{j=1}^m n_b(j) = n$$

*   **Normalized Probability (Matlab 'prob'):**
    The sum of the bin probabilities is normalized to unity. This represents the discrete probability mass function.
    $$\sum_{j=1}^{m} p_b(j) = 1$$

*   **Probability Density Function (Matlab 'pdf'):**
    To approximate a continuous p.d.f., the area under the histogram must equal 1. This requires dividing the bin probability by the bin width $h$.
    $$\int_{-\infty}^{\infty} h_n(y) dy \approx \sum_{j=1}^{m} h \cdot \left(\frac{p_b(j)}{h}\right) = 1$$
    Here, $h_n(y) = \frac{p_b(j)}{h}$ for $y$ in bin $j$.

*   **Cumulative Representations:**
    *   **Normalized Cumulative Count (Matlab 'cumcount'):** A running sum of the counts.
    *   **Cumulative Probability Function (Matlab 'cdf'):** An empirical approximation of the Cumulative Distribution Function (CDF), where the value at bin $k$ is $\sum_{j=1}^k p_b(j)$.

![](_page_161_Figure_12.jpeg)

#### Visualizing the Estimates
The following figures illustrate the transition from raw data samples to a structured histogram and finally to a cumulative distribution. The choice of bin width $h$ is critical: if $h$ is too small, the estimate is too noisy (overfitting); if $h$ is too large, important features of the distribution are smoothed out (underfitting).

![](_page_161_Picture_13.jpeg)

![](_page_161_Picture_14.jpeg)