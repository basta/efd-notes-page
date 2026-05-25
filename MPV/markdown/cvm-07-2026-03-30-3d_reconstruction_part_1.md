<!-- image -->

## 3D Reconstruction Part 1: Camera Pose Estimation

## Computer Vision Methods 2026 Lecture 7

## The 3D Reconstruction Problem

<!-- image -->

video credit: Jonas Kulhanek

[Jonas Kulhanek, Songyou Peng, Zuzana Kukelova, Marc Pollefeys, Sattler, WildGaussians: 3D Gaussian Splatting In the Wild, NeurIPS 2024]

<!-- image -->

## 3D Reconstruction Pipelines

<!-- image -->

<!-- image -->

Images

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## 3D Reconstruction Pipelines

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## 3D Reconstruction Pipelines

<!-- image -->

## 3D Reconstruction Pipelines

Images Camera Pose Estimation via Structure-from-Motion Dense Reconstruction (MVS, NeRF, Gaussian Splatting, etc.)

<!-- image -->

<!-- image -->

## 3D Reconstruction Pipelines

Images Camera Pose Estimation via Structure-from-Motion Camera Pose Estimation via Structure-fromMotion Dense Reconstruction (MVS, NeRF, Gaussian Splatting, etc.)

## Structure-from-Motion (SfM)

Input: images

<!-- image -->

Output: (sparse) 3D point cloud, camera poses

<!-- image -->

## Feature-Based Structure-from-Motion (SfM)

<!-- image -->

<!-- image -->

||

||

## Feature-Based Structure-from-Motion (SfM)

<!-- image -->

Incremental SfM

<!-- image -->

## Feature-Based Structure-from-Motion (SfM)

<!-- image -->

Incremental SfM

<!-- image -->

## Feature-Based Structure-from-Motion (SfM)

True trajectory

<!-- image -->

<!-- image -->

<!-- image -->

## Feature-Based Structure-from-Motion (SfM)

True trajectory Estimated trajectory

<!-- image -->

<!-- image -->

<!-- image -->

## Feature-Based Structure-from-Motion (SfM)

<!-- image -->

<!-- image -->

## Feature-Based Structure-from-Motion (SfM)

<!-- image -->

<!-- image -->

## Feature-Based Structure-from-Motion (SfM)

<!-- image -->

<!-- image -->

<!-- image -->

## Camera Obscura

<!-- image -->

attic  wall in Prague castle image source: wikipedia

<!-- image -->

## Camera Obscura

<!-- image -->

Camera obscura in Gemma Frisius' 1545 book De Radio Astronomica et Geometrica image source: wikipedia

<!-- image -->

## Pinhole Camera Model

<!-- image -->

slide credit: Olof Enqvist

f its projection in an image.

## Pinhole Camera Model a centre a point in the scene and let w be the vector to its by looking closer at w . We introduce a camera coordinate tre and two axes parallel to the image plane. The third axis

Start by looking at Figure

??

.

We already know that the distance from the camera centre

hat a vector from the camera centre to a point in the image

Figure 6.1:



x

1

x

2

f



era equation





in the camera coordinate system.

Let

ole) in the global coordinate system. Consider a point

n is to derive an equation that relates a point

rdinates (

tem.

u, v

) of its projection in an image.

from the camera centre a point in the scene and let

e.

Let's start by looking closer at

the camera centre and two axes parallel to the image plane.

e image plane.

<!-- image -->

We already know that the distance from the camera centre

35

Figure 6.1:

The camera equati

The aim of this section is to derive an

world to the pixel coordinates (

Let u, v

<!-- image -->

) of

be the vector from the camera

projection in the image.

Let's start by

slide credit: Olof Enqvist system with origin at the camera centre

is perpendicular to the image plane.

Principle of a pinhole camera.

x

=

<!-- image -->

<!-- image -->

## Pinhole Camera Model

<!-- image -->

C

figure adapted from Hartley and Zisserman, 2004

## Homogeneous Coordinates

## Homogenous coordinates

<!-- formula-not-decoded -->

̸

De-homogenization:

<!-- formula-not-decoded -->

2D projective space:

