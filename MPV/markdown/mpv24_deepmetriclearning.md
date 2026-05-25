## deep metric learning:

image retrieval with deep networks

Computer Vision Methods 2024 CTU in Prague

Giorgos Tolias

## metric learning

- § learn metric                   ,  so that
- relevant examples have small distances
- non-relevant examples have high distances
- § instead of directly learning
- learn a representation function E Rd
- for a standard metric in d R
- § function f is a deep neural network
- § deep learning for metric learning / retrieval
- architectures for f
- loss functions
- training data

<!-- image -->

architectures

## fully convolutional network

- § fully convolutional network (FCN)
- map images to 3D activation tensor with dimensionality WxHxD
- no restrictions on input image size or aspect ratio
- § activation tensor = densely extracted set of local descriptors
- replaces classical local descriptors
- apply classical approaches on top of deep local descriptors
- -end-to-end training: components should be trainable
- -transfer learning: FCN is pre-trained on a different task

<!-- image -->

## BoW with CNN features

- § dense deep descriptors replace classical ones, eg SIFT
- § apply BoW as with SIFT

<!-- image -->

## NetVLAD

- § VLAD on dense deep local descriptors
- § the codebook is a learnable parameter matrix
- § soft-assignment to all visual words
- assignment weights: function of the distance to the centroid
- more useful gradients in training

<!-- image -->

## sum pooling - SPoC descriptor

- global sum pooling: WxHxD à 1x1xD
- ·

<!-- formula-not-decoded -->

- ·

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

- simple but works well: discriminative power of CNN activations
- translation invariant representation

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## max pooling - MAC descriptor

- § global max pooling: WxHxD à 1x1xD
- § activation tensor as set of D feature maps (WxH matrices)
- § keep maximum value per feature map (channel)
- § each descriptor element corresponds to a feature map
- implicitly corresponds to an image region

<!-- image -->

conv 5 - channel 1        conv

<!-- image -->

5 - channel 2

- representation: X =

<!-- image -->

<!-- formula-not-decoded -->

input image

<!-- image -->

….     conv 5 - channel D

<!-- image -->

[Razavian et al., MTA'16] [Tolias et al., ICLR'16]

## max pooling - MAC descriptor

- § image-to-image similarity = MAC descriptor dot product
- § implicitly takes region correspondences into account
- each descriptor element corresponds to an image region
- see which elements contribute most to the dot product

<!-- image -->

receptive field for activations that contribute the most to MAC descriptors dot product

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

[Razavian et al., MTA'16] [Tolias et al., ICLR'16]

## generalized mean pooling - GeM descriptor

- § generalized mean pooling
- generalizes average and max pooling
- 𝑝 → ∞ : max pooling (MAC)
- 𝑝 = 1 :  average  pooling (SPoC)
- § parameter 𝑝 can be fixed or learned

<!-- formula-not-decoded -->

<!-- image -->

p=1

<!-- image -->

p=3

<!-- image -->

p=10

## performance results

mAP on R-Oxford with database of 1m images

<!-- image -->

## weighted sum pooling - CroW descriptor

<!-- image -->

w: attention weight based on L2 norm of local descriptors β : inverted-document-frequency weight

- § closer look at attention weights w

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

