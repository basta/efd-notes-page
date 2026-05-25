## Deep Neural Networks II.

<!-- image -->

Jan Čech

## Lecture Outline

1. Deep neural networks for Object detection
2. Deep neural networks for Segmentation
3. 'Deeper' insight into the Deep Nets
4. Foundation models

<!-- image -->

2

## Deep Neural Networks for Object Detection

<!-- image -->

3

## Convolutional Networks for Object Detection

-  What is the object detection?

## Grocery store

<!-- image -->

## Image recognition

- What?
- holistic

<!-- image -->

## Object detection

- What + Where?
- Bounding boxes

<!-- image -->

## Semantic segmentation

- What + Where?
- Pixel-level accuracy

<!-- image -->

<!-- image -->

<!-- image -->

## Instance segmentation

- What instance + Where
- Pixel-level accuracy

4

## How to measure detector accuracy?

<!-- image -->

-  Ground-Truth bounding boxes, Detections - predicted bounding boxes
-  Intersection over Union (IoU), a.k.a. Jaccard index
-  A detection is correct (= true positive) if it has enough overlap with the ground-truth
- -Typically, IoU &gt; 50%

<!-- image -->

<!-- image -->

5

## How to measure detector accuracy?

-  Mean Average Precision (mAP)

precision true negatives

<!-- image -->

0

true positives falsepositives

selected elements

True positive: IoU &gt; 50%

<!-- image -->

6

How many selected items are relevant?

<!-- image -->

How many relevant items are selected? How many relevant items are selected?

<!-- image -->

- -Average Precision (Area under the precision-recall curve)

<!-- formula-not-decoded -->

- -Mean over all classes

<!-- formula-not-decoded -->

## Pascal VOC 2007 challenge

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Classes: Person, bird, cat, car, ...

relevantelements

false negatives

## 1. Scanning window + CNN

<!-- image -->

-  CNN - Outstanding recognition accuracy of holistic image recognition [Krizhevsky-NIPS-2012]

7

-  A trivial detection extension - exhaustive scanning window
1. Scan all possible bounding boxes
2. Crop bounding box, warp to 224x224 (fixed-size input image)
3. Run CNN
-  Works, but
- -prohibitively slow…

<!-- image -->

