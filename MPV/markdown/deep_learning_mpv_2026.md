## A Shallow Introduction into the Deep Machine Learning

'A quick tour from old principles to the most recent neural architectures'

<!-- image -->

<!-- image -->

Jan Čech

##  Outline of lectures :

<!-- image -->

1. Introduction, basic principles, layers, neural architectures, image recognition
2. Object detection, Semantic/Instance segmentation, further insight (Deep fakes, Adversarial examples, Visualization, Style transfer)

## Deep Learning

2

## Deep learning - top awards in science

-  Deep learning pioneers received Alan Touring Prize in 2018
-  Nobel Prize in Physics 2024
- -"for foundational discoveries and inventions that enable machine learning with artificial neural networks"

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

3

Nobel Prize Outreach.Photo: Nanaka Adachi John J.Hopfield

<!-- image -->

<!-- image -->

Nobel Prize Outreach.Photo: ClementMorin Geoffrey Hinton

## What is the 'Deep Learning' ?

-  Deep learning (by G. Hinton, DL pioneer, Touring+Nobel prize)
- = both the classifiers and the features are learned automatically

<!-- image -->

image label classifier

- Typically not feasible, due to high dimensionality
- Suboptimal, requires expert knowledge, works in specific domain only

<!-- image -->

<!-- image -->

## What is the 'Deep Learning' ? Other definitions…

<!-- image -->

-  Andrew Ng (founder of Google Brain, chief of Baidu AI research)

5

- -' Very large neural networks we can now have and … huge amounts of data that we have access to.'
-  Jeff Dean (head of Google AI)
- -'When you hear the term deep learning, just think of a large deep neural net . Deep refers to the number of layers typically and so this kind of the popular term that's been adopted in the press. I think of them as deep neural networks generally.'
-  Yoshua Bengio (DL pioneer, Turing Award Holder 2018)
- -'Deep learning algorithms seek to exploit the unknown structure in the input distribution in order to discover good representations , often at multiple levels , with higher-level learned features defined in terms of lower-level features.'
-  Yann LeCun (DL pioneer, Turing Award Holder 2018)
- -'Deep learning [is] … a pipeline of modules all of which are trainable . … deep because [has] multiple stages in the process of recognizing an object and all of those stages are part of the training.'

## Deep Learning omnipresent

<!-- image -->

