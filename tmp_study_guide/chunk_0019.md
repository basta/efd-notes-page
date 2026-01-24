# <span id="page-34-0"></span>**3. Bayesian method**

![](_page_34_Picture_1.jpeg)

In the previous sections, we explored Maximum Likelihood (ML) estimation, which treats the parameter $\theta$ as a fixed but unknown constant. We now shift our perspective to **Bayesian Statistics**, a framework where parameters are treated as random variables. This allows us to quantify our uncertainty about the world using probability distributions.

### Classical vs. Bayesian Statistics

The distinction between these two schools of thought lies in the interpretation of probability and the nature of the parameters being estimated.

#### **Classical (Frequentist) Approach**
*   **Definition of Probability:** Probability is viewed as the long-run limit of the relative frequency of an event occurring over many repeated trials.
*   **Nature of Parameters:** Parameters are fixed, objective quantities. The "quality" of an estimate is judged by how it performs over an infinite data set (e.g., unbiasedness, consistency).
*   **Observer Independence:** The probability is an inherent property of the system, independent of the observer's prior knowledge.

#### **Bayesian Approach**
*   **Definition of Probability:** Probability density functions (p.d.f.) are used to describe two distinct concepts:
    *   **Randomness:** The "objective" variability found in a family of independent and identically distributed (i.i.d.) samples.
    *   **Uncertainty:** The "subjective" degree of belief regarding a single parameter's value.
*   **Rational Behavior:** Under uncertainty, the Bayesian framework posits that uncertainty follows the same mathematical structure as probability. It provides a formal tool for the **accumulation of information** as new data arrives.
*   **Finite Data Sets:** Unlike frequentist methods that often rely on asymptotic (infinite data) properties, Bayesian analysis is valid for any sample size, including very small data sets.

---

### Bayesian Inference

In Bayesian inference, we do not "estimate" a parameter in the sense of picking a single point; instead, we **calculate the posterior distribution**. This distribution represents our updated state of knowledge after observing data.

#### Elements of Bayes' Formula
The core of this method is the Bayes' formula, which relates the posterior probability to the likelihood and the prior:

$$p(\theta|y) = \frac{p(y|\theta) p(\theta)}{p(y)} = \frac{p(y|\theta) p(\theta)}{\int p(y|\theta) p(\theta) d\theta}$$

1.  **The Model (Likelihood):** $p(y|\theta)$ explains the observations $y_i$ based on the unknown parameter $\theta$. When viewed as a function of $\theta$ for a fixed $y$, it is called the **Likelihood** $l(\theta|y)$.
2.  **The Prior:** $p(\theta)$ is the subjective p.d.f. representing the statistician's knowledge before seeing the data.
3.  **The Posterior:** $p(\theta|y)$ is the updated knowledge.

#### Recursive Information Update
One of the most powerful features of Bayesian inference is its naturally recursive structure. As we receive a sequence of observations $y_1, y_2, \dots, y_n$, our knowledge is updated step-by-step:

$$p(\theta|y_1) \propto l(\theta|y_1)p(\theta)$$
$$p(\theta|y_1, y_2) \propto l(\theta|y_2)p(\theta|y_1)$$
$$\vdots$$
$$p(\theta|y_1, y_2, \dots, y_n) \propto l(\theta|y_n)p(\theta|y_1, y_2, \dots, y_{n-1})$$

**Key Conclusions:**
*   The **posterior p.d.f.** is always proportional to the **prior p.d.f.** multiplied by the **likelihood**.
*   The likelihood $l(\theta|y_i)$ captures **all information** about $\theta$ contained within the specific data point $y_i$.
*   The resulting p.d.f. effectively bridges the gap between the inherent randomness of observations and the subjective uncertainty of the parameter.

![](_page_36_Picture_13.jpeg)

![](_page_36_Picture_14.jpeg)