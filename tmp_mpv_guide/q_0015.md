## Bag-of-Words Representation for Image Retrieval

The Bag-of-Words (BoW) model is a foundational technique for large‑scale instance‑level image retrieval. It draws an analogy to text retrieval: a document is represented by the set of words it contains, ignoring word order. In the visual domain, an image is represented by a histogram of **visual words** obtained by quantising the space of local descriptors. This section explains how the BoW histogram is constructed, the role and estimation of **inverse document frequency (idf)** weighting, how image‑to‑image similarity is computed, and how the codebook size – along with other factors – determines the sparsity of the representation.

### 1. Construction of the BoW Histogram

The BoW representation is built in three stages: codebook generation, descriptor assignment, and histogram accumulation.

#### 1.1 Visual Codebook Generation

A **visual codebook** (or vocabulary) is a set of representative vectors that partition the local descriptor space. It is typically obtained by clustering a large sample of local descriptors extracted from a training set of images. The most common clustering algorithm is **k‑means**. Each resulting cluster centre $\mathbf{c}_k \in \mathbb{R}^D$ is called a **visual word**. The number of clusters $K$ is the **codebook size**. The codebook is denoted $\mathcal{C} = \{\mathbf{c}_1, \dots, \mathbf{c}_K\}$.

The choice of $K$ is a critical design parameter. Small codebooks (e.g., $K = 128$) produce a coarse quantisation; large codebooks (e.g., $K = 10^6$) produce a fine partition. The impact on sparsity and retrieval performance is discussed in Section 4.

#### 1.2 Descriptor Assignment (Quantisation)

Given an image $I$, a set of $N$ local descriptors $\{\mathbf{x}_1, \dots, \mathbf{x}_N\}$ is extracted (e.g., SIFT, RootSIFT). Each descriptor $\mathbf{x}_i$ is assigned to its nearest visual word in the codebook:

$$
q(\mathbf{x}_i) = \arg\min_{k \in \{1,\dots,K\}} \|\mathbf{x}_i - \mathbf{c}_k\|_2.
$$

The assignment is **hard**: each descriptor contributes to exactly one visual word. This is the simplest form of vector quantisation; soft‑assignment variants (e.g., Fisher Vectors) exist but are not part of the classical BoW model.

#### 1.3 Histogram Accumulation

The image is represented by a $K$‑dimensional vector $\mathbf{h} \in \mathbb{R}^K$, where the $k$‑th component is the number of local descriptors assigned to visual word $k$:

$$
h_k = \sum_{i=1}^{N} \mathbf{1}\big[ q(\mathbf{x}_i) = k \big].
$$

This vector is called the **term frequency (TF)** histogram. It captures which visual words appear in the image and how often. Because the number of local features $N$ varies across images, the histogram is often normalised (e.g., by $L_1$ or $L_2$ norm) to reduce the influence of image size and texture density.

### 2. Inverse Document Frequency (idf) Weighting

Not all visual words are equally informative. Some words occur very frequently across the entire database – for example, words corresponding to uniform background patches or repetitive textures. These words are analogous to stop‑words in text retrieval: they appear in many images and therefore provide little discriminative power. To down‑weight such words, the BoW model borrows the **inverse document frequency (idf)** from text retrieval.

#### 2.1 Definition and Estimation

For a database of $M$ images, let $M_k$ be the number of images that contain visual word $k$ at least once. The idf weight for word $k$ is defined as

$$
w_k = \log \frac{M}{M_k}.
$$

If a word appears in all images ($M_k = M$), its idf weight is $\log 1 = 0$; it contributes nothing to the similarity. If a word appears in only a few images, its idf weight is large, emphasising its rarity and discriminative power. In practice, $M_k$ is estimated from the database itself (or a representative sample) by counting the number of images whose BoW histogram has $h_k > 0$.

#### 2.2 Problem Handled by idf

The idf weighting addresses the problem that **frequent visual words dominate the similarity score without providing meaningful evidence of a match**. Without idf, two images of completely different objects might share many common‑but‑generic visual words (e.g., those arising from uniform regions or common textures) and receive a spuriously high similarity. By multiplying each histogram bin by $w_k$, the contribution of such words is suppressed, and the similarity is driven by rare, distinctive visual words that are more likely to indicate a true correspondence.

The idf‑weighted BoW vector for an image is

$$
\tilde{\mathbf{h}} = \mathbf{h} \odot \mathbf{w},
$$

