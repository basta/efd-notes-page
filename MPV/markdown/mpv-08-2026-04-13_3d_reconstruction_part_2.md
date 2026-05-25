<!-- image -->

## 3D Reconstruction Part 2: Dense 3D Reconstruction

## Computer Vision Methods 2026 Lecture 8

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

True trajectory Estimated trajectory

<!-- image -->

<!-- image -->

<!-- image -->

## Depth Anything 3

<!-- image -->

[Haotong Lin, Sili Chen, Jun Hao Liew, Donny Y. Chen, Zhenyu Li, Guang Shi, Jiashi Feng, Bingyi Kang, Depth Anything 3: Recovering the Visual Space from Any Views, ICLR 2026]

<!-- image -->

<!-- image -->

## 3D Reconstruction Pipelines

Images Camera Pose Estimation via Structure-from-Motion Dense Reconstruction (MVS, NeRF, Gaussian Splatting, etc.) Dense Reconstruction (MVS, NeRF, Gaussian Splatting, etc.)

## Multi-View Stereo (MVS) in a Nutshell

<!-- image -->

images with known poses &amp; intrinsics

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## Multi-View Stereo (MVS) in a Nutshell

<!-- image -->

images with known poses &amp; intrinsics

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## Multi-View Stereo (MVS) in a Nutshell

error depth

<!-- image -->

images with known poses &amp; intrinsics

<!-- image -->

## Multi-View Stereo (MVS) in a Nutshell

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

images with known poses &amp; intrinsics

<!-- image -->

<!-- image -->

## Multi-View Stereo (MVS) in a Nutshell

<!-- image -->

<!-- image -->

## Multi-View Stereo (MVS) in a Nutshell

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

images with known poses &amp; intrinsics

<!-- image -->

<!-- image -->

## Multi-View Stereo (MVS) in a Nutshell

<!-- image -->

How to sample depth values?

- Uniformly
- Coarse-to-fine / adaptively
- 'Randomly'

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

images with known poses &amp; intrinsics

<!-- image -->

<!-- image -->

## Patch Match Stereo

- Randomly initialize depth values (+plane normal) for each pixel
- Iterate:
- For each pixel:
- Evaluate the photometric error for the depth (and plane normal) parameters of neighboring points, keep parameters that lead to lowest error
- Refine the current estimate by randomly sampling parameters around estimate and keeping the best parameters

## Patch Match Stereo

<!-- image -->

<!-- image -->

[Bleyer, Rehmann, Rother, PatchMatch Stereo - Stereo Matching with Slanted Support Windows, BMVC 2011]

<!-- image -->

## Patch Match Stereo

## after 3 iterations:

<!-- image -->

for modern versions, see e.g. [Galliani, Lasinger, Schindler, Massively Parallel Multiview Stereopsis by Surface Normal Diffusion, ICCV 2015], [Schönberger, Zheng, Pollefeys, Frahm, Pixelwise View Selection for U nstructured Multi-View Stereo, ECCV 2016]

[Bleyer, Rehmann, Rother, PatchMatch Stereo - Stereo Matching with Slanted Support Windows, BMVC 2011]

<!-- image -->

## Multi-View Stereo in a Nutshell

<!-- image -->

<!-- image -->

## Explicit Scene Representations

<!-- image -->

<!-- image -->

## Explicit Scene Representations

<!-- image -->

<!-- image -->

## Explicit Scene Representations

<!-- image -->

<!-- image -->

## From Point Clouds to Meshes - Marching Cubes

Signed distance function (SDF):

<!-- image -->

<!-- image -->

## From Point Clouds to Meshes - Marching Cubes

## Signed distance function (SDF):

<!-- image -->

<!-- image -->

- Store signed distance values in voxel grid:
- Integrate each depth map into the volume
- Truncated SDF (TSDF): Only consider a small depth range around depth values
- Marching Cubes: Geometry / mesh can be obtained by extracting level set for distance 0

## Marching Cubes Algorithm

## Here, Marching Squares (2D equivalent):

<!-- image -->

<!-- image -->

- 7 possible configurations (up to symmetries &amp; rotations) (15 in 3D):
- Look-up connectivity to construct mesh

<!-- image -->

## Marching Cubes Algorithm

## Here, Marching Squares (2D equivalent):

