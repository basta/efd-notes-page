# Introduction to Combinatorial Optimization — Worked Examples

> *This page collects worked examples mined from the lecture slides. Solutions are synthesised by DeepSeek from the slides' stated algorithms — verify against the originals before relying on them for an exam.*

### Time Complexity of Algorithms Table

> *Solution synthesised by DeepSeek from the lecture's stated algorithm — verify against the slides before relying on it for an exam.*

**Problem.**  
The table shows execution times for six different time‑complexity functions on a hypothetical computer. Several entries are missing, especially for the factorial function $n!$ when $n \ge 40$. Using the given value for $n=30$, estimate the missing execution times for $n!$ and interpret what the numbers tell us about the tractability of combinatorial problems.

**Approach.**  
The execution time for $n!$ grows proportionally to the factorial itself. If we know the time $T(30)$ for $n=30$, then for any larger $n$

$$
T(n) = T(30) \cdot \frac{n!}{30!}.
$$

We compute the ratio $\frac{n!}{30!}$ exactly for small $n$ and use Stirling’s approximation for larger $n$ to obtain the order of magnitude. The results are expressed in years using scientific notation.

**Solution.**

1. **Base value.**  
   From the table, $T(30) = 8 \times 10^{15}$ years.

2. **Compute $T(40)$.**  
   $\displaystyle \frac{40!}{30!} = 31 \times 32 \times \cdots \times 40$.  
   Multiplying step‑by‑step:

   $$31 \cdot 32 = 992$$
   $$992 \cdot 33 = 32\,736$$
   $$32\,736 \cdot 34 = 1\,113\,024$$
   $$1\,113\,024 \cdot 35 = 38\,955\,840$$
   $$38\,955\,840 \cdot 36 = 1\,402\,410\,240$$
   $$1\,402\,410\,240 \cdot 37 = 51\,889\,178\,880$$
   $$51\,889\,178\,880 \cdot 38 = 1\,971\,788\,797\,440$$
   $$1\,971\,788\,797\,440 \cdot 39 = 76\,899\,763\,100\,160$$
   $$76\,899\,763\,100\,160 \cdot 40 = 3\,075\,990\,524\,006\,400 \approx 3.076 \times 10^{15}$$

   Hence  

   $$T(40) = 8 \times 10^{15} \times 3.076 \times 10^{15} \approx 2.46 \times 10^{31}\ \text{years}.$$

3. **Compute $T(50)$.**  
   $\displaystyle \frac{50!}{30!} = \frac{40!}{30!} \times \frac{50!}{40!}$.  
   $\frac{50!}{40!} = 41 \times 42 \times \cdots \times 50$:

   $$41 \cdot 42 = 1\,722$$
   $$1\,722 \cdot 43 = 74\,046$$
   $$74\,046 \cdot 44 = 3\,258\,024$$
   $$3\,258\,024 \cdot 45 = 146\,611\,080$$
   $$146\,611\,080 \cdot 46 = 6\,744\,109\,680$$
   $$6\,744\,109\,680 \cdot 47 = 316\,973\,154\,960$$
   $$316\,973\,154\,960 \cdot 48 = 15\,214\,711\,438\,080$$
   $$15\,214\,711\,438\,080 \cdot 49 = 745\,520\,860\,465\,920$$
   $$745\,520\,860\,465\,920 \cdot 50 = 3.7276 \times 10^{16}$$

   Therefore  

   $$\frac{50!}{30!} \approx 3.076 \times 10^{15} \times 3.7276 \times 10^{16} \approx 1.146 \times 10^{32},$$
   $$T(50) = 8 \times 10^{15} \times 1.146 \times 10^{32} \approx 9.17 \times 10^{47}\ \text{years}.$$

4. **Compute $T(60)$.**  
   $\frac{60!}{30!} = \frac{50!}{30!} \times \frac{60!}{50!}$.  
   $\frac{60!}{50!} = 51 \times 52 \times \cdots \times 60$:

   $$51 \cdot 52 = 2\,652$$
   $$2\,652 \cdot 53 = 140\,556$$
   $$140\,556 \cdot 54 = 7\,590\,024$$
   $$7\,590\,024 \cdot 55 = 417\,451\,320$$
   $$417\,451\,320 \cdot 56 = 23\,377\,273\,920$$
   $$23\,377\,273\,920 \cdot 57 = 1.3325 \times 10^{12}$$
   $$1.3325 \times 10^{12} \cdot 58 = 7.7285 \times 10^{13}$$
   $$7.7285 \times 10^{13} \cdot 59 = 4.5598 \times 10^{15}$$
   $$4.5598 \times 10^{15} \cdot 60 = 2.7359 \times 10^{17}$$

   Thus  

   $$\frac{60!}{30!} \approx 1.146 \times 10^{32} \times 2.7359 \times 10^{17} \approx 3.135 \times 10^{49},$$
   $$T(60) = 8 \times 10^{15} \times 3.135 \times 10^{49} \approx 2.51 \times 10^{65}\ \text{years}.$$

