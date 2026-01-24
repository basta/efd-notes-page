# Generators of (pseudo)random numbers (3)

In many control and estimation problems, we require random samples from a specific, often non-standard, probability distribution. While most software environments provide generators for uniform and normal distributions, we must employ specific mathematical techniques to generate samples for a **General Distribution**.

#### Transformation by Inverse of Cumulative Distribution Function (CDF)

The most fundamental method for generating a random variable $x$ with a desired probability density function (p.d.f.) $f(x)$ is the **Inverse Transform Sampling** method. This method relies on the cumulative distribution function $F(x) = \int_{-\infty}^x f(t) dt$.

The algorithm is as follows:
1.  Generate a sample $u$ from a standard uniform distribution, $u \sim U(0,1)$, where $u \in [0,1]$.
2.  Compute the desired sample by applying the inverse CDF: $x = F^{-1}(u)$.

### Proof:
To prove that $x = F^{-1}(u)$ follows the distribution $f(x)$, let $g(u) = F^{-1}(u)$. Consequently, the inverse mapping is $g^{-1}(x) = F(x)$. Using the rule for the transformation of random variables:

$$p_x(x) = p_u(F(x)) \left| \frac{d F(x)}{d x} \right|$$

Since $u \sim U(0,1)$, its density $p_u$ is equal to $1$ for all values in the range $[0,1]$. Furthermore, the derivative of the CDF $F(x)$ is by definition the p.d.f. $f(x)$. Thus:
$$p_x(x) = 1 \cdot f(x) = f(x)$$

#### Theorem: Transformation of a Random Variable

This general theorem allows us to determine the p.d.f. of a random variable $y$ that is a function of another random variable $x$.

Let $x$ be a random variable with p.d.f. $p_x(x)$, and let $y = g(x)$ be a monotonic function of $x$. The p.d.f. of $y$, denoted $p_y(y)$, is given by:

$$p_{y}(y) = p_{x}(g^{-1}(y)) \left| \frac{dg^{-1}(y)}{dy} \right|$$

**Proof:**
Consider the case where $g(x)$ is a strictly increasing function (a decreasing function would simply result in a sign change, which is handled by the absolute value in the final formula). We start with the Cumulative Distribution Function of $y$:

$$P_y(y) = \Pr\{Y \le y\} = \Pr\{g(X) \le y\}$$

Applying the inverse function $g^{-1}$ to both sides of the inequality:
$$P_y(y) = \Pr\{X \le g^{-1}(y)\} = P_x\left(g^{-1}(y)\right)$$

To find the probability density function $p_y(y)$, we take the derivative of the CDF with respect to $y$ using the chain rule:

$$p_{y}(y) = \frac{d P_{y}(y)}{dy} = \frac{d P_{x}(g^{-1}(y))}{dy} = p_{x}(g^{-1}(y)) \frac{dg^{-1}(y)}{dy}$$

This theorem is a cornerstone of estimation theory, particularly when propagating uncertainty through non-linear system dynamics or measurement equations.

![](_page_166_Picture_15.jpeg)

![](_page_166_Picture_16.jpeg)