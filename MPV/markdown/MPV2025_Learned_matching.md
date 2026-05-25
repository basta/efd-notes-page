<!-- image -->

## Learning for Image Matching and Structure from-Motion

## Dmytro Mishkin

Visual Recognition Group, Faculty of Electronical Engineering, Czech Technical University in Prague

## Includes slides by :

- n Daniel DeTone, Paul-Eduard Sarlin, MagicLeap
- n Jerome Revaud, Naver Labs Europe

<!-- image -->

## Image Matching Pipeline Recap

<!-- image -->

<!-- image -->

## Why bother with learning for SfM?

<!-- image -->

Main motivations (from most important) to use learned features:

- n Being able to reconstruct things, you could not before
- Sparse views (just 5-10 images/scene)
- Day/night, other domains
- n To be faster
- n To be more precise

## RoMA

<!-- image -->

<!-- image -->

<!-- image -->

Dust3r

<!-- image -->

DUSt3R: Geometric 3D Vision Made Easy

## Learning the WBS pipeline components (or all)

<!-- image -->

<!-- image -->

*  - significant data augmentation used

** - starting from pretrained model (CroCov2/DINOv2 ViT)

Number of images is a bit wrong metric here:

# patches for patch, #image pairs/tuples for matchers are better

## 3 Components of Any Deep Learning Model

## n Data

- Usually the hardest to get/process for image matching
- We need clever augmentations/synthetic data

## n Architecture

- Usually the simplest - just use pick CNN (detector/descriptor) and/or Transformer (matcher)

## n Loss

- Can be easy or hard depending on the task

<!-- image -->

## Local descriptor learning

<!-- image -->

## Loss:

- n Use any good stateless metric learning loss (contrastive, triplet, AP-based) with hard-negative mining.

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- image -->

## Local descriptor learning (simplest)

<!-- image -->

1.5

## Patch training data: Brown dataset

3 sets, 400k patches each:

- Liberty (shown)
- Notredame
- Yosemite

Size: 64x64, grayscale. Obtained from SfM model, 3D point → DoG keypoints

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## Brown dataset: data generation

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

1. Detect local features in the reference image
2. Reproject them via depth map to neighboring ('target') images
- Check visibility. If not visible, skip feature.
3. Find local features in the target image, such that:
- position, orientation and scale are in a specific range w.r.t the reprojected point.

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## R2D2: Optical flow and augmentation supervision

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

1. Get high-quality optical flow
2. Reproject points via optical flow to neighboring ('target') images
- If not confident, skip feature.

<!-- image -->

<!-- image -->

## Local detector learning

<!-- image -->

<!-- image -->

## Local detector learning: supervised (when you know what to learn)

## Supervised keypoint detector is similar to segmentor

- n SuperPoint: you want to learn corners as segmentation
- n DeDoDe, Tilde: you want to learn DoG features, but more robust

<!-- image -->

Cross entrory for pixel classification (keypoint or not)

<!-- image -->

(a)  Stack of training images

<!-- image -->

## Supervised keypoint detector data

- n Synthetic (SuperPoint), static webcamera (TILDE), SfM Tracks (DeDoDe)
- n Augmentation: homography and color/blur

<!-- image -->

<!-- image -->

<!-- image -->

## Local detector discovery: (when you do not know what to learn)

## Toy (by loss and issues) example: OriNet/AffNet

<!-- image -->

If you know, what result you want, add it to the data and loss function. AffNet/OriNet idea:

- -Distorted patches after normalization should look the same

<!-- image -->

## Possible losses:

- -Patch similarity (pixel level)
- -L2 on residual transformation.

## Discovering detector: harder

## Possible ways:

- n Regression-base covariance constraint - DetNet. - model, x - patch, T - transformation

<!-- formula-not-decoded -->

Input image

Regressed locations

Detections

<!-- image -->

<!-- image -->

## R2D2

<!-- image -->

## Failure causes:

- The keypoint detector only focuses on repeatable locations
- But repeatable locations are not necessarily reliable for matching.

2019 NAVER LAB8. Allrights reserved.

