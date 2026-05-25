## self-supervised representation learning

Computer Vision Methods 2024 CTU in Prague

Giorgos Tolias

## visual representation

- § visual representation: at the core of every computer vision task
- global image representation - single vector
- retrieval, classification
- dense image representation - 3D tensor
- segmentation, detection, depth prediction

follow-up processing with task-specific blocks (heads)

<!-- image -->

backbone

- § the backbone requires lots of training data à use self-supervision
- train one backbone and use for many final tasks
- § heads can be trained with fewer data given a good representation

## SSL pre-training and task-related fine-tuning

<!-- image -->

<!-- image -->

- § auto-encoders
- input is the output label
- § concealed-restored information
- concealed part of the input is the output label
- § exploit spatial/temporal context
- relation between parts of the input is the label
- § instance discrimination / multi-view invariance
- each image constitutes a class
- § image collection processing
- joint processing of many images provides labels
- discovery of repeating patterns/parts/objects
- -non-exhaustive listing of method types
- -non-exhaustive listing of methods - the literature is vast

[Balestriero, A Cookbook of Self-Supervised Learning. arxiv 2023]

## SSL method types

## auto-encoders

- §

## auto-encoder

<!-- image -->

- § reconstruct the input at the output
- pixel-wise mean-squared error as loss
- reconstruction works à representation captures structures/regularities of the input data
- § denoising auto-encoder
- add noise to the input: remove the effect of stochastic corruption
- better representation

## concealed-restored information

## colorization

<!-- image -->

- § use Lab color space
- § L in the input à predict ab at the output
- § cast as classification task
- better than regression
- § the better the colorization performance
- the better the internal representation

<!-- image -->

## colorization

- § the last layer is not the best at generalization
- § use the learned representation and fine-tune for other tasks
- classification
- detection
- segmentation

<!-- image -->

| Dataset and Task Generalization on PASCAL [37]   | Dataset and Task Generalization on PASCAL [37]   | Dataset and Task Generalization on PASCAL [37]   | Dataset and Task Generalization on PASCAL [37]   | Dataset and Task Generalization on PASCAL [37]   | Dataset and Task Generalization on PASCAL [37]   | Dataset and Task Generalization on PASCAL [37]   | Dataset and Task Generalization on PASCAL [37]   | Dataset and Task Generalization on PASCAL [37]   |
|--------------------------------------------------|--------------------------------------------------|--------------------------------------------------|--------------------------------------------------|--------------------------------------------------|--------------------------------------------------|--------------------------------------------------|--------------------------------------------------|--------------------------------------------------|
|                                                  |                                                  | Class. (%mAP)                                    | Class. (%mAP)                                    |                                                  | Det. (%mAP)                                      | Det. (%mAP)                                      | Seg. (%mIU)                                      | Seg. (%mIU)                                      |
| fine-tune layers                                 | [Ref]                                            | fc8                                              | fc6-8                                            | all                                              | [Ref]                                            | all                                              | [Ref]                                            | all                                              |
| ImageNet [38]                                    |                                                  | 76.8                                             | 78.9                                             | 79.9                                             | [36]                                             | 56.8                                             | [42]                                             | 48.0                                             |
| Gaussian                                         | [10]                                             | 一                                               | 一                                               | 53.3                                             | [10]                                             | 43.4                                             | [10]                                             | 19.8                                             |
| Autoencoder                                      | [16]                                             | 24.8                                             | 16.0                                             | 53.8                                             | [10]                                             | 41.9                                             | [10]                                             | 25.2                                             |
| k-means [36]                                     | [16]                                             | 32.0                                             | 39.2                                             | 56.6                                             | [36]                                             | 45.6                                             | [16]                                             | 32.6                                             |
| Ours (gray)                                      |                                                  |                                                  | 52.4 61.5                                        | 65.9                                             | 一                                               | 46.1                                             | 一                                               | 35.0                                             |
| Ours (color)                                     |                                                  |                                                  | 52.4 61.5 65.6                                   |                                                  |                                                  | 46.9                                             | 一                                               | 35.6                                             |

## inpainting

- § hide a part of the input à reconstruct it at the output
- § reconstruction loss + adversarial loss (sharper results)
- discriminator network predicts whether an image is real or synthetic
- two player game as in GANs

<!-- image -->

