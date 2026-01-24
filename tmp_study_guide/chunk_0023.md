# Parameters of normal distribution (3)

In the simultaneous estimation of the mean $\mu$ and standard deviation $\sigma$, the joint posterior probability density function (p.d.f.) captures the total uncertainty regarding both parameters after observing the data $y$.

### **The Joint Posterior P.D.F.**

By combining the likelihood function with the non-informative prior $p(\mu, \sigma) \propto \sigma^{-1}$, we arrive at the joint posterior distribution:

$$p(\mu, \sigma | y) = \left(\frac{n}{2\pi}\right)^{1/2} \frac{2}{\Gamma(\nu/2)} \left(\frac{\nu s^2}{2}\right)^{\nu/2} \sigma^{-(n+1)} \exp\left(-\frac{(\mu - \overline{y})^2}{2\sigma^2/n} - \frac{\nu s^2}{2\sigma^2}\right)$$

To ensure this is a valid p.d.f., it must integrate to 1. We can verify the normalization constants using the following standard integrals:
1.  **For the scale parameter ($\sigma$):** $\int_{0}^{\infty} x^{-(\nu+1)} e^{-a/x^{2}} dx = \frac{1}{2} a^{-\nu/2} \Gamma(\nu/2)$
2.  **For the location parameter ($\mu$):** $\int_{-\infty}^{\infty} e^{-\frac{1}{2\sigma^{2}}(x-\mu)^{2}} dx = \sqrt{2\pi}\sigma$

### **Factorization of the Posterior**

A powerful feature of Bayesian inference is the ability to decompose complex joint distributions into simpler components. The joint posterior can be factorized using the product rule:
$$p(\mu, \sigma | y) = p(\mu | \sigma, y) p(\sigma | y)$$

#### **1. Conditional p.d.f. for $\mu$**
If we assume the standard deviation $\sigma$ is known (or fixed), the distribution of the mean $\mu$ is Gaussian. It is centered at the sample average $\overline{y}$ with a variance scaled by the number of observations $n$:
$$p(\mu | \sigma, y) = (2\pi\sigma^2/n)^{-1/2} \exp\left(-\frac{(\mu - \overline{y})^2}{2\sigma^2/n}\right) = \mathcal{N}\left(\overline{y}, \frac{\sigma^2}{n}\right)$$

#### **2. Marginal p.d.f. for $\sigma$**
By integrating the joint p.d.f. over all possible values of $\mu$, we obtain the marginal distribution for $\sigma$. This represents our knowledge of the noise/scale parameter regardless of the specific value of the mean:
$$p(\sigma|y) = \frac{2}{\Gamma(\nu/2)} \left(\frac{\nu s^2}{2}\right)^{\nu/2} \sigma^{-(\nu+1)} \exp\left(-\frac{\nu s^2}{2\sigma^2}\right)$$
This result is related to the **Scaled Inverse Chi-Squared distribution**, specifically $\chi_{\nu}^2 \left(\frac{\nu s^2}{\sigma^2}\right)$. An important property of this distribution is that the expected value of the variance, given the data, is simply the sample variance: $E[\sigma^2 | y] = s^2$.

![](_page_43_Picture_11.jpeg)