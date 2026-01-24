# Numerical implementation of bayesian estimation algorithms (6)

### **Dyadic reduction algorithm**

The dyadic reduction algorithm is a fundamental numerical tool used to maintain the triangular structure of factorized matrices during covariance updates. In Bayesian estimation, we often represent the covariance matrix $P$ in its $LD L^T$ form to ensure numerical stability and positive definiteness.

*   **Input:** A factorized covariance matrix $R = MDM^T$.
*   **Objective:** If $M$ is an extended monic lower triangular matrix (e.g., resulting from a rank-1 update or data update), we need to recover the standard triangular form while preserving the equality.
*   **Core Concept:** The algorithm operates on the sum of two dyads. Let $m_i$ and $m_j$ be monic vectors (vectors where the first non-zero element is 1).

Consider the sum of two dyads:
$$Q_{i,j} = m_i d_i m_i^T + m_j d_j m_j^T$$

The structure of the vectors is defined as:
$$m_i^T = [0, \dots, 0, 1, m_{i,i+1}, \dots, m_{i,n}]$$
$$m_j^T = [0, \dots, 0, m_{j,i}, m_{j,i+1}, \dots, m_{j,n}]$$

Note that $m_j$ has a non-zero element $m_{j,i}$ at the $i$-th position, which violates the strict lower triangular structure if we consider $m_j$ as a column of a triangular matrix.

#### **The Algorithm Steps**
The goal is to transform these into new dyads $\tilde{m}_i$ and $\tilde{m}_j$ such that the $i$-th element of the second vector becomes zero ($\tilde{m}_{j,i} = 0$), effectively "triangularizing" the pair:

$$Q_{i,j} = \tilde{m}_i \tilde{d}_i \tilde{m}_i^\mathsf{T} + \tilde{m}_j \tilde{d}_j \tilde{m}_j^\mathsf{T}$$

The updated vectors maintain the following structure:
$$\tilde{m}_{i}^{T} = [0, \dots, 0, 1, \tilde{m}_{i,i+1}, \dots, \tilde{m}_{i,n}]$$
$$\tilde{m}_{j}^{T} = [0, \dots, 0, 0, \tilde{m}_{j,i+1}, \dots, \tilde{m}_{j,n}]$$

The transformation parameters are calculated as follows:

1.  **Update the first diagonal element:**
    $$\tilde{d}_{i} = d_{i} + m_{j,i}^{2} d_{j}$$
2.  **Update the second diagonal element:**
    $$\tilde{d}_{j} = (d_{j} \cdot d_{i}) / \tilde{d}_{i}$$
3.  **Calculate the weight factor $\mu$:**
    $$\mu = (d_{j} \cdot m_{j,i}) / \tilde{d}_{i}$$
4.  **Update the vectors:**
    $$\tilde{m}_{j} = m_{j} - m_{j,i} m_{i}$$
    $$\tilde{m}_{i} = m_{i} + \mu \tilde{m}_{j}$$

This sequence of operations allows for the recursive update of the $L$ and $D$ factors. By applying this dyadic reduction systematically across the rows and columns of the factorized matrix, we can perform complex updates (like adding a new observation or incorporating process noise) while keeping the matrix in a computationally efficient and stable triangular form.

![](_page_95_Picture_11.jpeg)

![](_page_95_Picture_12.jpeg)