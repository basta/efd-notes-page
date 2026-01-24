# Statistical hypothesis testing (2)

#### **Quality of the Test**

The performance of a statistical test is evaluated by its ability to correctly distinguish between the null hypothesis $H_0$ and the alternative hypothesis $H_1$. This performance is quantified by two types of probabilities:

▶ **Significance level ($\alpha$)**: This is the probability of incorrectly rejecting $H_0$ when it is actually true. In engineering and statistics, this is known as a **Type I error** or the **false positive rate**.
$$\alpha = P\left\{\mathcal{Y}^N \in \Omega_1^N | H_0 \right\} = P\left\{g(\mathcal{Y}^N) \neq 0 | H_0 \right\}$$

▶ **Test power ($1 - \beta$)**: This represents the probability of correctly rejecting $H_0$ when $H_1$ is true. Conversely, $\beta$ is the probability of failing to reject $H_0$ when $H_1$ is true, known as a **Type II error** or the **false negative rate**.
$$\beta = P\left\{\mathcal{Y}^N \in \Omega_0^N | H_1 \right\} = P\left\{g(\mathcal{Y}^N) \neq 1 | H_1 \right\}$$

#### **Example: Change of the Mean Value**

Consider a scenario where we observe a single sample $y$ and must decide between two hypotheses regarding its distribution. Both distributions are Gaussian with the same variance but different means:

$$H_0: y \sim \mathcal{N}(0, 0.1), \qquad H_1: y \sim \mathcal{N}(1, 0.1)$$

In this case, the decision involves setting a threshold. If the observed $y$ exceeds the threshold, we reject $H_0$. The overlap between the two probability density functions (PDFs) illustrates the trade-off: decreasing the threshold increases the test power ($1-\beta$) but also increases the significance level ($\alpha$), leading to more false alarms.

![](_page_135_Figure_8.jpeg)

![](_page_135_Figure_9.jpeg)

The figures above visualize the distribution of the test statistic under both hypotheses. The critical region $\Omega_1^N$ is typically defined where the likelihood of $H_1$ is significantly higher than $H_0$.

![](_page_135_Picture_10.jpeg)

![](_page_135_Picture_11.jpeg)