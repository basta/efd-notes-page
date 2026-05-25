## Selecting the Learning Rate for Deep Neural Networks

The learning rate $\eta$ is arguably the single most important hyper‑parameter in training deep neural networks. It controls the step size taken in the direction of the negative gradient during stochastic gradient descent (SGD) and its variants. Choosing an appropriate learning rate – and a schedule for adapting it over time – is critical for achieving both rapid convergence and good generalisation. This section explains the role of the learning rate, the consequences of poor choices, and the practical strategies for selecting and scheduling it, drawing on the principles and techniques presented in the course slides and the broader deep learning literature.

### 1. The Role of the Learning Rate in SGD

Recall the standard SGD update rule for a parameter vector $\mathbf{W}$ at iteration $t$, given a mini‑batch gradient $\nabla J_{\mathcal{B}_t}(\mathbf{W}_t)$:

$$
\mathbf{W}_{t+1} = \mathbf{W}_t - \eta \, \nabla J_{\mathcal{B}_t}(\mathbf{W}_t).
$$

The learning rate $\eta$ scales the gradient to determine how far the parameters move in a single update. If the loss landscape were a perfect quadratic bowl, an optimal constant learning rate would exist that guarantees the fastest descent without oscillation. In reality, the loss surface of a deep network is highly non‑convex, with varying curvature across dimensions, saddle points, and sharp minima. The learning rate must therefore be chosen to balance two competing risks:

- **Too large a learning rate** causes the optimisation to take steps that overshoot minima, leading to divergence or wild oscillations. The loss may explode, and the network fails to learn.
- **Too small a learning rate** makes progress agonisingly slow. The optimisation may get trapped in poor local minima or saddle points, and training may require an impractical number of epochs.

The course slides highlight that the learning rate is a central hyper‑parameter of SGD, and that modern techniques such as batch normalisation and adaptive optimisers can reduce the sensitivity to its exact value, but careful tuning remains essential.

### 2. Consequences of Poor Learning Rate Selection

The slides do not enumerate these consequences explicitly, but they are implied by the discussion of vanishing gradients, training speed, and the need for tricks. In practice:

- **Divergence:** If $\eta$ is too high, the loss increases rapidly and the weights become NaN.
- **Oscillation:** A moderately high learning rate can cause the loss to fluctuate without decreasing, especially in narrow valleys of the loss surface.
- **Stagnation:** A very low learning rate leads to negligible weight updates; the loss decreases so slowly that training appears stuck.
- **Poor generalisation:** The learning rate also influences the flatness of the minima found. Large learning rates with a suitable schedule often converge to flatter minima that generalise better, while very small learning rates may settle into sharp minima that overfit.

### 3. Practical Strategies for Selecting the Initial Learning Rate

There is no universal formula for the perfect learning rate, but several empirical strategies are widely used.

#### 3.1 Learning Rate Range Test

A systematic method, popularised by Leslie Smith, is the **learning rate range test**. The idea is to run a short training (a few epochs) while increasing the learning rate linearly or exponentially from a very small value (e.g., $10^{-6}$) to a very large value (e.g., $1$ or $10$). The loss is recorded at each step. The resulting plot typically shows three regimes:

1. **Too small:** loss barely decreases.
2. **Just right:** loss decreases rapidly.
3. **Too large:** loss diverges or oscillates wildly.

The recommended initial learning rate is chosen from the region where the loss decreases fastest, often an order of magnitude below the value at which the loss starts to increase. This test provides a data‑driven starting point that is tailored to the specific architecture and dataset.

#### 3.2 Heuristics Based on Architecture and Batch Size

- **Default values:** For SGD with momentum, a learning rate of $0.01$ or $0.1$ is a common starting point for image classification tasks. For the ADAM optimiser, the default $\eta = 0.001$ works well in many cases, as noted in the slides (“Low sensitivity on learning rate setting”).
- **Linear scaling with batch size:** When increasing the mini‑batch size $m$, the gradient estimate becomes more accurate. To maintain the same effective step size in the parameter space, the learning rate should be scaled linearly: $\eta \propto m$. For example, if a learning rate of $0.1$ works for a batch size of $256$, a batch size of $1024$ might use $\eta = 0.4$. This principle is especially important for large‑batch training and is often combined with a learning rate warmup.

