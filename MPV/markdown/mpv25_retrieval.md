## image retrieval

## Computer Vision Methods 2025

## CTU in Prague Giorgos Tolias

slide credits also to: Jiri Matas, Ondrej Chum, Andrej Mikulik, Filip Radenovic, Michal Perdoch, James Pritts, Dmytro Mishkin, Jan Cech

- task formulation
- bag-of-words (BoW) model
- BoW generic point-of-view  other approaches
- fast spatial (geometric) matching
- special retrieval tasks

## outline

## the task

## image retrieval - example

<!-- image -->

query image

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## image retrieval

<!-- image -->

<!-- image -->

for image copy detection

<!-- image -->

<!-- image -->

## image retrieval

<!-- image -->

<!-- image -->

<!-- image -->

for image copy detection image retrieval for image geo-localization

<!-- image -->

<!-- image -->

6

## image retrieval

for image geo-localization

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

6

## image retrieval

for image geo-localization

<!-- image -->

6

## image retrieval

for image geo-localization

<!-- image -->

6

<!-- image -->

## History[ edit ]

<!-- image -->

Originally a family business, the pub was founded in 1499,[1] and thereforecelebratedits500thanniversaryin1999.Ithas beenreferredtoastheoldestbreweryinPrague.In1762the

## image retrieval

<!-- image -->

<!-- image -->

## for landmark recognition

## image retrieval

<!-- image -->

for e-commerce

## image retrieval

<!-- image -->

for logo infringement identification

## image retrieval - task

- given a query image and an image collection (database)
- retrieve database images according to their relevance to the query
- rank all images
- retrieve most relevant
- relevance defined in different ways, according to the task
- retrieval approaches characterized by performance
- quality: ability to retrieve relevant images first
- speed: small query time
- memory footprint: low memory requirements

<!-- image -->

<!-- image -->

identical photo

<!-- image -->

<!-- image -->

identical object

<!-- image -->

<!-- image -->

<!-- image -->

- scalability: applicability to large image collections

<!-- image -->

infringement

<!-- image -->

<!-- image -->

## image retrieval - task

- retrieval is a ranking task for a given query ' q '
- relevance is defined for pairs (q,a) , ' a ' is a database image
- degree of relevance s(q,a)
- estimate it to perform retrieval
- need for ground-truth
- difficult to obtain continuous degree of relevance in ground-truth
- binary approximation
- 1: positive / matching /relevant pair
- 0: negative / non-matching / non-relevant pair

## query:

<!-- image -->

## ranking:

## image retrieval - evaluation

- 10 database images
- 5 relevant images, according to binary pairwise labels
- select a 'window' of top-k images
- measure precision @ k and recall @ k
- what should k be? should we use only one window?

<!-- image -->

<!-- image -->

selected elements

<!-- image -->

## query:

<!-- image -->

## ranking:

## image retrieval - evaluation

- 10 database images
- 5 relevant images, according to binary pairwise labels
- select a 'window' of top-k images
- measure precision @ k and recall @ k
- what should k be? should we use only one window?

<!-- image -->

recall

## query:

<!-- image -->

## ranking:

<!-- image -->

## image retrieval - evaluation

- 10 database images
- 5 relevant images, according to binary pairwise labels
- select a 'window' of top-k images
- measure precision @ k and recall @ k
- what should k be? should we use only one window?

<!-- image -->

recall

## query:

<!-- image -->

## ranking:

<!-- image -->

## image retrieval - evaluation

- 10 database images
- 5 relevant images, according to binary pairwise labels
- select a 'window' of top-k images
- measure precision @ k and recall @ k
- what should k be? should we use only one window?

<!-- image -->

<!-- image -->

recall

## query:

<!-- image -->

## ranking:

<!-- image -->

## image retrieval - evaluation

- 10 database images
- 5 relevant images, according to binary pairwise labels
- select a 'window' of top-k images
- measure precision @ k and recall @ k
- what should k be? should we use only one window?

<!-- image -->

<!-- image -->

<!-- image -->

recall

1

## query:

<!-- image -->

## ranking:

<!-- image -->

## image retrieval - evaluation

- 10 database images
- 5 relevant images, according to binary pairwise labels
- select a 'window' of top-k images
- measure precision @ k and recall @ k
- what should k be? should we use only one window?

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

recall

1

## query:

<!-- image -->

## ranking:

## image retrieval - evaluation