[Oquab et al. Learning and Transferring Mid-Level Image Representations using Convolutional Neural Networks, CVPR, 2014.](https://doi.org/10.1109/CVPR.2014.222)

## 2. Region proposals + CNN

<!-- image -->

-  CNN not evaluated exhaustively, but on regions where objects are likely to be present
-  Region proposals (category independent):
- -Selective search [Uijlings-IJCV-2013]
- [-Edgeboxes [Zitnick-ECCV-2014]](https://doi.org/10.1007/978-3-319-10602-1_26)

<!-- image -->

<!-- image -->

8

## 2. Region proposals + CNN

-  R-CNN   'Regions with CNN feature'

9

<!-- image -->

- [-Girshick et al. Rich feature hierarchies for accurate object detection and semantic segmentation . CVPR 2014.](https://www.cv-foundation.org/openaccess/content_cvpr_2014/html/Girshick_Rich_Feature_Hierarchies_2014_CVPR_paper.html)

<!-- image -->

1. Input image

<!-- image -->

-  Highly improved SotA on Pascal VOC 2012 by more than 30% (mAP)
-  Still slow
- -For each region: crop + warp + run CNN  (~2k)
- -47 s/image

##  Idea (1):

- -Do not run the entire CNN for each ROI, but
- run convolutional (representation) part once for the entire image and
- for each ROI pool the features and run fully connected (classification) part
- [-He et al. Spatial Pyramid Pooling in Deep Convolutional Networks for Visual Recogniton. ECCV 2014.](https://arxiv.org/abs/1406.4729)
- -Arbitrary size image =&gt; fixed-length representation
- -Implemented by max-pooling operations
- -Speeds testing up

<!-- image -->

## 2. Region proposals + CNN

<!-- image -->

10

##  Idea (2):

- -Refine bounding box by regression
- -Multi-task loss: classification + bounding box offset
-  Fast R-CNN (= R-CNN + idea 1 + idea 2)
- -Girshick R. Fast R-CNN, ICCV 2015.
- -End-to-end training
- -Speed up, but  proposals still expensive

<!-- image -->

## 2. Region proposals + CNN

<!-- image -->

11

-  Idea (3):
- -Implement region proposal mechanism by CNN with shared convolutional features (RPN + fast R-CNN)

## ⇒ Faster R-CNN

- [-Ren et al. Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks . NIPS 2015.](https://papers.nips.cc/paper/2015/hash/14bfa6bb14875e45bba028a21ed38046-Abstract.html)
- -Region proposal network: object/not-object + bb coord. (k-anchor boxes)
- -Training: simple alternating optimization (RPN, fast R-CNN)
- -Accurate: 73.2% mAP (VOC 2007), Fast: 5 fps

<!-- image -->

<!-- image -->

## 2. Region proposals + CNN

<!-- image -->

12

## 2. Region proposals + CNN + Instance segmentation

-  Mask R-CNN
- -He et al., Mask R-CNN. ICCV 2017
- -Faster R-CNN + fully convolutional branch for segmentation
- -ROI alignment
- Improved pooling with interpolation
- -Running 5 fps

<!-- image -->

<!-- image -->

13

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

COCO dataset 'Common Object in Context' (&gt;200K images, 91 categories)

<!-- image -->

<!-- image -->

<!-- image -->

+ keypoint localization (pose estimation)

<!-- image -->

<!-- image -->

<!-- image -->

[video1]   [video2]

<!-- image -->

<!-- image -->

## 3. Detection CNN without region proposals

-  YOLO 'You Only Look Once'

15

<!-- image -->

- [-Redmond et al. You Only Look Once: Unified, Real-Time Object Detection. CVPR 2016.](https://arxiv.org/abs/1506.02640)
- -A single net predicts bounding boxes and class probabilities directly from the entire image in a single execution

2: number of bboxes per cell

5: (x,y,w,h, overlap score)

<!-- image -->

## 3. Detection CNN without region proposals

-  YOLO properties:
1. Reasons globally
- Entire image is seen for training and testing, contextual information is preserved (=&gt; less false positives)
2. Generalization
- Trained on photos, works on artworks
3. Fast (real-time)

<!-- image -->

<!-- image -->

|           | mAP (VOC 2007)   |   FPS (GPU Titan X) |
|-----------|------------------|---------------------|
| YOLO      | 63.4%            |                  45 |
| fast YOLO | 52.7%            |                 150 |

<!-- image -->

<!-- image -->

<!-- image -->

16

<!-- image -->

## 3. Detection CNN without region proposals

-  YOLOv2, YOLO 9000
- -Redmon J., Farhadi A. YOLO9000: Better, Faster, Stronger. CVPR 2017
- -Several technical improvements:
- Batch normalization, Higher resolution input image (448x448), Finer output grid (13x13), Anchor boxes (found by K-means)
- -Hierarchical output labels:
- -Trained on COCO and ImageNET datasets
- -Able to learn from images without bounding box annotation (weak supervision)

<!-- image -->

water

<!-- image -->

17

## 3. Detection CNN without region proposals

-  YOLOv2, YOLO 9000 summary
- -The most accurate, the fastest…

<!-- image -->

18

<!-- image -->

[video]

<!-- image -->

## 3. Detection CNN without region proposals

-  RetinaNet (Lin et al., ICCV-2017, IEEE TPAMI 2020)
- -Focal Loss
- Imbalance between positive and negative (background) classes (1:1000)
- Assign more weight on hard examples

<!-- image -->

<!-- image -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- image -->

## Object Detection with Transformers

<!-- image -->

21

-  End-to-end Object Detection with Transformers (DETR) [Carion-ECCV-2020]
- -CNN as a feature extractor, nowadays image patches instead
- -Transformer encoder - decoder architecture
- -FFN - 3-layer perceptron to predict (bbox + object class/no-object)
- -Bipartite matching between prediction and ground-truth bboxes for training
- Hungarian algorithm to maximize the matching score
- Invariant to permutation of predicted objects

<!-- image -->

<!-- formula-not-decoded -->

## DETR - for segmentation

<!-- image -->

-  Observation: encoder self-attention shows individual instances

22

<!-- image -->

-  Segmentation head on the attention maps

<!-- image -->

## Detection DNN - summary

1. Exhaustive scanning windows + CNN
2. Region proposals + CNN
1. R-CNN
2. Fast R-CNN
3. Faster R-CNN
4. Mask R-CNN
3. CNN/DNN without region proposals
1. YOLO
2. YOLO v2, YOLO 9000
3. RetinaNet
4. DETR

<!-- image -->

23

<!-- image -->

24

## Deep Neural Networks for Semantic Segmentation

## Fully Convolutional Net (FCN)

- [ Shelhammer et al. Fully Convolutional Networks for Semantic Segmentation , TPAMI 2017  (originally CVPR, 2015)](https://arxiv.org/abs/1411.4038)
-  Fully Convolutional (no fully connected layers)
- -The output size proportional to input size
-  Upsampling at the last layer
- -Deconvolution layer (= transposed convolution, fractional-strided convolution)
- [-[Dumoulin, Visen, 2018]](https://arxiv.org/abs/1603.07285)

<!-- image -->

<!-- image -->

<!-- image -->

25

## U-Net

<!-- image -->

- [ Ronneberger, et al. U-Net: Convolutional Networks for Biomedical Image Segmentation, Medical Image Computing and Computer-Assisted Intervention, 2015](https://arxiv.org/abs/1505.04597)
- [ Bahnik et al., Visually Assisted AntiLock Braking System. IEEE IV, 2020](https://doi.org/10.1109/IV47402.2020.9304807)
- -Surface segmentation

<!-- image -->

26

<!-- image -->

## DeepLab v3+

<!-- image -->

- [ Chen et al., Encoder-Decoder with Atrous Separable Convolution for Semantic Image Segmentation, ECCV 2018.](https://arxiv.org/abs/1802.02611)

27

-  Atrous Convolutions (= with 'holes', dilated convolutions)
- -Same number of parameters with larger receptive field

<!-- image -->

5x5 =&gt; 3x3 parameters

<!-- image -->

## Segmentation with Transformers

<!-- image -->

-  Segmentation head on top of the transformer features or attention maps
-  SEGMENTER [Strudel-ICCV-2021]
- -No convolutions at all

<!-- image -->

28

## Detection/Segmentation frameworks

-  Detectron2 (Meta, FAIR)
- -Detection, segmentation, keypoints
- -Large model zoo (Faster RCNN, RetinaNet, Mask RCNN, …)
-  YOLOv8 (Ultralytics)
- -User-friendly, accurate and fast…

Classify Detect Segment Track

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

29

<!-- image -->

Pose

<!-- image -->

## Autonomous student formula (eForce)

-  eForce (CTU formula student team)
- -Electric vehicle
- -Acceleration ~ 2.5sec 0-100 km/h
-  Driverless disciplines
- -YOLO-type detection of traffic cones

<!-- image -->

<!-- image -->

<!-- image -->

30

<!-- image -->

<!-- image -->

## 'Deeper' Insight into the Deep Nets

## Deep Fake

<!-- image -->

-  Seamless swapping a face in an image/video, e.g. [Nguyen et al., 2020]
-  Auto-encoder architecture
- -Single shared encoder (to capture pose / expressions)
- -Two decoders (Source and Target to capture person's identity)
-  Controversy:
- -fake news, fake porn, …
-  Deep fake detection

<!-- image -->

<!-- image -->

<!-- image -->

32

## Deep Network Can Easily Be Fooled

<!-- image -->

-  Szegedy et al. Intriguing properties of neural networks. ICLR 2014

33

- -Small perturbation of the input image changes the output of the trained 'well-performing' neural network
- -The perturbation is a non-random image, imperceptible for human

ostrich

I+r

<!-- image -->

<!-- image -->

<!-- formula-not-decoded -->

- -Optimum found by gradient descent

<!-- formula-not-decoded -->

## Deep Network Can Easily Be Fooled

<!-- image -->

- [ Nguyen et al. Deep Neural Networks are Easily Fooled: High Confidence Predictions for Unrecognizable Images. CVPR 2015.](https://arxiv.org/abs/1412.1897)

34

- -Artificial images that are unrecognizable to humans, producing high output score can be found
- -The optimum images found by evolutionary algorithm
- Starting from random noise
- Direct/Indirect encoding

<!-- formula-not-decoded -->

- ⇒ The images found do not have the natural image statistics

<!-- image -->

## Deep Network Can Easily Be Fooled

-  Adversarial physical attacks on neural networks
- -Adversarial sticker [Brown-2018]
- -Adversarial T-shirt [Xu-2019]
- -Adversarial glasses [Sharif-2016]

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

35

orange

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

## Visualization the Deep Nets

<!-- image -->

- [ Mahendran A., Vedaldi A. Understanding Deep Image Representations by Inverting Them . CVPR 2015.](https://arxiv.org/abs/1412.0035)

36

<!-- image -->

- -Start from a random Image I
- -Best match between features + image regularization (natural image prior)

<!-- formula-not-decoded -->

- -Total Variation regularizer (TV)

<!-- formula-not-decoded -->

## Visualizing the Deep Nets

-  CNN reconstruction

<!-- image -->

37

<!-- image -->

- -Gradient descent from random initialization
- -Reconstruction is not unique
- ⇒ All these images are identical for the CNN
-  Similarly, find an image that causes a particular neuron fires (maximally activate)

<!-- image -->

## Verification what the deep net learned

-  Deep nets often criticized for a lack of interpretability

<!-- image -->

38

-  Grad-CAM: Visual Explanations from Deep Networks [Selvaraju-ICCV-2017]
- -GRADient weight Class Activation Mapping
- -Trianed model =&gt; Coarse localization map highlighting important regions for a class c

<!-- image -->

## VGG ' c =cat'

<!-- image -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

VGG ' c =dog'

<!-- image -->

…Feature tensor (last convolution layer) - spans spatial dimensions - spans channels Φ i,J k

## Verification what the deep net learned (2)

-  For transformers: Self-Attention exploited

<!-- image -->

39

<!-- image -->

-  Self-Attention: Query, Key, Value
- -Models long-distance relationships between tokens
- -A matrix of size N x N ,  where N is the number of tokens
- -Self-attention map of the [class] token is used (reshaped to image size)
-  Multiple heads, multiple layers

(recap)

## Verification what the deep net learned (3)

-  Attention Roll-out [Abnar-2020]

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- image -->

40

<!-- image -->

-  Combination of gradient + attention [Chafer-ECCV-2021]

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- image -->

Cat →→

<!-- image -->

## Deep Dream

<!-- image -->

41

-  Manipulate the input image so that response scores are higher for all classes
-  Start from an original image
-  Regularization with TV prior

<!-- formula-not-decoded -->

<!-- image -->

<!-- image -->

## Deep Dream

-  Maybe…

## Salvador Dalí

Soft Construction with Boiled Beans (1936)

<!-- image -->

Hieronymus Bosch , Garden of Earthly Delights (~1510), [part]

42

Swans Reflecting Elephants (1937)

<!-- image -->

<!-- image -->

Apparition of a Face and Frui Dish on a Beach (1937)

<!-- image -->

## Deep Aging

<!-- image -->

-  Our network trained for predicting age (gender and landmarks) was used

Input: age=85

<!-- image -->

Input: age=28

<!-- image -->

43

Output: age=30

<!-- image -->

<!-- image -->

Output: age=99

<!-- image -->

<!-- formula-not-decoded -->

## Deep Art - Neural Style

<!-- image -->

-  Gatys et al. A Neural Algorithm of Artistic Style. Journal of Vision, 2015.

44

- -Generate high-quality artistic rendering images from photographs
- -Combines content of the input image with a style of another image

<!-- image -->

Content image

<!-- image -->

<!-- image -->

- -More examples at Deepart.io

<!-- image -->

Style images

<!-- image -->

Result images

<!-- image -->

<!-- image -->

-  Main idea:
- -the style is captured by correlation of lower network layer responses
- -the content is captured by higher level responses
-  The optimization problem:

<!-- image -->

<!-- formula-not-decoded -->

G is a Gram matrix (dot product matrix of vectorized filter responses)

## Deep Art - Neural Style

45

-  Deep fake
-  Using Network gradient according to the image for various optimization
- -Fooling the net
- -Visualization + Interpretation
- -Dreaming, Hallucination
- -Aging
- -Artistic rendering of photographs
- =&gt; Understanding of the trained model

<!-- image -->

## Summary

46

## Foundation models

<!-- image -->

## CLIP - Connecting Text and Images

-  CLIP [Radford-2021] by OpenAI
- -' Contrastive Language-Image Pre-training'
- -Learn joint text-image embedding =&gt; Text-image (cosine) similarity
- -Learned from 400M WebImageText (WIT) dataset

<!-- image -->

<!-- image -->

48

## CLIP - Connecting Text and Images

<!-- image -->

-  Zero-shot prediction (on par with Resnet on ImageNET benchmark)
- -Loop over ImageNET-classes:

max CLIP( E T (' A photo of a &lt;class&gt; '), E I ( I ) )

<!-- image -->

-  Trained model publicly available
-  Alternative model: ALIGN [Jia-ICML-2021] (by Google), but not public
- -A Large scale ImaGe and Noisy-text embedding

⇒ 76.2% top-1 accuracy on ImageNET

49

## DINO - self-supervised vision transformer

<!-- image -->

-  DINO (self-Distillation with NO labels) [Caron-ICCV-2021] by Meta

50

<!-- image -->

-  No labels, random crops of the same image
-  Student - Teacher training
- -Student and teacher nets of the same architecture
- -
- Student updated by Cross-entropy loss min

<!-- formula-not-decoded -->

- -Teacher's weights are exponentially moving average of the student

<!-- formula-not-decoded -->

## DINO - self-supervised vision transformer

-  Model learns class-specific features without label supervision

<!-- image -->

51

<!-- image -->

Self-attention of the [CLASS] token on the heads of last hidden layer [video]

-  Universal representation for downstream tasks
- -k-NN/linear classifier on the features 78.3/80.1% top-1 accuracy on ImageNET
- -Transfer learning (fine-tuning on other datasets)
- -Image retrieval
- -Segmentation

- …

## Segment Anything

-  Segment Anything Model (SAM) [Kirillov-ICCV-2023] by Meta
-  Promptable segmentation
-  Human in the loop training (11M images, 1B masks)
- -3 stages (assisted-manual 120k, semiautomatic 180k, fully-automatic 11M)
-  Handles natural ambiguity by providing multiple solutions (3)
-  Lightweight prompt encoder and mask decoder
- ⇒ Interactive segmentation (50 ms in web browser)

<!-- image -->

<!-- image -->

<!-- image -->

validmasks

## Segment Anything

-  Qualitative results - various prompts
-  Outstanding zero-shot capabilities

<!-- image -->

<!-- image -->

<!-- image -->

[[project-page / demo]](https://segment-anything.com/)

<!-- image -->

<!-- image -->

53

<!-- image -->

<!-- image -->

## Depth Anything

-  Large Monodepth model [Yang-CVPR-2024] by TikTok
-  Trained from 1.5M of depth labeled images + 62M of unlabeled images
- -Semi-Supervised Learning (SSL):
- Teacher - trained from labeled,
- Student - trained from labeled + pseudo-labeled  (from the Teacher)
- -Normalizing depth (inverse depth, 0-1 range)
- -Strong data augmentation (color jitter, blur, geometry - CutMix)

<!-- image -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

- -Semantic preservation (alignment with DINO features)

<!-- image -->

54

##  Qualitative results

<!-- image -->

55

<!-- image -->

## Depth Anything

## FARL - FAcial Representation Learning

-  FARL [Zheng-CVPR-2022] by Microsoft
-  Universal representation for face images
-  Trained from 20M LAION-Face dataset
-  Combines text-image contrastive learning and masked image modeling

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- image -->

56

<!-- image -->

<!-- formula-not-decoded -->

-  'CLIP for faces', many downstream tasks (segmentation, landmarks, age)

## Conclusions

-  No doubt that the paradigm has shifted
-  Turbulent period
- -The research is extremely accelerated, many novel approaches
- -New results are still astonishing
-  Large foundation models appear and are usually publicly available

<!-- image -->

60