where $\odot$ denotes element‑wise multiplication and $\mathbf{w} = (w_1, \dots, w_K)^\top$.

### 3. Image‑to‑Image Similarity with BoW

Given two images $A$ and $B$ with idf‑weighted BoW vectors $\tilde{\mathbf{h}}_A$ and $\tilde{\mathbf{h}}_B$, the similarity is typically measured by the **dot product** (or, equivalently, the cosine similarity if the vectors are $L_2$‑normalised):

$$
s(A, B) = \tilde{\mathbf{h}}_A^\top \tilde{\mathbf{h}}_B = \sum_{k=1}^{K} w_k^2 \, h_{A,k} \, h_{B,k}.
$$

This sum can be interpreted as a voting process: each visual word $k$ that appears in both images contributes a vote proportional to the product of its term frequencies, weighted by $w_k^2$. If a word is absent in either image, its contribution is zero.

#### 3.1 Efficient Retrieval with an Inverted File

For large databases, computing the dot product with every database image is prohibitively expensive. The BoW representation is **sparse** (see Section 4), so the sum can be computed efficiently using an **inverted file** structure. An inverted file maintains, for each visual word $k$, a **posting list** of image identifiers that contain that word, along with the corresponding term frequency $h_{A,k}$ (and possibly other pre‑computed quantities). At query time, only the posting lists of the visual words present in the query are accessed. The similarity score for each candidate image is accumulated incrementally:

1. Initialise a score accumulator for each database image to zero.
2. For each visual word $k$ in the query:
   - Retrieve the posting list for word $k$.
   - For each entry $(B, h_{B,k})$ in the list, add $w_k^2 \, h_{\text{query},k} \, h_{B,k}$ to the accumulator of image $B$.
3. After processing all query words, the accumulators contain the dot‑product scores. The images are then ranked by decreasing score.

This inverted‑file approach reduces the query time from $O(M \cdot K)$ to $O(\sum_{k \in \text{query}} L_k)$, where $L_k$ is the length of the posting list for word $k$. Since the query contains only a small fraction of the $K$ words, and posting lists are short for rare words, retrieval is extremely fast.

### 4. Codebook Size and Sparsity of the BoW Histogram

The BoW histogram is inherently sparse: an image contains only a finite number of local features, and each feature activates exactly one visual word. The **sparsity** of the histogram – the fraction of zero entries – is determined primarily by the codebook size $K$ and the number of local features $N$ per image, but also by other factors.

#### 4.1 Effect of Codebook Size

- **Small codebook** (e.g., $K = 128$): The quantisation is coarse. Many different local patches are assigned to the same visual word. Consequently, most images will contain a large fraction of the vocabulary, and the histogram becomes **dense**. A dense representation is compatible with approximate nearest neighbour search methods (e.g., product quantisation, locality‑sensitive hashing) and has a small memory footprint per image ($K$ floating‑point numbers). However, the discriminative power is limited because different visual patterns are collapsed into the same word.

- **Large codebook** (e.g., $K = 10^6$): The quantisation is fine. Each visual word corresponds to a very specific local appearance. An image will activate only a tiny subset of the vocabulary, resulting in a **highly sparse** histogram. Sparsity enables the use of inverted files for fast retrieval and dramatically reduces the memory footprint when storing only the non‑zero entries (image‑id plus term frequency). Large codebooks are preferred for instance‑level retrieval because they provide high discriminative power: two images of the same object are likely to share many rare visual words, while different objects share very few.

The slide material explicitly contrasts these two regimes: small codebooks (e.g., 128) yield dense representations suitable for category‑level matching and approximate NN search, while very large codebooks (e.g., $10^6$) yield sparse representations that exploit inverted files for instance‑level retrieval.

#### 4.2 Other Factors Affecting Sparsity

Beyond the codebook size, the sparsity of the BoW histogram is influenced by:

- **Number of local features per image ($N$).** An image with many detected keypoints (e.g., a highly textured scene) will activate more visual words than a smooth, uniform image. For a fixed $K$, increasing $N$ reduces sparsity because more bins become non‑zero. In the extreme case where $N \gg K$, the histogram may become nearly dense.

- **Image content.** Textured images with many distinct local structures naturally produce more diverse descriptors, activating a larger portion of the vocabulary. Conversely, images dominated by homogeneous regions (sky, walls) yield fewer features and sparser histograms.

