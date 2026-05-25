## RANSAC Robust Model Estimation From Data Contaminated By Outliers

Lecturer

: Jiří Matas

Authors : Ondřej Chum, Jiří Matas, Ondřej Drbohlav Czech Technical University in Prague

http://cmp.felk.cvut.cz

Last update: March 2021

## Talk outline

- Standard Single Class Single Instance Fitting Problem (SCSI)

<!-- image -->

)

<!-- image -->

- Robust Single Class Single Instance Fitting Problem (R-SCSI)

<!-- image -->

)

<!-- image -->

- Single Class Multiple Instance Fitting Problem (SCMI)

<!-- image -->

)

<!-- image -->

- Multiple Class Multiple Instance Fitting Problem (MCMI)

<!-- image -->

)

<!-- image -->

<!-- image -->

## Single/Multi-Class Single/Multi-Instance Fitting Applications

- detection of geometric primitives
- epipolar geometry estimation
- detection of planar surfaces
- multiple motion segmentation
- Interpretation of lidar scans

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

## What is RANSAC?

- RANSAC = RANdom SAmple Consensus
- M.A. Fischler and R.C. Bolles. Random sample consensus: A paradigm for model fitting with applications to image analysis and automated cartography. CACM, 24(6):381-395, June 1981.
- Example : Finding a line in 2D
- -Not all input points are on the line.
- -Finding a line implicitly divides points to inliers (=those on a line) and outliers (=those not on a line)

y

- -Due to noise, 'on a line' actually means inside a narrow strip around the line

<!-- image -->

<!-- image -->

## Example: Line Fitting

First, let us introduce a line parametrization and define the 'strip around the line' formally:

<!-- image -->

$$Note: n : (cos Φ, sin Φ)$$

(thus ||nl = 1)

