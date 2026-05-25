## Tracking with Correlation Filters

Lecture for AE4M33MVP

Acknowledgement to Joao F. Henriques from Institute of Systems a and Robotics R University of Coimbra for providing materials for this presentation

<!-- image -->

<!-- image -->

## Lecture Overview

-  Discriminative tracking
-  Connection of correlation and the discriminative tracking
-  Brief history of correlation filters
-  Breakthrough by MOSSE tracker
-  Why 1 MOSSE works?

learning conncction of correlation filters a and machine

- Qirculant matrices
- Ridge Regression
-  Kernelized Correlation Filters

<!-- image -->

<!-- image -->

<!-- image -->

## Discriminative Tracking

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## Discriminative Tracking

-  How to get training samples for the classifier?
-  S+andard approach:
- bhoxes with high overlap with the GT →&gt; Pos. samples
- bboxes far from the GT → Neg. samples
-  What with the samples in the unspecified area?

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## Connection to Correlation

-  Let's have a linear classifier with weights W

<!-- formula-not-decoded -->

-  x During tracking to evaluate we want the classifier at subwindows During tracking we want to evaluate

<!-- formula-not-decoded -->

-  y i y (i.e. response map) Then into vector we can a i.e. response map)
-  This is equivalent to cross-correlation formulation which can be computed efficiently in Fourier domain

<!-- image -->

<!-- formula-not-decoded -->

- 𝐰 → P P Note: Convolution iS related: it is the as cross-correlation, but with the flipped image of

<!-- image -->

<!-- image -->

<!-- image -->

## Connection to Correlation

## The Convolution Theorem

Cross-correlation is equivalent to an element-wise product in 1 Fourier ( domain

<!-- image -->

<!-- formula-not-decoded -->

##  where:

- 𝐲   = ℱ(𝐲) 𝐲 𝐱 𝐰 is S1 the Discrete Fourier Transform DFT) (likewise and
- × iS s element-wise product
- . ∗ iS complex-conjugate i.e. 1 negate imaginary part)
- Note that cross-correlation. and the DFT, are cyclic (the window wraps at the image edges).

<!-- image -->

<!-- image -->

<!-- image -->

## Connection to Correlation

## The Convolution Theorem