<!-- image -->

<!-- formula-not-decoded -->

## Homogeneous Coordinates

Homogenous coordinates

<!-- formula-not-decoded -->

̸

De-homogenization:

<!-- formula-not-decoded -->

2D projective space:

<!-- image -->

<!-- formula-not-decoded -->

Mapping 2D points ⟷ 3D lines

<!-- image -->

## Homogeneous Coordinates

Homogenous coordinates

<!-- formula-not-decoded -->

̸

De-homogenization:

<!-- formula-not-decoded -->

2D projective space:

<!-- image -->

<!-- formula-not-decoded -->

Mapping 2D points ⟷ 3D lines

<!-- image -->

## Homogeneous Coordinates

Homogenous coordinates

<!-- formula-not-decoded -->

̸

De-homogenization:

<!-- formula-not-decoded -->

2D projective space:

<!-- image -->

<!-- formula-not-decoded -->

Mapping 2D points ⟷ 3D lines





<!-- image -->

## Pinhole Camera Model - Projection

<!-- image -->

<!-- image -->

## Pinhole Camera Model - Projection

Projection as matrix multiplication:

<!-- formula-not-decoded -->

figure from Hartley and Zisserman, 2004

<!-- image -->

<!-- image -->

x

## Mapping to Pixel Coordinates w 1 w 2 f  =  ( u -p u ) ρ ( v -p v ) ρ f  =  ρ 0 -ρ p u 0 ρ -ρ p c 0 0 f   u v 1  (6.2) s x ions that allow local deformations of the image, we will write x

˜

y

˜

alled the calibration

)

1

)

(

)

)

