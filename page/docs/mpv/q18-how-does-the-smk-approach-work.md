## Selective Match Kernel (SMK)

The Selective Match Kernel (SMK) is a local‑feature‑based image similarity measure that extends the Bag‑of‑Words (BoW) model by replacing the binary, word‑level vote with a **fine‑grained, non‑linear function of descriptor residuals**. It belongs to the family of match kernels that compare sets of local features directly, but it retains the inverted‑file compatibility of BoW by restricting comparisons to features assigned to the same visual word. This section explains the mechanics of SMK, how it builds upon BoW, its key differences, and the resulting trade‑offs in memory, speed, and retrieval performance.

### 1. How SMK Works

Let an image be represented by a set of local descriptors $\mathcal{X} = \{\mathbf{x}_1, \dots, \mathbf{x}_N\}$, each assigned to a visual word $q(\mathbf{x})$ from a codebook of size $K$. The residual vector of a descriptor is $\mathbf{r}(\mathbf{x}) = \mathbf{x} - \mathbf{c}_{q(\mathbf{x})}$, where $\mathbf{c}_k$ is the centroid of the $k$-th visual word.

The SMK similarity between two images with descriptor sets $\mathcal{X}$ and $\mathcal{Y}$ is defined as a sum over all pairs of descriptors that share the same visual word, weighted by a **local similarity function** $f$:

$$
s_{\text{SMK}}(\mathcal{X}, \mathcal{Y}) = \sum_{k=1}^{K} \sum_{\substack{\mathbf{x} \in \mathcal{X}_k \\ \mathbf{y} \in \mathcal{Y}_k}} f\!\left( \mathbf{r}(\mathbf{x})^\top \mathbf{r}(\mathbf{y}) \right),
$$

where $\mathcal{X}_k$ and $\mathcal{Y}_k$ are the subsets of descriptors assigned to word $k$. The function $f$ is chosen to be **non‑linear and selective**, typically a power‑law with sign preservation:

$$
f(u) = \operatorname{sign}(u) \, |u|^\alpha, \quad \alpha > 1.
$$

Setting $\alpha = 1$ recovers a linear sum of residual dot products, which is equivalent to the VLAD voting interpretation (but without aggregation into a global vector). Choosing $\alpha > 1$ (e.g., $\alpha = 2$ or $3$) makes the kernel **selective**: weak matches (small $u$) are strongly down‑weighted, while strong matches are emphasised. This selectivity suppresses the influence of noisy or generic feature correspondences and sharpens the similarity score.

Because the sum is restricted to descriptors that fall into the same visual word, SMK can be computed efficiently using an **inverted file**. The posting list for word $k$ stores, for each database image, the list of residual vectors (or the original descriptors) of all its features assigned to that word. At query time, for each visual word present in the query, the dot products between the query residuals and all database residuals in that list are computed, passed through $f$, and accumulated into per‑image scores. This is a voting process: each pair of matching visual words contributes a vote $f(\mathbf{r}_q^\top \mathbf{r}_{db})$.

### 2. How SMK Extends the BoW Approach

BoW represents an image by a histogram of visual word counts. The similarity between two images is the dot product of their idf‑weighted histograms, which can be interpreted as a voting process where each co‑occurring visual word contributes a vote of $1$ (or $\text{idf}^2$). SMK extends this in two fundamental ways:

1. **Fine‑grained votes.** Instead of a binary “same word / different word” decision, SMK uses the dot product of the residual vectors to measure how similar two descriptors are *within* the same cluster. This captures first‑order information about the descriptor distribution, much like VLAD, but without aggregating into a global vector.

2. **Non‑linear selectivity.** The function $f$ applies a non‑linearity that amplifies strong matches and suppresses weak ones. In BoW, every co‑occurrence is treated equally (up to idf). In SMK, a pair of nearly identical descriptors contributes a large vote, while a pair of barely matching descriptors (small residual correlation) contributes almost nothing. This makes the kernel far more discriminative.

Thus, SMK can be seen as a **selective, residual‑aware BoW**: it retains the inverted‑file structure and the hard assignment of BoW, but enriches the voting with descriptor‑level similarity and a non‑linear gating function.

### 3. Differences from BoW