5. **Compute $T(80)$ using order‑of‑magnitude estimation.**  
   $\frac{80!}{60!}$ is the product of 20 numbers around 70, roughly $70^{20}$.  
   $70^{20} = 7^{20} \times 10^{20}$.  
   $7^{10} = 282\,475\,249 \approx 2.825 \times 10^{8}$, so $7^{20} \approx (2.825 \times 10^{8})^{2} \approx 7.98 \times 10^{16}$.  
   Hence $\frac{80!}{60!} \approx 8 \times 10^{16} \times 10^{20} = 8 \times 10^{36}$.  

   $$\frac{80!}{30!} \approx 3.135 \times 10^{49} \times 8 \times 10^{36} \approx 2.5 \times 10^{86},$$
   $$T(80) \approx 8 \times 10^{15} \times 2.5 \times 10^{86} \approx 2.0 \times 10^{102}\ \text{years}.$$

6. **Compute $T(100)$ similarly.**  
   $\frac{100!}{80!}$ is the product of 20 numbers around 90, roughly $90^{20} = 9^{20} \times 10^{20}$.  
   $9^{10} = 3\,486\,784\,401 \approx 3.487 \times 10^{9}$, so $9^{20} \approx (3.487 \times 10^{9})^{2} \approx 1.216 \times 10^{19}$.  
   Thus $\frac{100!}{80!} \approx 1.2 \times 10^{19} \times 10^{20} = 1.2 \times 10^{39}$.  

   $$\frac{100!}{30!} \approx 2.5 \times 10^{86} \times 1.2 \times 10^{39} \approx 3.0 \times 10^{125},$$
   $$T(100) \approx 8 \times 10^{15} \times 3.0 \times 10^{125} \approx 2.4 \times 10^{141}\ \text{years}.$$

7. **Use Stirling’s approximation for $n=200, 500, 1000$.**  
   Stirling: $\log_{10}(n!) \approx n \log_{10}(n/e) + \tfrac{1}{2}\log_{10}(2\pi n)$.  
   For $n=30$, $\log_{10}(30!) \approx 32.4$ (actual $30! \approx 2.65 \times 10^{32}$).  

   - **$n=200$:**  
     $\log_{10}(200!) \approx 200 \log_{10}(200/e) + 0.5\log_{10}(400\pi) \approx 200 \times 1.867 + 1.55 \approx 374.95$.  
     $\log_{10}(200!/30!) \approx 374.95 - 32.4 = 342.55$, so $200!/30! \approx 10^{342.55} \approx 3.55 \times 10^{342}$.  
     $T(200) \approx 8 \times 10^{15} \times 3.55 \times 10^{342} \approx 2.8 \times 10^{358}$ years.

   - **$n=500$:**  
     $\log_{10}(500!) \approx 500 \log_{10}(500/e) + 0.5\log_{10}(1000\pi) \approx 500 \times 2.2647 + 1.75 \approx 1134.1$.  
     $\log_{10}(500!/30!) \approx 1134.1 - 32.4 = 1101.7$, so $500!/30! \approx 10^{1101.7} \approx 5.0 \times 10^{1101}$.  
     $T(500) \approx 8 \times 10^{15} \times 5.0 \times 10^{1101} \approx 4.0 \times 10^{1117}$ years.

   - **$n=1000$:**  
     $\log_{10}(1000!) \approx 1000 \log_{10}(1000/e) + 0.5\log_{10}(2000\pi) \approx 1000 \times 2.5657 + 1.9 \approx 2567.6$.  
     $\log_{10}(1000!/30!) \approx 2567.6 - 32.4 = 2535.2$, so $1000!/30! \approx 10^{2535.2} \approx 1.58 \times 10^{2535}$.  
     $T(1000) \approx 8 \times 10^{15} \times 1.58 \times 10^{2535} \approx 1.26 \times 10^{2551}$ years.

**Answer.**  
The missing execution times for $n!$ are (in years):

| $n$ | $T(n)$ for $n!$ |
|-----|-----------------|
| 40  | $2.5 \times 10^{31}$ |
| 50  | $9.2 \times 10^{47}$ |
| 60  | $2.5 \times 10^{65}$ |
| 80  | $2.0 \times 10^{102}$ |
| 100 | $2.4 \times 10^{141}$ |
| 200 | $2.8 \times 10^{358}$ |
| 500 | $4.0 \times 10^{1117}$ |
| 1000| $1.3 \times 10^{2551}$ |

These numbers are so enormous that they have no physical meaning (the age of the universe is about $1.4 \times 10^{10}$ years). The table vividly illustrates why algorithms with factorial time complexity are utterly impractical for all but the smallest instances.

**Pitfalls / insight.**  
- The table is not just a collection of numbers; it demonstrates the **combinatorial explosion** that makes exhaustive search infeasible. Even for $n=30$, $n!$ already requires $8 \times 10^{15}$ years – far longer than the universe has existed.  
- When filling missing entries, always use the **multiplicative property** of the factorial: $T(n) = T(k) \cdot \frac{n!}{k!}$. Avoid linear extrapolation, which would give absurdly small results.  
- For large $n$, Stirling’s approximation gives the correct order of magnitude quickly. The exact integer product is unnecessary once the exponent exceeds a few dozen.  
- The same reasoning applies to other exponential complexities like $2^n$; the table shows that even $2^n$ becomes intractable around $n=100$ ($4 \times 10^{13}$ years). This is why combinatorial optimization must rely on smarter algorithms (e.g., dynamic programming, branch‑and‑bound, heuristics) rather than brute force.
