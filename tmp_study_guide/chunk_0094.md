# Generators of (pseudo)random numbers

In control theory and estimation, particularly when dealing with Monte Carlo simulations or stochastic filtering (like Particle Filters), the ability to generate random variables is fundamental. Since digital computers are deterministic, we generate **pseudorandom numbers**—sequences that appear random but are produced by a deterministic algorithm.

### Uniform distribution $u \sim U(0,1)$

The foundation of all random number generation is the uniform distribution on the interval $[0, 1]$. Most other distributions (Normal, Exponential, etc.) are derived by transforming a uniform source.

#### The Linear Congruential Method
One of the most common algorithms for generating pseudorandom numbers is the **congruence method**. This method relies on modular arithmetic to produce a sequence of integers that cycle through a very large range.

1.  **Select a Seed**: Choose an initial value $x_0$. In modern systems, this is often a 32-bit unsigned integer (`UINT32`).
2.  **Iterate**: Generate the next integer in the sequence using the linear equation:
    $$x_i = (a x_{i-1} + c) \mod M$$
    In the specific example provided (a common implementation):
    $$x_i = (69069 x_{i-1} + 1) \mod 2^{32}$$
    Here, $a=69069$ is the multiplier, $c=1$ is the increment, and $M=2^{32}$ is the modulus.
3.  **Normalize**: To obtain a value $u_i$ in the range $[0, 1]$, divide the integer by the modulus:
    $$u_i = 2^{-32}x_i$$

#### Verification of Randomness
To ensure a generator is suitable for estimation tasks, it must be tested for two primary qualities:
*   **Distribution**: Does the histogram of $u_i$ look flat across the interval $[0, 1]$?
*   **Independence**: Are subsequent samples uncorrelated? This is verified by checking the **covariance function**. For a truly random sequence, the covariance should be zero for all lags $k \neq 0$.

The following figures illustrate the testing of the Matlab `rand()` implementation, showing its distribution and the resulting covariance function to ensure there are no hidden periodicities or patterns.

<span style="display:block;text-align:center;">
![](_page_164_Figure_7.jpeg)
</span>

<span style="display:block;text-align:center;">
![](_page_164_Picture_9.jpeg)
</span>