# Statistical hypothesis testing (3)

#### Test optimization criteria

In change detection, the performance of a statistical test is defined by the trade-off between the probability of a false alarm ($\alpha$) and the probability of a missed detection ($\beta$). These errors are functions of the chosen critical function $g$:

$$\alpha = \alpha(g) \ge 0, \quad \beta = \beta(g) \ge 0$$

Depending on the application requirements, different criteria can be used to optimize the decision rule.

### Most powerful test $g_{MP}^*$
The goal of the Most Powerful (MP) test is to maximize the detection capability for a strictly controlled false alarm rate.
- **Procedure**: Select a fixed significance level $\alpha_0$ (typically between $0.01$ and $0.05$).
- **Optimization**: Minimize the Type II error (thereby maximizing the test power, $1-\beta$) subject to the constraint that the Type I error does not exceed $\alpha_0$.
$$g_{MP}^* = \arg\min_{g} \beta(g) \quad \text{subject to} \quad \alpha(g) = \alpha_0$$

### Bayesian test $g_B^*$
The Bayesian approach treats the hypotheses as random variables with known prior probabilities $P\{H_0\}$ and $P\{H_1\}$.
- **Optimization**: Minimize the total weighted probability of error.
$$w(g) = P\{g(\mathcal{Y}^N) \neq 0 | H_0\} P\{H_0\} + P\{g(\mathcal{Y}^N) \neq 1 | H_1\} P\{H_1\} = \alpha(g)P\{H_0\} + \beta(g)P\{H_1\}$$
$$g_B^* = \arg\min_{g} w(g)$$
This framework can be extended to a **minimum loss test**, where specific costs (weights) are assigned to false positives versus false negatives.

### Minimax test $g_{MinMax}^*$
When prior probabilities are unknown, the Minimax criterion is used to protect against the worst-case scenario by minimizing the maximum possible error.
$$g_{\textit{MinMax}}^* = \arg\min_{g} \max\{\alpha(g), \beta(g)\}$$

![](_page_136_Picture_16.jpeg)

![](_page_136_Picture_17.jpeg)

### Likelihood ratio methods: simple hypothesis

#### **Neyman-Pearson lemma (1933)**
The Neyman-Pearson lemma provides the fundamental basis for the Most Powerful test. For two simple hypotheses $H_0$ and $H_1$ with probability distributions $p_0(\mathcal{Y}^N)$ and $p_1(\mathcal{Y}^N)$, the optimal test is a Likelihood Ratio (LR) test. There exists a constant $\lambda_\alpha$ such that:

- $g(\mathcal{Y}^N)=1$ (reject $H_0$) if $\frac{p_1(\mathcal{Y}^N)}{p_0(\mathcal{Y}^N)} \geq \lambda_\alpha$
- $g(\mathcal{Y}^N)=0$ (accept $H_0$) if $\frac{p_1(\mathcal{Y}^N)}{p_0(\mathcal{Y}^N)} < \lambda_\alpha$

Where $\lambda_\alpha$ is chosen such that the expected value of the decision (the probability of rejection under $H_0$) equals the significance level: $\mathcal{E}\{g(\mathcal{Y}^N)|H_0\} = \alpha$.

#### **Likelihood Ratio Test (LR) implementation**
For a sequence of $N$ independent samples, the likelihood ratio can be decomposed into a product of individual ratios. To simplify computation and avoid numerical underflow, we typically use the **Log-Likelihood Ratio (LLR)**:

$$\ln \frac{p_{1}(\mathcal{Y}^{N})}{p_{0}(\mathcal{Y}^{N})} = \sum_{k=1}^{N} \ln \frac{p_{1}(y(k))}{p_{0}(y(k))} = \sum_{k=1}^{N} s(y(k))$$

This allows for a recursive update of the sufficient statistic $S_k$:
$$S_k = S_{k-1} + s(y(k))$$
The decision rule then becomes: $S_N \geq \ln \lambda_{\alpha}$.

![](_page_137_Picture_11.jpeg)

![](_page_137_Picture_12.jpeg)

### Likelihood ratio methods: composite hypothesis

#### **Generalized Neyman-Pearson lemma**
In many practical cases, the parameters $\theta$ are not fixed but belong to sets $\Theta_0$ and $\Theta_1$. The Generalized Likelihood Ratio (GLR) test uses the supremum of the likelihoods over these sets:

$$\hat{g}(\mathcal{Y}^N) = 1 \quad \text{if} \quad \frac{\sup_{\theta \in \Theta_1} p_{\theta}(\mathcal{Y}^N)}{\sup_{\theta \in \Theta_0} p_{\theta}(\mathcal{Y}^N)} \geq \lambda_{\alpha}$$

#### **Generalized Likelihood Ratio Test (GLR) implementation**
The GLR test effectively replaces the unknown parameters with their Maximum Likelihood (ML) estimates:
$$\hat{\theta}_0 = \arg \sup_{\theta \in \Theta_0} p(\mathcal{Y}^N|\theta), \qquad \hat{\theta}_1 = \arg \sup_{\theta \in \Theta_1} p(\mathcal{Y}^N|\theta)$$
The test is then performed as a standard LR test using these estimates:
$$\hat{g}(\mathcal{Y}^N) = 1 \text{ for } \frac{p_{\hat{\theta}_1}(\mathcal{Y}^N)}{p_{\hat{\theta}_0}(\mathcal{Y}^N)} \geq \lambda_{\alpha}$$

![](_page_138_Picture_9.jpeg)

![](_page_138_Picture_10.jpeg)

## Sequential likelihood ratio method

#### **Classical vs. Sequential Approach**
While the classical LR test uses a fixed sample size $N$, the **Sequential Likelihood Ratio (SLR) test** (developed by Wald in 1945) allows the number of observations to vary, making a decision as soon as enough evidence is accumulated.

### **Sequential Likelihood Ratio (SLR) test – Wald (1945)**
The statistics are updated recursively:
$$S_k = S_{k-1} + \ln \frac{p_1(y(k))}{p_0(y(k))}$$

The decision scheme involves two thresholds, $a$ and $b$:
1.  **Accept $H_1$**: if $S_k \ge b$
2.  **Accept $H_0$**: if $S_k \le a$
3.  **Continue**: if $a < S_k < b$ (accumulate more data)

The thresholds are approximated based on the desired error rates $\alpha$ and $\beta$:
$$a \approx \ln \frac{\beta}{1-\alpha}, \qquad b \approx \ln \frac{1-\beta}{\alpha}$$
This approach is highly efficient as it minimizes the average number of samples required to reach a decision.

![](_page_139_Picture_14.jpeg)

![](_page_139_Picture_15.jpeg)

### Detection algorithms based on LR test

#### Objectives and Assumptions
We aim to develop "on-line" recursive algorithms to detect a single abrupt change in the parameter $\theta$ of a stochastic process.
- **Assumption**: $\theta = \theta_0$ for $t \le t_0$ and $\theta = \theta_1$ for $t > t_0$, where $t_0$ is the unknown change time.
- **Statistic**: The core of these algorithms is the log-likelihood ratio $s(y) = \ln \frac{p_{\theta_1}(y)}{p_{\theta_0}(y)}$.

**Key Property**:
- Under $H_0$, $\mathcal{E}\{s(y)|\theta_0\} < 0$ (the cumulative sum drifts downward).
- Under $H_1$, $\mathcal{E}\{s(y)|\theta_1\} > 0$ (the cumulative sum drifts upward).
The detection of a change is essentially the detection of this change in the sign of the mean of the increments $s(y)$.