<!-- image -->

<!-- image -->

Heatmap-base covariance constraint - R2D2:

detector response value should be the same in the corresponding locations of the matching images - repeatability.

<!-- image -->

<!-- image -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- image -->

- n Idea: detector response value should be the same in the corresponding locations of the matching images

<!-- formula-not-decoded -->

- n Deep networks are lazy. The easiest way to satisfy the condition is to return the constant response everywhere
- Solution: require response to be 'peaky':

<!-- formula-not-decoded -->

<!-- image -->

## Total R2D2 detector loss

<!-- image -->

U GT correspondences S detector response P - patch

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

## R2D2: reliability

<!-- image -->

- n Idea: predict a descriptor loss (matchability). Combine it with detector score.

## Reliability maps

<!-- image -->

ALIKE: iteration over R2D2.

- Minimize reprojection loss between scoremap argmax augmentation warps

<!-- image -->

<!-- image -->

## Reinforcement learning

<!-- image -->

- n DISK, S-TREK, DaD - use Reinforcement Learning to find good keypoints.
- Good keypoints are those, which you can sample from both images.
- Reward is proportional to the to inverse of reprojection error (S-TREK, DaD) or +1/-0.25 for DISK

<!-- formula-not-decoded -->

## (un-)expected properties of discovered keypoints

<!-- image -->

Toy model of keypoint detection. Under a constraint of K = 10 keypoints and a random spatial distribution of the keypoints, the only consistent way to choose the keypoints is to either only choose white, or only choose black.

<!-- image -->

## (un-)expected properties of discovered keypoints

## KP2D V0 detections

<!-- image -->

Many discovered keypoint detectors tend to detect dark corners

<!-- image -->

## (un-)expected properties of discovered keypoints

<!-- image -->

<!-- image -->

Dark kiki and Light bouba - under different runs, different detectors are discovered by RL

## Kiki and Bouba

<!-- image -->

Figure 7. Demonstration of kiki and bouba. Because of the sharp inflection of the visual shape, subjects tend to map the name kiki onto the figure on the left, while the rounded contours of the figure on the right make it more like the rounded auditory inflection of bouba.

<!-- image -->

<!-- image -->

## How do you learn descriptor matcher? You don't, you learn better descriptors with context

<!-- image -->

no SuperGlue

## SuperGlue: learned matcher

## The importance of context

<!-- image -->

with SuperGlue

<!-- image -->

22.10.2020. VRG, CTU in Prague, online seminar

Sarlin et. al  SuperGlue: Learning Feature Matching with Graph Neural Networks , CVPR 2020 Slide source: https://psarlin.com/superglue/doc/superglue\_slides.pdf

<!-- image -->

## SuperGlue: learned matcher

<!-- image -->

<!-- image -->

## SuperGlue: learned matcher

<!-- image -->

<!-- image -->

## A Graph Neural Network with n attention

Encodes contextual cues &amp; priors

Reasons about the 3D scene

## Solving a partial assignment problem

Differentiable solver

Enforces the assignment constraints domain knowledge 二

Sarlin et. al  SuperGlue: Learning Feature Matching with Graph Neural Networks , CVPR 2020 Slide source: https://psarlin.com/superglue/doc/superglue\_slides.pdf

## SuperGlue: learned matcher

## Attentional Graph Neural Network

## Optimal Matching Layer

<!-- image -->

- Combines visual appearance and position with an MLP:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Sarlin et. al  SuperGlue: Learning Feature Matching with Graph Neural Networks , CVPR 2020 Slide source: https://psarlin.com/superglue/doc/superglue\_slides.pdf

<!-- image -->

## SuperGlue: learned matcher

## Attentional Aggregation

- Compute the message ?←3u using self and cross attention
- Soft database retrieval: query Qi, key kj, and value

<!-- formula-not-decoded -->

- X = [tile, position (70, 100)]

[Vaswani et al, 2017]

<!-- image -->

<!-- image -->

<!-- image -->

## Self-attention

= intra-image information flow

## Cross-attention

- = inter-image

