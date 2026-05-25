## Mapping Images to a Vector Space for Retrieval

The previous sections described retrieval pipelines built on local features, visual vocabularies, and inverted files. A fundamentally different paradigm – and the one that dominates modern instance‑level and semantic retrieval – is to **map each entire image to a single global descriptor vector** in a Euclidean space, and then perform retrieval by nearest‑neighbour search in that space. This section explains the benefits of such a vector‑space embedding and how retrieval is carried out once the mapping is learned.

### 1. The Vector‑Space Embedding

Let $f_\theta : \mathcal{I} \to \mathbb{R}^d$ be a function parameterised by a deep neural network that takes an image $I$ and produces a $d$‑dimensional **global descriptor** $\mathbf{X} = f_\theta(I)$. The function is trained so that a standard distance or similarity in $\mathbb{R}^d$ reflects the visual relevance between images:

- **Euclidean distance** $\|\mathbf{X} - \mathbf{Y}\|_2$ is small for relevant pairs and large for irrelevant ones.
- Equivalently, **cosine similarity** or **dot product** $\mathbf{X}^\top \mathbf{Y}$ is high for relevant pairs (assuming $\ell_2$‑normalised descriptors).

The mapping $f_\theta$ is typically a fully convolutional network (FCN) followed by a pooling layer that collapses the spatial dimensions into a single vector, or a Vision Transformer (ViT) whose class token or pooled patch tokens serve as the global descriptor. Crucially, the whole pipeline – from pixels to the final descriptor – is differentiable, enabling **end‑to‑end metric learning**.

### 2. Benefits of the Vector‑Space Approach

Compared to the local‑feature + inverted‑file paradigm (BoW, VLAD, SMK), mapping images to a global descriptor vector offers several practical and performance advantages.

#### 2.1 Efficient and Scalable Retrieval

Once every database image is represented by a $d$‑dimensional vector, the similarity between a query and *all* database images can be computed as a single matrix‑vector multiplication (or a batch of dot products). For large‑scale collections, **approximate nearest neighbour (ANN)** search libraries such as FAISS can retrieve the top‑$k$ results in sub‑linear time, often in a few milliseconds even with billions of vectors. This is a stark contrast to inverted files, where the query must traverse posting lists and accumulate scores per image – a process that, while also sub‑linear, involves many random memory accesses and per‑posting operations.

The vector‑space model also decouples the representation from the search index: the same descriptor can be used with brute‑force search, product quantisation, graph‑based indices, or any other ANN method, without changing the feature extraction.

#### 2.2 Compact, Fixed‑Size Representation

A global descriptor is a single vector of fixed length (e.g., 512–2048 dimensions), regardless of the number of local features in the image. This leads to **low and predictable memory consumption**: storing $N$ images requires $N \times d \times 4$ bytes (for float32). In contrast, an inverted file storing local descriptors (as in SMK) or even aggregated vectors (VLAD) can be orders of magnitude larger because it scales with the total number of local features.

The compactness also makes it feasible to keep the entire descriptor database in RAM or even on GPU, enabling extremely fast brute‑force search for moderate‑sized collections.

#### 2.3 End‑to‑End Learning for the Retrieval Task

Because the mapping $f_\theta$ is a neural network, it can be trained with loss functions that directly target the desired retrieval behaviour. The slides present a spectrum of losses:

- **Classification losses** (cross‑entropy, arc‑face) that treat each instance or category as a class.
- **Pairwise losses** (contrastive, triplet) that explicitly push positive pairs together and negative pairs apart.
- **Listwise losses** that optimise a differentiable surrogate of a retrieval metric, such as **smooth Average Precision (AP)** or **Recall@k surrogate**. These directly maximise the quality of the ranked list, often yielding superior results.

This end‑to‑end optimisation allows the network to learn invariance to nuisance factors (illumination, viewpoint, clutter) and to focus on discriminative details, all from data. It eliminates the hand‑crafted stages of classical pipelines (detector, descriptor, codebook, aggregation) and replaces them with a single, jointly optimised function.

#### 2.4 Implicit Spatial Reasoning and Invariance

Different pooling strategies confer different geometric properties to the global descriptor, without requiring explicit spatial verification at query time:

- **Sum pooling (SPoC)** yields a **translation‑invariant** representation because summing over all spatial locations discards positional information.
- **Max pooling (MAC)** retains some spatial information: each dimension of the descriptor corresponds to the maximum activation of a feature map, which implicitly corresponds to a specific image region. The dot product between two MAC descriptors can be interpreted as a soft, implicit matching of corresponding regions, as illustrated in the slides.
- **Generalised mean (GeM) pooling** interpolates between sum and max pooling, with a learnable exponent $p$.
- **Weighted pooling (CroW, attention)** learns to emphasise foreground regions and suppress background, further improving robustness.

These properties mean that a single dot product can capture complex visual similarity, often making a separate spatial verification step unnecessary for many tasks.

#### 2.5 No Quantisation Artefacts

Classical BoW and VLAD rely on a visual codebook to quantise local descriptors. This hard assignment introduces quantisation errors and requires a large codebook for good performance. In the vector‑space approach, there is **no discrete vocabulary**: the network directly produces a real‑valued descriptor, avoiding information loss from quantisation. Even methods like NetVLAD, which internally use a soft assignment to learnable “visual words”, output a continuous global vector that is compared with a standard metric.

### 3. How Retrieval Is Performed

The retrieval workflow with a global descriptor is straightforward:

1. **Offline indexing.** For every image in the database, compute $\mathbf{X}_i = f_\theta(I_i)$. Normalise the vectors (e.g., $\ell_2$ normalisation) so that dot product equals cosine similarity. Build an ANN index over the set $\{\mathbf{X}_i\}$.

