## Zoom-In Retrieval Using Retrieval and RANSAC

The standard image retrieval pipeline, described in previous sections, ranks database images by their visual similarity to the query – typically returning near‑duplicates or images depicting the same object at a similar scale. In many applications, however, we are interested in a **zoom‑in** operation: given a query image, find database images that show a *higher‑resolution* view of some object or region present in the query. This is essential for detail mining, 3D reconstruction from a single image, and exploring fine‑grained structures. This section explains how a modified retrieval stage combined with RANSAC‑based spatial verification can perform zoom‑in retrieval, how the initial retrieval differs from standard BoW, and why that modification is necessary.

### 1. The Zoom‑In Task

Formally, the zoom‑in task asks: for a query image $I_q$, retrieve database images $I_{db}$ such that $I_{db}$ depicts a part of $I_q$ at a **larger scale**. That is, the object or region visible in the query appears bigger (more pixels) in the database image. This is the opposite of zoom‑out, and it requires identifying images where the geometric transformation between the query and the database involves a scale factor $s > 1$ (the database image is “zoomed in” relative to the query).

Standard BoW retrieval is scale‑agnostic: it counts how many visual words co‑occur, regardless of whether the matching features have the same, larger, or smaller scale. Consequently, a near‑duplicate image at the same scale will often receive a higher BoW score than a zoomed‑in image that shares only a subset of the visual words (because the zoomed‑in image covers a smaller field of view). To perform zoom‑in retrieval, we must therefore **modify the initial ranking** to favour candidates with a large scale change, and then use **spatial verification** to accurately estimate the scale factor and re‑rank the shortlist.

### 2. Two‑Stage Zoom‑In Retrieval

The approach follows the familiar two‑stage paradigm – fast initial retrieval followed by geometric re‑ranking – but with crucial adaptations at both stages.

#### 2.1 Stage 1: Scale‑Aware BoW Retrieval

In standard BoW, the similarity between query $q$ and database image $d$ is

$$
s_{\text{BoW}}(q,d) = \sum_{k=1}^{K} \text{idf}_k^2 \cdot \text{tf}_q(k) \cdot \text{tf}_d(k),
$$

where $\text{tf}(k)$ is the number of local features assigned to visual word $k$. This score treats every co‑occurrence equally, irrespective of the geometric properties of the underlying features.

For zoom‑in, we exploit the fact that each local feature carries a **shape** $A$ (a $2\times2$ matrix encoding scale and rotation, or an affine shape). When a query feature with shape $A_q$ matches a database feature with shape $A_{db}$ via the same visual word, the relative scale change can be extracted directly from the shapes. For a similarity‑covariant feature, the scale is proportional to the determinant or the singular values of $A$; the scale ratio is

$$
r = \frac{\text{scale}(A_{db})}{\text{scale}(A_q)}.
$$

A zoom‑in corresponds to $r > 1$. We can therefore modify the voting weight of each match to be a function of $r$ that **increases with $r$**. For example, the score can be redefined as

$$
s_{\text{zoom}}(q,d) = \sum_{k=1}^{K} \sum_{\substack{\mathbf{x} \in \mathcal{X}_q^{(k)} \\ \mathbf{y} \in \mathcal{X}_d^{(k)}}} \text{idf}_k \cdot g\!\left( \frac{\text{scale}(A_{\mathbf{y}})}{\text{scale}(A_{\mathbf{x}})} \right),
$$

where $g(r)$ is a monotonically increasing function for $r \ge 1$, e.g., $g(r) = r^\alpha$ or a step function that only counts matches with $r > 1$. This **scale‑aware scoring** can be implemented efficiently by storing the scale (or the full shape) of each feature in the inverted file’s posting lists. During query time, for each candidate match, the scale ratio is computed and the vote is weighted accordingly.

The result of this first stage is a shortlist of images that are likely to contain a zoomed‑in view of some part of the query. The ranking is no longer purely based on visual word co‑occurrence; it is biased toward images where the matched features exhibit a larger scale than the query features.

#### 2.2 Stage 2: RANSAC‑Based Verification and Re‑Ranking by Scale Change