-  Besides the Computer Vision DL is extremely successful in, e.g.
- -Automatic Speech Recognition
- Speech to text, Speaker recognition
- -Natural Language Processing (LLMs)
- Machine translation, Question answering, Chatbots ( GPT )
- -Robotics / Autonomous driving (e.g., Reinforcement learning )
- Touring Award 2024 (Adrew G. Barto, Richard S. Sutton)
- -Data Science / Bioinformatics (e.g., Alphafold )
- Nobel Prize in Chemistry 2024 (D. Baker, D. Hassabis, J. Jumper)
-  Shift of paradigm started in Computer Vision
- Large-scale image category recognition (ILSVRC' 2012 challenge)

INRIA/Xerox 33%, Uni Amsterdam 30%, Uni Oxford 27%, Uni Tokyo 26%, Uni Toronto 16% (deep neural network) [Krizhevsky-NIPS-2012]

6

## Explosion of interest in 'Deep Learning' after 2012

-  Paper title keywords, CVPR

<!-- image -->

7

<!-- image -->

2019

-  Number of attendees/submissions in major Computer Vision and Machine Learning grows exponentially

Number of attendees at CVPR and NeurlPS

2018

<!-- image -->

14,000

12,000

10,000

8,000

6,000

4,000

2,000

CVPR

NeurIPS

2019

## Examples of Deep learning in Computer Vision

-  Image classification [Krizhevsky-NIPS-2012]
- -Input: RGB-image
- -Output: Single label (Probability Distribution over Classes)

<!-- image -->

<!-- image -->

ENET

IM.

- -ImageNet dataset (14M images, 21k classes, Labels by Amazon Mechanical Turk)
- -ImageNet Benchmark (1000 classes, 1M training images)

<!-- image -->

8

## Examples of Deep learning in Computer Vision

-  Object Detection
- -Multiple objects in the image [RCNN, YOLO, …]
- -E.g. Face [Hu-Ramanan-2017], Text localization [Busta-2017]

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

9

## Examples of Deep learning in Computer Vision

-  (3D) Pose estimation
- -[Hu-2018], [OpenPose]
- [-[Cech-2016]](https://www.sciencedirect.com/science/article/pii/S026288561500133X)

<!-- image -->

PETSET

<!-- image -->

10

<!-- image -->

<!-- image -->

<!-- image -->

500

## Examples of Deep learning in Computer Vision

-  Image Segmentation (Semantic/Instance Segmentation)
- -Each pixel has a label  [Long-2015], [Mask-RCNN-2017]

<!-- image -->

<!-- image -->

Semantic segmentation

<!-- image -->

<!-- image -->

Instance segmentation

<!-- image -->

11

## Examples of Deep learning in Computer Vision

-  Motion
- [-Tracking [Neoral-Serych-2024]](https://github.com/serycjon/MFT)
- -Optical Flow [Neoral-2018]
- Predict pixel level displacements between consecutive frames

<!-- image -->

<!-- image -->

<!-- image -->

12

## Examples of Deep learning in Computer Vision

-  Stereo (depth from two images)
-  Depth from a single (monocular) image [Godard-2017]

<!-- image -->

<!-- image -->

13

## Examples of Deep learning in Computer Vision

-  Image based novel view synthesis
- -Given: a set of sparse images =&gt; arbitrary view (smooth camera path)
- -NeRF (Neural Radiance Field for View Synthesis), [Mildenhall-2020]

<!-- image -->

<!-- image -->

[[video]](http://cseweb.ucsd.edu/%7Eviscomp/projects/LF/papers/ECCV20/nerf/website_renders/colorspout_200k_rgb.mp4)

[video]

<!-- image -->

[video]

<!-- image -->

14

## Examples of Deep learning in Computer Vision

-  Medical Imaging - Computer Aided Diagnosis
- -X-ray, mammography, etc.
- -AI as good as doctors at checking X-rays - study  (BBC news)
- -Commercial tools, Startups

<!-- image -->

<!-- image -->

15

## Examples of Deep learning in Computer Vision

##  Faces

- -Recognition / Verification
- -Gender/Age
- -Landmarks, pose
- -Expression, emotions

…already in commerce

<!-- image -->

<!-- image -->

<!-- image -->

16

<!-- image -->

## Examples of Deep learning in Computer Vision

-  Lip reading [Chung-2017]

<!-- image -->

17

<!-- image -->

<!-- image -->

## Examples of Deep learning in Computer Vision

-  Image-to-Image translation [Isola-2017]

## Day to Night

## BW to Color

<!-- image -->

<!-- image -->

-  Deblurring, Super-resolution [Šubrtová-2018]

16x16

<!-- image -->

256x256 (predicted)     256x256 (ground-truth)

output

<!-- image -->

input

<!-- image -->

18

## Examples of Deep learning in Computer Vision

-  Generative models
- -Generating photo-realistic samples from image distributions
- -Variational Autoencoders, GANs [Nvidia-GAN]

<!-- image -->

<!-- image -->

<!-- image -->

(Images synthetized by a random sampling)

<!-- image -->

19

## Examples of Deep learning in Computer Vision

-  Generative models (cont.)

<!-- image -->

20

- -Large text2image models, 2022+ (DALL-E2, Imagen, Midjourney, Stable Diffusion - open source, model available)

panda madscientistmixing sparkling chemicals,artstation

<!-- image -->

a propaganda poster depicting a cat dressed asfrench emperor napoleonholding apiece of cheese

<!-- image -->

## Examples of Deep learning in Computer Vision

-  Real image manipulation / editing
- -Instruct Pix2Pix (textual image manipulation) [Brooks-2023]

<!-- image -->

Input

"Apply face paint"

<!-- image -->

"Whatwouldshelooklikeasa beardedman?"

<!-- image -->

- -Hairstyle Transfer [Šubrtová-2021]

<!-- image -->

"Put on a pair of sunglasses"

<!-- image -->

"Sheshould look100yearsold"

<!-- image -->

[video]

<!-- image -->

21

## Examples of Deep learning in Computer Vision

<!-- image -->

-  Video synthesis (text2video, image2video, video2video, talking heads, synthetic avatars, …)

[[Tian-2024]](https://humanaigc.github.io/emote-portrait-alive/)

<!-- image -->

[Synthesia ~2024](https://www.synthesia.io/)

<!-- image -->

22

SORA2024, OpenAI

<!-- image -->

VEO3, May 2025

<!-- image -->

## Examples of Deep learning in Computer Vision

-  Action/Activity recognition
-  Neural Style Transfer
-  Image Captioning/Visual Question Answering
-  and many more…

<!-- image -->

<!-- image -->

23

[[deepart.io](https://deepart.io/)

[[GPT-4]](https://openai.com/research/gpt-4)

User

[[BLIP]](https://github.com/salesforce/BLIP)

What is unusual about this image?

<!-- image -->

Source:https://www.barnorama.com/wp-content/uploads/2016/12/03-Confusing-Pictures.jpg

<!-- image -->

a brown dog wearing glasses while sitting at a desk

GPT-4 The unusual thing about this image is that a man is ironing clothes on an ironing board attached to the roof of a moving taxi.

## History: (Artificial) Neural Networks

-  Neural networks are here for 70 years
- -Rosenblatt-1956 (perceptron)
- -Minsky-1969 (xor issue, =&gt; skepticism)

<!-- image -->

<!-- image -->

<!-- image -->

## History: Neural Networks

Rumelhart and McClelland - 1986:

- -Multi-layer perceptron,
- -Back-propagation (supervised training)
- Differentiable activation function
- Stochastic gradient descent

## Empirical risk

<!-- formula-not-decoded -->

## Update weights:

<!-- formula-not-decoded -->

What happens if a network is deep? (it has many layers)

<!-- image -->

<!-- image -->

<!-- image -->

29

## Backpropagation - Training of NNs

<!-- image -->

<!-- formula-not-decoded -->

<!-- image -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

## What was wrong with back propagation?

<!-- image -->

-  Local optimization only (needs a good initialization, or re-initialization)
-  Prone to over-fitting
- -too many parameters to estimate
- -too  few labeled examples
-  Computationally intensive
- =&gt; Skepticism: A deep network often performed worse than a shallow one

<!-- image -->

31

## Why does it work now?

<!-- image -->

<!-- image -->

##  However nowadays:

- -Large collections of labeled data available
- ImageNet (14M images, 21k classes, hand-labeled)
- -Reducing the number of parameters by weight sharing
- Convolutional layers - [LeCun-1989]
- -Novel tricks to prevent overfitting of deep nets
- -Fast enough computers (parallel hardware, GPU)
- =&gt; Optimism: It works!

## Computational power

<!-- image -->

<!-- image -->

33

<!-- image -->

<!-- image -->

TheoreticalPeakFloating Point Operations per Watt,SinglePrecision

GTX Titan xNVIDIA Titan )

Te

Titan

GTX

HD 7970 GHz Ed.

FirePro.W9100

HD8970

Xeon

E5-2699 V3 E5-26991

680

GTX:

E5-2699v3

E5-2697v2

E5-2690

INTEL Xeon CPUs

NVIDIAGeForceGPUs

AMD Radeon GPUs

INTEL Xeon Phis

2014

Time

102

GFLOP/sec per Watt

10

100

HD 4870

HD 3870

8800GTS

GTX280

X5492

X5482

2008

HD5870

GTX285

HD6970

GTX*580

2010

HD6970

GTX580

2012

End of Year

(KNL

2016

## Deep convolutional neural networks

-  An example for Large Scale Classification Problem:
- [-Krizhevsky, Sutskever, Hinton: ImageNet classification with deep convolutional neural networks . NIPS, 2012.](https://papers.nips.cc/paper_files/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html)
- Recognizes 1000 categories from ImageNet
- Outperforms state-of-the-art by significant margin (ILSVRC 2012)

<!-- image -->

<!-- image -->

'Alex-Net'

- 5 convolutional layers, 3 fully connected layers
- 60M parameters, trained on 1.2M images (~1000 examples for each category)
- Cross-Entropy loss (softmax log-loss)

34

## Deep CNNs - basic building blogs

<!-- image -->

-  A computational graph (chain/directed acyclic graph) connecting layers
- -Each layer has: Forward pass, Backward pass
- -The graph is end-to-end differentiable
1. Input Layer
2. Intermediate Layers
1. Convolutions
2. Max-pooling
3. Activations
3. Output Layer
4. Loss function over the output layer for training

<!-- image -->

35

## Convolutional layer

-  Input : tensor ( W×H×D )
- -'image' of size W ×H with D channels
-  Output : tensor ( W'×H'×D' )
-  A bank of D' filters of size ( K×K×D ) is convolved with the input to produce the output tensor
- -Zero Padding ( P ), extends the input by zeros
- -Stride ( S ), mask shifts by more than 1 pixel
- -K×K×D×D' parameters to be learned

<!-- image -->

## dot pro duc t

<!-- image -->

<!-- image -->

36

## Max-pooling layer

<!-- image -->

-  Same inputs ( W×H×D ) and outputs ( W'×H'×D ) as convolutional layer

37

-  Same parameters: Mask Size ( K ), Padding ( P ), Stride ( S )
-  Same sliding window as in convolution, but instead of the dot product, pick maximum
-  Non-linear operation
-  No parameters to be learned

<!-- image -->

## Activation functions

-  Non-linearity, applied to every singe cell of the tensor
-  Input tensor and output tensor of the same size

## Sigmoid

<!-- formula-not-decoded -->

## tanh

tanh(x)

## ReLU

max(0,c)

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## LeakyF ReLU

max(0.1, x)

## Maxout

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- image -->

-  ReLU is the simplest (used in the AlexNet, good baseline)
-  Saturating non-linearity (sigmoid, tanh) causes 'vanishing' gradient

38

## Multiclass Classification loss

-  Cross-Entropy loss (softmax log loss)
- -Softmax output as discrete PDF over classes

<!-- image -->

<!-- formula-not-decoded -->

- -Ground-truth classes 'one-hot encoding'

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

39

<!-- image -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

* iS index of the truth class

## Deep convolutional neural networks

-  Additional tricks:  'Devil is in the details'
- -Rectified linear units instead of standard sigmoid
- =&gt; Mitigate vanishing gradient problem
- -Convolutional layers followed by max-pooling

40

<!-- image -->

<!-- image -->

- Local maxima selection in overlapping windows (subsampling)
- =&gt; dimensionality reduction, shift insensitivity
- -Dropout
- 50% of hidden units are randomly omitted during the training, but weights are shared in test time
- Averaging results of many independent models (similar idea as in Random forests)
- =&gt; Probably very significant to reduce overfitting
- -Data augmentation
- Images are artificially shifted and mirrored (10 times more images)
- =&gt; transformation invariance, reduce overfitting

## Deep convolutional neural networks

-  Supervised training
- -The training is done by a standard back-propagation
- -enough labeled data: 1.2M labeled training images for 1k categories
- -Learned filters in the first layer
- Resemble cells in primary visual cortex
-  Training time:
- -5 days on NVIDIA GTX 580, 3GB memory (Krizhevsky, today faster)
- -90 cycles through the training set
-  Test time (forward step) on GPU
- -Implementation by Yangqing Jia, http://caffe.berkeleyvision.org/
- -5 ms/image in a batch mode

[Hubel-Wiesel-1959]

<!-- image -->

<!-- image -->

Learned first-layer filters

<!-- image -->

41

## Early experiments 1: Category recognition

<!-- image -->

-  Implementation by Yangqing Jia, 2013, http://caffe.berkeleyvision.org/
- -network pre-trained for 1000 categories provided
-  Which categories are pre-trained?
- -1000 'most popular' (probably mostly populated)
- -Typically very fine categories (dog breeds, plants, vehicles…)
- -Category 'person' (or derived) is missing
- -Recognition accuracy subjectively surprisingly good…

<!-- image -->

<!-- image -->

42

## It is not a texture only...

<!-- image -->

<!-- image -->

<!-- image -->

45

<!-- image -->

## Early experiments 2: Category retrieval

-  50k randomly selected images from Profimedia dataset
-  Category: Restaurant (results out of 50k-random-Profiset)

<!-- image -->

<!-- image -->

## Early experiments 2: Category retrieval

<!-- image -->

-  Category: stethoscope (results out of 50k-random-Profiset)

48

<!-- image -->

## Early experiments 3: Similarity search

<!-- image -->

-  Indications in the literature that the last hidden layer carry semantics

49

- -Last hidden layer (4096-dim vector), final layer category responses (1000-dim vector)
- -New (unseen) categories can be learned by training (a linear) classifier on top of the last hidden layer
- [Oquab, Bottou, Laptev, Sivic, CVPR, 2014](https://openaccess.thecvf.com/content_cvpr_2014/html/Oquab_Learning_and_Transferring_2014_CVPR_paper.html)
- -Responses of the last hidden layer can be used as a compact global image descriptor
- Semantically similar images should have small Euclidean distance
- [Novak, Cech, Zezula, ICSSA, 2015](https://link.springer.com/chapter/10.1007/978-3-319-25087-8_22)

image

<!-- image -->

48

## Early experiments 3: Similarity search

<!-- image -->

-  Qualitative comparison: (20 most similar images to a query image)

50

1. MUFIN annotation (web demo), http://mufin.fi.muni.cz/annotation/, [Zezula et al., Similarity Search: The Metric Space Approach. 2005.]
- Nearest neighbour search in 20M images of Profimedia
- Standard global image statistics (e.g. color histograms, gradient histograms, etc.)
2. Caffe NN (last hidden layer response + Euclidean distance),
- Nearest neighbour search in 50k images of Profimedia
- 400 times smaller dataset !

MUFIN results

<!-- image -->

## Early experiments 3: Similarity search

<!-- image -->

<!-- image -->

51

51

## Early experiments 3: Similarity search

## MUFIN results

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

<!-- image -->

<!-- image -->

<!-- image -->

52 52

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## Caffe NN results

## Early experiments 3: Similarity search

<!-- image -->

<!-- image -->

53

53

## Early experiments 3: Similarity search

## MUFIN results

<!-- image -->

<!-- image -->

54 54

## Early experiments 3: Similarity search

1:0

6:3286.28

11:3495.67

16:3574.01

2:2812.02

7:3304.93

12:3528.47

17:3576.81

3:2968.18

8:3402.86

13:3549.56

18:3597.88

4:3189.3

9:3433.69

14:3559.5

19:3599.39

5:3284.86

10:3473.81

<!-- image -->

15:3562.74

20:3662.85

<!-- image -->

m p

55 55

## Early experiments 3: Similarity search

## MUFIN results

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

<!-- image -->

<!-- image -->

<!-- image -->

56 56

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## Caffe NN results

## Early experiments 3: Similarity search

57 57

<!-- image -->

w

<!-- image -->

## Early experiments 3: Similarity search

## MUFIN results

<!-- image -->

E

Z

工

D

<!-- image -->

58 58

福

## Early experiments 3: Similarity search

<!-- image -->

<!-- image -->

59

59

-  Network initialization

<!-- image -->

60

- -Mishkin, Matas. All you need is a good init . ICLR 2016
- -Weights initialization: zero mean, unit variance, orthogonality
-  Batch normalization
- [-Iosse, Szegedy. Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift. NIPS 2015](https://arxiv.org/abs/1502.03167)
- -Zero mean and unit variance weights are 'supported' during training to avoid vanishing gradient
- ⇒ Small sensitivity to learning rate setting (can be higher, faster training
- 10 times fewer epochs needed)
- ⇒ Regularizer (dropout can be excluded/smaller) (better optimum found)

Algorithm 1: Batch Normalizing Transform, applied to activation 2 over a mini-batch.

<!-- image -->

## Novel tricks

## Novel tricks II.

-  Exponential Linear Units (ELU)  [Clevert et al., ICLR 2016]

<!-- formula-not-decoded -->

<!-- image -->

61

<!-- image -->

X

- -Self normalizing properties, batch normalization unnecessary
- -Faster training reported
-  ADAM optimizer  [Kingma and Ba, ICLR 2015]
- =  (ADAptive Moments)
- -Often improves over SGD (with momentum),
- -Low sensitivity on learning rate setting

## Novel architectures

<!-- image -->

-  ImageNet Large Scale Visual Recognition Challenge (ILSVRC)

62

<!-- image -->

##  AlexNet

- [-[Krishevsky et al., NIPS 2012]](https://papers.nips.cc/paper_files/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html)

<!-- image -->

## CNN architectures

<!-- image -->

<!-- image -->

63

## CNN architectures

-  VGG Net: VGG-16, VGG-19
- [-[Simonyan and Zisserman, ICLR 2015]](https://arxiv.org/abs/1409.1556)
- -Deeper than AlexNet
- -Smaller filters (3x3 convolutions), more layers
- =&gt; Same effective receptive field, but more 'non-linearity'

<!-- image -->

##  GoogLeNet

- [-[Szegedy et al., CVPR 2015]](https://paperswithcode.com/paper/going-deeper-with-convolutions)
- -22 layers, No Fully-Connected layers
- -Accurate, much less parameters
- -'Inception' module (Net in net)

<!-- image -->

## CNN architectures

<!-- image -->

<!-- image -->

65

##  ResNet

<!-- image -->

- -Residual modules, 152 layers

<!-- image -->

## CNN architectures

<!-- image -->

## CNN architectures

##  ResNeXt

- [-[Xie-CVPR-2017]](https://openaccess.thecvf.com/content_cvpr_2017/html/Xie_Aggregated_Residual_Transformations_CVPR_2017_paper.html)
- -Improvement of ResNet
- -Cardinality
- number of branches in a block
- -'Increasing cardinality, better than going wider or deeper"

<!-- image -->

67

<!-- image -->

<!-- image -->

<!-- image -->

##  DenseNet

- [-[Huang-CVPR-2017]](https://paperswithcode.com/paper/densely-connected-convolutional-networks)
- -Densifying Skip connections
- -Chain of several 'dense blocks'
- -Argument: Features are reused
- -Higher accuracy with fewer parameters over ResNet reported
- -Best paper award @ CVPR

68

<!-- image -->

<!-- image -->

<!-- image -->

## CNN architectures

## CNN architectures

-  Squeeze-and-Excitation Network (SE-Net)
- -[Hu-CVPR-2018, Hu-TPAMI-2019]
- -Chain of SE-blocks
- -Squeeze:
- Channel descriptor by aggregating over spatial dimension
- -Excitation
- Small bottleneck fully connected net producing scale of each channel
- -Capture channel interdependences
- -Winner of ILSVRC 2017 (Top-5 err 2.25%)
- -Negligible extra computational cost

<!-- image -->

<!-- image -->

<!-- image -->

## CNN architectures

-  Computationally efficient architectures
- -MobileNet [Howard-2017,  Google Inc.]
- depth wise separable convolutions
- -ShuffleNet [Zhang-CVPR-2018, Face++]
- Comparable accuracy with AlexNet, 13x speed up

<!-- image -->

<!-- image -->

<!-- image -->

70

## DNN architecture - Transformer

-  Taken from Natural Language Processing
-  'Attention is all you need' [Wasvani-2017]
-  Originally for machine translation (seqence2sequence)
- -Replaces recurrent neural networks (RNNs)

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

71

## DNN architectures - Transformers

-  Vision Transformers [Dosovitskiy-2021]
- -No Convolutions, Encoder only transformer, Parallel processing
- -Image is cut into fixed-size patches and the sequence of vectorized patches (tokens/words) is fed into the transformer
- -Outperforms ResNET on ImageNet, but needs 100M image pretraining

<!-- image -->

<!-- image -->

72

## DNN architectures - Transformers

-  (Vision) Transformer
- -Input tokens treated equally, but order of the sequence is important
- 'Dog bites man' vs. 'Man bites dog'

<!-- image -->

## ⇒ Positional Encoding

- Encodes absolute position of each token
- Using smooth functions (sin, cos) - each token's position gives a vector

<!-- formula-not-decoded -->

<!-- image -->

<!-- image -->

Position Dimension

73

## DNN architectures - Transformers

-  (Vision) Transformer
- -Main idea: Self-Attention Mechanism
- Inputs (vectors x1 , …, xm )
- Parameters (matrices WQ , WK , WV )

<!-- image -->

<!-- formula-not-decoded -->

<!-- image -->

## DNN architectures - Transformers

-  (Vision) Transformer
- -Main idea: Self-Attention Mechanism
- Inputs (vectors x1 , …, xm )
- Parameters (matrices WQ , WK , WV )

<!-- formula-not-decoded -->

<!-- image -->

<!-- image -->

75

## DNN architectures - Transformers

-  (Vision) Transformer
- -Main idea: Self-Attention Mechanism
- Inputs (vectors x1 , …, xm )
- Parameters (matrices WQ , WK , WV )

<!-- formula-not-decoded -->

<!-- image -->

<!-- image -->

76

## DNN architectures - Transformers

-  (Vision) Transformer
- -Main idea: Self-Attention Mechanism
- Inputs (vectors x1 , …, xm )
- Parameters (matrices WQ , WK , WV )

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- image -->

<!-- image -->

77

## DNN Architectures- Transformers

-  SWIN Transformer [Liu-2021] ('Shifted Windows')
- -Improvement of ViT transformer
- data hungry (needs large set pretraining)
- Image tokens too large - unsuitable for object detection, semantic segmentation
- -Hierarchical features
- Self attention within windows (linear complexity w.r.t. image size)
- Cross-window connection (cyclic window shifting in subsequent  layers)
- -State-of-the-art general purpose backbone (recognition, detection,

<!-- image -->

<!-- image -->

<!-- image -->

78

## DNN Architectures - ConvNext

##  ConvNeXt [Liu-2022]

- -Pure Convolutional Neural Network (again)
- -Similar to ResNet, but tweaked
- -Larger kernel size, BatchNorm → LayerNorm
- ReLU → GeLU (smoother)

## ImageNet-1KAcc.

<!-- image -->

## ResNet Block

79

<!-- image -->

ConvNeXt Block Top-1 accuracy [%]

<!-- image -->

<!-- image -->

## CNN models (comparison)

<!-- image -->

<!-- image -->

<!-- image -->

- [ [Canziani et al., An Analysis of Deep Neural Network Models for Practical Applications, 2017. arXiv:1605.07678v4]](https://arxiv.org/abs/1605.07678)

## CNN models (comparison)

-  ImageNet leaderboard (Top-1 accuracy)

<!-- image -->

81

<!-- image -->

## Face Interpretation Problems

<!-- image -->

## Face interpretation problems

-  Face recognition, face verification
- -Architecture similar to AlexNet - deep CNN (softmax at the last layer)

<!-- image -->

[Taigman-ECVV-2014] DeepFace: Closing the Gap to Human-Level Performance in Face Verification (authors from Facebook)

[Parkhi-BMVC-2015] Deep Face recognition (authors from Oxford Uni)

- 2.6M images of  2.6k celebrities, trained net available

[Deng-CVPR-2019] ArcFace (faces mapped onto a unit sphere)

<!-- image -->

False Positive Rate

-  Face represented by penultimate layer response, similarity search, large scale indexing

<!-- image -->

83

## Face interpretation problems

-  Facial landmarks, Age / Gender estimation
- -Multitask network
- Shared representation
- Combination of both classification and regression problems

<!-- image -->

<!-- image -->

<!-- image -->

84

## Age estimation - How good the network is?

-  Our survey
- ~20 human subjects , ~100 images of 2 datasets

## MORPH dataset

True:36,MAE:17.8

<!-- image -->

True:33,MAE:16.3

<!-- image -->

True:22,MAE:18.8

<!-- image -->

## IMDB dataset

True:66,MAE:1.0

<!-- image -->

True:29,MAE:1.0

<!-- image -->

True:25,MAE:0.5

<!-- image -->

True:22,MAE:16.1

<!-- image -->

<!-- image -->

85

True:25,MAE:16.0

True:19,MAE:1.0

<!-- image -->

True:43,MAE:1.0

<!-- image -->

<!-- image -->

## Age estimation - How good the network is?

-  Better than average human…

<!-- image -->

15

MAE

CS5

MaxAE

Average

human

6.8

48.6

24.1

Human

1 crowd

4.7

65.1

19.0

Machine

3.2

82.6

26.0

- [ [Franc-Cech-IVC-2018]](https://cmp.felk.cvut.cz/%7Exfrancv/pages/emcnn.html)
-  Network runs real-time on CPU

<!-- image -->

86

|               |   MAE |   CS5 |   MaxAE |
|---------------|-------|-------|---------|
| Average human |   8.2 |  41.7 |    31.5 |
| Human crowd   |   5.7 |  59.0 |    21.0 |
| Machine       |   5.1 |  62.5 |    42.7 |

<!-- image -->

## Predicting Decision Uncertainty from Faces

<!-- image -->

- [ [Jahoda, Vobecky, Cech, Matas. Detecting Decision Ambiguity from Facial Images . In Face and Gestures, 2018]](https://github.com/JahodaPaul/DecisionAmbiguityRecognition)
-  Can we train a classifier to detect uncertainty?

<!-- image -->

=&gt; YES, we can…

- CNN 25% error rate, while human volunteers 45%

<!-- image -->

87

<!-- image -->

Training set: 1,628 sequences

Test set: 90 sequences

<!-- image -->

## Sexual Orientation from Face Images

<!-- image -->

88

- [ [Wang and Kosinki. Deep neural networks are more accurate than humans at detecting sexual orientation from facial images . Journal of Personality and Social Psychology, 2018]](https://www.gsb.stanford.edu/faculty-research/publications/deep-neural-networks-are-more-accurate-humans-detecting-sexual)
-  Better accuracy than human in (gay vs. heterosexual)
- -
- 81% accuracy (for men), average human accuracy (61%)
- -
- 71% accuracy (for women) average human accuracy (54%)
- -Accuracy further improved if 5 images provided (91%, 83%)

Composite hcterosexual faces Composite gay faces

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

Male

Female

<!-- image -->

## Summary

<!-- image -->

## General recipe to use deep neural networks

<!-- image -->

-  Recipe to use deep neural network to 'solve any problem' (G. Hinton 2013) 90
- -Have a deep net
- -If you do not have enough labeled data, pre-train it by unlabeled data; otherwise do not bother with pre-initialization
- -Use rectified linear units instead of standard neurons (sigmoid)
- -Use dropout to regularize it (you can have many more parameters than training data)
- -If there is a spatial structure in your data, use convolutional layers

##  Novel:

- -Use Batch Normalization  [Ioffe-Szegedy-NIPS-2015] =&gt; LayerNorm
- -ReLU =&gt; ELU, GELU
- -Adaptive Optimizers (ADAM)
- -Various architectures (AlexNet, VGG, GoogLeNet, ResNet, ResNeXt, DenseNet, SE-Net, MobileNet, ShuffleNet, Transformers, Swin, ConvNext

##  Experience:

- -Data matters (the more data the better), transfer learning, data

## Conclusions

-  DNNs efficiently learns the abstract representation
-  Low computational demands for running, Training needs GPU
-  Many 'deep' toolboxes: Caffe (Berkeley), MatconvNet (Oxford), TensorFlow (Google), Theano (Montreal), PyTorch (Facebook), …
-  NNs are (again) in the 'Golden Age' (or witnessing a bubble), as many practical problems seem solvable in near future
-  Explosion of interest of DNN in literature, graduates get incredible offers, start-ups appear all the time
- 
- Do we understand enough what is going on?

<!-- image -->

[http://www.youtube.com/watch?v=LVLoc6FrLi0](http://www.youtube.com/watch?v=LVLoc6FrLi0)

<!-- image -->

<!-- image -->

91

## Further Resources

-  Deep Learning Textbook
- -Ian Goodfellow and Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
- -Available on-line for free.
-  Lectures / video-lectures
- -Stanford University course on Deep Learning (cs231n)
- -MIT lectures on Introduction in Deep Learning (MIT 6.S191)
-  Various blogs and on-line journals
- [-Google AI blog (https://ai.googleblog.com/)](https://ai.googleblog.com/)
- [-OpenAI blog (https://openai.com/blog)](https://openai.com/blog)
- [-MetaAI blog (https://ai.facebook.com/blog/)](https://ai.facebook.com/blog/)
- -Andrej Karpathy (blog)

<!-- image -->

- …

92