- **Detector and descriptor parameters.** The choice of local feature detector (e.g., Hessian‑Affine, DoG) and the detection threshold control the number and spatial distribution of keypoints, thereby affecting $N$ and the resulting sparsity.

- **Codebook construction.** The clustering algorithm and the training data used to build the codebook influence how the descriptor space is partitioned. A codebook trained on a diverse dataset will have words that cover the space more uniformly, potentially altering the typical sparsity for a given image collection.

In practice, instance‑level retrieval systems use a very large codebook (often $10^5$–$10^6$ words) combined with idf weighting and an inverted file. The resulting BoW histograms are extremely sparse – typically only a few hundred non‑zero entries per image – enabling sub‑linear query times and compact storage.

### 5. Summary

The Bag-of-Words representation for image retrieval is constructed by:

1. **Quantising** local descriptors to the nearest visual word from a pre‑computed codebook (k‑means clustering).
2. **Accumulating** a histogram of visual word occurrences (term frequencies) for each image.
3. **Weighting** the histogram by **inverse document frequency (idf)**, estimated as $\log(M / M_k)$, to suppress the influence of frequent, non‑discriminative visual words.
4. **Comparing** images via the dot product of their idf‑weighted histograms, efficiently implemented with an inverted file that exploits the sparsity of the representation.

The **codebook size** is the primary factor controlling sparsity: small codebooks produce dense histograms, while large codebooks produce highly sparse ones. Additional factors include the number of local features per image, image content, and detector settings. This sparse, idf‑weighted BoW model forms the core of many classical large‑scale image retrieval engines and provides the tentative correspondences that are later refined by spatial verification.

---

### Self-Test

1. Two images of completely different scenes share many visual words; why does idf weighting reduce their spurious similarity score, and what property of the shared words makes this work?
2. If you increase the codebook size $K$ from $10^3$ to $10^6$ while keeping the number of local features $N$ per image fixed, how does this affect both the sparsity of $\mathbf{h}$ and the query-time complexity when using an inverted file?
3. An image of a clear blue sky produces very few SIFT keypoints. How does this affect its BoW histogram sparsity compared to a textured urban scene, and what consequence does this have for retrieval accuracy?
4. The dot-product similarity $s(A, B) = \sum_k w_k^2\, h_{A,k}\, h_{B,k}$ only sums over visual words present in both images. Under what conditions could this cause the BoW model to fail to retrieve a true match between two photos of the same object?

### Answer Key

1. idf weighting assigns each visual word $k$ a weight $w_k = \log(M / M_k)$, which is small (near zero) when $M_k \approx M$ — i.e., when the word appears in nearly every database image. Words shared by two completely different scenes are almost certainly common, generic words (analogous to stop-words), so their $w_k$ is close to zero and their contribution to $s(A, B)$ is suppressed. The mechanism works precisely because those shared words are frequent across the database, which is the property idf directly penalises.

2. Increasing $K$ from $10^3$ to $10^6$ while holding $N$ fixed makes the quantisation finer: each visual word covers a smaller region of descriptor space, so a given image activates a much smaller fraction of the vocabulary, and the histogram $\mathbf{h}$ becomes far sparser (most of the $10^6$ bins are zero). At query time, the inverted-file traversal visits only the posting lists of the non-zero query words; because those words are rarer (shorter posting lists), the cost $O(\sum_{k \in \text{query}} L_k)$ decreases substantially compared to the coarser codebook, giving faster retrieval.

3. A clear blue sky produces very few SIFT keypoints, so $N$ is small and the BoW histogram is extremely sparse — only a handful of bins are non-zero. A textured urban scene activates many more visual words, producing a denser histogram. For retrieval, a very sparse query histogram means only a tiny number of posting lists are consulted, so very few database images accumulate any score at all; if the matching image does not share those exact visual words (e.g., due to illumination changes or quantisation noise), it will receive a score of zero and be missed entirely, hurting recall.

4. The dot product is zero for any word absent in either image, so the model fails when the two photos of the same object share few or no visual words after quantisation. This can happen under large viewpoint or scale changes (different local patches are detected and described), significant illumination or appearance variation (descriptors shift across Voronoi cell boundaries in the codebook), or when a large codebook causes fine-grained quantisation that maps visually similar patches to different visual words. Occlusion that removes the distinctive features from one image will also eliminate the shared words needed for a non-zero similarity score.