2. **Querying.** Given a query image $I_q$, compute its descriptor $\mathbf{X}_q = f_\theta(I_q)$ with the same network and normalisation.

3. **Similarity computation.** The relevance of a database image $I_i$ to the query is measured by a simple scalar function:
   - **Cosine similarity:** $s(\mathbf{X}_q, \mathbf{X}_i) = \mathbf{X}_q^\top \mathbf{X}_i$ (if $\ell_2$‑normalised).
   - **Euclidean distance:** $d(\mathbf{X}_q, \mathbf{X}_i) = \|\mathbf{X}_q - \mathbf{X}_i\|_2$, often converted to similarity via $s = -d$ or $s = 1/(1+d)$.

4. **Ranking.** Retrieve the $K$ database images with the highest similarity (or smallest distance). This can be done by:
   - **Brute force:** compute the dot product with every database vector. Feasible for up to a few million images on a single GPU.
   - **Approximate nearest neighbours:** use an ANN index (e.g., inverted file with product quantisation, HNSW graph) to quickly find the top‑$K$ without scanning the whole collection. This scales to billions of images.

5. **Optional re‑ranking.** The shortlist can be further refined by spatial verification (as described in the Spatial Verification section) if the global descriptor does not already capture sufficient geometric consistency. However, many modern deep global descriptors are so discriminative that re‑ranking is often omitted or replaced by simple query expansion.

### 4. Relation to Classical Aggregation Methods

It is worth noting that classical aggregation methods like VLAD and Fisher Vectors also produce a global vector. The key difference is that in deep metric learning, the **entire process – local feature extraction, aggregation, and dimensionality reduction – is learned jointly** from data, rather than being designed by hand. This results in descriptors that are far more compact (typically 256–2048 dimensions vs. 32k–262k for uncompressed VLAD/FV) and significantly more accurate, as shown by the performance results on standard benchmarks (e.g., R‑Oxford with 1M distractors).

### 5. Summary

Mapping images to a vector space via a deep neural network transforms retrieval into a nearest‑neighbour search problem. The benefits are:

- **Speed and scalability** through ANN libraries.
- **Compact, fixed‑size representations** with low memory footprint.
- **End‑to‑end learning** that directly optimises retrieval metrics.
- **Built‑in invariance** and implicit spatial reasoning from pooling.
- **No quantisation artefacts** from a visual vocabulary.

Retrieval is then performed by extracting the query descriptor, computing its similarity to all (or a pruned set of) database descriptors, and ranking by that similarity. This paradigm has become the standard for both instance‑level and semantic image retrieval.

---

### Self-Test

1. MAC pooling is said to perform "implicit spatial matching" via a dot product — why does this emerge from max pooling, and under what conditions would this implicit matching break down?
2. How does end-to-end training with a listwise loss (e.g., smooth AP) differ in what it optimises compared to a triplet loss, and why might that difference matter for retrieval performance at the top of the ranked list?
3. If you $\ell_2$-normalise all descriptors before indexing and querying, cosine similarity and Euclidean distance become equivalent up to a monotone transform — given this, why would you ever prefer one over the other in an ANN index?
4. Suppose you deploy a global descriptor system and notice it performs well on clean studio images but poorly on cluttered street-scene queries. Which design choices in $f_\theta$ or training could explain this failure, and how might you address it?

### Answer Key

1. MAC pooling takes the maximum activation across each spatial location per channel, meaning each dimension of the descriptor implicitly "votes" for the most strongly activated region in the image. When two descriptors are compared via dot product, each channel contributes positively only if both images have a strong response in the same feature type, which loosely corresponds to matching salient regions — hence the "implicit spatial matching." This breaks down when images contain many similarly activated regions (clutter), when the dominant region in one image has no counterpart in the other, or when strong background activations dominate the foreground object, causing the max to be "claimed" by an irrelevant region.

2. A triplet loss optimises a **margin** between a single positive pair and a single negative pair at a time: it only ensures $d(\mathbf{X}_q, \mathbf{X}^+) + \epsilon < d(\mathbf{X}_q, \mathbf{X}^-)$ for sampled triplets, with no direct regard for the global rank order. A listwise loss such as smooth AP instead optimises a differentiable surrogate of the entire ranked list simultaneously, directly rewarding the network for placing all positives as high as possible. This matters for top-of-list retrieval (e.g., P@1, mAP) because a triplet loss can be satisfied by a solution that still ranks some positives far down the list, while smooth AP penalises every misranked positive, producing better-calibrated ranked lists.

3. Under $\ell_2$ normalisation, $\|\mathbf{X} - \mathbf{Y}\|_2^2 = 2 - 2\mathbf{X}^\top\mathbf{Y}$, so minimising Euclidean distance is equivalent to maximising dot product — they induce the same ranking. In practice the choice is driven by the ANN index's internal data structure: dot-product (inner-product) indices such as FAISS's `IndexFlatIP` or graph-based HNSW variants may offer different speed/memory trade-offs than $\ell_2$ indices, and some quantisation schemes (e.g., product quantisation) are designed for one metric or the other, so the "preference" is an engineering decision rather than a mathematical one.

4. The failure on cluttered scenes likely stems from sum or average pooling (SPoC) giving too much weight to background activations, or from a training set dominated by clean, object-centric images that never taught the network to suppress clutter. Architecturally, switching to **attention-based or CroW-style weighted pooling** would allow the network to down-weight irrelevant background regions. On the training side, using hard negatives that are visually similar in background but differ in foreground object, and augmenting with cluttered or occluded training images, would expose the network to the distribution shift and learn more foreground-focused descriptors.