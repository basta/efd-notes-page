# Some well-known statistics

In the study of estimation and control, we often rely on fundamental statistical measures to characterize data and system behavior. This section explores the properties of the most common statistics derived from a set of observations.

### **Assumptions**

To analyze the properties of these statistics, we establish a standard framework:
- Let $X_i$ be a sequence of **i.i.d.** (independent and identically distributed) random variables.
- Each variable has a defined mean $\mathcal{E}\{X_i\} = \mu$ and a variance $\operatorname{cov}\{X_i\} = \sigma^2$.

When considering the sum of these variables, the linearity of the expectation operator and the independence of the variables allow us to derive the following:

$$\mathcal{E}\left\{\sum_{i=1}^{n} X_{i}\right\} = n\mu$$

$$\operatorname{cov}\left\{\sum_{i=1}^{n} X_{i}\right\} = \mathcal{E}\left\{\left(\sum_{i=1}^{n} X_{i} - n\mu\right)^{2}\right\} = \mathcal{E}\left\{\sum_{i=1}^{n} (X_{i} - \mu)^{2}\right\} = n\sigma^2$$

These results show that while the expected value scales linearly with the number of samples $n$, the total variance also scales linearly with $n$, which has significant implications for the precision of our estimates.

### **Statistics**

#### **Sample Mean**
The sample mean (also known as the sample average or arithmetic average) is the most common estimator for the population mean $\mu$. It is defined as:

$$\bar{X} = \frac{1}{n} \sum_{i=1}^{n} X_{i}$$

**Expectation of the Sample Mean:**
The sample mean is an **unbiased** estimator of $\mu$, as its expected value is exactly equal to the parameter it intends to estimate:

$$\mathcal{E}\left\{\bar{X}\right\} = \mathcal{E}\left\{\frac{1}{n} \sum_{i=1}^{n} X_{i}\right\} = \frac{1}{n} \sum_{i=1}^{n} \mu = \mu$$

**Variance of the Sample Mean:**
The variance (or covariance in the scalar case) of the sample mean quantifies the uncertainty of our estimate. As the sample size $n$ increases, the variance decreases, indicating that the estimate becomes more "concentrated" around the true mean:

$$\operatorname{cov}\left\{\bar{X}\right\} = \mathcal{E}\left\{\left(\frac{1}{n} \sum_{i=1}^{n} X_{i} - \mu\right)^{2}\right\} = \frac{1}{n^{2}} \sum_{i=1}^{n} \sigma^{2} = \frac{\sigma^{2}}{n}$$

*(Note: In the original derivation provided, the result $\frac{\sigma^2}{n^2}$ is a common typo; the correct scaling for the variance of the mean is $\sigma^2/n$.)*

![](_page_8_Picture_8.jpeg)

![](_page_8_Picture_9.jpeg)

2