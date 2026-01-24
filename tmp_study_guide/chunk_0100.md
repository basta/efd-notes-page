# Kalman filter implementation summary (2)

In the context of Sequential Monte Carlo methods (such as Particle Filters), we represent continuous probability density functions (p.d.f.) using a finite set of weighted samples, or "particles." This approach allows us to handle non-linearities and non-Gaussian noise that traditional Kalman Filters cannot accommodate.

#### P.d.f. representation by samples

The core idea is to approximate the true density function using a sum of Dirac delta functions centered at specific sample points.

**1. Data-update: Prior Representation**
Before incorporating the new measurement at time $t$, the prior p.d.f. (the prediction from the previous time step) is represented by a set of $N$ samples $x^{(i)}(t)$ with associated weights $w^{(i)}(t|t-1)$:

$$r_N\left(x(t)\,\Big|\,\mathcal{D}^{t-1}\right) = \sum_{i=1}^N w^{(i)}(t|t-1)\,\,\delta\left(x(t)-x^{(i)}(t)\right)$$

In a standard bootstrap filter or importance sampling scheme, we often start the update step with equal prior weights, assuming the samples were drawn directly from the transition density:

$$w^{(i)}(t|t-1)=\frac{1}{N}$$

**2. Data-update: Posterior Representation**
Once the measurement $y(t)$ becomes available, we update the importance of each sample. The posterior p.d.f. is represented by the same set of samples, but with updated weights $w^{(i)}(t|t)$:

$$r_N(x(t) \mid \mathcal{D}^t) = \sum_{i=1}^N w^{(i)}(t|t) \delta(x(t) - x^{(i)}(t))$$

The posterior weights are calculated based on the likelihood of the observation $y(t)$ given each state sample. To ensure the result remains a valid probability distribution, these weights must be normalized so that their sum equals one:

$$w^{(i)}(t|t) = \frac{p(y(t)|x^{(i)}(t|t-1), u(t))}{\sum_{j=1}^{N} p(y(t)|x^{(j)}(t|t-1), u(t))}$$

This weighting process effectively "filters" the samples: particles that are consistent with the new measurement receive higher weights, while those that are inconsistent are marginalized.

![](_page_176_Figure_10.jpeg)

![](_page_176_Picture_11.jpeg)

![](_page_176_Picture_12.jpeg)