- 10 database images
- 5 relevant images, according to binary pairwise labels
- select a 'window' of top-k images
- measure precision @ k and recall @ k
- what should k be? should we use only one window?

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

recall

1

## query:

<!-- image -->

## ranking:

## image retrieval - evaluation

- 10 database images
- 5 relevant images, according to binary pairwise labels
- select a 'window' of top-k images
- measure precision @ k and recall @ k
- what should k be? should we use only one window?

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

recall

1

## query:

<!-- image -->

## ranking:

## image retrieval - evaluation

- 10 database images
- 5 relevant images, according to binary pairwise labels
- select a 'window' of top-k images
- measure precision @ k and recall @ k
- what should k be? should we use only one window?

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

1

## query:

<!-- image -->

## ranking:

## image retrieval - evaluation

- 10 database images
- 5 relevant images, according to binary pairwise labels
- select a 'window' of top-k images
- measure precision @ k and recall @ k
- what should k be? should we use only one window?

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## query:

<!-- image -->

## ranking:

## image retrieval - evaluation

- 10 database images
- 5 relevant images, according to binary pairwise labels
- select a 'window' of top-k images
- measure precision @ k and recall @ k
- what should k be? should we use only one window?

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

1

## query:

<!-- image -->

## ranking:

## image retrieval - evaluation

- 10 database images
- 5 relevant images, according to binary pairwise labels
- select a 'window' of top-k images
- measure precision @ k and recall @ k
- what should k be? should we use only one window?

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## query:

<!-- image -->

## ranking:

## image retrieval - evaluation

- 10 database images
- 5 relevant images, according to binary pairwise labels
- select a 'window' of top-k images
- measure precision @ k and recall @ k
- what should k be? should we use only one window?

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## query:

<!-- image -->

## ranking:

## image retrieval - evaluation

- 10 database images
- 5 relevant images, according to binary pairwise labels
- select a 'window' of top-k images
- measure precision @ k and recall @ k
- what should k be? should we use only one window?

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## visual representation

## visual representation - vector space

- map images to a high dimensional representation space
- image descriptor X f R D E
- function   is hand-crafted or learned f
- so that proximity reflects relevance
- retrieval is performed by nearest neighbor search
- how to obtain (global) image descriptors?
- let's revisit local features &amp; descriptors first…

<!-- image -->

<!-- image -->

## visual representation - local descriptors

<!-- image -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

## visual representation - local descriptors

- represent an image by a set of local descriptors

<!-- formula-not-decoded -->

<!-- image -->

<!-- formula-not-decoded -->

- obtain global descriptor as a function of a local descriptor set

<!-- formula-not-decoded -->

## visual representation - local descriptors

- represent an image by a set of local descriptors

<!-- formula-not-decoded -->

<!-- image -->

<!-- formula-not-decoded -->

- obtain global descriptor as a function of a local descriptor set

<!-- formula-not-decoded -->

- inherit their invariance properties
- robustness to occlusions and background clutter

## local features

<!-- image -->

<!-- image -->

## bag-of-words BoW

## bag-of-words - representation

- inspired by natural language processing
- text document represented by the set of words in it
- quantize the space of local descriptors
- eg. with k-means clustering
- each cluster is a visual word
- visual codebook: set of visual words (centroids)

<!-- image -->

```
[Sivic & Zisserman. ICCV'03] [Csurka et al. ECCVW'04]
```

## features (patches) in the same cluster

ClusterID:88646-Size:261

<!-- image -->

<!-- image -->

## bag-of-words - representation

- inspired by natural language processing
- text document represented by the set of words in it
- quantize the space of local descriptors
- eg. with k-means clustering
- each cell (cluster) is a visual word
- visual codebook: set of visual words (centroids)
- assign local descriptors to visual words
- according to the nearest centroid
- histogram of visual word occurrences (term-frequency) per image

<!-- image -->

```
[Sivic & Zisserman. ICCV'03] [Csurka et al. ECCVW'04]
```

<!-- image -->

## local features with the same visual word

<!-- image -->

<!-- image -->

<!-- image -->

## bag-of-words - similarity

<!-- image -->

<!-- formula-not-decoded -->

bag of words representation

## bag-of-words - similarity

<!-- image -->

<!-- formula-not-decoded -->

bag of words representation

<!-- image -->

## bag-of-words - similarity

<!-- image -->

## bag-of-words - similarity

<!-- image -->

## local features with the same visual word

<!-- image -->

<!-- image -->

## local features with the same visual word

<!-- image -->