<!-- image -->

(a) Input context

<!-- image -->

(c)ContextEncoder (L2 loss)

<!-- image -->

<!-- image -->

(a) Central region

(b) Random block

<!-- image -->

<!-- image -->

(c) Random region

<!-- image -->

<!-- image -->

(b) Human artist

<!-- image -->

(d) ContextEncoder (L2+Adversarial loss)

[Pathak, Context Encoders: Feature Learning by Inpainting, CVPR2016]

## masked auto-encoder (mae)

<!-- image -->

- § similar to denoising auto-encoders / inpainting: tailored for ViT
- mask-out some of the input patches
- reconstruct them at the output
- § asymmetric encoder-decoder operation
- encoder: operates on non masked patches
- ·
- decoder: operates on all patches - learnable mask token included [He, Masked Autoencoders Are Scalable Vision Learners, CVPR2022]

## masked auto-encoders (mae)

- § do not allow to solve by extrapolation of visible patches
- large masking ratio
- random samples for masking
- § even if wrong, semantically plausible reconstructions
- representation captures semantics

<!-- image -->

<!-- image -->

block 50%

random 75%

<!-- image -->

grid 75%

<!-- image -->

[He, Masked Autoencoders Are Scalable Vision Learners, CVPR2022]

## masked auto-encoder (mae)

<!-- image -->

blocks

blocks

1

1

2

2

4

4

8

8

12

ft

84.8

84.8

84.9

84.9

84.9

84.9

84.9

84.9

84.4

lin

lin

65.5

65.5

70.0

70.0

71.9

71.9

73.5

73.5

73.3

12

84.4

73.3

der depth. A deep decoder can imear probing accuracy. (a) Decoder depth. A deep decoder can improve linear probing accuracy.

| case   |   ratio |   ft |   lin |
|--------|---------|------|-------|
| random |      75 | 84.9 |  73.5 |
| block  |      50 | 83.9 |  72.3 |
| block  |      75 | 82.8 |  63.9 |
| grid   |      75 | 84.0 |  66.0 |

- (f) Mask sampling. Random sampling works the best. See Figure 6 for visualizations.

[He, Masked Autoencoders Are Scalable Vision Learners, CVPR2022]

## exploit spatial/temporal context

## context prediction

- § choose a deformed 3 x 3 grid of image regions
- § input: central region + a second region
- à predict the position of the second region

<!-- image -->

<!-- image -->

## context prediction

- § chromatic aberration: failure of a lens to focus all colors to the same point
- § deep networks are good at finding solution shortcuts
- task solved through learning chromatic aberration patterns
- -no useful representation learned
- skip 2 out of 3 color channels
- -good representation learned

<!-- image -->

<!-- image -->

## predicting object rotations (rotnet)

- § assumption: people typically take photos of upright objects
- § rotate images and use object orientation as label

<!-- image -->

## predicting object rotations (rotnet)

|   # Rotations | Rotations                           |   CIFAR-10 Classification Accuracy |
|---------------|-------------------------------------|------------------------------------|
|             4 | 0°,90°, 180°, 270°                  |                              89.06 |
|             8 | 0°,45°,90°,135°,180°,225°,270°,315° |                              88.51 |
|             2 | 0°,180°                             |                              87.46 |
|             2 | 90°, 270°                           |                              85.52 |

| Method                                           |   Conv4 |   Conv5 |
|--------------------------------------------------|---------|---------|
| ImageNet labels from (Bojanowski & Joulin, 2017) |    59.7 |    59.7 |
| Random from (Noroozi & Favaro, 2016)             |    27.1 |    12.0 |
| Tracking Wang & Gupta (2015)                     |    38.8 |    29.8 |
| Context (Doersch et al.l 2015)                   |    45.6 |    30.4 |
| Colorization (Zhang et al.),2 2016a]             |    40.7 |    35.2 |
| Jigsaw Puzzles (Noroozi & Favaro, 2016)          |    45.3 |    34.6 |
| BIGAN (Donahue et al., 2016)                     |    41.9 |    32.2 |
| NAT (Bojanowski & Joulin, 2017)                  |         |    36.0 |
| (Ours) RotNet                                    |    50.0 |    43.8 |

## video tracking for positive examples