| Aspect | BoW | SMK |
|--------|-----|-----|
| **Vote type** | Binary (1 if same word, else 0) or idf‑weighted | Continuous, non‑linear function of residual dot product $f(\mathbf{r}_q^\top \mathbf{r}_{db})$ |
| **Information used** | 0‑order statistics (counts) | 1‑order statistics (residuals) + non‑linear selectivity |
| **Global descriptor** | Yes – histogram vector; similarity is a dot product | No – the kernel cannot be expressed as an inner product of global vectors (due to non‑linear $f$) |
| **Codebook size** | Very large ($10^5$–$10^6$) for instance search | Large (e.g., $65$k) – smaller than BoW’s extreme sizes but still large |
| **Index structure** | Inverted file with (image‑id, tf) | Inverted file with (image‑id, residual vectors) |
| **Query time** | Fast: add a scalar per posting | Slower: compute dot products and apply $f$ for each posting |
| **Memory** | Low: one integer (tf) per posting | High: must store a $d$‑dimensional residual per posting |
| **Tentative correspondences** | Yes (word‑level) | Yes (word‑level, but with similarity scores) |
| **Performance** | Good; limited by hard quantisation | Better than BoW; approaches VLAD/FV quality while keeping inverted‑file compatibility |

### 4. Advantages, Drawbacks, Memory, Speed, and Performance

#### Advantages
- **Higher discriminative power than BoW.** By using residual similarities and a selective non‑linearity, SMK significantly outperforms BoW in instance‑level retrieval, especially when fine‑grained distinctions are needed.
- **Inverted‑file compatibility.** Unlike VLAD, which produces a dense global descriptor and requires approximate nearest neighbour search, SMK works directly with an inverted index. This makes it suitable for large‑scale retrieval where inverted files are already deployed.
- **Provides tentative correspondences.** Because SMK operates at the visual‑word level, it naturally yields a set of matching feature pairs (with similarity scores), which can be used for subsequent spatial verification – a crucial step in many retrieval pipelines.
- **Tunable selectivity.** The exponent $\alpha$ controls the sharpness of the kernel; it can be adjusted to the task or dataset.

#### Drawbacks
- **No global descriptor.** SMK is a pure voting kernel; it cannot be reduced to a single vector per image. This precludes the use of efficient ANN libraries (e.g., FAISS) that rely on vector‑space representations. Retrieval must proceed via the inverted file and pairwise accumulation.
- **Higher memory than BoW.** Each posting must store the residual vector (or the original descriptor) to compute dot products. For $d = 128$ and a dataset with $F_{\text{total}}$ features, the memory is roughly $F_{\text{total}} \times (128 \times 4 + \text{id})$ bytes, compared to BoW’s $F_{\text{total}} \times (\text{tf} + \text{id})$ bytes. This can be an order of magnitude larger.
- **Slower query time than BoW.** For each candidate in a posting list, SMK computes a dot product and applies $f$, whereas BoW simply adds a pre‑computed weight. The cost is proportional to the total number of feature pairs that share a visual word, which can be substantial for common words.
- **Codebook size trade‑off.** SMK typically uses a large but not extreme codebook (e.g., $65$k). A very large codebook ($10^6$) would make the posting lists very short, reducing the number of pairwise comparisons, but the memory overhead of storing residuals for every feature remains. The codebook size must balance selectivity and memory.

#### Memory
SMK memory is dominated by the inverted file that stores, for each visual word, a list of (image‑id, residual vector) entries. The total number of entries equals the total number of local features in the database, $F_{\text{total}}$. Each entry requires:
- Image identifier (4 bytes)
- Residual vector: $d$ floats (e.g., $128 \times 4 = 512$ bytes)

Thus $\text{Memory}_{\text{SMK}} \approx F_{\text{total}} \times (512 + 4)$ bytes, plus the index overhead. This is significantly larger than BoW’s memory (which stores only a term frequency per posting, ~2–4 bytes). For a dataset with $10^9$ features, SMK would require hundreds of gigabytes, whereas BoW might fit in tens of gigabytes.

#### Speed
Query time is proportional to the sum, over all query visual words, of the length of each posting list multiplied by the cost of a dot product and $f$ evaluation. In BoW, the cost per posting is a single addition. SMK is therefore slower, but still sub‑linear in database size because only the posting lists of the query’s words are accessed. The use of a large codebook keeps posting lists short, mitigating the cost. In practice, SMK is feasible for datasets up to a few million images, but for web‑scale collections the speed and memory penalties may be prohibitive.