Cross-correlation is equivalent to an element-wise product in 1 Fourier ( domain

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

∗

<!-- formula-not-decoded -->

<!-- image -->

-  In practice:

##  Cn . be orders s of magnitude e faster:

- 𝑛 × 𝑛 𝒪(𝑛 4 ) cross-correlation is
- 𝒪(𝑛 2 log 𝑛) Fast Fourier Transform and its inverse are

<!-- image -->

<!-- image -->

<!-- image -->

## Connection to Correlation

## The Convolution Theorem

Cross-correlation is equivalent to an element-wise product in 1 Fourier ( domain

<!-- formula-not-decoded -->

-  Conclusion:

The evaluation of any linear classifier can be accelerated with the Convolution Theorem. (Not just for tracking.)

-  "linear' can become e non-linear using kernel trick in some specific : cases will 1 be discussed later
-  w

<!-- image -->

<!-- formula-not-decoded -->

<!-- image -->

<!-- image -->

<!-- image -->

## Connection to Correlation

<!-- image -->

-  w Q: How the for correlation should look like? What a about training?

## Objective

<!-- image -->

-  w x Intuition of requirements of cross-correlation of classifier filter a training image
- V high peak near the true location of the target
- Low 1 values elsewhere to r minimize false e positive

<!-- image -->

<!-- image -->

## Brief History of Correlation Filters

## Minimum Average Correlation Energy (MACE) filters, 1980's

-  Bring : average correlation output t towards 0O:

<!-- formula-not-decoded -->

except for target location, keep the peak value e fixed:

𝐰 𝑇 𝐱 = 1

subject to:

-  This produces a sharp peak at target t location with closed form solution:

<!-- formula-not-decoded -->

- 𝐱 ∗ ×𝐱 and is real-valued.
- × division and product are element-wise.
-  Sharp peak 川 good localization! Are we done?

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## Brief History of Correlation Filters

The MACE filter suffer from 2 main issues:

1. Hord. constraints easily lead to overfitting.
2. UMACE ("Unconstrained MACE"） addresses this by removing the hard constraints and require to produce a high average correlation response on positive samples. However, it still suffer from the 2nd problem.
3. Fnforcing a sharp peak is too strong condition; lead to overfitting 2.
4. Gaussian-MACE / MSE-MACE - peak to follow a 2D Gaussian shape

<!-- formula-not-decoded -->

,

subject to:  𝐰 𝑇 𝐱 = 1

<!-- image -->

- In the 0riginal method (1990's), t the minimization was still subject to the MACE hard constraint.

(It later turned out to be unnecessary!)

<!-- image -->

<!-- image -->

<!-- image -->

## Brief History of Correlation Filters

## Sharp Vs. Gaussian peaks

Training image: Training image:

𝐰 Classifier

𝐰∗𝐱 Output

𝐱 =

<!-- image -->

𝐰 = 𝐱 Naive filter

<!-- image -->

<!-- image -->

<!-- image -->

- Very broad peak is hard t to localize especially I with clutter).
- State-of-the-art classifiers (e.g. SVM) show s behavior! same

<!-- image -->

m d

<!-- image -->

<!-- image -->

## Brief History of Correlation Filters

## Sharp Vs. Gaussian peaks

Training image: Training image:

𝐰 Classifier

𝐰∗𝐱 Output

𝐱 =

<!-- image -->

𝐰 = 𝐱 Naive filter

<!-- image -->

<!-- image -->

Sharp peak (UMACE)

<!-- image -->

<!-- image -->

<!-- image -->

- A very s sharp peak is obtained bv emphasizing small image details (like the fish's scales here).
- generalizes poorly: fine scale details that a are usually not robust

<!-- image -->

<!-- image -->

<!-- image -->

## Brief History of Correlation Filters

## Sharp Vs. Gaussian peaks

Training image: Training image:

𝐰 Classifier

𝐰∗𝐱 Output

𝐱 =

<!-- image -->

𝐰 = 𝐱 Naive filter

Sharp peak (UMACE)

<!-- image -->

<!-- image -->

Gaussian peak (GMACE)

<!-- image -->

<!-- image -->

- A good compromise.
- Tiny details are ignored.

·

<!-- image -->

<!-- image -->

- focuses on larger, more robust structures.

<!-- image -->

<!-- image -->

m d

<!-- image -->

<!-- image -->

## Breakthrough by MOSSE tracker

## Min. Output Sum of s Sq. Errors (MOSSE)

-  Presented by David Bolme and colleagues at CVPR 2010
-  Tracker run at speed over a 600 frames per second
-  Vartr simple e toi implement
- no complex features only rov pixel l values
- only FFT and element-wise operation
-  performance similar to the most s sophisticated tracker (at that time)

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## Breakthrough by MOSSE tracker

## How does it work?

-  Use only the Gaussian peak objective (no hard constraints)
-  Found the following solution using the Convolution Theorem:

<!-- image -->

<!-- formula-not-decoded -->

𝜆 = 10 -4 is artificially added to prevent divisions by 0)

-   No e expensive matrix operations! FFT and e element-wise op.

<!-- image -->

<!-- image -->

<!-- image -->

## Breakthrough by MOSSE tracker

## Implementation aspects

-  Cosine (or sine) window preprocessing

<!-- image -->

×

<!-- image -->

- image edges smooth to zero
-  the filter sees an i image as a cyclic' (important for the FFT)
- gives more e importance to the target center.
-  Simple update

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

⇒

<!-- image -->

<!-- image -->

𝐰   new 𝐱 Train a a MOSSE filter using the new image

𝐰   𝑡-1 𝐰   new Update previous s solution with b.y linear interpolation.

<!-- image -->

<!-- image -->

## Breakthrough by MOSSE tracker

## Implementation aspects

-  Scale adaptation

<!-- image -->

Scale Input image Detection output

<!-- image -->

- Extract patches with different s scales and normalize them + the same Size
- Run classification; use bounding box with the highest response

<!-- image -->

<!-- image -->

## Circulant matrices

is a tool that connects correlation filters with machine learning

<!-- formula-not-decoded -->

##  𝐶(𝐱) is a circulant matrix:

<!-- image -->

## Why MOSSE works?

<!-- image -->

<!-- image -->

<!-- image -->

## Circulant matrices

is a tool that connects correlation f filters With 1 machine learning

-  X = 𝐶 𝐱 𝐱 We can s as a dataset with cyclically shifted versions of the

<!-- formula-not-decoded -->

- 𝑃 shifts the pixels in 1 vertical/horizontal direction by 1 element.
- 𝑖 𝑃 𝑖 𝐱 Arbitrary with power
- 𝑃 𝑛 𝐱 = 𝑃 0 𝐱 = 𝐱

<!-- image -->

## Why MOSSE works?

<!-- image -->

<!-- image -->

<!-- image -->

## Circulant matrices

is a tool that connects correlation filters with machine learning

-  Similar role to the Convolution Theorem

<!-- formula-not-decoded -->

-  ⇒ Most of the "data" is 0 and can be ignored!

## Why MOSSE works?

<!-- image -->

<!-- image -->

<!-- image -->

## Why MOSSE works?

## Ridge Regression Formulation

- Least-Squares with 1 regularization avoids overfitting!)
-  Consider simple Ridge e Regression RR) problem:

<!-- formula-not-decoded -->

s closed-form s solution:

<!-- formula-not-decoded -->

has

X = 𝐶(𝐱) 𝐲 = 𝐠 We can j (circulant data), and Gaussian t targets).