Attention builds a soft, dynamic, sparse graph

22.10.2020. VRG, CTU in Prague, online seminar

## SuperGlue: learned matcher

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

Sarlin et. al  SuperGlue: Learning Feature Matching with Graph Neural Networks , CVPR 2020 Slide source: https://psarlin.com/superglue/doc/superglue\_slides.pdf

<!-- image -->

## Ideas:

- Match coarse to fine, the coarse is similar to SuperGlue on dense DINOv2 features
- Use fine-resolution backbone (VGG19) + regressor head to 'upscale' -- find pixel-wise warp similar to optical flow

<!-- image -->

## RoMa

<!-- image -->

## RoMA

- n Using pretrained features can give good start for matching model.

Images

VGG19

ResNet50

DINOv2

RoMa

<!-- image -->

<!-- image -->

<!-- image -->

## RoMa solves WxBS dataset

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

| Method mAA@ →                          |   10px↑ |
|----------------------------------------|---------|
| DISK [53] Neurlps20                    |    35.5 |
| DISK + LightGlue [31, 53] ICCV'23      |    41.7 |
| SuperPoint +SuperGlue [14, 41] cvpR'20 |    31.4 |
| LoFTR [44] cvPR'21                     |    55.4 |
| DKM [17] cvPR'23                       |    58.9 |
| RoMa                                   |    80.1 |

<!-- image -->

<!-- image -->

<!-- image -->

11206

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## Directly to 3D

*3R family

<!-- image -->

<!-- image -->

## DUSt3R

<!-- image -->

<!-- image -->

<!-- image -->

## Whys seek a unified model? The case Of NLP

## Translation

<!-- image -->

<!-- image -->

NAVER

<!-- image -->

Europe

## DUSt3R

## CroCo: Self-supervised learning with Cross-View Completion

A guessing game: what's behind the mask?

<!-- image -->

NAVERI

[NeurIPS'22] [ICCV'23]

<!-- image -->

<!-- image -->

## DUSt3R

## CroCo: Self-supervised learning with Cross-View Completion

<!-- image -->

Reference view

<!-- image -->

NAVER

[NeurIPS'22] [ICCV'23]

Query view

<!-- image -->

<!-- image -->

## DUSt3R

## CroCo: Self-supervised learning with Cross-View Completion

<!-- image -->

NAVER

[NeurIPS'22] [ICCV'23]

Reference view

<!-- image -->

Query view

## DUSt3R

<!-- image -->

<!-- image -->

## DUSt3R

<!-- image -->

<!-- image -->

<!-- image -->

## DUSt3R

## CroCo: Self-supervised learning g with Cross-View Completion

## Proof of concept:

- trainingwithsyntheticrandomscenes
- Test scene never seen before!

## What solving this implies:

- Match the query and reference images
- Estimate the relative pose
- Infer an object-centric 3D reconstruction of thereferencescene
- Align (rotate) the reference scene in 3D
- Render the reference scene based on imagined

<!-- image -->

<!-- image -->

NAVER

## Pre-training data