[Kalantidis et al., ECCVw'16]

example of w

## weighted sum pooling - attention map

<!-- image -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

- attention weights estimated in a learnable way
- small network on top of the 3D activation tensor

NetVLAD accuracy, San Francisco

NetVLAD accuracy, Tokyo 24/7

learned attention:  83.2

vs  CroW attention :  80.1

learned attention :  75.2   vs  no attention :  71.8

## flatten+FC layer representation

<!-- image -->

<!-- formula-not-decoded -->

## flatten+FC layer representation

- § image-to-image similarity:

<!-- formula-not-decoded -->

- § translation variant representation

<!-- image -->

## multi-scale representation

- § small tolerance to scale-change
- § create multi-scale representation
- global descriptor for multiple resolutions
- sum-pooling of global descriptors

<!-- image -->

## representation with ViT

Vision Transformer (ViT)

<!-- image -->

## representation with ViT

<!-- image -->

## network to extract global descriptors

<!-- image -->

## § labels

- discrete class labels: each image assigned to a category
- pairwise labels: two images are relevant or non-relevant
- § loss
- classification losses
- pairwise losses

global

descriptor

extractor losses

## classification loss

<!-- image -->

- § train an N-way classifier
- categorical supervision: class labels
- classification loss
- cross-entropy: standard choice
- arc-face loss  [Deng et al,CVPR'19]
- sub-center arc-face [Deng et al,ECCV'20]
- § network repurposing after training
- discard the classifier
- use descriptor extractor for retrieval
- § not directly optimizing pairwise similarity
- solution: use pairwise labels and pairwise loss

<!-- image -->

## contrastive loss

- § two-branch network; 2 networks that share weights

<!-- image -->

- § pushes descriptors of a positive pair as close as possible
- § pushes descriptors of a negative pair far enough
- 'enough' defined by the margin hyper-parameter

<!-- formula-not-decoded -->

<!-- image -->

[Hadsell et al. CVPR'06]

## triplet loss

- § three-branch network; 3 networks that share weights
- § triplet formed by one positive and one negative pair for the same anchor image
- § non-zero gradients only if the positive pair is close enough compared to the negative pair

<!-- image -->

<!-- image -->

## loss landscape

<!-- image -->

## hard-negatives

- § hard-negative mining is important
- typically, most pairs are negative - cannot include all
- many negatives already have far enough descriptor
- -zero gradients - nothing to learn
- choose hard ones - nearby in the descriptor space
- -find nearest according to the current network parameters
- § mining within the whole training set
- hardness of each pair keeps changing
- -hard-negative mining repeated frequently during training
- § mining within the batch
- memory constraints keep the batch-size small
- the larger the batch, the more likely to include hard negatives in the batch even with random sampling

## histogram loss

[Ustinova &amp; Lempitsky, 2016]

- minimize probability that similarity of a random negative pair is higher than the similarity of a random positive pair

<!-- formula-not-decoded -->

- approximated

<!-- formula-not-decoded -->

- by r=1
- histogram for positive pairs: ht M
- equivalently for the negative pairs

<!-- image -->

<!-- formula-not-decoded -->

<!-- image -->

## optimize the evaluation metric

- § retrieval evaluation metrics are not differentiable
- mean Average Precision (mAP)
- recall @ k
- precision @ k
- § optimize a differentiable surrogate instead
- AP loss [Revaud et al. ICCV 2019] [He et al, CVPR 2018]
- Smooth AP [Brown et al. ECCV 2020]
- Recall@k surrogate [Patel et al. arxiv 2021]

## recall@k

<!-- image -->

## recall@k

<!-- image -->

## recall@k

<!-- image -->

## recall surrogate

- § replace step function with appropriate sigmoid
- § trade-off: approximation vs non-zero gradient
- § recall surrogate loss vs contrastive loss (GeM descriptor)
- 46.1 vs 44.3 on Roxford-H
- 63.9 vs 61.5 on Rparis-H

<!-- image -->

<!-- image -->

## very large batch size

- § large batch size is essential to optimize recall
- § 3 step approach - implementation trick
- extra computational cost
- but significantly increases the maximum batch size

<!-- image -->

[Revaud et al., ICCV'19]

## smooth AP loss

<!-- image -->

- § Average-Precision (AP) is a common retrieval metric

<!-- formula-not-decoded -->

- § AP is not differentiable
- § optimize a smooth approximation instead [Brown et al. 2020]

## proxy anchor

- § proxy: a learnable vector per class
- § optimize distances between training examples and proxies

<!-- image -->

<!-- image -->

<!-- formula-not-decoded -->

[Kim et al., 2020]

<!-- formula-not-decoded -->

[Kim et al., 2020]

## proxy anchor

- § proxy: a learnable vector per class
- § optimize distances between training examples and proxies

<!-- image -->

<!-- image -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

training data

## labels for image pairs

- § need pairwise labels for ground-truth
- matching pair, also called positive or relevant
- non-matching pair, also called negative or non-relevant
- § pairwise labels are costly to obtain
- cost quadratic to the number of images in the training set
- § solutions:
- proxy labels
- weak labels
- automatically obtained labels
- self-supervision: tasks where labels are available for free

## class labels

- § if discrete image labels are available (as in classification)
- image pairs from different classes are labeled as non-matching
- image pairs from the same class are labeled as matching
- § not very useful for pairwise losses (and instance-level recognition)
- matching pairs do not necessarily depict the same object view

<!-- image -->

Leeds Castle

Kiev Pechersk Lavra

## weak labels - GPS

- § use GPS information as weak labeling
- § far enough images are negatives
- § nearby images are possibly positives
- camera orientation is unknown - might depict different objects
- use descriptor distance to disambiguate - closest descriptor
- candidate negatives
- anchor
- candidate positives

<!-- image -->

<!-- image -->

<!-- image -->

camera orientation (unknown)

## structure-from-motion - SfM

- § use result of large-scale SfM to pick training pairs
- camera orientation known
- number of inliers known
- § 7.4M images à 713 training 3D models

<!-- image -->

anchor

<!-- image -->

<!-- image -->

<!-- image -->

## hard negatives from SfM

- § negative examples: images from different 3D models than the anchor
- § hard negatives: closest negative examples to the anchor

## increasing CNN descriptor distance to the anchor

the most similar CNN descriptor naive hard negatives top k by CNN

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

diverse hard negatives top k: one per 3D model

[Radenovic et al. ECCV'16]

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## hard positives from SFM

- § positive examples: images that share 3D points with the anchor
- § hard positives: positive examples not close enough to the anchor

anchor top 1 by CNN

<!-- image -->

<!-- image -->

top 1 by SfM

<!-- image -->

<!-- image -->

harder positives random from top k by SfM

<!-- image -->

<!-- image -->

[Radenovic et al. ECCV'16]

<!-- image -->

<!-- image -->

## hard and diverse training examples

easy pos - hard neg: top 1 CNN + top k CNN

no fine-tuning: pre-trained

<!-- image -->

Oxford 5k Paris 6k

## other tasks

## semantic image retrieval

<!-- image -->

6op-

Query

+cat

## joint image-text query

Topsemanticallyretrieved

<!-- image -->

## CLIP - aligned text/image representation

<!-- image -->

## beyond binary labels: retrieval for pose estimation

<!-- image -->

<!-- formula-not-decoded -->

## camera overlap estimation

- § pairwise label: camera overlap

<!-- image -->

<!-- image -->

<!-- image -->

0.22

<!-- image -->

0.42

<!-- image -->

<!-- image -->

<!-- image -->

0.12

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

- § train s.t. descriptor distance estimates camera distance

<!-- formula-not-decoded -->

## bibliography

- § A Babenko, A Slesarev, A Chigorin, V Lempitsky, ECCV 2014, Neural codes for image retrieval
- § AS Razavian, J Sullivan, S Carlsson, A Maki, MTA 2016, Visual instance retrieval with deep convolutional networks
- § A Babenko, V Lempitsky, ICCV 2015, Aggregating local deep features for image retrieval
- § G Tolias, R Sicre, H Jégou, ICLR 2016, Particular object retrieval with integral max-pooling of CNN activations
- § F Radenovi ć , G Tolias, O Chum, ECCV 2016, CNN Image Retrieval Learns from BoW: Unsupervised Fine-Tuning with Hard Examples
- § Y Kalantidis, C Mellina, S Osindero, ECCVW 2016, Cross-dimensional weighting for aggregated deep convolutional features
- § R Arandjelovi ć , P Gronat, A Torii, T Pajdla, J Sivic, CVPR 2016, NetVLAD: CNN architecture for weakly supervised place recognition
- § A Gordo, J Almazan, J Revaud, D Larlus, ECCV 2016, Deep Image Retrieval: Learning Global Representations for Image Search
- § A Gordo, D Larlus, CVPR 2017, Beyond instance-level image retrieval: Leveraging captions to learn a global visual representation for semantic retrieval
- § F Radenovi ć , G Tolias, O Chum, PAMI 2019, Fine-tuning CNN Image Retrieval with No Human Annotation
- § J Revaud, J Almazán, RS Rezende, CR Souza, ICCV 2019, Learning with average precision: Training image retrieval with a listwise loss
- § E Ustinova, V Lempitsky, NeurIPS 2016, Learning deep embeddings with histogram loss
- § Y. Patel, G. Tolias, J. Matas, CVPR 2022, Recall@k Surrogate Loss with Large Batches and Similarity Mixup
- § A Brown, W Xie, V Kalogeiton, A Zisserman, ECCV 2020, Smooth-AP: Smoothing the path towards large-scale image retrieval
- § E Mohedano, KMcGuinness, N E O'Connor, A Salvador, F Marques, X Giró-i-Nieto, ICMR 2016, Bags of local convolutional features for scalable instance search
- § H Noh, A Araujo, J Sim, T Weyand, B Han, ICCV 2017, Large-Scale Image Retrieval with Attentive Deep Local Features
- § G Tolias, T Jenicek, O Chum, ECCV 2020, Learning and aggregating deep local descriptors for instance-level recognition
- § R Hadsell, S Chopra, Y LeCun, CVPR 2015, Dimensionality reduction by learning an invariant mapping
- § F Schroff, D Kalenichenko, J Philbin, CVPR 2015, Facenet: A unified embedding for face recognition and clustering
- § Balntas, Li, Prisacariu, ECCV 2018 RelocNet - Continuous Metric Learning Relocalisation using Neural Nets
- § S Kim, D Kim, M Cho, S Kwak, CVPR 2020, Proxy Anchor Loss for Deep Metric Learning
- § A. El-Nouby, N. Neverova, I. Laptev, H. Jégou, arxiv 2021, Training Vision Transformers for Image Retrieval

## questions

<!-- image -->

## metric learning of global descriptors to learn local descriptors

## from global to local descriptors

- § pairwise image labels
- are weak labels for local descriptors
- learn local descriptors without labels for image regions
- § learning global descriptors generated with sum pooling (SPoC)
- implicit learning of local descriptors

<!-- image -->

## § training

- weighted sum pooling: network-based weights
- use appropriate loss

## § inference

<!-- image -->

- keep local descriptors with largest attention weight
- reduce dimensionality with PCA
- index with ASMK or other approach

<!-- image -->

## deep local features - DELF

## closer look

- § global descriptor through weighted sum pooling

<!-- formula-not-decoded -->

- § image-to-image similarity interpreted as weighted cross-matching

<!-- formula-not-decoded -->

- background locations à small weights
- foreground locations à large weights
- matching locations à descriptors pushed closer
- non-matching locations à descriptors pushed apart

## matching example using ASMK

20 visual words with the largest contribution are shown different color per visual word

<!-- image -->

<!-- image -->

<!-- image -->

testing: detected features

<!-- image -->

## detection example

before our training w()

<!-- image -->

after our training w()

no attention network but use L2 norm of activation vector at each location instead

## classical metric learning

## metric learning: Mahalanobis distance

- § learn a parametric distance function from the data
- input examples are vectors
- example: Mahalanobis distance
- M is a D x D positive semi-definite matrix
- dM(x,Z) = V(x -z)T M(x-z), x,z ∈ RD
- dM(x,Z) = V(x-z)TLTL(x-z)= =/(L(x-z))TL(x- z) 川 V(Lx - Lz)T(Lx - Lz)= I|Lx - Lzll2 = Ilf(x)- f(z)Il2
- mapping function f(x) = Lx
- can be modeled by a single e fully-connected dlayer

Euclidean distance

<!-- image -->

Mahalanobis distance

<!-- image -->