(

of the source image. Hence, deformation function or deformation

ualize

visualize for each pixel in the warped as two matrices/images, one for the row deformation

ation. Figure 9.6 shows an example where all the deformation lies

<!-- formula-not-decoded -->

K

<!-- image -->

ond dimension of

d a deformation field

∆

Projection as matrix multiplication:

<!-- image -->

<!-- formula-not-decoded -->

=

(9.23)

(9.23)

## Intrinsic Camera Calibration Matrix K

<!-- image -->

aspect ratio of pixels

<!-- image -->

1

<!-- image -->

non-rectangular pixels for s ≠ 0

## Intrinsic Camera Calibration Matrix K

<!-- image -->

aspect ratio of pixels

<!-- image -->

1

<!-- image -->

non-rectangular pixels for s ≠ 0

## Forward and Backward Projections

A 3D point maps to a 2D point:

<!-- formula-not-decoded -->

A 2D point maps to a ray :

<!-- formula-not-decoded -->

<!-- image -->

<!-- image -->

<!-- image -->

## The Camera Pose

<!-- image -->

Transformation from global to camera coordinates:

<!-- formula-not-decoded -->

figure adapted from Hartley and Zisserman, 2004

## Sequential / Incremental SfM

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

<!-- image -->

Feature Detection

Detect interest points and extract descriptors for them, e.g., SIFT features

## Sequential / Incremental SfM

<!-- image -->

<!-- image -->

- Nearest neighbor search in descriptor space to establish feature matches
- Robust model fitting via RANSAC

<!-- image -->

<!-- image -->

## Epipolar Geometry

€

<!-- image -->

€

<!-- image -->

## Epipolar Geometry

<!-- image -->

€

€

<!-- image -->

## Epipolar Geometry

<!-- image -->

€

<!-- image -->

## Epipolar Geometry

<!-- image -->

€

<!-- image -->

## Epipolar Geometry

<!-- image -->

€

<!-- image -->

## Epipolar Geometry

<!-- image -->

<!-- formula-not-decoded -->

€

<!-- image -->

## Epipolar Geometry

<!-- image -->

<!-- formula-not-decoded -->

unknown

<!-- image -->

## Epipolar Geometry

<!-- image -->

€

&lt;latexi

sh

1\_b

64="G

q3dZWcC

RHAUYKE

7Fg

&gt;

X

V

NSwM

D

2

v

LI

o

5p

m

/

T

B

0

fj+

8

9

u

r

J

k

O

z

n

P

Q

y

<!-- image -->

## Epipolar Geometry

<!-- image -->

€

&lt;latexi

sh

1\_b

64="G

q3dZWcC

RHAUYKE

7Fg

&gt;

X

V

NSwM

D

2

v

LI

o

5p

m

/

T

B

0

fj+

8

9

u

r

J

k

O

z

n

P

Q

y

<!-- image -->

## Epipolar Geometry

<!-- image -->

€

&lt;latexi

sh

1\_b

64="G

q3dZWcC

RHAUYKE

7Fg

&gt;

X

V

NSwM

D

2

v

LI

o

5p

m

/

T

B

0

fj+

8

9

u

r

J

k

O

z

n

P

Q

y

<!-- image -->

## Epipolar Geometry

<!-- image -->

€

<!-- image -->

## Epipolar Geometry

<!-- image -->

€

<!-- formula-not-decoded -->

## Epipolar Geometry

<!-- image -->

<!-- image -->

## Epipolar Geometry

<!-- image -->

<!-- formula-not-decoded -->

<!-- image -->

<!-- image -->

€

## Epipolar Geometry

<!-- image -->

<!-- formula-not-decoded -->

<!-- image -->

## The Essential Matrix

<!-- formula-not-decoded -->

- Essential matrix E
- E is 3x3 matrix, has 5 DoF (degrees-of-freedom)
- E has two equal singular values, third singular value is 0
- E has rank 2

<!-- image -->

## The Fundamental Matrix

<!-- formula-not-decoded -->

- Fundamental Matrix F
- F has 7 DoF
- F has rank 2
- Computing F does not require intrinsic calibration

<!-- image -->

## Geometric Interpretation

€

<!-- image -->

€

<!-- image -->

## Geometric Interpretation

€

<!-- image -->

€

<!-- image -->

## Geometric Interpretation

€

<!-- image -->

€

<!-- image -->

## Geometric Interpretation

€

<!-- image -->

€

<!-- image -->

## Geometric Interpretation

<!-- image -->

€

<!-- image -->

## Geometric Interpretation

<!-- image -->

€

<!-- image -->

## Geometric Interpretation

<!-- image -->

€

<!-- image -->

## Geometric Interpretation

<!-- image -->

€

<!-- image -->

## Geometric Interpretation

<!-- image -->

<!-- image -->

## Geometric Interpretation

<!-- image -->

<!-- image -->

## Epipolar Lines

<!-- image -->

<!-- image -->

figure from Hartley and Zisserman, 2004

## Computing The Essential / Fundamental Matrix

- Estimate 2D-2D matches between images
- Compute E / F using RANSAC:
- Linear solver (8 points): E and F
- Minimal solver (7 points): E and F
- Calibrated solver (5 points): Only E
- Refine E / F based on all inliers
- For details, see:
- [Geometry of Computer Vision and Graphics lecture](https://cw.fel.cvut.cz/wiki/courses/gvg/start)
- Richard Szeliski's Computer Vision: Algorithms and Applications book (freely available online)
- Hartley &amp; Zisserman, Multiple View Geometry in Computer Vision, 2nd edition, Cambridge University Press, 2004

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

||

||

- Extract relative rotation and translation from H/E/F matrix
- Use 2D-2D matches to triangulate 3D structure

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

||

||

- Extract relative rotation and translation from H/E/F matrix
- Use 2D-2D matches to triangulate 3D structure

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

||

||

- Extract relative rotation and translation from H/E/F matrix
- Use 2D-2D matches to triangulate 3D structure

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

||

||

- Extract relative rotation and translation from H/E/F matrix
- Use 2D-2D matches to triangulate 3D structure

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

||

||

- Extract relative rotation and translation from H/E/F matrix
- Use 2D-2D matches to triangulate 3D structure

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

||

||

- Extract relative rotation and translation from H/E/F matrix
- Use 2D-2D matches to triangulate 3D structure

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

||

||

- Extract relative rotation and translation from H/E/F matrix
- Use 2D-2D matches to triangulate 3D structure

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

- How to select a good initial pair?
- Criteria:
- Accurate relative pose ≈ many inlier matches
- Non-planar scene (planar scenes are degeneracy for F-matrix fitting)
- Compute both homography H and E/F matrix
- Select pair with large ratio #inliers(E/F) / #inliers(H)
- No pure forward motion (triangulation inaccurate / impossible)
- In practice, try out multiple initial pairs

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

- Pick image(s) with large number of matches to existing cameras
- Obtain 2D-3D matches from 2D-2D matches
- Estimate absolute pose of new image

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

- Pick image(s) with large number of matches to existing cameras
- Obtain 2D-3D matches from 2D-2D matches
- Estimate absolute pose of new image

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

- Pick image(s) with large number of matches to existing cameras
- Obtain 2D-3D matches from 2D-2D matches
- Estimate absolute pose of new image

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

- Pick image(s) with large number of matches to existing cameras
- Obtain 2D-3D matches from 2D-2D matches
- Estimate absolute pose of new image

<!-- image -->

<!-- image -->

## Absolute Camera Pose Estimation

<!-- image -->

- Given: n 2D-3D correspondences ( x i , Xi )
- Compute pose [R|t] s.t. K[R|t] X i = α i x i , α i&gt;0
- Optionally: Also estimate internal calibration matrix K
- In form of individual parameters
- In form of projection matrix P = K[R|t]

<!-- image -->

## 3-Point Pose Problem (P3P)

<!-- image -->

- Case : Intrinsic calibration known [Haralick et al., ICVJ'94]

<!-- image -->

## 3-Point Pose Problem (P3P)

<!-- image -->

- Case : Intrinsic calibration known [Haralick et al., ICVJ'94]

<!-- image -->

## 3-Point Pose Problem (P3P)

<!-- image -->

- Case : Intrinsic calibration known [Haralick et al., ICVJ'94]

<!-- image -->

## 3-Point Pose Problem (P3P)

<!-- image -->

- Case : Intrinsic calibration known [Haralick et al., ICVJ'94]

<!-- image -->

## 3-Point Pose Problem (P3P)

<!-- image -->

- Case : Intrinsic calibration known [Haralick et al., ICVJ'94]

<!-- image -->

## 3-Point Pose Problem (P3P)

<!-- image -->

- Case : Intrinsic calibration known [Haralick et al., ICVJ'94]

<!-- image -->

## 3-Point Pose Problem (P3P)

<!-- image -->

<!-- image -->

- Case : Intrinsic calibration known [Haralick et al., ICVJ'94]

<!-- image -->

## 3-Point Pose Problem (P3P)

<!-- image -->

<!-- image -->

- Case : Intrinsic calibration known [Haralick et al., ICVJ'94]

<!-- image -->

## 3-Point Pose Problem (P3P)

<!-- image -->

<!-- image -->

- Case : Intrinsic calibration known [Haralick et al., ICVJ'94]

<!-- image -->

## 3-Point Pose Problem (P3P)

<!-- image -->

- Case : Intrinsic calibration known [Haralick et al., ICVJ'94]

<!-- image -->

## 3-Point Pose Problem (P3P)

<!-- image -->

- Case : Intrinsic calibration known [Haralick et al., ICVJ'94]
- Recover depths: Solve 4 th  degree univariate polynomial [Fischler, Bolles, CACM'91]

<!-- image -->

## 3-Point Pose Problem (P3P)

<!-- image -->

- Case : Intrinsic calibration known [Haralick et al., ICVJ'94]
- Recover depths: Solve 4 th  degree univariate polynomial [Fischler, Bolles, CACM'91]
- Recover pose by aligning local and global point positions

<!-- image -->

## 3-Point Pose Problem (P3P)

<!-- image -->

- Case : Intrinsic calibration known [Haralick et al., ICVJ'94]
- Recover depths: Solve 4 th  degree univariate polynomial [Fischler, Bolles, CACM'91]
- Recover pose by aligning local and global point positions
- Very efficient: ~2µs total [Kneip et al., CVPR'11] [code]

<!-- image -->

## 3-Point Pose Problem (P3P)

<!-- image -->

- Case : Intrinsic calibration known [Haralick et al., ICVJ'94]
- Recover depths: Solve 4 th  degree univariate polynomial [Fischler, Bolles, CACM'91]
- Recover pose by aligning local and global point positions
- Very efficient: ~2µs total [Kneip et al., CVPR'11] [code]
- Up to four solutions: Disambiguate using 4 th  point

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

- Associate existing 3D points with new features
- Triangulate new 3D points for features without associated 3D points

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

- Associate existing 3D points with new features
- Triangulate new 3D points for features without associated 3D points

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

- Associate existing 3D points with new features
- Triangulate new 3D points for features without associated 3D points

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

- Associate existing 3D points with new features
- Triangulate new 3D points for features without associated 3D points

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

True trajectory

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

True trajectory Estimated trajectory

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

True trajectory Estimated trajectory

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

True trajectory Estimated trajectory

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

True trajectory Estimated trajectory

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

True trajectory Estimated trajectory

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

True trajectory Estimated trajectory

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

True trajectory Estimated trajectory

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

True trajectory Estimated trajectory

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

True trajectory Estimated trajectory

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

True trajectory Estimated trajectory

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

- Errors accumulate, leading to drift over time

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

- Errors accumulate, leading to drift over time
- Adjust motion and structure frequently

<!-- image -->

<!-- image -->

## Sequential / Incremental SfM

<!-- image -->

- Errors accumulate, leading to drift over time
- Adjust motion and structure frequently

<!-- image -->

<!-- image -->

## Bundle Adjustment

<!-- image -->

<!-- image -->

<!-- image -->

## Gradient descent

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Iterate until convergence or for fixed number of iterations Initialization: X k = X 0 &lt;latexi sh 1\_b 64=" ovcjQ C2 u B Hw L p /A &gt; R V SgM F 3U q7EzW XJ Z N rG f0 T m y + 9 n 8 P I DY d O 5 K k : Step size (fixed or η &lt;latexi sh 1\_b 64="0rHn7N wzB L X Rf5 T dG &gt;A C c V gI FO3 /E S k jU M m 2 Z J + W 8Kv Po p y 9 Qu Y q D : Jacobian J = ∂ f ( X ) &lt;latexi sh 1\_b 64="y M2JH +CV LNwgj Io r 9 &gt;A n c S FE3 Z u XQT R d 0Y U k q KG z/B v f P W D 5 mO p 8 7 Compute gradient: ∇ f ( X k ) = J T ∆ &lt;latexi sh 1\_b 64=" v2q AYTn N+ 8R0 MG C/ k &gt; V3 c HBS EO Z u 9 J W wo r UQ F I K P X pjD g d 7 5 y m f z L Update: X k +1 = X k -η ∇ f ( X k ) &lt;latexi sh 1\_b 64="rVp YDdjJq P 7 U9 0 + Q &gt;A CZn c HBS N EO3M u XFg wL my W v I RKG / T k 8 f 5 o z 2      

adaptive)

Slow convergence near minimum point!

<!-- image -->

## Bundle Adjustment

<!-- image -->

## Newton's method

2 nd  order approximation (quadratic Taylor expansion):

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Find     that minimizes                            ! f ( X + δ ) | X = X k δ &lt;latexi sh 1\_b 64="8vfdKHN 2 qy3I uA G Pg &gt; CL c V S FJ r X W YB UQ R 9 Mp Tm zo5 + w D 7 j n / Z E 0 k O

<!-- image -->

<!-- formula-not-decoded -->

## Bundle Adjustment

<!-- image -->

&lt;latexi

sh

1\_b

64="0y2AQgCno

9

UX

w+

ru

W

kB

&gt;

H

c

VFNS8

E

3G7

/

L

Z

q

P

Y

T

m

Rd

O

f

p

5Mz

v

K

J

D

I

j

&lt;latexi

sh

1\_b

64="0HkB

JCN2Scgzv3PGZD

9

QK

&gt;A

UX

VF

wM

E

d

7

o

yq

L

r

p

5R

/

+

m

Wf

8

Y

j

I

n

T

u

O

## Bundle Adjustment

## Newton's method

Differentiate and set to 0 gives:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Computation of H is not trivial (2 nd  order derivatives) and optimization might get stuck at saddle point!

<!-- image -->

<!-- image -->

## Gauss-Newton

Approximate Hessian matrix by dropping 2nd order terms:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Might get stuck and slow convergence at saddle point!

<!-- image -->

## Bundle Adjustment

<!-- image -->

Solve normal equation:

&lt;latexi

sh

1\_b

64="2d

Y

N

y

ZzM

F+fwnCuA

VQ

&gt;

H

c

LSg

E3

v

50

G8

D

j

U

r

q

k

T

p

J

O

o

/

9

I

m

W

X

7

R

B

K

P

## Bundle Adjustment

## Levenberg-Marquardt

Regularized Gauss-Newton with damping factor

: Gauss-Newton (when convergence is rapid) λ → 0 &lt;latexi sh 1\_b 64="F3jv 2Rp+A ck C DMQ N dw &gt; H V LSg rPX W y5 B Z 0 J zY U / f T n Ou G 7 o 9 8 I EK q m

<!-- formula-not-decoded -->

: Gradient descent (when convergence is slow) λ →∞ &lt;latexi sh 1\_b 64="vA+MrUL I fpFCuE9 PSDNBk &gt; RX c VH g 3 q mW Z Y d K 5 zy Q8G / O 7 T 2 w n 0 o j J

Adapt λ during optimization:

-  Decrease λ when function value decreases
-  Increase λ otherwise

<!-- image -->

<!-- image -->

## Bundle Adjustment

<!-- image -->

Reconstruction of the old inner city of Aachen, Germany, using the Bundler SfM software

slide credit: Gim Hee Lee

<!-- image -->

<!-- image -->

- Not covered here:
- Sparse structure of the bundle adjustment problem
- Efficient strategies (e.g., Schur Complement Trick)
- …
- Recommended reading:
- Triggs et al., Bundle Adjustment - A Modern Synthesis, 1999

<!-- image -->

## Bundle Adjustment

<!-- image -->

## SfM Models Are Defined Up to Scale

<!-- image -->

photo credit: Zuzana Kukelova

<!-- image -->

## SfM Models Are Defined Up to Scale

<!-- image -->

[photo credit: Miguel Mendez](https://www.flickr.com/photos/flynn_nrg/34100940144/)

<!-- image -->

## SfM Models Are Defined Up to Scale

3D point X seen from camera with pose R, t, intrinsics K

Scale 3D scene by arbitrary factor s ≠ 0

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- image -->

&lt;latexi

sh

1\_b

64="3T9z

rAMyW

LFoq

gv+S

k/

8

&gt;

D

n

cfVJd

w

HU

P

YZ

GO

E5I

K

C

7Bp

X

Q

N

j

0

R

m

2

u

## Structure-from-Motion Software

<!-- image -->

- [COLMAP (https://colmap.github.io/index.html)](https://colmap.github.io/index.html)
- Linux, Mac OS X, Windows, open source
- SfM and dense reconstruction (NVidia GPU required for dense recon.)
- Efficient pipeline, GUI
- High code quality, great tool for research!

<!-- image -->

## Structure-from-Motion Software

<!-- image -->

- [COLMAP (https://colmap.github.io/index.html)](https://colmap.github.io/index.html)
- Linux, Mac OS X, Windows, open source
- SfM and dense reconstruction (NVidia GPU required for dense recon.)
- Efficient pipeline, GUI
- High code quality, great tool for research!

<!-- image -->

## Learning-based Structure-from-Motion?

<!-- image -->

<!-- image -->

## Learning-based Structure-from-Motion?

<!-- image -->

<!-- image -->

## Learning-based Structure-from-Motion?

<!-- image -->

<!-- image -->

## DUSt3R: Geometric 3D Vision Made Easy

<!-- image -->

<!-- image -->

relative pose estimation based on geometric reasoning , e.g., 3D point cloud alignment or 2D-3D correspondences

## DUSt3R: Geometric 3D Vision Made Easy

[online demo: https://huggingface.co/spaces/ pablovela5620/mini-dust3r](https://huggingface.co/spaces/pablovela5620/mini-dust3r)

<!-- image -->

[Shuzhe Wang, Vincent Leroy, Yohann Cabon, Boris Chidlovskii, Jérome Revaud, DUSt3R: Geometric 3D Vision Made Easy, CVPR 2024]

<!-- image -->

## Grounding Image Matching in 3D with MASt3R

<!-- image -->

Main takeaway: Feature correspondences make geometry estimation better!

<!-- image -->

## Grounding Image Matching in 3D with MASt3R

<!-- image -->

<!-- image -->

<!-- image -->

## Learning-based Structure-from-Motion?

<!-- image -->

<!-- image -->

## Learning-based Structure-from-Motion?

<!-- image -->

<!-- image -->

Computationally expensive: Minutes to days, depending on number of images

<!-- image -->

## Learning-based Structure-from-Motion?

<!-- image -->

<!-- image -->

Computationally expensive: Minutes to days, depending on number of images Can we train a network to perform Structure-from-Motion in a feedforward manner?

<!-- image -->

## VGGT: Visual Geometry Grounded Transformer

<!-- image -->

[Jianyuan Wang, Minghao Chen, Nikita Karaev, Andrea Vedaldi, Christian Rupprecht, David Novotny, VGGT: Visual Geometry Grounded Transformer, CVPR 2025] ( best paper award )

<!-- image -->

## Results - Single View Depth Estimation

<!-- image -->

<!-- image -->

CTU IN PRAGUE

Input

<!-- image -->

Two views

<!-- image -->

CTU IN PRAGUE

## Results - Two Views

<!-- image -->

DUSt3R

<!-- image -->

32 views

## Results - Multiple Views

<!-- image -->

<!-- image -->

## VGGT - Takeaways

<!-- image -->

[Jianyuan Wang, Minghao Chen, Nikita Karaev, Andrea Vedaldi, Christian Rupprecht, David Novotny, VGGT: Visual Geometry Grounded Transformer, CVPR 2025] ( best paper award )

<!-- image -->

## Depth Anything 3

<!-- image -->

<!-- image -->

## Ray Maps + Depth Maps

<!-- image -->

<!-- image -->

Combination of ray maps and depth maps sufficient to …

- … estimate camera pose
- … estimate camera intrinsics

## Depth Anything 3 (DA3) - Dynamic Scenes

<!-- image -->

<!-- image -->

<!-- image -->

[Haotong Lin, Sili Chen, Jun Hao Liew, Donny Y. Chen, Zhenyu Li, Guang Shi, Jiashi Feng, Bingyi Kang, Depth Anything 3: Recovering the Visual Space from Any Views, ICLR 2026]

<!-- image -->

CTUINPRAGUE

<!-- image -->

## Scalability via Chunking

<!-- image -->

## Do These Networks Learn About Epipolar Geometry?

- Train small network to predict fundamental matrices for different layers
- Measure error using predicted F-matrices and given correspondences

## VGGT

Sampson Error Across Layers

<!-- image -->

## Depth Anything 3

Sampson Error Across Layers

<!-- image -->

## Real data

[Jelena Bratulic, Sudhanshu Mittal, Thomas Brox, Christian Rupprecht, On Geometric Understanding and Learned Priors in Feed-forward 3D Reconstruction Models, arXiv:2512.11508]

<!-- image -->

CTU IN PRAGUE

## Has Learning Solved Structure-from-Motion?

<!-- image -->

<!-- image -->

## Has Learning Solved Structure-from-Motion?

<!-- image -->

<!-- image -->

## Main Takeaways

- Classical concepts (epipolar geometry, relative pose estimation, absolute pose estimation, bundle adjustment) still important
- Learning can make individual components more robust (not necessarily more accurate)
- Feed-forward SfM approaches significantly faster than classical SfM methods based on local features
- … but estimated poses are significantly less accurate
- Interested in working on these topics (software project, MSc thesis, etc.)? Contact me!

<!-- image -->

## Next Lecture: Dense 3D Reconstruction

Input: calibrated images, camera poses, SfM model

model computed using Colmap and Poisson Surface Reconstruction

<!-- image -->

Output: dense 3D scene representation

<!-- image -->