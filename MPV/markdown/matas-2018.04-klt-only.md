The KLT (Kanade-Lucas-Tomasi) tracker

<!-- image -->

## KLT Introduction

## Given :

- Input image I and the template image T
- Region of interest (ROI) in T
- Assumed transformation W g from ROI in T to (part of) I :

<!-- formula-not-decoded -->

## Find :

- a p * such that T ( x ) is 'close' to I f ( W g ( x ; g p ¤ f )) for x j 2 j ROI

## Template image T

<!-- image -->

## Input image I

<!-- image -->

I f ( W g ( x ; g p ¤ f )

<!-- image -->

## KLT, Transformation functions

Examples of transformation W g ( x ; g p ): g R 2 c ! j R 2 ( p = parameter)

Template image

Input image

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

- Translation by p k = j ( p 1 , p 2 j ) T , p j 2 j R 2 :

<!-- formula-not-decoded -->

- Affine transformation, p j 2 j R 2 £ 3 :

<!-- formula-not-decoded -->

- Rotation by p around origin, j p = j p 2 j [0, g 2 ¼ a ) :

<!-- formula-not-decoded -->

<!-- image -->

## KLT, Measuring Fit

Measure of 'closeness' of T ( x ) and I f ( W g ( x ; g p f )), x j 2 j ROI SSD (used most often):

<!-- formula-not-decoded -->

Optimization task: Find p * such that

<!-- formula-not-decoded -->

Note : In the subsequent text, for better clarity we use the following notation for 'function at a point' interchangeably:

<!-- formula-not-decoded -->

<!-- image -->

## KLT, Finding Best Transformation p *

<!-- image -->

<!-- formula-not-decoded -->

## How to find p * ?

It would be possible to quantize the search space of p , enumerate all possibilities and take the one minimizing SSD. But this computationally expensive and would be infeasible in practice.

## KLT approach :

1. Make the linearization (first-order Taylor approximation) inside brackets w.r.t. the parameter p
2. By this, the problem is converted to least-squares problem which is well understood and has a closed-form solution.
3. Because of approximation in step 1, iterate.

## Approximating the warp

<!-- image -->

<!-- formula-not-decoded -->

## Taylor approximation of I f ( W g ( x ; g p f )) :

(W(x; po + △p))

1\w(x;po)

△十

W(x,po)

image gradient im. for current p 0

aw

ap

△p

x,Po

Jacobian of W

<!-- formula-not-decoded -->

<!-- image -->

1

## Example, pure translation

<!-- image -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

## Example, pure translation

<!-- image -->

<!-- formula-not-decoded -->

## gradient

<!-- image -->

<!-- image -->

## approximation

<!-- image -->

## image

<!-- image -->

## LSQ problem to find Δ p *

<!-- image -->

<!-- formula-not-decoded -->

Taylor approximation of I f ( W g ( x ; g p f )) :

<!-- formula-not-decoded -->

Solve for Δ p * :

<!-- formula-not-decoded -->

## KLT, Finding Best Transformation p *

This:

<!-- formula-not-decoded -->

has a form of a classical least-squares problem:

<!-- formula-not-decoded -->

where

- rows of matrix A are equal to r I f T ( @ a W g =@ g p ) (for a given x and p 0 ),
- z = Δ p , and
- elements of b equal to T ( x ) i ¡ i I ( W g ( x ; g p 0 )) , that is, current residuals for given x .

Such problem has a well-known solution, z j = j ( A T A ) ¡ 1 A T j b .

<!-- image -->

## Example, pure translation

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Solution for update (from previous slide):

Rows of A :

Stability of computation will rely on rank of this matrix

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- image -->

<!-- formula-not-decoded -->

## Example, pure translation

<!-- formula-not-decoded -->

The stability of computation will depend on invertibility of this matrix.

We have already encountered this matrix in this course.

It is directly related to Harris corner detector.

For obvious reasons, the KLT tracking for translation is well posed when the ROI contains a corner, as opposed to a flat region or an edge.

## Aperture problem :

<!-- image -->

(image courtesy of Wolfe et al. Sensation &amp; Perception)

<!-- image -->

## KLT, algorithm summary

<!-- image -->

<!-- formula-not-decoded -->

Taylor approximation of I f ( W g ( x ; g p f )) :

<!-- formula-not-decoded -->

1. Input: current estimate p 0 . Solve for Δ p * :

<!-- formula-not-decoded -->

2. Update, p 0 ← p 0 + Δ p *
3. If not converged, go to 1.
4. Best transformation p * = p 0 .

## Multi-resolution Lucas-Kanade

<!-- image -->

KLT is based on 1 st  order Taylor approximation and cannot find the solution if the displacement is too high compared to frequencies in the image.

Possible solution is to blur the image on the scale of assumed displacement and get a rough estimate.

Subsequently, continue on less blurred image and make an update to that estimate. Repeat.

This is efficiently implemented using image pyramids.

## slide credit: Patrick Perez

<!-- image -->