<!-- image -->

## local features with the same visual word

<!-- image -->

<!-- image -->

## local features with the same visual word

<!-- image -->

<!-- image -->

## bag-of-words - similarity

<!-- image -->

<!-- formula-not-decoded -->

bag of words representation

## bag-of-words - similarity

<!-- image -->

<!-- formula-not-decoded -->

bag of words representation

<!-- image -->

## bag-of-words - similarity

<!-- image -->

## bag-of-words - similarity

<!-- image -->

## bag-of-words - similarity

<!-- image -->

<!-- formula-not-decoded -->

bag of words representation

<!-- formula-not-decoded -->

- inverse-document-frequency (idf):
- multiply dimension   with i wi = log # images # images with word i
- down-weighs highly populated visual words

<!-- image -->

## cluster sizes

<!-- image -->

## cluster size = 312

ClusterID:2596-Size:312

<!-- image -->

## cluster size = 92

ClusterID:4070-Size:92

<!-- image -->

## cluster size = 92

ClusterID:39426-Size:92

<!-- image -->

## bag-of-words - retrieval

<!-- image -->

- efficient computation by skipping zero elements
- inverted-file structure
- image-id list per visual word
- contains images with that word
- query time: visit only lists of words in the query

| score   | image ID   |
|---------|------------|
| 0.87    | 5          |
| 0.75    | 1573       |
| 0.52    | 11202      |
| …       | …          |
| 0.001   | 32         |

<!-- image -->

- small (eg. 128)
- dense representation: compatible with approximate NN search
- memory: #images x codebook-size x descriptor-element-footprint
- appropriate for category-level matching
- very large (eg. 10 6 )
- sparse representation: use of inverted-file
- memory: total-number-of-features x image-id-footprint
- appropriate for instance-level matching

<!-- image -->

<!-- image -->

## impact of codebook size

## bag-of-words - example

- local descriptors mapped to the same visual word for different codebook size

<!-- image -->

<!-- image -->

64 visual words

<!-- image -->

<!-- image -->

<!-- image -->

10 3  visual words

<!-- image -->

10 6  visual words

## BoW &amp; other approaches

from a different point of view

## bag-of-words

<!-- formula-not-decoded -->