- Line parameters: Φ E [O,π[, r E R
- Point x = (,y) on the line:

<!-- formula-not-decoded -->

- Signed( distance p(p) of point p from the line:

<!-- formula-not-decoded -->

- Point p inside a strip of half-width o:

<!-- formula-not-decoded -->

<!-- image -->

## Line Fitting, Inliers Only: Easy!

<!-- image -->

## Data points

<!-- formula-not-decoded -->

Find the line which 'best fits' these points.

<!-- image -->

## Line Fitting, Inliers Only: Easy!

<!-- image -->

## Data points

<!-- formula-not-decoded -->

Find the line which 'best fits' these points.

Optimization: Find best line with parameters    :

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

This is easily solvable by Singular Value Decomposition (SVD)

<!-- image -->

9

## General Case with Outliers, Example 1

## Example 1

<!-- image -->

C

<!-- image -->

9

## General Case with Outliers, Example 2

## Example 2

<!-- image -->

<!-- image -->

## General Case with Outliers, Robust Cost Function

- L set of data points

## Find:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

- No outliers: fLSQ(x,0) :

$$[0(x)]²$$

- For robust fitting, use instead :

<!-- formula-not-decoded -->

- Such cost function is non-convex (and the optimization task is to minimize the number of outliers)
- How to find optimal line parameters?

<!-- image -->

<!-- image -->

## RANdom SAmple Consensus - RANSAC

<!-- image -->

<!-- image -->

Select sample of m points at random (here m =2)

## RANSAC

<!-- image -->

<!-- image -->

Select sample of m points at random

Estimate model parameters from the data in the sample Select sample of m points at random Estimate model parameters from the data in the sample Evaluate the distance from model for each data point

<!-- image -->

<!-- image -->

## RANSAC

<!-- image -->

<!-- image -->

Select sample of m points at random

Estimate model parameters from the data in the sample

Evaluate the distance from model for each data point

Select data that support the current hypothesis

## RANSAC

<!-- image -->

<!-- image -->

Select sample of m points at random

Estimate model parameters from the data in the sample

Evaluate the distance from model for each data point

Select data that support the current hypothesis

Repeat sampling

## RANSAC

<!-- image -->

<!-- image -->

Select sample of m points at random

Estimate model parameters from the data in the sample

Evaluate the distance from model for each data point

Select data that support the current hypothesis

Repeat sampling

## RANSAC

<!-- image -->

<!-- image -->

Select sample of m points at random

Estimate model parameters from the data in the sample

Evaluate the distance from model for each data point

Select data that support the current hypothesis

Repeat sampling

## RANSAC [Fischler and Bolles 1981]

Input: X = {x,}=1

θ = (s)a data points estimates model parameters θ given sample S  X

<!-- image -->

if distance to model ≤ threshold o 0 f(x, 0) 1 otherwise Cost function for single data point x

<!-- formula-not-decoded -->

- required confidence in the solution, o － outlier threshold

Output: 0* p parameter of the model minimizing the cost function

1: iter ← 0, J* ← 00

2: repeat

Estimate parameters θ = e(S) 4:

Select random S ≤ &amp; (sample size m = ISl) 3:

Evaluate J(0) = ≥xex f(x, 0) 5:

<!-- formula-not-decoded -->

If J(0) &lt; J* then 6:

7: iter ← iter + 1

8: until P(better solution exists) = f(|&amp;], J*,iter) &lt; 1 -

Compute 0* from all inliers Xin: 9* ←- LocalOptimization(&amp;in, 0*) 9:

SAMPLING

VERIFICATION SO-FAR-THE-BEST

## RANSAC -how many samples?

J *

- N

Number of points

- Q Number of inliers, Q = N -

- m

Size of sample

- ² = Q/N Inlier ratio

Probability of all-inlier (uncontaminated) sample:

<!-- formula-not-decoded -->

Mean time for hitting all-inliers sample is proportional to 1/ P .

<!-- image -->

## RANSAC -how many samples?

- How about this formulation:
- -Set the number of samples k such that at least one pair of points from the line has been hit with probability larger than h
- -Equivalently … such that no pair of points from the line has been hit with probability lower than 1 h

J *

- Q Number of inliers, Q = N -

- m Size of sample

- ●

- ² = Q/N Inlier ratio

Probability of all-inlier (uncontaminated) sample:

<!-- formula-not-decoded -->

The required confidence in solution:

<!-- formula-not-decoded -->

Finding the solution with confidence h therefore requires at least k samples:

<!-- formula-not-decoded -->

<!-- image -->

## RANSAC termination -how many samples?

- m Size of sample

- ² = Q/N Inlier ratio

- h Confidence

- k

required number of samples

Probability of all-inlier (uncontaminated) sample:

<!-- formula-not-decoded -->

<!-- image -->

## RANSAC termination - How many samples?

Inlier ratio ² = Q/N [%]

Size of the sample m

| 15%        | 20%        | 30%        | 40%        | 50%        | 70%       |
|------------|------------|------------|------------|------------|-----------|
| 130        | 73         | 32         | 17         | 10         | 4         |
| 200        | 110        | 49         | 26         | 16         | 6         |
| 300        | 170        | 73         | 40         | 24         | 10        |
| 890        | 370        | 110        | 45         | 22         | 7         |
| 1400       | 570        | 170        | 70         | 34         | 11        |
| 2000       | 860        | 250        | 100        | 52         | 16        |
| 5900       | 1900       | 370        | 120        | 46         | 11        |
| 9100       | 2900       | 570        | 180        | 71         | 17        |
| 1.4·104    | 4300       | 850        | 270        | 110        | 25        |
| 1.2·107    | 1.2·106    | 4.6 · 104  | 4600       | 770        | 50        |
| 1.8.107    | 1.8 . 106  | 7.0·104    | 7000       | 1200       | 78        |
| 2.7·107    | 2.7· 106   | 1.1·105    | 1.1·104    | 1800       | 120       |
| 2.3 · 1010 | 7.3 · 108  | 5.6 · 106  | 1.8 · 105  | 1.2 · 104  | 210       |
| 3.5· 1010  | 1.1·109    | 8.7·106    | 2.7·105    | 1.9·104    | 330       |
| 5.3·1010   | 1.7·109    | 1.3·107    | 4.1·105    | 2.8 · 104  | 500       |
| 2.1 · 1015 | 1.1 · 1013 | 7.7 · 109  | 4.4 ·107   | 7.9 · 105  | 1800      |
| 3.2·1015   | 1.8· 1013  | 1.2· 1010  | 6.7· 107   | 1.2·106    | 2800      |
| 4.8· 1015  | 2.6 · 1013 | 1.8 · 1010 | 1.0·108    | 1.8 · 106  | 4200      |
| 8          | 8          | 1.3 · 1016 | 2.6 · 1012 | 3.2 · 109  | 1.3 · 105 |
| 8          | 8          | 2.1· 1016  | 3.1· 1012  | 4.9 · 109  | 2.0 · 105 |
| 8          | 8          | 3.1· 1016  | 5.1·1012   | 7.4 · 109  | 3.1·105   |
| 8          | 8          | 8          | 8          | 3.4 · 1015 | 1.7 · 108 |
| 8          | 8          | 8          | 8          | 5.2·1015   | 2.6 · 108 |
| 8          | 8          | 8          | 8          | 7.8· 1015  | 3.8· 108  |

Computed for confidences η = 0.95 (first row in each cell),

η = 0.99 (second row) and η = 0.999 (third row)

<!-- image -->

## Pros:

- extremely popular (&gt;17000 citations in Google Scholar)
- used in many applications
- percentage of inliers not needed and not limited
- a probabilistic guarantee for the solution
- mild assumptions: ¾ known

## Cons:

- slow if inlier ratio low
- It was observed experimentally that RANSAC takes several times longer than theoretically expected. This is due to noise not every all-inlier sample generates a good hypothesis:

## RANSAC Notes

<!-- image -->

## RANSAC Variants

- Cost function: MLESAC, Huber loss, …

- Outlier threshold s (how to set it in advance? Or, how to avoid setting it?): Least median of Squares, MINPRAN, MAGSAC, …
- Correctness of the results. Degeneracy.
- Accuracy (parameters are estimated from minimal samples).
- Speed: Running time grows with number of data points, number of iterations (polynomial in the inlier ratio)

Solution: DegenSAC.

Solution: Locally Optimized RANSAC

Addressing the problem: R-RANSAC (Randomized evaluation), RANSAC with SPRT

(WaldSAC),  PROSAC

<!-- image -->

9

<!-- image -->

<!-- image -->

Data: 200 points

9

<!-- image -->

<!-- image -->

Data: 200 points

Model, 100 inliers

## LO-RANSAC: Problem Introduction

For simplicity, consider only points belonging to the model (100 points)

9

<!-- image -->

<!-- image -->

9

## LO-RANSAC: Problem Introduction

For simplicity, consider only points belonging to the model (100 points)

<!-- image -->

RANSAC

Hypothesis generation from 2 points

Will every two points generate the whole inlier set?

This sample:

YES. 100 inliers.

<!-- image -->

9

## LO-RANSAC: Problem Introduction

For simplicity, consider only points belonging to the model (100 points)

<!-- image -->

RANSAC

Hypothesis generation from 2 points

Will every two points generate the whole inlier set?

This sample: NO. 45 inliers.

<!-- image -->

## LO-RANSAC: Problem Introduction

For simplicity, consider only points belonging to model (100 points)

<!-- image -->

The distribution of the number of inliers obtained while randomly sampling inlier points pairs RANSAC

Hypothesis generation from 2 points

Will every two points generate the whole inlier set?

<!-- image -->

Input: X = {x,}=1

e(S) = θ

<!-- image -->

data points

estimates model parameters θ given sample S  X

if distance to model ≤ threshold o 0 f(x, 0) 1 otherwise Cost function for single data point x

<!-- formula-not-decoded -->

- required confidence in the solution, o － outlier threshold

Output: 0* p parameter of the model minimizing the cost function

1: iter ← 0, J* ← 00

2: repeat

Estimate parameters θ = e(S) 4:

Select random S ≤ &amp; (sample size m = ISl) 3:

Evaluate J(0) = ≥xex f(x, 0) 5:

<!-- formula-not-decoded -->

If J(0) &lt; J* then 6:

7: iter ← iter + 1

8: until P(better solution exists) = f(|&amp;], J*,iter) &lt; 1 -

9:

## LO-RANSAC

SAMPLING

VERIFICATION SO-FAR-THE-BEST

Input: X = {x}=1

θ = (s)a data points estimates model parameters θ given sample S ≤ X

<!-- image -->

if distance to model ≤  threshold o 0 f(x,0) 1 otherwise Cost function for single data point x

<!-- formula-not-decoded -->

- required confidence in the solution, o - outlier threshold

Output: 0* parameter of the model minimizing the cost function

1: iter ← 0, J* ← 00

2: repeat

Estimate parameters θ = e(S) 4:

Select random S ≤ &amp; (sample size m = [Sl) 3:

Evaluate J(0) = ≥xex f(x, 0) 5:

0* ← LocalOptimization(&amp;in, 0), J* ← J(0*)

If J(0) &lt; J* then 6:

7: iter ← iter + 1

8: until P(better solution exists) = f(|&amp;|, J*, iter) &lt; 1 -

9: gone

## LO-RANSAC

SAMPLING

VERIFICATION SO-FAR-THE-BEST

9

<!-- image -->

<!-- image -->

9

<!-- image -->

<!-- image -->

9

<!-- image -->

<!-- image -->

9

<!-- image -->

<!-- image -->

9

<!-- image -->

<!-- image -->

## LO-RANSAC: Example

## Comparison with model (100 inliers):

9

<!-- image -->

<!-- image -->

## Locally Optimized RANSAC

<!-- image -->

Estimation of (approximate) models with lower complexity (less data points in the sample) followed by LO step estimating the desired model speeds the estimation up significantly.

The estimation of epipolar geometry is up  to 10000 times faster when using 3 region-to-region correspondences rather than 7 point-to-point correspondences.

Fish-eye images by Braňo Mičušík

<!-- image -->

<!-- image -->

Chum, Matas, Obdržálek : Enhancing RANSAC by Generalized Model Optimization, ACCV 2004

<!-- image -->

Simultaneous estimation of radial distortion and epipolar geometry with LO is superior to the state-of the art in both speed a precision of the model.

## LO-RANSAC: Problem Summary

<!-- image -->

It was observed experimentally that RANSAC takes several times longer than theoretically expected. This is due to the noise - not every all-inlier sample generates a good hypothesis.

By applying local optimization (LO) to the-best-so-far hypotheses:

- (i) a near perfect agreement with theoretical performance
- (ii) lower sensitivity to noise and poor conditioning.

The LO is shown to be executed so rarely, log( iter ) times,  that it has minimal impact on the execution time.

## RANSAC -Time Complexity

Repeat k times  ( k is a function of sample size m , number of inliers Q, number of data N, and confidence h )

1. Hypothesis generation
- Select a sample of m data points
- Calculate parameters of the model(s)
2. Model verification
- Find the support (consensus set) by verifying all N data points

tM time needed to draw a sample

ms 一 average number of models per sample

## Running time :

<!-- formula-not-decoded -->

Note 1 : unit of time = time to evaluate 1 point ( ⇒ evaluating N points takes time N ).

Note 2 : number of models per sample for our toy, line fitting example, is equal to 1. Some tasks (e.g. epipolar geometry estimation) generate different number of solutions (models) per sample, depending on the sample data. 7-point algorithm, for example, generates up to 3 models.

<!-- image -->

y

## Randomised RANSAC (R-RANSAC) [Matas, Chum 02]

Repeat until termination condition is met:

1. Hypothesis generation (as before)
2. 2a. Model pre-verification

Td,d test: Evaluate 𝑑 ≪ 𝑁 data points, reject the model if not all d data points are consistent with the model

- 2b. Model verification Verify the rest of the data points if pre-verification test was successful

<!-- image -->

## Example ( d =1)

1. Generate a model (sample 2 points)
2. 2a. Sample another point ● Does it fall within threshold? No. Go to 1.

<!-- image -->

y

## Randomised RANSAC (R-RANSAC) [Matas, Chum 02]

Repeat until termination condition is met:

1. Hypothesis generation (as before)
2. 2a. Model pre-verification Td,d test:

Evaluate 𝑑 ≪ 𝑁 data points, reject the model if not all d data points are consistent with the model

- 2b. Model verification Verify the rest of the data points if pre-verification test was successful

<!-- image -->

## Example ( d =1)

1. Generate a model (sample 2 points)
2. 2a. Sample another point ● Does it fall within threshold? Yes.
3. 2b. Verify all other points.

®

<!-- image -->

## R-RANSAC Example, Running Time Analysis

Find a line in 2D points. N =10k, ² = 0.1 (10% inliers.)

## RANSAC

:

Probability of selecting 2 'good' points is 𝜖 2 .

Average number of samples to find a good model is 1/𝜖 2 = 100.

For each model, N points are verified.

Total number of evaluations is 100 N = 1M

9

<!-- image -->

<!-- image -->

## R-RANSAC Example, Running Time Analysis

Find a line in 2D points. N =10k, ² = 0.1 (10% inliers.)

## R-RANSAC ( d =1):

Probability of selecting 2 'good' points is 𝜖 2

.

Probability of selecting inlier point for pre-verification is 𝜖.

Average number of samples to find a good model is 1/𝜖 3 = 1000 .

Probability of a random point passing pre-verification test for a 'bad' model is δ = 0.03

y

<!-- image -->

```
In 1000 samples: 1000 ∙ 𝜖 2 = 10 'good' models 10 ∙ ² = 1 passes pre-verification 10 ∙ (1² )=9 fails pre-verification 1000 ∙ (1 - 𝜖 2 ) = 990 'bad' models 990 ∙ δ = 30 passes pre-verification 990 ∙(1 -δ ) = 960   fails pre-verification Total number of evaluations, on average: 1 N (good model, point accepted) + 9 (good model, point rejected) + 30 N (bad model, point accepted) +  960   (bad model, point rejected) ≈ 311k
```

?

<!-- image -->

## R-RANSAC Example, Running Time Analysis

Find a line in 2D points. N =10k, ² = 0.1 (10% inliers.)

## R-RANSAC ( d =2):

Probability of selecting 2 'good' points is 𝜖 2

.

Probability of selecting 2 inlier points for pre-verification is 𝜖 2 .

Average number of samples to find a good model is 1/𝜖 4 = 10000 .

y

<!-- image -->

```
In 10000 samples: 10000 ∙ 𝜖 2 = 100 'good' models 100 ∙ 𝜖 2 = 1 passes pre-verification 100 ∙ (1² ) = 99   fails pre-verification 10000 ∙ (1 - 𝜖 2 ) = 9900 'bad' models 9900 ∙ δ 2 = 9 passes pre-verification 990 ∙( 1δ 2 ) = 9891 fails pre-verification
```

Total number of evaluations, on average: 1 N (good model, 2 points accepted) + 99 ∙ 2 (good model, point(s) rejected) + 9 N (bad model, 2 points accepted) +  9891 2 (bad model, point rejected)

∙ ≈ 120k

Note : For this case, d

=2 is optimal (fastest)

<!-- image -->

## Randomised RANSAC (R-RANSAC) [Matas, Chum 02]

Speeds up RANSAC; 'Randomised' stands for randomised verification

Running time (RANSAC → R-RANSAC):

<!-- formula-not-decoded -->

V - average number of data points verified

a probability that a good model is rejected by Td,d test

k - number of samples (function of sample size, inlier ratio and confidence)

<!-- image -->

## Optimal Randomised Strategy

Model Verification employing Sequential Decision Making

where Hg - hypothesis of a 'good' model ( ≈ from an uncontaminated sample) Hb - hypothesis of a 'bad' model ( ≈ from a contaminated sample)  - probability of a data point being consistent with an arbitrary model Hg:1 P(c = 1|Hg) ≥ ε Hb: P(∞=1|Hb) = c is consistent with the model C=1

Optimal (the fastest) test that ensures with probability α that that Hg is not incorrectly rejected is  the Sequential probability ratio test (SPRT) [Wald47]

<!-- image -->

## SPRT  [simplified from Wald 47]

Likelihood ratio

<!-- formula-not-decoded -->

Set (compute) threshold A . Set j =1

1. Select a point and check whether it is consistent with model
2. Update likelihood ratio
3. If λj &gt;A decide the model is 'bad', else increment j
4. If j &gt; N (total number of points) decide model is 'good', else go to 1.

## Properties of SPRT:

1. probability of rejecting a 'good' model α &lt; 1/ A
2. average number of verifications V= C log( A

)

<!-- formula-not-decoded -->

<!-- image -->

## SPRT properties

Probability of rejecting a 'good' model a =1/ A

<!-- formula-not-decoded -->

If 入 &gt; A then P(x|Hg) &lt; P(x|Hb)/A, therefore

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- image -->

## WaldSAC

## Running time

<!-- formula-not-decoded -->

In sequential statistical decision problem decision errors are traded off for time. These are two incomparable quantities, hence the constrained optimization.

In WaldSAC, decision errors cost time (more samples) and there is a single minimised quantity, time t(A) ,  a function of a single parameter A .

<!-- image -->

## Optimal test (optimal A) given e and 

Optimal A *

<!-- formula-not-decoded -->

Optimal A * found by solving

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Computed in several iterations:

<!-- formula-not-decoded -->

<!-- image -->

## SPRT

<!-- image -->

<!-- image -->

Note: the Wald's test is s equivalent to： series of T(d,c), [(log A dlog 入1)/ log 入ol where c三 一

<!-- image -->

Exp. 1: Wide-baseline matching

<!-- image -->

<!-- image -->

|      |   samples |   models |     V |    time |   spd-up |
|------|-----------|----------|-------|---------|----------|
| R    |      2914 |     7347 | 110.0 | 1099504 |      1.0 |
| R-R  |      7825 |    19737 |   3.0 |  841983 |      1.3 |
| Wald |      3426 |     8648 |   8.2 |  413227 |      2.7 |

## Exp. 2 Narrow-baseline stereo

<!-- image -->

<!-- image -->

|      |   samples |   models |     V |   time |   spd-up |
|------|-----------|----------|-------|--------|----------|
| R    |       155 |      367 | 600.0 | 235904 |      1.0 |
| R-R  |       247 |      587 |  86.6 |  75539 |      3.1 |
| Wald |       162 |      384 |  23.1 |  25032 |      9.4 |

<!-- image -->

<!-- image -->

## Randomised Verification in RANSAC: Conclusions

-  The same  confidence h in the solution reached faster (data dependent, ¼ 10x )
-  No change in the character of the algorithm, it was randomised anyway.
-  Optimal strategy derived using Wald's theory for known e and  .
-  Results with e and  estimated during the course of RANSAC are not significantly different. Performance of SPRT is insensitive to errors in the estimate.
-  can be learnt, an initial estimate can be obtained by geometric consideration
- Lower bound on e is given by the best-so-far support

## PROSAC -PROgressive SAmple Consensus

- Not all correspondences are created equally
- Some are better than others
- Sample from the best candidates first

<!-- image -->

Sample from here

<!-- image -->

## PROSAC Samples

<!-- image -->

Draw T l samples from (1 … l )

Draw T l +1 samples from (1 … l +1)

Samples from (1 … l ) that are not from (1 … l +1) contain

Draw Tl +1 -Tl samples of size m -1 and add l +1

<!-- image -->

<!-- image -->

## Degenerate Configurations

<!-- image -->

The presence of degenerate configuration causes RANSAC to fail in estimating a correct model, instead a model consistent with the degenerate configuration and some outliers is found.

The DEGENSAC algorithm handles scenes with:

- all points in a single plane
- majority of the points in a single plane and the rest off the plane
- no dominant plane present

No a-priori knowledge of the type of the scene is required

<!-- image -->

Chum, Werner, Matas : Epipolar Geometry Estimation unaffected by dominant plane, CVPR 2005 59

## GC-RANSAC [Barath and Matas, CVPR 2018]

e(S) = θ estimates model parameters θ,given sample S C X

<!-- formula-not-decoded -->

Output:0*parameter of the model minimizing the cost function

- 1.iter =0,J*=∞o
- 2.repeat
3. Select random S ≤ &amp; (sample size m = |Sl)
4. Estimate parameter θ = e(S)
5. Evaluate J(0) = ∑xex f(x,0)
6. If J(0)&lt; J* then

7.

<!-- formula-not-decoded -->

8. J*←J(0*)
9. iter←iter+1

Run graph-cut, if a so-far-the-best solution is found.

10. until P(better solution exists) = f(|&amp;|, J*,iter)&lt;μ

<!-- image -->

<!-- image -->

Figure 1: The proposed graph-cut based local optimization converging from a "not-all-inlier"s sample, i.e. it is contaminated by an outlier, to the desired model. (a) The input data points, (b) RANSAC-like sampling and model fitting, (c) computation of model support, e.g. counting the inliers, (d) considering spatial proximity by graph-cut, (e-f) iterated local optimization using least-squares fitting and graph-cut.

<!-- image -->

## GC-RANSAC

<!-- image -->

|          |        |                                 | Min. 60 FPS with 99% confidence   | Min. 60 FPS with 99% confidence   | Min. 60 FPS with 99% confidence   | Min. 60 FPS with 99% confidence   | Min. 60 FPS with 99% confidence   | Confidence 95%         | Confidence 95%        | Confidence 95%        | Confidence 95%        | Confidence 95%            |
|----------|--------|---------------------------------|-----------------------------------|-----------------------------------|-----------------------------------|-----------------------------------|-----------------------------------|------------------------|-----------------------|-----------------------|-----------------------|---------------------------|
|          |        |                                 | PLAIN                             | LO                                | LO+                               | LO'                               | GC                                | PLAIN                  | LO                    | LO+                   | LO'                   | GC                        |
| kusvod2  | #24    | LO Error (px) Time (ms) Samples | 一 5.01 6.17 117.00               | 2 4.95 6.09 96.00                 | 2 4.97 6.26 99.00                 | 2 5.02 5.85 111.00                | 1 (3) 4.65 4.58 70.00             | 一 5.18 4.94 93.00     | 1 5.08 5.19 76.00     | 1 5.03 5.14 78.00     | 1 5.22 4.86 87.00     | 2 (3) 4.69 3.64 53.00     |
| Adelaide | 61#    | LO Error (px) Time (ms) Samples | 一 0.55 14.20 124.00              | 2 0.53 14.83 113.00               | 2 0.52 14.85 113.00               | 2 0.55 14.13 122.00               | 1 (3) 0.50 18.94 116.00           | 一 0.44 262.73 1363.00 | 2 0.45 194.18 1126.00 | 2 0.43 210.85 1205.00 | 3 0.44 237.09 1305.00 | 2 (4) 0.43 227.12 1115.00 |
| Multi    | # E    | LO Error (px) Time (ms) Samples | 一 0.35 10.34 83.00               | 1 0.34 11.53 76.00                | 1 0.34 11.11 76.00                | 1 0.34 10.34 82.00                | 1 (3) 0.32 14.64 74.00            | 一 0.33 12.81 107.00   | 2 0.33 15.11 89.00    | 1 0.33 14.11 90.00    | 2 0.34 12.37 100.00   | 1 (3) 0.32 36.01 78.00    |
| EVD      | 15 #   | LO Error (px) Time (ms)         | 一 1.53 16.84                     | 2 1.63 18.34                      | 2 1.51 18.04                      | 2 1.58 16.82                      | 2 (2) 1.53 19.19                  | 一 0.96 247.25         | 4 0.95 248.01         | 4 0.95 251.31         | 4 0.96 246.95         | 3 (6) 0.92 249.89         |
| Bouou    | H, #16 | Samples LO Error (px) Time (ms) | 320.00 一 0.53 7.13               | 298.00 2 0.53 10.37               | 301.00 2 0.53 9.83                | 318.00 2 0.53 7.10                | 301.00 1 (3) 0.51 7.56            | 4303.00 一 0.50 17.10  | 4203.00 2 0.50 10.09  | 4248.00 2 0.49 9.89   | 4291.00 2 0.50        | 4204.00 1 (4) 0.47 7.94   |
| avg.     |        | Samples LO Error (px)           | 193.00 一 2.10                    | 175.00 2                          | 175.00 2                          | 189.00 2 2.11                     | 159.00 1 (3) 1.96                 | 450.00 一 1.98         | 212.00 2              | 214.00 2              | 8.52 226.00           | 165.00 2 (3)              |
|          | #      | Time (ms) Samples               | 10.59 171.00                      | 2.09 11.73 154.00                 | 2.07 11.60 156.00                 | 10.46 168.00                      | 12.01 144.00                      | 115.90 1286.00         | 1.95 98.36 1154.00    | 1.93 102.88 1183.00   | 2 2.00 107.89 1224.00 | 1.81 107.06 1134.00       |

## GC RANSAC - Speed

<!-- image -->

Figure 7: The breakdown of the processing times in milliseconds. Computed as the mean of all tests. Best viewed in color.

<!-- image -->