-  Diagonalizing the involved circulant r matrices with n the DFT yields:

<!-- formula-not-decoded -->

- Exactly the e MOSSE solution!
- good learning a algorithm (RR) with lots of data circulant shifted samples).

<!-- image -->

<!-- image -->

<!-- image -->

## Kernelized Correlation Filters

<!-- image -->

-  Circulant matrices are a very general l tool 1 which allows to replace standard ( operations with n fast Fourier operations.
-   The same e idea can by applied e.g. to the Kernel Ridge Regression: with K kernel matrix X; and dual space e representation

<!-- formula-not-decoded -->

-   circulant K matrix

<!-- formula-not-decoded -->

, 𝐤 𝐱𝐱

𝒪 𝑛 2

𝐾

-  Diagonalizing with the DFT for learning the classifier yields:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- image -->

<!-- image -->

## Kernelized Correlation Filters

-  𝐤 𝐱𝐱′ x x' is kernel correlation of two

<!-- formula-not-decoded -->

-  For Gaussian kernel it yields:

multiple channels can be concatenated to the vector X and then sum over in this term

<!-- formula-not-decoded -->

-  𝜶 Evaluation on subwindows of image z with classifier model X:
- 𝐾 𝐳 = 𝐶 𝐤 𝐱𝐳 1.
- 𝐟(𝐳) = ℱ -1 𝐤 𝐱𝐳 ⊙ 𝛂 2.
-  𝜶 Update classifier model X by linear interpolation from the e location of maximum response f(z)
-  Kernel allows integration of more complex and multi-channel features

<!-- image -->

<!-- image -->

<!-- image -->

## Kernelized Correlation Filters

## KCF Tracker

-  few very hyperparameters
-  code fits slide on one of the presentation!
-  Use HoG features channels) (32
-  ~300 1 FPS

<!-- image -->

## Training and detection (Matlab)

```
function alphaf = train (x, y, sigma, lambda) k = kernel_correlation (x, x, sigma); alphaf = fft2(y) ./ (fft2(k) + lambda); end function y = detect (alphaf, x, z, sigma) k = kernel_correlation (z, x, sigma); y = real(ifft2(alphaf .* fft2(k))); end function k = kernel_correlation (x1, x2, sigma) c = ifft2(sum(conj(fft2(x1)) .* fft2(x2), 3)); d = x1(:)'*x1(:) + x2(:)'*x2(:) - 2 * c; k = exp(-1 / sigma^2 * abs(d) / numel(d)); end
```

-  Open-Source (Matlab/Python) /Java / C)

Sum channel dimension over in kernel computation

<!-- image -->

<!-- image -->

## Basic

-  Honriques et al. - CSK
- grayscale pixel values as features raw
-  Honriques et al. - KCF
- HoG multi-channel features

## Further work

-  Donolljan et al. - DSST:
- PCA-HoG + grayscale pixels features
- filters for translation and for scale (in the scale-space pyramid)
-  Ii ot l.- SAMF:
- HaG, color-naming and grayscale pixels features
- quantize scale space and normalize each scale to one size by bilinear inter. → only one filter on normalized size

## Variations of KCF trackers

<!-- image -->

<!-- image -->

<!-- image -->

## Further work

-  Donelljan et al. -SRDCF:
- spatial regularization in the learning process
- → limits boundary effect
- -→ penalize filter coefficients depending on their spatial location
- llows to use much larger search region
- more discriminative to background (more training data)

## CNN-based Correlation Trackers

-  Mo ot al.
- features : VGG-Net pretrained on ImageNet dataset extracted from third, fourth and fifth convolution layer
- for each feature learn a linear correlation filter
- coarse-to-fine approach from 5—→3 layer
-  Nom ct al. - MDNet:
- CNN classification (3 convolution lavers and 2 fully connected layers) learn on tracking sequences with bbox regression

## Variations of KCF trackers

<!-- image -->

<!-- image -->

<!-- image -->

## Results of KCF-based trackers

<!-- image -->

## Result t on recent standard evaluation benchmarks

DSST, SAMF, KCF, DGT, PLT14, PLT13

<!-- image -->

<!-- image -->