- § representation learning with triplet loss: as in deep metric learning
- § use video frames as training data
- negatives: frame region far enough in time
- positives: output of a video tracking algorithm

<!-- image -->

## instance discrimination multi-view invariance

## instance discrimination

- § each image (and all of its augmentations) forms a class by itself
- § optimize non-parametric soft-max classifier
- a type of contrastive loss
- § cannot process all training images in a batch

<!-- formula-not-decoded -->

- memory of previously extracted representations
- works despite inconcistency of the representation extraction

<!-- image -->

| Training / Testing   |      |   LinearSVM&#124;NearestNeighbor |
|----------------------|------|----------------------------------|
| Param Softmax        | 60.3 |                             63.0 |
| Non-Param Softmax    | 75.4 |                             80.8 |
| NCE m = 1            | 44.3 |                             42.5 |
| NCE m = 10           | 60.2 |                             63.4 |
| NCE m = 512          | 64.3 |                             78.4 |
| NCE m = 4096         | 70.2 |                             80.4 |

## momentum contrast - moco

- § train with contrastive loss for instance discrimination
- end-to-end: memory size coupled with mini-batch size
- memory bank: old entry inconsistency &amp; no memory back-prop
- queue &amp; momentum encoder: 0k m0k + (1 be(u ↑ 一
- reuse examples from the preceding mini-batches
- slowly progressing encoder for the memory

[He, Momentum Contrast for Unsupervised Visual Representation Learning , CVPR2020]

<!-- image -->

## moco

## Algorithm 1 Pseudocode of MoCo in a PyTorch-like style.

```
# f_q, f_k: encoder networks for query and key # queue: dictionary as a queue of K keys (CxK) # m: momentum # t: temperature f_k.params = f_q.params # initialize for x in loader: # load a minibatch x with N samples x_q = aug(x) # a randomly augmented version x_k = aug(x) # another randomly augmented version q = f_q.forward(x_q) # queries: NxC k = f_k.forward(x_k) # keys: NxC k = k.detach() # no gradient to keys # positive logits: Nxl l_pos = bmm(q.view(N,l,C), k.view(N,C,l)) # negative logits: NxK 1_neg = mm(q.view(N,C), queue.view(C,K)) # logits: Nx(l+K) logits = cat([l_pos, l_neg], dim=l) # contrastive loss, Eqn.(1) labels = zeros(N) # positives are the O-th loss = CrossEntropyLoss(logits/t, labels) # SGD update: query network loss.backward() update(f_q.params) # momentum update: key network f_k.params = m*f_k.params+(l-m) *f_q.params # update dictionary enqueue(queue, k) # enqueue the current minibatch dequeue(queue) # dequeue the earliest minibatch
```

bmm: batch matrix multiplication; mm: matrix multiplication; cat: concatenation.

<!-- image -->

## simple framework for contrastive learning - simclr

- § end-to-end approach
- no memory or asymmetric encoding
- large batch through hardware support
- § introduce disposable projection block
- used for training and then removed
- internal representation generalizes better
- § composition of augmentations is a key

<!-- image -->

<!-- image -->

## simple framework for contrastive learning - simclr

<!-- image -->

2nd transformation

## simple framework for contrastive learning - simclr

[Chen, A Simple Framework for Contrastive Learning of Visual Representations, ICML2020]

<!-- image -->

## redundancy reduction - Barlow twins

- § invariance term: standard term of matching the positives
- § redundancy term: decorrelate the representation dimensions

<!-- image -->

## variance-invariance-covariance regularization - VICreg

v(z)

<!-- image -->

- Invariance: the mean square distance between the embedding vectors.
- Variance: a hinge loss to maintain the standard deviation (over a batch) of each variable of the embedding above a given threshold. This term forces the embedding vectors of samples within a batch to be different.
- Covariance: a term that attracts the covariances (over a batch) between every pair of (centered) embedding variables towards zero. This term decorrelates the variables of each embedding and prevents an informational collapse in which the variables would vary together or be highly correlated.

[Bardes, VICREG: VARIANCE-INVARIANCE-COVARIANCE REGULARIZATION FOR SELFSUPERVISED LEARNING, ICLR2022]

:maintain variance

C

: bring covariance to zero

S

:minimize distance

T

:distributionoftransformations

t,t'

:randomtransformations

fe,f'e, :encoders

h+, h' o: expanders

1

: batch of images

X, X': batches of views

Y, Y':batches of representations

Z, Z': batches of embeddings

## variance-invariance-covariance regularization - VICreg 34

- § on par with previous approaches, but
- simpler to implement
- more intuitive

|                          | Linear Classification   |   Linear Classification |   Linear Classification | Object Detection           | Object Detection   | Object Detection   |
|--------------------------|-------------------------|-------------------------|-------------------------|----------------------------|--------------------|--------------------|
| Method                   | Places205 VOC07 iNat18  |                         |                         | VOC07+12 COCO det COCO seg |                    |                    |
| Supervised               | 53.2                    |                    87.5 |                    46.7 | 81.3                       | 39.0               | 35.4               |
| MoCo [22]                | 46.9                    |                    79.8 |                    31.5 |                            | 一                 | 一                 |
| PIRL [33]                | 49.8                    |                    81.1 |                    34.1 | -                          |                    | -                  |
| SimCLR [8]               | 52.5                    |                    85.5 |                    37.2 |                            |                    | 一                 |
| MoCo v2 [10]             | 51.8                    |                    86.4 |                    38.6 | 82.5                       | 39.8               | 36.1               |
| SimSiam [11]             |                         |                         |                         | 82.4                       |                    | -                  |
| BYOL [21]                | 54.0                    |                    86.6 |                    47.6 |                            | 40.4t              | 37.0t              |
| SwAV (w/ multi-crop) [7] | 56.7                    |                    88.9 |                    48.6 | 82.6                       | 41.6               | 37.8               |
| Barlow Twins [21]        | 54.1                    |                    86.2 |                    46.5 | 82.6                       | 40.0t              | 36.7t              |
| VICReg (ours)            | 54.3                    |                    86.6 |                    47.0 | 82.4                       | 39.4               | 36.4               |

## SSL of local representation - VICregL

- § targets dense prediction tasks:
- VICreg + loss on local representation

<!-- image -->

## SSL of local representation - VICregL

- § targets dense prediction tasks:
- VICreg + loss on local representation
- § corresponding/positive locations given by
- the relative geometric transformation
- neighbors in the representation space

<!-- image -->

<!-- image -->

[Bardes, VICRegL: Self-Supervised Learning of Local Visual Features , NeurIPS2022]

## SSL of local representation - VICregL

- § good performance for global and for dense prediction tasks

|                              | Linear Cls. (%)   | Linear Cls. (%)   | Linear Seg. (mIoU)   | Linear Seg. (mIoU)   | Linear Seg. (mIoU)   |
|------------------------------|-------------------|-------------------|----------------------|----------------------|----------------------|
|                              |                   | ImageNet          | Pascal VOC           | Pascal VOC           | Cityscapes           |
| Method                       | Epochs            | Frozen            | Frozen               | Fine-Tuned           | Frozen               |
| Global features              |                   |                   |                      |                      |                      |
| MoCo v2 [Chen et al., 2020b] | 200               | 67.5              | 35.6                 | 64.8                 | 14.3                 |
| SimCLR [Chen et al., 2020a]  | 400               | 68.2              | 45.9                 | 65.4                 | 17.9                 |
| BYOL [Grill et al., 2020]    | 300               | 72.3              | 47.1                 | 65.7                 | 22.6                 |
| VICReg [Bardes et al., 2022] | 300               | 71.5              | 47.8                 | 65.5                 | 23.5                 |
| Local features               |                   |                   |                      |                      |                      |
| PixPro [Xie et al., 2021]    | 400               | 60.6              | 52.8                 | 67.5                 | 22.6                 |
| DenseCL [Wang et al., 2021]  | 200               | 65.0              | 45.3                 | 66.8                 | 11.2                 |
| DetCon [Hénaff et al., 2021] | 1000              | 66.3              | 53.6                 | 67.4                 | 16.2                 |
| InsLoc [Yang et al., 2022]   | 400               | 45.0              | 24.1                 | 64.4                 | 7.0                  |
| CP2 [Wang et al., 2022]      | 820               | 53.1              | 21.7                 | 65.2                 | 8.4                  |
| ReSim [Xiao et al., 2021]    | 400               | 59.5              | 51.9                 | 67.3                 | 12.3                 |
| Ours                         |                   |                   |                      |                      |                      |
| VICRegL α = 0.9              | 300               | 71.2              | 54.0                 | 66.6                 | 25.1                 |
| VICRegL Q = 0.75             | 300               | 70.4              | 55.9                 | 67.6                 | 25.2                 |

## object discovery and dense representation networks

[Henaff : Object discovery and representation networks, ECCV'22 ]

<!-- image -->

## image collection processing

## deep clusters as supervision

- § assumption: common objects repeat in the training set
- § clustering of the current representation à pseudo-labels
- § iterative process (network and pseudo-labels get improved):
- clustering à training à clustering à …
- § no domain knowledge
- does not rely on well designed augmentations for positives

<!-- image -->

[Mathilde Caron, Piotr Bojanowski, Armand Joulin, and Matthijs Douze , Deep Clustering for Unsupervised Learning of Visual Features, ECCV2018]

## deep clusters as supervision

<!-- image -->

[Mathilde Caron, Piotr Bojanowski, Armand Joulin, and Matthijs Douze , Deep Clustering for Unsupervised Learning of Visual Features, ECCV2018]

## deep clusters as supervision

- § intermediate number of clusters is the optimal
- § mutual information between clusters and class labels increases

<!-- image -->

<!-- image -->

[Mathilde Caron, Piotr Bojanowski, Armand Joulin, and Matthijs Douze , Deep Clustering for Unsupervised Learning of Visual Features, ECCV2018]

## neighbors as positives

- § assumption: repeating objects
- use them for positives: realistic compared to augmentations

<!-- image -->

[Dwibedi, With a Little Help from My Friends: Nearest-Neighbor Contrastive Learning of Visual Representations]

## neighbors as positives

- § search requires same representation model for query and database
- re-processing takes time
- using previously processed examples: inconsistent representation
- § use queue with momentum encoder

| Queue Size   | 8192      | 16384     | 32768     | 65536     | 98304     |
|--------------|-----------|-----------|-----------|-----------|-----------|
| Top-1 Top-5  | 73.6 91.2 | 74.2 91.7 | 74.9 92.1 | 75.0 92.2 | 75.4 92.3 |
| k in k-NN    | 1         | 2         | 4 8       | 16        | 32        |
| Top-1 S-don  | 74.9 92.1 | 74.1 91.6 | 73.8 73.8 | 73.8 91.3 | 73.2 91.2 |
|              |           |           | 91.5 91.4 |           |           |

[Dwibedi, With a Little Help from My Friends: Nearest-Neighbor Contrastive Learning of Visual Representations, ICCV'21]

## ssl for fine-tuning

## mining (neighbors) on manifolds

- § rely on manifold distance instead of Euclidean distance
- § mine positives and negatives
- § focus on hard-examples
- differences between Euclidean and manifold neighbors

<!-- image -->

[Iscen, Mining on Manifolds: Metric Learning without Labels, CVPR2018]

## mining on manifolds

<!-- image -->

[Iscen, Mining on Manifolds: Metric Learning without Labels, CVPR2018]

## MoM: discovery of training pairs from 10 6 images

<!-- image -->

## self-taught deep metric learning

- § teacher-student scheme with a strong teacher
- EMA teacher (momentum encoder)
- larger dinensionality of the teacher representation
- use of contextual similarity: improved compared to Euclidean
- § relaxed contrastive loss: uses soft teacher labels

[Kim, Self-Taught Metric Learning without Labels , CVPR2022]

<!-- image -->

## self-taught deep metric learning

|           |       | CUB   | Cars   | SOP   |
|-----------|-------|-------|--------|-------|
| Methods   | Arch. | R@1   | R@1    | R@1   |
| MoCo [20] | G128  | 48.3  | 37.2   | 53.3  |
| BYOL [18] | G128  | 47.7  | 31.5   | 48.7  |
| MSF [31]  | G128  | 46.0  | 30.5   | 41.6  |
| STML      | G128  | 59.7  | 49.0   | 65.8  |
| MoCo [20] | G512  | 51.0  | 39.0   | 53.4  |
| BYOL [18] | G512  | 50.9  | 38.5   | 51.2  |
| MSF [31]  | G512  | 49.6  | 32.5   | 47.8  |
| STML      | G512  | 60.6  | 50.5   | 65.3  |

## questions

<!-- image -->