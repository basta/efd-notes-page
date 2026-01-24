# <span id="page-6-0"></span>**2. Statistics, estimation methods**

![](_page_6_Picture_1.jpeg)

### Statistics

In the study of control theory and estimation, we must first establish a rigorous understanding of statistics. This field provides the mathematical foundation for interpreting signals, identifying system parameters, and estimating hidden states in the presence of noise.

### **Meaning of the term "statistics"**

The term "statistics" is used in two primary contexts within engineering and mathematics:

1.  **As a Field of Science:** It refers to the study of **inference**—the systematic process of drawing meaningful conclusions from data that are subject to uncertainty or random variations. In this sense, it is the framework we use to move from observations to knowledge.
2.  **As a Mathematical Quantity:** A "statistic" is any function of observed data $x$ that is independent of the unknown parameter $\theta$. For example, the sample mean is a statistic because it is calculated directly from the data without needing to know the true underlying mean of the population.

#### **Statistical model**

A statistical model is a formal assumption about the population from which data is drawn. It is typically expressed as a **sampling probability density function (PDF)**, denoted as $p_{\theta}(x)$. 

Developing a robust model requires more than just observing data; it necessitates a deep understanding of the underlying **first principles** and causal relations of the system. It is critical to distinguish between mere correlation (two variables moving together) and causation (one variable influencing another), as only causal models provide reliable predictive power in control systems.

#### **Random sample**

A random sample is a set of $n$ representative data items selected from a statistical population. Mathematically, we represent this as:

$$X_i \sim p_{\theta}(x) \rightarrow \{X_1, \dots, X_n\}$$

Where:
*   $n$ is the **size of the sample**.
*   $\theta$ is the **parameter** of interest (which may be unknown and is what we aim to estimate).

In most standard estimation problems, we assume that $X_i$ are **i.i.d. random variables** (independent and identically distributed). This means each observation is collected under the same conditions and the outcome of one observation does not influence another.

#### **Estimate**

An **estimate** is a specific type of statistic used to infer the value of an unknown parameter (such as the population mean $\mu$ or variance $\sigma^2$). Because an estimate is a function of random data, the estimate itself is a random variable with its own distribution. To be considered "good" or "useful," an estimate should ideally possess the following three properties:

*   **Unbiased:** The expected value of the estimate is equal to the true parameter value. On average, the estimate is correct.
*   **Consistent:** As the sample size $n$ increases, the estimate converges in probability to the true parameter value. Essentially, more data leads to more certainty.
*   **Efficient:** Among all possible unbiased estimates, an efficient estimate has the minimum possible variance. It achieves the **Cramer-Rao lower bound**, meaning it extracts the maximum possible information from the available data.

![](_page_7_Picture_18.jpeg)

![](_page_7_Picture_19.jpeg)