The top‑ranked candidates from the scale‑aware BoW stage are then subjected to **fast spatial matching** (the deterministic RANSAC variant described in the Spatial Verification section). Recall that from a single tentative correspondence $(A, x, y) \leftrightarrow (A', x', y')$, we can directly hypothesise a similarity or affine transformation

$$
F = A' \, A^{-1}.
$$

For each hypothesis, we count the number of inliers – correspondences that satisfy the reprojection error threshold. The transformation $F$ also provides an accurate estimate of the **global scale change** between the two images. For a similarity transformation, the scale factor $s$ is simply the singular value of the upper‑left $2\times2$ submatrix of $F$; for an affine transformation, it can be taken as the square root of the determinant of that submatrix.

The final re‑ranking of the shortlist is then performed according to the **estimated scale change** $s$, possibly combined with the inlier count to ensure geometric consistency. A typical strategy is to rank images by $s$ (largest first) among those that have a sufficient number of inliers, or to use a combined score such as $\text{inliers} \times s$. This directly implements the “maximise scale change” objective mentioned in the slides.

### 3. Differences from Standard BoW Retrieval

The table below summarises the key differences between the first stage of zoom‑in retrieval and the standard BoW pipeline.

| Aspect | Standard BoW Retrieval | Zoom‑In First Stage |
|--------|------------------------|----------------------|
| **Vote weight** | $\text{idf}^2$ (or $\text{idf}$) per co‑occurrence | $\text{idf} \cdot g(\text{scale ratio})$, with $g$ favouring $r>1$ |
| **Information used** | Visual word identity only | Visual word identity + local feature scale (or shape) |
| **Inverted file contents** | (image‑id, term frequency) | (image‑id, scale/shape, optionally residual) |
| **Ranking criterion** | Visual similarity (same scale preferred) | Likelihood of zoom‑in (larger scale preferred) |
| **Output** | Top‑$K$ visually similar images | Top‑$K$ candidate zoom‑in images |

### 4. Why the Modification Is Necessary

Without the scale‑aware modification, standard BoW retrieval would rank images that are globally similar to the query – typically near‑duplicates or images taken from a similar viewpoint and scale – at the very top. A zoomed‑in image, which captures only a portion of the query’s content, will naturally share fewer visual words with the query and will therefore receive a lower BoW score. It would be buried deep in the ranking, often outside the shortlist that is feasible to process with spatial verification.

By incorporating scale information directly into the initial scoring, we **pull zoom‑in candidates toward the top** of the ranking. This ensures that the subsequent RANSAC‑based verification, which is computationally more expensive, is applied to a set of images that are genuinely likely to contain a zoomed‑in view. The RANSAC stage then provides a precise estimate of the scale factor and filters out any false positives that may have been boosted by accidental scale‑consistent matches.

In summary, the modification is necessary because the zoom‑in task requires a **different relevance criterion** – scale change rather than visual similarity – and the initial retrieval must reflect this criterion to make the two‑stage pipeline effective.

### 5. Summary

Zoom‑in retrieval is achieved by a two‑stage process:

1. **Scale‑aware BoW retrieval** – The inverted file stores feature scales (or shapes). During querying, each match is weighted by a function of the scale ratio $r = \text{scale}_{db} / \text{scale}_{query}$, favouring $r > 1$. This produces a shortlist of candidate zoom‑in images.
2. **RANSAC‑based verification and re‑ranking** – Fast spatial matching estimates the geometric transformation and counts inliers. The scale factor $s$ extracted from the transformation is used to re‑rank the candidates, maximising the scale change.

The first stage differs from standard BoW by replacing the scale‑blind idf vote with a scale‑dependent weight. This is essential because standard BoW would otherwise rank same‑scale near‑duplicates above zoomed‑in images, preventing the latter from ever reaching the spatial verification stage.

---

### Self-Test

1. Standard BoW retrieval is described as "scale-agnostic." Why does this property cause it to systematically rank zoomed-in images lower than near-duplicates, even when the zoomed-in image is a more relevant result for the task?
2. The scale-aware score weights each match by $g(r)$ where $r = \text{scale}(A_{db}) / \text{scale}(A_q)$. How would the retrieval behaviour change if $g$ were replaced with a constant function $g(r) = 1$, and is there any scenario where this substitution would still produce correct zoom-in results?
3. In Stage 2, the transformation $F = A' A^{-1}$ is hypothesised from a single correspondence. When would this single-correspondence hypothesis be unreliable, and how does counting inliers compensate for that unreliability?
4. If the database contains images captured with a very wide-angle lens (extreme zoom-out relative to the query), how might the pipeline incorrectly rank or miss true zoom-in candidates, and what modification to the scoring or re-ranking could address this?

### Answer Key

1. A zoomed-in image shares only a subset of visual words with the query because it depicts a smaller field of view — fewer query features fall within the zoomed-in region, so the BoW co-occurrence count is inherently lower. Near-duplicates, by contrast, cover the same scene at the same scale and therefore match a much larger fraction of the query's visual words, yielding a higher $s_{\text{BoW}}$ score. Because scale is completely ignored in the standard vote weight $\text{idf}^2 \cdot \text{tf}_q(k) \cdot \text{tf}_d(k)$, there is no mechanism to compensate for this structural disadvantage of zoomed-in images.

2. Setting $g(r) = 1$ reduces the scale-aware score back to a standard (unnormalised) BoW score, removing the preference for $r > 1$ matches and making Stage 1 scale-blind again. Zoom-in results could still reach the shortlist if the zoomed-in image happens to share enough visual words with the query by chance — for instance, if the query image is nearly blank except for one highly distinctive region that dominates the match count — but this would be coincidental rather than systematic, and the pipeline would generally fail to surface zoom-in candidates.

3. The single-correspondence hypothesis $F = A'A^{-1}$ relies on the local affine shapes $A$ and $A'$ being accurately detected and mutually consistent; noisy or degenerate feature shapes (e.g., from textureless regions or repeated patterns) can yield a wildly incorrect $F$. Counting inliers compensates by checking how many other correspondences are geometrically consistent with the hypothesised $F$ under a reprojection error threshold — a spurious hypothesis will produce few inliers, while a correct one will accumulate many, making the inlier count a robust quality measure even when individual hypotheses are unreliable.

4. Wide-angle (strongly zoomed-out) database images have feature scales much smaller than query features, giving scale ratios $r = \text{scale}_{db}/\text{scale}_{query} \ll 1$. With a monotonically increasing $g(r)$ these images receive very low Stage-1 scores, so they are correctly suppressed — but if such images happen to share a large number of visual words they could still fill the shortlist and crowd out true zoom-in candidates. A targeted fix is to enforce a hard lower bound, discarding matches with $r < 1$ entirely (i.e., $g(r) = 0$ for $r \le 1$), and to cap the shortlist evaluation at candidates whose Stage-2 estimated scale $s$ exceeds a minimum threshold, ensuring wide-angle images are excluded at both stages.