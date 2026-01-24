# **Estimation, Filtering, and Detection**

### **Vladimír Havlena**
**vladimir.havlena@cvut.cz**

*EFD Lecture Notes, September 2024*

Welcome to the study guide for **Estimation, Filtering, and Detection (EFD)**. This course is designed to provide a rigorous mathematical foundation for extracting meaningful information from uncertain data. In the realm of control theory and signal processing, we rarely have direct access to the internal variables of a system. Instead, we must rely on noisy measurements and mathematical models to infer the "truth."

This guide explores the methodologies used to estimate hidden parameters, filter noise from dynamic states, and detect structural changes or faults within a system. We will move from classical statistical foundations to the unifying framework of Bayesian inference, eventually covering advanced topics like Gaussian Processes and Monte Carlo methods.

---

## Outline

The following sections form the core of our study. Each chapter builds upon the previous one, transitioning from static estimation to dynamic state tracking and complex non-linear approximations.

1.  **[About this course](#page-2-0)**  
    An introduction to the course philosophy, prerequisites, and the distinction between system identification (parameters) and state estimation (states).
    
2.  **[Statistics, estimation methods](#page-6-0)**  
    A review of the statistical bedrock required for estimation, including probability distributions, moments, and the properties of estimators such as bias, consistency, and efficiency.

3.  **[Bayesian method](#page-34-0)**  
    The conceptual heart of the course. We treat unknown quantities as random variables and use Bayes' Rule to update our beliefs based on new evidence, moving from prior to posterior distributions.

4.  **[Parameter estimation](#page-47-0)**  
    Focuses on identifying the constant or slowly varying coefficients of a system (e.g., in ARX or ARMAX models). We will cover Least Squares, Maximum Likelihood, and recursive identification techniques.

5.  **[Kalman filter](#page-104-0)**  
    The optimal recursive estimator for the state of a linear dynamic system subjected to Gaussian noise. This section covers the derivation, implementation, and various extensions of the Kalman Filter.

6.  **[Change detection](#page-131-0)**  
    Techniques for monitoring systems in real-time to identify abrupt changes in behavior, such as sensor failures, actuator faults, or structural shifts in the underlying process.

7.  **[Monte Carlo implementation of Bayesian methods](#page-158-0)**  
    When systems are highly non-linear or non-Gaussian, analytical solutions often fail. Here we explore numerical methods, including Particle Filtering, to approximate the Bayesian posterior.

8.  **[Gaussian process regression](#page-181-0)**  
    A non-parametric approach to regression and estimation. Instead of assuming a fixed functional form, we define a prior over functions, allowing for flexible and powerful modeling of complex data patterns.