#### Performance
SMK consistently outperforms BoW in retrieval benchmarks. By leveraging residual information and non‑linear selectivity, it closes a substantial part of the gap between BoW and the more powerful but aggregation‑based methods like VLAD and Fisher Vectors. It is particularly attractive when inverted‑file infrastructure is already in place and spatial verification is required, because it delivers higher quality tentative correspondences than BoW.

### 5. Summary

The Selective Match Kernel extends BoW by replacing binary visual‑word votes with a **non‑linear function of residual dot products**. It retains the inverted‑file indexing of BoW, making it suitable for large‑scale retrieval, while achieving significantly better accuracy. The price is higher memory (storing residuals per feature) and slower query time (dot products instead of scalar additions). SMK occupies a middle ground: it offers the discriminative power of residual‑based methods without sacrificing the inverted‑file compatibility and the ability to produce tentative correspondences for spatial verification.

---

### Self-Test

1. Why does setting $\alpha > 1$ in $f(u) = \operatorname{sign}(u)|u|^\alpha$ improve retrieval over a linear kernel ($\alpha = 1$), and in what scenario might an excessively large $\alpha$ hurt performance?
2. SMK retains inverted-file compatibility but cannot be expressed as an inner product of global per-image vectors — why does this architectural choice force a different retrieval strategy compared to VLAD, and what concrete capability does it preserve that VLAD loses?
3. If you double the codebook size $K$ from 65k to 130k, how would posting list lengths, per-query dot-product cost, and retrieval accuracy each be expected to change?
4. Consider a database where many images share a highly distinctive landmark but are photographed under very different lighting conditions, causing descriptor residuals to differ substantially within the same visual word. Would SMK handle this better or worse than BoW, and why?

### Answer Key

1. With $\alpha > 1$, the power-law $f(u) = \operatorname{sign}(u)|u|^\alpha$ strongly down-weights small residual dot products (weak, noisy matches) while amplifying large ones (strong, genuine matches), making the kernel far more selective than the linear case as described in Section 1. An excessively large $\alpha$ could hurt performance by suppressing even moderately correct correspondences — descriptors that genuinely match but differ slightly due to viewpoint or illumination changes would receive near-zero votes, reducing recall for non-identical but valid feature pairs.

2. Because $f$ is non-linear, $s_{\text{SMK}}(\mathcal{X}, \mathcal{Y})$ cannot be factored into $\phi(\mathcal{X})^\top \phi(\mathcal{Y})$ for any fixed per-image encoding $\phi$; the score depends on all pairwise residual dot products across the two images jointly. This forces retrieval to proceed through the inverted file with pairwise accumulation rather than ANN search over a vector space (as VLAD uses). The concrete capability preserved is **tentative correspondences**: since SMK scores individual feature pairs sharing a visual word, it naturally produces a ranked list of matching feature pairs that can feed directly into spatial verification (e.g., RANSAC), which VLAD's aggregated global vector discards entirely (Section 4).

3. Doubling $K$ from 65k to 130k halves the expected posting list length per visual word (features are distributed over twice as many bins), which directly reduces the number of dot products computed per query word and thus lowers per-query cost. Retrieval accuracy would likely improve modestly because finer quantisation means descriptors assigned to the same word are more similar, producing higher-quality tentative correspondences and reducing the contribution of accidental co-assignments; however, very short posting lists also risk missing true matches that land in adjacent but different words (the hard-assignment problem inherent to BoW-style methods noted in Section 3).

4. SMK would perform **worse** in this scenario relative to its usual advantage over BoW. The selective kernel $f$ rewards pairs with large residual dot products $\mathbf{r}(\mathbf{x})^\top \mathbf{r}(\mathbf{y})$; if lighting changes cause residuals within the same visual word to diverge substantially, those dot products will be small and heavily suppressed by $\alpha > 1$, yielding low similarity scores even for true matches. BoW, by contrast, treats every co-occurrence of the same visual word as an equal vote regardless of residual similarity, so it would still accumulate evidence across all lighting conditions without penalising the residual discrepancy — making BoW more robust here, at the cost of lower discriminative power in cases where residuals are informative.