#### 3.3 Exploiting Batch Normalisation

The slides emphasise that **batch normalisation** (BatchNorm) dramatically reduces the sensitivity to the learning rate. By normalising activations to zero mean and unit variance, BatchNorm prevents the scale of weights from exploding or vanishing, allowing much higher learning rates. The slides state: “Small sensitivity to learning rate setting (can be higher, faster training 10 times fewer epochs needed).” Therefore, when BatchNorm is present, one can often start with a learning rate that is $5$–$10$ times larger than what would be used without it, accelerating convergence without instability.

#### 3.4 Adaptive Optimisers

The course material introduces **ADAM** (ADAptive Moment estimation) as an optimiser that “often improves over SGD (with momentum)” and has “low sensitivity on learning rate setting.” ADAM adapts the effective learning rate for each parameter individually based on estimates of the first and second moments of the gradients. This means that even a sub‑optimal global learning rate is partially compensated by the per‑parameter scaling. The recommended default $\eta = 0.001$ is a robust starting point for many problems. Other adaptive methods such as RMSprop and AdaGrad share this property.

### 4. Learning Rate Schedules

Using a constant learning rate throughout training is rarely optimal. As the optimisation approaches a minimum, smaller steps are needed to avoid overshooting and to settle into a good basin. The course slides mention that AlexNet was trained for $90$ cycles (epochs) through the training set, implying that some form of schedule was likely used. Modern practice employs a variety of **learning rate schedules** to decay $\eta$ over time.

#### 4.1 Step Decay

The learning rate is reduced by a constant factor $\gamma$ (e.g., $0.1$) every $T$ epochs:

$$
\eta_t = \eta_0 \cdot \gamma^{\lfloor t / T \rfloor}.
$$

For example, starting with $\eta_0 = 0.1$ and multiplying by $0.1$ every $30$ epochs. This is simple and effective, but the drop points must be chosen manually.

#### 4.2 Exponential Decay

The learning rate decays continuously by a factor per epoch:

$$
\eta_t = \eta_0 \cdot e^{-\lambda t},
$$

where $\lambda$ controls the decay rate. This provides a smoother reduction than step decay.

#### 4.3 Cosine Annealing

Introduced by Loshchilov and Hutter, cosine annealing smoothly decreases the learning rate following a half‑cosine curve from the initial value to a small final value over $T$ epochs:

$$
\eta_t = \eta_{\min} + \frac{1}{2}(\eta_0 - \eta_{\min})\left(1 + \cos\left(\frac{t}{T}\pi\right)\right).
$$

This schedule is popular because it avoids sudden drops and often yields better final performance. It can be combined with **warm restarts**, where the learning rate is periodically reset to a high value, encouraging the optimisation to escape local minima.

#### 4.4 Warmup

The slides do not explicitly discuss warmup, but it is a standard technique, especially when using large batch sizes or training transformers. During the first few epochs, the learning rate is linearly increased from a very small value (e.g., $10^{-6}$) to the target initial learning rate $\eta_0$. This prevents the network from making destructive updates before the gradient statistics stabilise. Warmup is particularly important when BatchNorm is used, because the running estimates of mean and variance need a few iterations to become reliable.

#### 4.5 Plateau‑Based Reduction

A common heuristic is to monitor the validation loss and reduce the learning rate by a factor (e.g., $0.5$ or $0.1$) when the loss stops improving for a pre‑defined number of epochs (“patience”). This is adaptive and does not require fixing the decay epochs in advance.

### 5. Interaction with Other Hyper‑Parameters and Techniques

The learning rate does not exist in isolation. Its optimal value is coupled with:

- **Momentum:** Higher momentum ($\mu \approx 0.9$–$0.99$) allows a slightly higher learning rate because momentum smooths the updates and dampens oscillations.
- **Weight decay:** The effective learning rate for weight decay is $\eta \lambda$. If $\eta$ is changed, the regularisation strength changes as well. Some optimisers (e.g., AdamW) decouple weight decay from the learning rate to avoid this interaction.
- **Batch size:** As noted, the learning rate should scale linearly with batch size to keep the noise level and effective step size consistent.
- **Batch normalisation:** Reduces sensitivity, enabling higher learning rates and faster training, as highlighted in the slides.
- **Adaptive optimisers:** ADAM and its variants adapt the per‑parameter learning rate, making the choice of global $\eta$ less critical but still important.