<!-- image -->

<!-- image -->

- 7 possible configurations (up to symmetries &amp; rotations) (15 in 3D):
- Look-up connectivity to construct mesh

<!-- image -->

<!-- image -->

## Marching Cubes Algorithm

## Here, Marching Squares (2D equivalent):

<!-- image -->

- 7 possible configurations (up to symmetries &amp; rotations) (15 in 3D):
- Look-up connectivity to construct mesh
- Various improvements over original formulation (predicting intersections on edges, adaptive resolution, feature interpolation, recovering corners, …)

<!-- image -->

[Lorensen, Cline, Marching cubes: A high resolution 3D surface construction algorithm. SIGGRAPH 1987]

## Real-Time Reconstruction on Mobile Devices

<!-- image -->

[Schöps, Sattler, Häne, Pollefeys, Large-Scale Outdoor 3D Reconstruction on a Mobile Device. CVIU'16]

<!-- image -->

<!-- image -->

## From Point Clouds to Meshes - Poisson Surface Reconstruction

<!-- image -->

<!-- image -->

- Recover indicator function by solving optimization problem:
- Cost function: gradients of indicator function are as close as possible to normals of 3D points
- Typically solved by voxelizing the space
- Recover surface from indicator function

Indicator function

## Surface Reconstruction from Point Clouds

<!-- image -->

[Labatut, Pons, Keriven. Efficient multi-view reconstruction of large-scale scenes using interest points, delaunay triangulation and graph cuts. ICCV, 2007]

[Jancosek, Pajdla, Multi-View Reconstruction Preserving Weakly-Supported Surfaces. CVPR 2011]

[Vu, Labatut, Pons, Keriven, High Accuracy and Visibility-Consistent Dense Multiview Stereo. TPAMI 2012]

<!-- image -->

## Surface Reconstruction from Point Clouds

<!-- image -->

- Define volume from (dense or sparse) 3D point cloud via Delaunay triangulation

[Labatut, Pons, Keriven. Efficient multi-view reconstruction of large-scale scenes using interest points, delaunay triangulation and graph cuts. ICCV, 2007]

[Jancosek, Pajdla, Multi-View Reconstruction Preserving Weakly-Supported Surfaces. CVPR 2011] [Vu, Labatut, Pons, Keriven, High Accuracy and Visibility-Consistent Dense Multiview Stereo. TPAMI 2012]

<!-- image -->

## Surface Reconstruction from Point Clouds

<!-- image -->

- Define volume from (dense or sparse) 3D point cloud via Delaunay triangulation
- Label tetrahedra as inside / outside by solving a graph cut problem

[Labatut, Pons, Keriven. Efficient multi-view reconstruction of large-scale scenes using interest points, delaunay triangulation and graph cuts. ICCV, 2007]

[Jancosek, Pajdla, Multi-View Reconstruction Preserving Weakly-Supported Surfaces. CVPR 2011] [Vu, Labatut, Pons, Keriven, High Accuracy and Visibility-Consistent Dense Multiview Stereo. TPAMI 2012]

<!-- image -->

## Surface Reconstruction from Point Clouds

<!-- image -->

[Jancosek, Pajdla, Multi-View Reconstruction Preserving Weakly-Supported Surfaces. CVPR 2011]

<!-- image -->

## Surface Reconstruction from Point Clouds

<!-- image -->

- Define volume from (dense or sparse) 3D point cloud via Delaunay triangulation
- Label tetrahedra as inside / outside by solving a graph cut problem
- Triangles adjacent to both inside and outside tetrahedra correspond to the surface

[Labatut, Pons, Keriven. Efficient multi-view reconstruction of large-scale scenes using interest points, delaunay triangulation and graph cuts. ICCV, 2007]

[Jancosek, Pajdla, Multi-View Reconstruction Preserving Weakly-Supported Surfaces. CVPR 2011] [Vu, Labatut, Pons, Keriven, High Accuracy and Visibility-Consistent Dense Multiview Stereo. TPAMI 2012]

<!-- image -->

## Surface Reconstruction from Point Clouds

[http://www.acute3d.com](http://www.acute3d.com/)

<!-- image -->

[Vu, Labatut, Pons, Keriven, High Accuracy and Visibility-Consistent Dense Multiview Stereo. TPAMI 2012]

<!-- image -->

## Novel View Synthesis via Neural Radiance Fields (NeRFs)

<!-- image -->

<!-- image -->

## Novel View Synthesis via Neural Radiance Fields

<!-- image -->

[Mildenhall, Srinivasan, Tancik, et al., NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis, ECCV 2020]

<!-- image -->

color c i , volume density σ i

## Basics: Volume Rendering

<!-- image -->

<!-- image -->

visibility

## Basics: Volume Rendering

<!-- image -->

<!-- formula-not-decoded -->

<!-- image -->

<!-- image -->

## Basics: Volume Rendering

<!-- image -->

<!-- formula-not-decoded -->

Torsten Sattler [Kajiya, Herzen, Ray tracing volume densities, SIGGRAPH 1984]

## Neural Radiance Fields (NeRFs)

✔

<!-- formula-not-decoded -->

Neural Radiance Field : Learn the volumetric representation

<!-- formula-not-decoded -->

ray direction

<!-- formula-not-decoded -->

density

Continuous scene representation (vs. discrete voxel volumes)

[Mildenhall, Srinivasan, Tancik, et al., NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis, ECCV 2020]

<!-- image -->

## Neural Radiance Fields (NeRFs)

output: color and density

<!-- image -->

Compute color for each pixel via volume rendering

[Mildenhall, Srinivasan, Tancik, et al., NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis, ECCV 2020]

<!-- image -->

<!-- image -->

## Training a NeRF

<!-- image -->

<!-- image -->

## Volume Sampling

uniform sampling inside intervals → continuous sampling of the volume

<!-- image -->

subdivide into equally sized intervals

## Hierarchical Volume Sampling

Coarse sampling (coarse network): Uniform sampling in equally-spaced intervals

σ

<!-- image -->

'Fine' sampling ('fine' network): Sample according to observed densities

All samples are used during volume rendering

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## Important Details

<!-- image -->

<!-- image -->

## Important Details

<!-- image -->

## Important Details

<!-- image -->

Input encoding [Tancik, Srinivasan, Mildenhall, et al., Fourier Features: Let Networks Learn High Frequency Functions in Low Dimensional Domains, NeurIPS 2020]

Helps network preserve high-frequency variations, similar in spirit to positional encoding of transformers

[Mildenhall, Srinivasan, Tancik, et al., NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis, ECCV 2020]

<!-- image -->

<!-- image -->

## Important Details

Pure 5D coordinates

<!-- image -->

Input encoding

<!-- image -->

## Neural Radiance Fields (NeRFs)

<!-- image -->

## NeRFs Are Very Slow!

<!-- image -->

For each 3D point, we need to evaluate the network

Training takes hours on single GPU Rendering image takes seconds to minutes

[Mildenhall, Srinivasan, Tancik, et al., NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis, ECCV 2020]

<!-- image -->

## NeRFs Are Very Slow!

<!-- image -->

For each 3D point, we need to evaluate the network

Training takes hours on single GPU Rendering image takes seconds to minutes

[Mildenhall, Srinivasan, Tancik, et al., NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis, ECCV 2020]

<!-- image -->

## Plenoxels: Radiance Fields without Neural Networks

optimize weights of harmonics instead of weights a neural network

<!-- image -->

[Fridovich-Keil, Yu, Tancik, Chen, Recht, Kanazawa, Plenoxels: Radiance Fields without Neural Networks, CVPR 2022]

<!-- image -->

## Plenoxels: Radiance Fields without Neural Networks

<!-- image -->

<!-- image -->

## Plenoxels: Radiance Fields without Neural Networks

<!-- image -->

[Fridovich-Keil, Yu, Tancik, Chen, Recht, Kanazawa, Plenoxels: Radiance Fields without Neural Networks, CVPR 2022]

<!-- image -->

## Plenoxels: Radiance Fields without Neural Networks

without regularization

<!-- image -->

with regularization

<!-- image -->

[Fridovich-Keil, Yu, Tancik, Chen, Recht, Kanazawa, Plenoxels: Radiance Fields without Neural Networks, CVPR 2022]

<!-- image -->

## Plenoxels: Radiance Fields without Neural Networks

<!-- image -->

[Fridovich-Keil, Yu, Tancik, Chen, Recht, Kanazawa, Plenoxels: Radiance Fields without Neural Networks, CVPR 2022]

<!-- image -->

Torsten Sattler

## Plenoxels: Radiance Fields without Neural Networks

<!-- image -->

[Fridovich-Keil, Yu, Tancik, Chen, Recht, Kanazawa, Plenoxels: Radiance Fields without Neural Networks, CVPR 2022]

<!-- image -->

## Plenoxels: Radiance Fields without Neural Networks

<!-- image -->

## Reducing training times at cost of higher memory consumption !

[Fridovich-Keil, Yu, Tancik, Chen, Recht, Kanazawa, Plenoxels: Radiance Fields without Neural Networks, CVPR 2022]

<!-- image -->

## Combining Voxel Grids with Networks

Concatenated trilinearly interpolated features with additional information (viewing direction, etc.)

(shallow) neural network

<!-- image -->

<!-- image -->

## Jointly train features and neural network!

[Fridovich-Keil, Yu, Tancik, Chen, Recht, Kanazawa, Plenoxels: Radiance Fields without Neural Networks, CVPR 2022] [Müller, Evans, Schied, Keller, Instant Neural Graphics Primitives with a Multiresolution Hash Encoding, SIGGRAPH 2022]

<!-- image -->

## Combining Voxel Grids with Networks

'standard' NeRF 438k + 0 parameters 13:53 (mm:ss)

<!-- image -->

shallow network trainable features

Multi-resolution grid 10k + 16.3M parameters 1:26 (mm:ss)

<!-- image -->

[Müller, Evans, Schied, Keller, Instant Neural Graphics Primitives with a Multiresolution Hash Encoding, SIGGRAPH 2022]

<!-- image -->

Can we improve quality while reducing memory requirements?

## Multi-Resolution Hash Encoding

<!-- image -->

[Müller, Evans, Schied, Keller, Instant Neural Graphics Primitives with a Multiresolution Hash Encoding, SIGGRAPH 2022]

<!-- image -->

## Multi-Resolution Hash Encoding

<!-- image -->

<!-- image -->

<!-- image -->

- Same hash table size for each resolution
- Injective mapping for coarsest level (no hash collisions)
- No collision handling on finer levels: simply average gradients
- Intuition: let network handle collisions, more important samples (with larger gradients) will dominate

<!-- image -->

## Combining Voxel Grids with Networks

<!-- image -->

'standard' NeRF 438k + 0 parameters 13:53 (mm:ss)

Multi-resolution grid 10k + 16.3M parameters 1:26 (mm:ss)

<!-- image -->

Hashtable (T=2 14 ) 10k + 494k parameters 1:40 (mm:ss)

<!-- image -->

[Müller, Evans, Schied, Keller, Instant Neural Graphics Primitives with a Multiresolution Hash Encoding, SIGGRAPH 2022]

<!-- image -->

## Instant Neural Graphics Primitives (Instant NGP)

<!-- image -->

## Combining hash encodings with with highly efficient network implementation

[Müller, Evans, Schied, Keller, Instant Neural Graphics Primitives with a Multiresolution Hash Encoding, SIGGRAPH 2022]

<!-- image -->

## NeRF in the Wild: Neural Radiance Fields for Unconstrained Photo Collections

illumination changes

transient objects

<!-- image -->

[Martin-Brualla, Radwan, Sajjadi, et al., NeRF in the Wild: Neural Radiance Fields for Unconstrained Photo Collections, CVPR 2021]

<!-- image -->

## NeRF in the Wild: Neural Radiance Fields for Unconstrained Photo Collections

low-dimensional vector encoding appearance (learned)

learned per image to account for transient objects (not needed at testing time)

Explain pixels by transient objects

<!-- image -->

[Martin-Brualla, Radwan, Sajjadi, et al., NeRF in the Wild: Neural Radiance Fields for Unconstrained Photo Collections, CVPR 2021]

<!-- image -->

## NeRF in the Wild: Neural Radiance Fields for Unconstrained Photo Collections

<!-- image -->

<!-- image -->

## NeRF in the Wild: Neural Radiance Fields for Unconstrained Photo Collections

<!-- image -->

[Martin-Brualla, Radwan, Sajjadi, et al., NeRF in the Wild: Neural Radiance Fields for Unconstrained Photo Collections, CVPR 2021]

<!-- image -->

## Extracting 3D Geometry from Neural Radiance Fields

## Extract geometry as level set of some density value

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## Extracting 3D Geometry from Neural Radiance Fields

What is the 'right' density threshold to use?

σ

<!-- image -->

There might not be a good choice!

<!-- image -->

## Extracting 3D Geometry from Neural Radiance Fields

- Problem : volume density does necessarily model 3D geometry
- Solution : estimate signed distance function (SDF), model volume density as learnable function of SDF
- Well-defined geometry : zero level set of SDF

<!-- image -->

<!-- image -->

<!-- image -->

## VolSDF vs. NeRF

<!-- image -->

[Yariv, Gu, Kasten, Lipman, Volume Rendering of Neural Implicit Surfaces, NeurIPS 2021]

## Neural Radiance Fields

<!-- image -->

<!-- image -->

<!-- image -->

## 3D Gaussian Splatting

## 3D Gaussian:

- 3D position
- covariance matrix
- view-dependent color function
- GPUs were designed for this
- Real-time rendering, even in a web browser

<!-- image -->

## Surface Splatting

<!-- image -->

<!-- image -->

## oriented disk:

- 3D position
- plane normal n
- radius r
- color

[Rusinkiewicz, Levoy, QSplat: A Multiresolution Point Rendering System for Large Meshes, SIGGRAPH 2000] [Zwicker, Pfister, van Baar, Gross, Surface Splatting, SIGGRAPH 2001]

<!-- image -->

## Surface Splatting

Michelangelo's statue of St. Matthew 14.8M 3D points

<!-- image -->

<!-- image -->

[Rusinkiewicz, Levoy, QSplat: A Multiresolution Point Rendering System for Large Meshes, SIGGRAPH 2000]

## Rendering Textured Splats

## Rendering Textured Splats

<!-- image -->

[Untzelmann, Sattler, Middelberg, Kobbelt, A Scalable Collaborative Online System for City Reconstruction, ICCVW 2013]

<!-- image -->

## Rendering Textured Splats

<!-- image -->

[Untzelmann, Sattler, Middelberg, Kobbelt, A Scalable Collaborative Online System for City Reconstruction, ICCVW 2013]

<!-- image -->

## Rendering Textured Splats

<!-- image -->

[Untzelmann, Sattler, Middelberg, Kobbelt, A Scalable Collaborative Online System for City Reconstruction, ICCVW 2013]

<!-- image -->

## Gaussian Splatting: High-Quality, Real-Time Novel View Synthesis

<!-- image -->

[Kerbl, Kopanas, Leimkühler, Drettakis, 3D Gaussian Splatting for Real-Time Radiance Field Rendering, SIGGRAPH 2023]

<!-- image -->

## 3D Gaussian Splatting

<!-- image -->

[Kerbl, Kopanas, Leimkühler, Drettakis, 3D Gaussian Splatting for Real-Time Radiance Field Rendering, SIGGRAPH 2023]

<!-- image -->

## Gaussian Splatting Issues

<!-- image -->

slide credit: Zehao Yu

[Zehao Yu, Anpei Chen, Binbin Huang, Sattler, Andreas Geiger, Mip-Splatting: Alias-free 3D Gaussian Splatting, CVPR 2024]

<!-- image -->

## Gaussian Splatting Issues

<!-- image -->

- Gaussian Splatting tends to generate many small Gaussians to model fine details
- Small Gaussian lead to numerical and optimization issues
- Use 2D dilation to restrict minimum size of 2D Gaussians → improves robustness
- Not described in paper!

slide credit: Zehao Yu

[Zehao Yu, Anpei Chen, Binbin Huang, Sattler, Andreas Geiger, Mip-Splatting: Alias-free 3D Gaussian Splatting, CVPR 2024]

<!-- image -->

<!-- image -->

## Gaussian Splatting Issues

<!-- image -->

<!-- image -->

2D dilation leads to artifacts when zooming out / moving away from the scene

slide credit: Zehao Yu

<!-- image -->

## Gaussian Splatting Issues

<!-- image -->

2D dilation leads to degenerate Gaussians

slide credit: Zehao Yu

## Gaussian Splatting Issues

<!-- image -->

2D dilation leads to erosion and high-frequency artifacts when zooming in / moving closer to the scene

slide credit: Zehao Yu

[Zehao Yu, Anpei Chen, Binbin Huang, Sattler, Andreas Geiger, Mip-Splatting: Alias-free 3D Gaussian Splatting, CVPR 2024]

<!-- image -->

## Mip-Splatting

<!-- image -->

- Small Gaussians = high-frequency details
- Principled way of handling issues caused by high-frequency details? Low-pass filtering !
- In 3D : Enforce minimum size of 3D Gaussians, filter sizes derived from training data
- In 2D : Simulate physical box filter in imagining process by 2D Gaussian

slide credit: Zehao Yu

[Zehao Yu, Anpei Chen, Binbin Huang, Sattler, Andreas Geiger, Mip-Splatting: Alias-free 3D Gaussian Splatting, CVPR 2024]

<!-- image -->

<!-- image -->

## Ablation Study: 3D Smoothing

w/o 3D Smoothing Filter

<!-- image -->

Ours

slide credit: Zehao Yu

## Ablation Study: 2D Mip Filter

<!-- image -->

<!-- image -->

slide credit: Zehao Yu

[Zehao Yu, Anpei Chen, Binbin Huang, Sattler, Andreas Geiger, Mip-Splatting: Alias-free 3D Gaussian Splatting, CVPR 2024]

<!-- image -->

## Mip-Splatting

<!-- image -->

Try it yourself: https://github.com/autonomousvision/mip-splatting

[Zehao Yu, Anpei Chen, Binbin Huang, Sattler, Andreas Geiger, Mip-Splatting: Alias-free 3D Gaussian Splatting, CVPR 2024]

<!-- image -->

## Gaussians In Uncontrolled Environments

<!-- image -->

video credit: Jonas Kulhanek

[Jonas Kulhanek, Songyou Peng, Zuzana Kukelova, Marc Pollefeys, Sattler, WildGaussians: 3D Gaussian Splatting In the Wild, NeurIPS 2024]

<!-- image -->

## Challenges

<!-- image -->

<!-- image -->

slide credit: Songyou Peng

[Jonas Kulhanek, Songyou Peng, Zuzana Kukelova, Marc Pollefeys, Sattler, WildGaussians: 3D Gaussian Splatting In the Wild, NeurIPS 2024]

<!-- image -->

## WildGaussians: Handling Appearance Changes

<!-- image -->

[Jonas Kulhanek, Songyou Peng, Zuzana Kukelova, Marc Pollefeys, Sattler, WildGaussians: 3D Gaussian Splatting In the Wild, NeurIPS 2024]

<!-- image -->

## WildGaussians: Handling Occlusions

<!-- image -->

[Jonas Kulhanek, Songyou Peng, Zuzana Kukelova, Marc Pollefeys, Sattler, WildGaussians: 3D Gaussian Splatting In the Wild, NeurIPS 2024]

<!-- image -->

## WildGaussians: Learning Uncertainty

<!-- image -->

[Jonas Kulhanek, Songyou Peng, Zuzana Kukelova, Marc Pollefeys, Sattler, WildGaussians: 3D Gaussian Splatting In the Wild, NeurIPS 2024]

<!-- image -->

## Results: NeRF On-The-Go Dataset

<!-- image -->

slide credit: Songyou Peng

[Jonas Kulhanek, Songyou Peng, Zuzana Kukelova, Marc Pollefeys, Sattler, WildGaussians: 3D Gaussian Splatting In the Wild, NeurIPS 2024]

<!-- image -->

## Results: PhotoTourism Dataset

<!-- image -->

slide credit: Songyou Peng

[Jonas Kulhanek, Songyou Peng, Zuzana Kukelova, Marc Pollefeys, Sattler, WildGaussians: 3D Gaussian Splatting In the Wild, NeurIPS 2024]

<!-- image -->

## Smooth Appearance Interpolation

<!-- image -->

slide credit:

Songyou Peng

[Jonas Kulhanek, Songyou Peng, Zuzana Kukelova, Marc Pollefeys, Sattler, WildGaussians: 3D Gaussian Splatting In the Wild, NeurIPS 2024]

<!-- image -->

## Extracting Meshes from 3D Gaussians

<!-- image -->

[Zehao Yu, Sattler, Andreas Geiger, Gaussian Opacity Fields: Efficient Adaptive Surface Reconstruction in Unbounded Scenes, SIGGRAPH Asia 2024]

<!-- image -->

## Extracting Meshes from 3D Gaussians

## Existing work:

<!-- image -->

slide credit: Zehao Yu

<!-- image -->

## Prior Work: SuGaR (Poisson Reconstruction)

<!-- image -->

slide credit: Zehao Yu

[Guedon, Lepetit, SuGaR: Surface-Aligned Gaussian Splatting for Efficient 3D Mesh Reconstruction and High-Quality Mesh Rendering, CVPR 2024

<!-- image -->

## Prior Work: 2D Gaussian Splatting (TSDF Fusion)

<!-- image -->

slide credit: Zehao Yu

[Huang, Yu, Chen, Geiger, Gao, 2DGS: 2D Gaussian Splatting for Geometrically Accurate Radiance Fields, SIGGRAPH 2024]

<!-- image -->

## Extracting Meshes from 3D Gaussians

## Existing work:

<!-- image -->

slide credit: Zehao Yu

<!-- image -->

## Extracting Meshes from 3D Gaussians

<!-- image -->

<!-- image -->

## Gaussian Opacity Fields

<!-- image -->

slide credit: Zehao Yu

[Zehao Yu, Sattler, Andreas Geiger, Gaussian Opacity Fields: Efficient Adaptive Surface Reconstruction in Unbounded Scenes, SIGGRAPH Asia 2024]

<!-- image -->

<!-- image -->

## Ray Tracing-based Rendering

<!-- image -->

<!-- image -->

slide credit: Zehao Yu

<!-- image -->

## Ray Tracing-based Rendering

<!-- image -->

slide credit: Zehao Yu

## Evaluating Opacity Along The Ray

<!-- image -->

<!-- image -->

slide credit: Zehao Yu

## Evaluating Opacity Along The Ray

<!-- image -->

<!-- image -->

slide credit: Zehao Yu

<!-- image -->

## Gaussian Opacity Fields

<!-- image -->

slide credit: Zehao Yu

## Mesh Extraction Via Gaussian Opacity Fields

<!-- image -->

slide credit: Zehao Yu

[Zehao Yu, Sattler, Andreas Geiger, Gaussian Opacity Fields: Efficient Adaptive Surface Reconstruction in Unbounded Scenes, SIGGRAPH Asia 2024]

<!-- image -->

## Qualitative Examples

Ours slide credit: Zehao Yu

<!-- image -->

[Zehao Yu, Sattler, Andreas Geiger, Gaussian Opacity Fields: Efficient Adaptive Surface Reconstruction in Unbounded Scenes, SIGGRAPH Asia 2024]

<!-- image -->

## Qualitative Examples

<!-- image -->

slide credit: Zehao Yu

[Zehao Yu, Sattler, Andreas Geiger, Gaussian Opacity Fields: Efficient Adaptive Surface Reconstruction in Unbounded Scenes, SIGGRAPH Asia 2024]

<!-- image -->

## Qualitative Examples

<!-- image -->

slide credit: Zehao Yu

[Zehao Yu, Sattler, Andreas Geiger, Gaussian Opacity Fields: Efficient Adaptive Surface Reconstruction in Unbounded Scenes, SIGGRAPH Asia 2024]

<!-- image -->

## Qualitative Examples

<!-- image -->

slide credit: Zehao Yu

[Zehao Yu, Sattler, Andreas Geiger, Gaussian Opacity Fields: Efficient Adaptive Surface Reconstruction in Unbounded Scenes, SIGGRAPH Asia 2024]

<!-- image -->

## Main Takeaways

- Classical approach: Compute dense depth maps, integrate them into a scene representation (e.g., point clouds or volumes) and extract mesh from the representation
- Neural Radiance Fields (NeRFs): Use classical volume rendering (1984!) to learn a volumetric scene representation from images
- 3D Gaussian Splatting (3DGS): Use explicit scene representation to make learning &amp; rendering more efficient
- Interested in working on these topics (software project, MSc thesis, etc.)? Contact me!

<!-- image -->