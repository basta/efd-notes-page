# Non-parametric estimate of p.d.f.

In Bayesian estimation, we often encounter situations where the posterior probability density function (p.d.f.) does not follow a standard parametric form (like a Gaussian distribution). In such cases, we rely on non-parametric methods to represent and estimate the underlying distribution directly from a set of observed data samples.

### **Empirical p.d.f.**

The most fundamental way to represent a distribution from data is through the empirical p.d.f. Given a sample set $\mathcal{Y}^n = \{y_1, \dots, y_n\}$, we assume that the probability mass is concentrated entirely at the locations of the observed samples.

▶ **Definition**: The empirical p.d.f. $r_n(y)$ is defined using the Dirac delta function $\delta(y)$, which represents an idealized point mass:
$$r_n(y) = \frac{1}{n} \sum_{i=1}^n \delta(y-y_i)$$
Here, each observation contributes a weight of $1/n$ to the total probability density.

▶ **Recursive Update**: To handle streaming data efficiently without recomputing the entire sum, the empirical p.d.f. can be updated recursively as new samples arrive:
$$r_n(y) = \frac{n-1}{n} r_{n-1}(y) + \frac{1}{n} \delta(y - y_n)$$
This formulation shows that the new estimate is a weighted average of the previous estimate and the newest observation.

▶ **Multivariable Case**: In higher dimensions, the empirical distribution is often visualized as a "scatter plot," where the density of points in a specific region of the state space indicates the local probability mass.

---

### **Histogram**

While the empirical p.d.f. is mathematically useful, it is often too "spiky" for practical visualization or decision-making. The histogram provides a smoother, discretized approximation by grouping data into intervals.

▶ **Binning Process**: 
1. We divide the range of the data sample $\mathcal{Y}^n = \{y_1, \dots, y_n\}$ into $m$ disjoint bins (intervals), each with a fixed width $h$.
2. We define an **indicator (membership) function** $I_j(y)$ to determine if a point belongs to a specific bin:
   $$I_j(y) = \begin{cases} 1 & \text{if } y \text{ is in the } j\text{-th bin} \\ 0 & \text{otherwise} \end{cases}$$

▶ **Histogram Definition**: 
The histogram $h_n(y)$ is calculated by counting how many samples fall into each bin and normalizing the result so that the total area under the histogram equals one:
$$h_n(y) = \frac{1}{nh} \sum_{i=1}^n \sum_{j=1}^m I_j(y_i)$$
In this equation, $n$ is the total number of samples and $h$ is the bin width. The term $1/nh$ ensures that the resulting function is a valid probability density.

![](_page_160_Picture_13.jpeg)

![](_page_160_Picture_14.jpeg)

The choice of the bin width $h$ is critical:
*   If $h$ is **too small**, the histogram becomes jagged and overfits the noise in the sample (high variance).
*   If $h$ is **too large**, the histogram becomes too smooth and loses the underlying structure of the distribution (high bias).