2M image pairs from the Habitat simulator [Savva et al., IccV'19]

<!-- image -->

<!-- image -->

<!-- image -->

+ 5M training real image pairs

## DUSt3R

<!-- image -->

<!-- image -->

<!-- image -->

## DUSt3R

## Unifying all 3D vision tasks?

## COLMAP's official restrictions

## Capture images with good texture.

Avoid texture-less images

## Capture images at similar illumination conditions

Avoid high dynamic range scenes Avoid specularities on shiny surfaces

## Capture images with high visual overlap.

each object in at least 3 images - the more the better

## Capture images from different viewpoints.

ra e s ae e a a'a ' a u o  oi s  o sa n o oa At the same time, try to have enough images from a relatively similar viewpoint

""Structure-from-Motion Revisited", "Pixelwise View Selection for Unstructured Multi-View Stereo", Schonberger et al., in CVPR'16 &amp; ECCV'16

<!-- image -->

NAVER

<!-- image -->

Europe

## Unifying all 3D vision tasks?

## 3D reconstruction is a "super-task"

- intrinsically connected to all other 3DV tasks

## Current solution is problematic

- Brittle, requires enough images &amp; overlap &amp; textures &amp; viewpoints
- Heavily handcrafted at all levels An engineering hell!
- Multiple minimal problems solved sequentially No internal collaboration between them
- Slow

<!-- image -->

<!-- image -->

<!-- image -->

Europe

## Unifying all 3D vision tasks?

## 3D reconstruction is a "super-task"

- intrinsically connected to all other 3DV tasks

## Current solution is problematic

- Brittle, requires enough images &amp; overlap &amp; textures &amp; viewpoints
- Heavily handcrafted at all levels An engineering hell!
- Multiple minimal problems solved sequentially No internal collaboration between them
- Slow

<!-- image -->

NAVER

## DUSt3R

<!-- image -->

<!-- image -->

## DUSt3R

<!-- image -->

<!-- image -->

<!-- image -->

## DUSt3R: Dense Unconstrained Stereo 3D Reconstruction

## Training data

| Datasets             | Type                | N Pairs   |
|----------------------|---------------------|-----------|
| Habitat [103]        | Indoor / Synthetic  | 1000k     |
| CO3Dv2 [93]          | Object-centric      | 941k      |
| ScanNet++ [165]      | Indoor / Real       | 224k      |
| ArkitScenes [25]     | Indoor / Real       | 2040k     |
| Static Thing 3D [68] | Object / Synthetic  | 337k      |
| MegaDepth [55]       | Outdoor / Real      | 1761k     |
| BlendedMVS [161]     | Outdoor / Synthetic | 1062k     |
| Waymo [121]          | Outdoor / Real      | 1100k     |

<!-- image -->

<!-- image -->

NAVER

<!-- image -->

## Jointly recovering cameras and scene

<!-- image -->

<!-- image -->

<!-- image -->

NAVER

<!-- image -->

Europe

<!-- image -->

## DUSt3R

<!-- image -->

## Jointly recovering cameras and scene

NAVER

<!-- image -->

## DUSt3R

<!-- image -->

<!-- image -->

<!-- image -->

## DUSt3R

"impossible matching" = 3D reconstruction without any overlap!

Dus

<!-- image -->

<!-- image -->

<!-- image -->

## DUSt3R

<!-- image -->

<!-- image -->

<!-- image -->

## DUSt3R: limitations

## Not all routes leads to accurate visual localization

- Route 2: DUSt3R→PnP

| Methods                     | GT   | 7Scenes (Indoor) [48]   | 7Scenes (Indoor) [48]      | 7Scenes (Indoor) [48]                          | 7Scenes (Indoor) [48]   | 7Scenes (Indoor) [48]   | 7Scenes (Indoor) [48]   | 7Scenes (Indoor) [48]   |
|-----------------------------|------|-------------------------|----------------------------|------------------------------------------------|-------------------------|-------------------------|-------------------------|-------------------------|
|                             |      |                         |                            | Focals Chess Fire Heads Office Pumpkin Kitchen | Stairs                  |                         |                         |                         |
| DUSt3R 512from 2D-matching  |      |                         | 3/0.973/0.952/1.373/1.01   | 4/1.14                                         | 4/1.3411/2.84           |                         |                         |                         |
| DUSt3R512fromscaledrel-pose |      |                         | 5/1.085/1.18 4/1.33 6/1.05 | 7/1.25                                         | 6/1.37 26/3.56          |                         |                         |                         |

## Best results obtained from pixel correspondences

- but DUST3R is not trained explicitly for matching
- What if we did?

<!-- image -->

NAVER

<!-- image -->

<!-- image -->

## DUSt3R

<!-- image -->

<!-- image -->

## VGGT

<!-- image -->

<!-- image -->

VGGT starts from DINOv2 tokens and jointly processes multiple images. It predicts: pointmap, depth, camera pose, tracks.

32 views

## VGGT

<!-- image -->

<!-- image -->

## Bonus: how to evaluate

Image Matching Challenge

<!-- image -->