- local embedding: Φ(x) = [0,..., 1 X&amp; assigned to word q(x) q(x)-th element

<!-- image -->

[0 0 0 1]

[1 0 0 0]

[0 0 1 0]

D

A

C

VU

w

CONDENSED

O

U

TOMAT

P

[1 0 1 1]

## bag-of-words

<!-- formula-not-decoded -->

- local embedding: Φ(x) = [0,..., 1 X&amp; assigned to word q(x) q(x)-th element

<!-- image -->

[0 0 0 1]

[1 0 0 0]

[0 0 1 0]

D

A

C

VU

w

CONDENSED

O

U

TOMAT

P

[1 0 1 1]

## bag-of-words

<!-- image -->

- local embedding: Φ(x) = [0,..., 1 X&amp; assigned to word q(x) q(x)-th element

<!-- image -->

## bag-of-words

<!-- image -->

- local embedding: Φ(x) = [0,..., 1 X8 assigned to word q(x) q(x)-th element

<!-- image -->

## bag-of-words

<!-- image -->

- local embedding: [0, 1, 01 T X &amp; assigned to word q(x) q(x)-th e element
- same result achieved in two ways:
- voting approach: accumulate local similarity of all pairs
- dot product of two vectors (efficient)
- accumulate 0 if different visual word, 1 (or idf) if same visual word
- what about more fine-grained votes?

## vector of locally aggregated descriptors (VLAD)

- fine-grained votes equal Ito
- 0 if c q(x)≠ ≠q(y)( (different visual words)
- r(x) )Tr(y), if q(x) = = q(y) (same visual word)
- residual vector r(x) = x - Cq(x)
- local embedding (x)Φ = [oT oTjT X q(x)-th sub-vector

<!-- image -->

## vector of locally aggregated descriptors (VLAD)

- voting approach
- intuitive but inefficient

<!-- formula-not-decoded -->

- global descriptor similarity
- efficient via a dot product (dK c dimensions

<!-- formula-not-decoded -->

<!-- image -->

## vector of locally aggregated descriptors (VLAD)

- global descriptor similarity
- sum to obtain global descriptors
- dot product for similarity
- non-binary votes
- according to descriptor similarity
- voting approach

<!-- image -->

<!-- image -->

<!-- image -->

## VLAD and related approaches

- VLAD variations
- use L2 normalized residuals [Delhumeau et al. ACMMM'13]
- only angles matter
- L2 normalization of each d-dimensional VLAD sub-vector
- handles features from repeating patterns
- -[Arandjelovic &amp; Zisserman, CVPR'13]
- Fisher vectors [Perronnin et al. CVPR'10]
- Gaussian-Mixture-Model instead of k-means
- different derivation: gradient log-likelihood of local descriptors
- soft-assign to all visual words
- residual vectors normalized (divided) by cluster variance

## selective match kernel (SMK)

- use a local similarity function to estimate votes

<!-- formula-not-decoded -->

- equivalently iterate over common visual words W between X and J

<!-- formula-not-decoded -->

- non-linear local similarity function (more selective votes)

<!-- formula-not-decoded -->

<!-- image -->

- only / seen as a voting approach
- no equivalence to global descriptor. why?

## impact of the local similarity function

- numerical example:
- ▪
- ▪
- ▪
- exponent ▪ [0.5 0.5 0.5 0.5 0.5] → 2.5 ▪ [0.7 0.7 0.7 0.2 0.2] → 2.5 exponent ▪ [0.5 0.5 0.5 0.5 0.5] → 1.25 ▪ [0.7 0.7 0.7 0.2 0.2] → 1.55 exponent ▪ [0.5 0.5 0.5 0.5 0.5] → 0.62 ▪ [0.7 0.7 0.7 0.2 0.2] → 1.05 α = 1 α = 2 α = 3

## SMK - retrieval

<!-- image -->

- lists of (image-id, residual vectors) per visual word
- iterate over elements of relevant lists (of query visual word)
- dot product between query and db-image vectors
- use local similarity function
- accumulate votes per db-image

<!-- image -->

## ▪ BoW

- very large codebook (eg. 10 6 )
- compatible with inverted-file
- lower memory requirements than SMK but less precise
- provides tentative correspondences

## ▪ VLAD

- small codebook (eg. 128)
- dimensionality reduction
- small memory footprint
- efficient search
- -compatible with approximate nearest neighbor search methods

## ▪ SMK

- large codebook (eg. 65k)
- compatible with inverted-file
- memory demanding and slower search than BoW but better performance
- provides tentative correspondences

## settings for identical object retrieval

## fast spatial matching

## spatial matching and verification

- RANSAC-like approach to find inlier correspondences
- find the geometric transformation with the largest number of inliers
- use the number of inliers as image-to-image similarity
- 1st stage of retrieval: rank all images with BoW
- 2nd stage: re-rank top-ranked images according to the number of inliers
- efficiency is important → method inspired by RANSAC but sped-up

query

<!-- image -->

top retrieved

## spatial verification: input - output

input: tentative correspondences based on visual words

out: inlier correspondences also geometric transformation but that's not what we are after

<!-- image -->

## preliminaries: 2D image-to-image transformations

- 2D transformations as linear transformations in homogeneous coordinates

̂

<!-- formula-not-decoded -->

̂

- homogeneous coordinates: [

x , y ,1] ⊤

- represent a 2D transformation as a 3x3 matrix F

̂

̂

<!-- image -->

̂

## preliminaries: 2D transformations

- translation in 2D cartesian coordinates

̂

<!-- formula-not-decoded -->

- translation in homogenous coordinates

̂

<!-- formula-not-decoded -->

̂

- rotation in homogenous coordinates

̂

<!-- formula-not-decoded -->

̂

- rotation &amp; translation in homogenous coordinates

̂

<!-- formula-not-decoded -->

̂

̂

## preliminaries: 2D transformations

- Euclidean/rigid transformation (3 DoF) - preserves distances and angles

̂

<!-- formula-not-decoded -->

- similarity transformation (4 DoF) - preserves angles, not distances

̂

<!-- formula-not-decoded -->

̂

- affine transformation (6 DoF) - preserves parallel lines, not angles/distances

̂

<!-- formula-not-decoded -->

̂

## point correspondences vs local feature correspondences 55

- point correspondences: ( x , y ) ↔ ( x ′ , y ′ )
- local feature correspondences: ( A , x , y ) ↔ ( A ′ , x ′ , y ′ )
- represents the shape of the local feature A
- eg. scale and rotation, affine shape

<!-- image -->

<!-- image -->

## point correspondences vs local feature correspondences 55

- point correspondences: ( x , y ) ↔ ( x ′ , y ′ )
- local feature correspondences: ( A , x , y ) ↔ ( A ′ , x ′ , y ′ )
- represents the shape of the local feature A
- eg. scale and rotation, affine shape

<!-- image -->

<!-- image -->

## transformation hypothesis

- sample the minimum number of correspondences required to estimate the parameters of the geometric transformation
- one correspondece → two equations
- similarity transformation  (4 DoF) → 2 correspondences

<!-- formula-not-decoded -->

- affine transformation (6 DoF) → 3 correspondences

<!-- image -->

<!-- image -->

̂

̂

## transformation hypothesis

- sample the minimum number of correspondences required to estimate the parameters of the geometric transformation
- one correspondece → two equations
- similarity transformation  (4 DoF) → 2 correspondences

<!-- formula-not-decoded -->

- affine transformation (6 DoF) → 3 correspondences

<!-- image -->

<!-- image -->

̂

̂

## transformation hypothesis from a single correspondence 57

- estimate the transformation hypothesis from a single correspondence
- scale and rotation invariant local features → similarity transformation
- affine invariant local features → affine transformation

<!-- image -->

<!-- image -->

## transformation hypothesis from a single correspondence 57

- estimate the transformation hypothesis from a single correspondence
- scale and rotation invariant local features → similarity transformation
- affine invariant local features → affine transformation

<!-- image -->

<!-- image -->

## transformation hypothesis from a single correspondence 57

- estimate the transformation hypothesis from a single correspondence
- scale and rotation invariant local features → similarity transformation
- affine invariant local features → affine transformation

<!-- image -->

<!-- image -->

## spatial verification

- estimate the transformation hypothesis from a single correspondence
- scale and rotation invariant local features → similarity transformation
- affine invariant local features → affine transformation

<!-- image -->

<!-- image -->

## spatial verification

- estimate the transformation hypothesis from a single correspondence
- scale and rotation invariant local features → similarity transformation
- affine invariant local features → affine transformation

<!-- image -->

## spatial verification

- estimate the transformation hypothesis from a single correspondence
- scale and rotation invariant local features → similarity transformation

<!-- image -->

## spatial verification

- estimate the transformation hypothesis from a single correspondence
- scale and rotation invariant local features → similarity transformation
- affine invariant local features → affine transformation

<!-- image -->

## spatial verification

- estimate the transformation hypothesis from a single correspondence
- scale and rotation invariant local features → similarity transformation
- affine invariant local features → affine transformation

<!-- image -->

## spatial verification

- estimate the transformation hypothesis from a single correspondence
- scale and rotation invariant local features → similarity transformation
- affine invariant local features → affine transformation

<!-- image -->

## spatial verification

- estimate the transformation hypothesis from a single correspondence
- scale and rotation invariant local features → similarity transformation
- affine invariant local features → affine transformation

<!-- image -->

## spatial verification

- estimate the transformation hypothesis from a single correspondence
- scale and rotation invariant local features → similarity transformation
- affine invariant local features → affine transformation

<!-- image -->

̂

## conventional RANSAC

- correspondence c i = ( x i , y i ) ↔ ( x ′ i , y ′ i )
- correspondence set C = { c 1 , c 2 , … c n }

## conventional RANSAC with point correspondences

- for j in 1…T # max number of hypotheses
- sample a minimal set from # size depends on DoFs Cm C
- estimate from # inlier free sample for good estimate F Cm
- for   in 1…n # loop over all correspondences i

̂

<!-- formula-not-decoded -->

̂

- is\_inlier = error # error between projected and given point ([ x i , y i ], [ x ′ i , y ′ i ]) &lt; τ

̂

- …… # inlier count, track with most inliers, early termination, … F

̂

## fast spatial matching

- correspondence c i = ( Ai , x i , y i ) ↔ ( A ′ i , x ′ i , y ′ i )
- correspondence set C = { c 1 , c 2 , … c n }

## fast spatial matching with local feature correspondences

- for   in 1…n # loop over all correspondences j
- estimate from   # single correspondence hypothesis F c j
- for   in 1…n # loop over all correspondences no randomness

̂

<!-- formula-not-decoded -->

- ‣ # transform points from an image to the other i

̂

- is\_inlier = error # error between projected and corresponding point ([ x i , y i ], [ x ′ i , y ′ i ]) &lt; τ

̂

- …… # inlier count, track with most inliers, early termination, … F

## transformation hypothesis verification - inlier counting 61

<!-- image -->

<!-- image -->

## transformation hypothesis verification - inlier counting 61

<!-- image -->

## transformation hypothesis verification - inlier counting 61

<!-- image -->

## transformation hypothesis verification - inlier counting 61

<!-- image -->

## transformation hypothesis verification - inlier counting 61

<!-- image -->

## transformation hypothesis verification - inlier counting 61

<!-- image -->

## transformation hypothesis verification - inlier counting 61

<!-- image -->

## transformation hypothesis verification - inlier counting 61

<!-- image -->

## transformation hypothesis verification - inlier counting 61

<!-- image -->

## transformation hypothesis verification - inlier counting 61

<!-- image -->

## spatial verification - retrieval

<!-- image -->

[Philbin et al. CVPR'07]

[Perdoch et al. CVPR'09]

## special retrieval tasks

## beyond visual similarity retrieval

- most similar images: near identical
- is this what we want?

<!-- image -->

<!-- image -->

query 1

<!-- image -->

query 2

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## beyond visual similarity retrieval

let's zoom-in!

<!-- image -->

<!-- image -->

## image retrieval for zoom-in

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## image retrieval for zoom-in

<!-- image -->

## image retrieval for zoom-in

<!-- image -->

<!-- image -->

## image retrieval for zoom-in

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## image retrieval for zoom-in

<!-- image -->

<!-- image -->

## image retrieval for zoom-in

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## image retrieval for zoom-in

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## image retrieval for zoom-out

<!-- image -->

<!-- image -->

## zoom in/out

<!-- image -->

## zoom in/out

<!-- image -->

problem specific ranking function, e.g. maximize scale change

## zoom in/out

1. inverted file: posting list per visual word

## 2. Image ranking

<!-- image -->

geometry compressed in inverted file taken into account during scoring

problem specific ranking function, e.g. maximize scale change

## what should you not miss?

<!-- image -->

## highest resolution transform

- given a query, for every pixel in the query image:
- find  the  database  image  with  the  maximum  resolution  depicting the pixel

<!-- image -->

## retrieval for 3D reconstruction

- visually most similar search
- many near duplicates
- details lost
- zoom-in and details search
- details retrieved
- transition images to match the details
- zoom-out search
- viewpoint change
- more context
- sideways crawl
- significant viewpoint change
- more context

<!-- image -->

<!-- image -->

## sideways image crawl

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## sideways left: step by step

<!-- image -->

## sideways left: step by step

<!-- image -->

<!-- image -->

## sideways left: step by step

<!-- image -->

## sideways left: step by step

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## summary

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

visually most similar

<!-- image -->

zoom-in / details

<!-- image -->

zoom-out

<!-- image -->

<!-- image -->

<!-- image -->

sideways right

## 3D reconstruction - from a single image

<!-- image -->

## 3D reconstruction - from a single image

<!-- image -->

## questions

<!-- image -->

- BoW
- J Sivic, A Zisserman, Video Google: A text retrieval approach to object matching in videos, ICCV 2003
- G Csurka, C Dance, L Fan, J Willamowski, C Bray, Visual categorization with bags of keypoints, ECCVW 2004
- VLAD
- H Jegou, M Douze, C Schmid, P Pérez, Aggregating local descriptors into a compact image representation, CVPR 2010
- J Delhumeau, PH Gosselin, H Jégou, P Pérez, Revisiting the VLAD image representation, ACMMM 2013
- Fisher vectors
- F Perronnin, Y Liu, J Sánchez, H Poirier, Large-scale image retrieval with compressed fisher vectors CVPR 2010
- SMK / Hamming Embedding
- G Tolias, Y Avrithis, H Jégou, To aggregate or not to aggregate: Selective match kernels for image search ICCV 2013
- H Jegou, M Douze, C Schmid, Hamming embedding and weak geometric consistency for large scale image search, CVPR 2010
- spatial verification
- J Philbin, O Chum, M Isard, J Sivic, A Zisserman, Object retrieval with large vocabularies and fast spatial matching, CVPR 2007
- M Perdoch, O Chum, J Matas, Efficient representation of local geometry for large scale object retrieval, CVPR 2009
- other retrieval tasks
- A Mikulık, F Radenovic, O Chum, J Matas, Efficient Image Detail Mining, ACCV 2014
- JL Schonberger, F Radenovic, O Chum, JM Frahm, From single image query to detailed 3D reconstruction, CVPR 2015

## bibliography