### 6. Summary of Recommendations

Based on the course material and current best practices, a systematic approach to selecting the learning rate is:

1. **Choose an optimiser.** If using SGD with momentum, start with $\eta = 0.01$ or $0.1$. If using ADAM, start with $\eta = 0.001$.
2. **Apply batch normalisation** if possible; it will make the network more forgiving of a sub‑optimal learning rate and allow a higher value.
3. **Perform a learning rate range test** to find a data‑specific initial value. Pick a rate where the loss decreases steeply.
4. **Use a warmup** if the batch size is large or if training is unstable in the first few iterations.
5. **Decay the learning rate** over time. A cosine annealing schedule or a step decay with a factor of $0.1$ at $50\%$ and $75\%$ of total epochs is a robust default.
6. **Monitor the training and validation loss curves.** If the loss oscillates or diverges, reduce $\eta$. If the loss decreases too slowly, increase $\eta$ (provided the network remains stable).
7. **Consider adaptive methods** (ADAM) when tuning resources are limited, as they are less sensitive to the exact learning rate.

The learning rate is not a set‑and‑forget parameter; it is a dynamic control that guides the optimisation through the complex loss landscape. Mastery of learning rate selection – through a combination of heuristics, schedules, and monitoring – is essential for training deep neural networks effectively, as emphasised throughout the course’s “general recipe” for deep learning.

---

### Self-Test

1. Batch normalisation is said to reduce sensitivity to the learning rate — why does normalising activations have this effect on the optimisation dynamics?
2. If you double the mini-batch size $m$, how should $\eta$ change and why? What breaks down if you simply keep $\eta$ constant?
3. Cosine annealing and step decay both reduce $\eta$ over time, but in different ways — in what training scenario would you prefer cosine annealing with warm restarts over plain step decay?
4. The learning rate range test finds the “sweet spot” by sweeping $\eta$ from very small to very large — when might this test give a misleading recommendation (i.e., when could the chosen rate still lead to poor training)?

### Answer Key

1. Batch normalisation normalises each layer's activations to zero mean and unit variance, which prevents the scale of weights from exploding or vanishing across layers. Because the effective curvature seen by each layer is stabilised, the optimiser is less likely to overshoot in high-curvature directions or stall in low-curvature ones, meaning a wider range of $\eta$ values produce stable, fast descent. The text notes this allows learning rates $5$–$10$ times larger than without BatchNorm, resulting in up to $10\times$ fewer epochs needed.

2. Doubling the mini-batch size $m$ halves the variance of the gradient estimate, making each gradient step a more accurate reflection of the true gradient. To maintain the same effective noise level and step size in parameter space, $\eta$ should also be doubled (the linear scaling rule $\eta \propto m$). If $\eta$ is kept constant, the updates become too conservative relative to the improved gradient signal, effectively slowing down learning — or conversely, if the batch size is very large, the implicit regularisation from gradient noise is lost without a corresponding learning rate increase to compensate.

3. Cosine annealing with warm restarts is preferable when you suspect the loss surface has multiple basins of attraction that a single monotone decay might miss. The periodic resets let the optimiser escape sharp or poor local minima and re-explore the landscape, which can yield flatter, better-generalising solutions. Plain step decay is simpler and adequate when the training regime is well-understood and the schedule boundaries can be fixed in advance, but it lacks the ability to escape local minima between drops.

4. The range test runs for only a few epochs with a continuously increasing $\eta$, so the chosen rate is identified under transient, non-stationary conditions — the network weights are far from any minimum and gradient statistics (e.g., ADAM's moment estimates or BatchNorm's running statistics) have not stabilised. The test can therefore recommend a rate that is too aggressive once training settles into a narrower loss basin, or it may be misleading when the architecture uses warm-up (so a high initial rate is inherently harmful) or when the dataset is very small and a short sweep cannot reliably distinguish good from overfit dynamics.