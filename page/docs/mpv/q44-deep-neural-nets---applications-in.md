## Deep Neural Nets — Applications in Computer Vision

The previous sections have established the fundamental building blocks of deep convolutional neural networks, the principles of their training, and the architectures that underpin modern object detection. This section broadens the perspective to survey the extraordinary range of **computer vision tasks** that deep neural networks have come to dominate. The course material presents a whirlwind tour of applications, from the foundational problem of image classification to generative models that synthesise entirely new visual content. What unifies these diverse applications is the ability of deep networks to learn hierarchical, abstract representations directly from raw pixels, replacing hand‑crafted features and task‑specific pipelines with end‑to‑end differentiable models.

We organise the applications into thematic groups, following the structure of the lecture slides, and highlight the key ideas, representative architectures, and the impact each has had on the field.

### 1. Image Classification

Image classification is the task that ignited the deep learning revolution in computer vision. Given an input RGB image, the network must assign a single label — a probability distribution over a fixed set of categories. The course uses **AlexNet** as the canonical example: a deep CNN with five convolutional layers and three fully connected layers, trained on the ImageNet dataset (1.2 M images, 1000 classes). It achieved a dramatic improvement over traditional methods in the ILSVRC 2012 challenge, reducing the top‑5 error rate by roughly 10 percentage points.

The core pipeline — convolutional feature extraction followed by fully connected classification layers — has since been refined into a zoo of architectures: **VGG** (small 3×3 filters, deeper stacks), **GoogLeNet** (Inception modules, no fully connected layers), **ResNet** (residual connections enabling 152 layers), **ResNeXt** (cardinality), **DenseNet** (dense skip connections), **Squeeze‑and‑Excitation Networks** (channel attention), and computationally efficient designs such as **MobileNet** and **ShuffleNet**. More recently, **Vision Transformers (ViT)** and their hierarchical variants (e.g., **Swin Transformer**) have challenged the convolutional paradigm by applying self‑attention to sequences of image patches, while **ConvNeXt** modernises the pure convolutional ResNet blueprint to match transformer performance.

Classification networks serve not only as standalone solutions but also as **backbones** for almost every other vision task, providing pre‑trained feature extractors that transfer to detection, segmentation, and beyond.

### 2. Object Detection

Object detection extends classification to answer both *what* objects are present and *where* they are located, outputting a set of bounding boxes with class labels and confidence scores. The course traces the evolution from exhaustive scanning‑window approaches to sophisticated end‑to‑end architectures, a story already detailed in the previous section. To summarise the key milestones:

- **R‑CNN** and its descendants (**Fast R‑CNN**, **Faster R‑CNN**) introduced the two‑stage paradigm: generate region proposals, then classify and refine them using shared convolutional features. **Mask R‑CNN** added a parallel segmentation branch, unifying detection and instance segmentation.
- **Single‑shot detectors** such as **YOLO** and **RetinaNet** predict bounding boxes and class probabilities in one forward pass, trading a small amount of accuracy for real‑time speed. YOLO divides the image into a grid and directly regresses boxes; RetinaNet uses a dense set of anchor boxes and the **focal loss** to handle the extreme foreground–background class imbalance.
- **DETR** (Detection Transformer) casts detection as a direct set prediction problem, using a Transformer encoder–decoder and bipartite matching loss, eliminating the need for anchors and non‑maximum suppression.

These detectors are evaluated with **mean Average Precision (mAP)** based on the Intersection over Union (IoU) metric. The slides highlight practical deployments, including the CTU eForce formula student team’s use of YOLO‑type detectors for traffic cone perception in autonomous driving.

### 3. Semantic and Instance Segmentation

Segmentation requires pixel‑level understanding. **Semantic segmentation** assigns a class label to every pixel (e.g., “road”, “car”, “sky”), while **instance segmentation** additionally distinguishes individual objects of the same class.

The course presents three influential architectures:

- **Fully Convolutional Networks (FCNs)** replace the fully connected layers of a classification network with 1×1 convolutions and upsample the feature maps to the input resolution using transposed convolution (deconvolution). This was the first end‑to‑end deep segmentation model.
- **U‑Net** employs an encoder–decoder structure with skip connections that concatenate high‑resolution encoder features with the upsampled decoder features. Originally designed for biomedical images, it excels when training data is limited and precise boundaries are required. The slides mention its use in surface segmentation for a visually assisted anti‑lock braking system.
- **DeepLab v3+** uses atrous (dilated) convolutions to enlarge the receptive field without increasing parameters, combined with an encoder–decoder architecture. It achieves state‑of‑the‑art results on standard benchmarks.
- **Transformer‑based segmentation** methods, such as **SEGMENTER**, apply self‑attention directly to image patches, dispensing with convolutions entirely. The self‑attention maps of DETR and DINO also naturally reveal object instances, enabling segmentation heads to be attached.

The course also introduces **Segment Anything (SAM)**, a promptable foundation model trained on over 1 B masks. SAM can segment arbitrary objects given points, boxes, or text prompts, and it handles ambiguity by predicting multiple plausible masks. Its zero‑shot capabilities represent a shift toward generalist vision models.

### 4. Human and Face Analysis

Faces are a particularly important domain where deep networks have achieved super‑human performance on several tasks:

- **Face recognition and verification:** Deep CNNs (e.g., DeepFace, ArcFace) map face images to compact embeddings where Euclidean distance corresponds to identity similarity. The penultimate layer response serves as a face descriptor, enabling large‑scale similarity search.
- **Facial landmark localisation, age, and gender estimation:** Multi‑task networks share a common representation and jointly predict landmarks (regression), age (regression or classification), and gender (classification). The slides report that a CNN trained for age estimation achieves a mean absolute error lower than that of an average human on certain datasets.
- **Expression and emotion recognition, lip reading, and even predicting decision uncertainty or sexual orientation from facial images** are cited as examples of the surprising information that deep networks can extract. The course notes the ethical sensitivity of some of these applications.

### 5. Motion, Depth, and 3D Understanding

Deep networks have revolutionised the recovery of 3D structure and motion from 2D images:

- **Optical flow and tracking:** Networks such as those by Neoral et al. predict dense pixel‑level displacement fields between consecutive frames, enabling motion estimation and object tracking.
- **Stereo matching:** Deep stereo networks compute disparity maps from rectified image pairs, producing depth estimates.
- **Monocular depth estimation:** A single image is sufficient for a network (e.g., Godard et al.) to predict a dense depth map. The slides present **Depth Anything**, a large foundation model trained with semi‑supervised learning on 1.5 M labelled and 62 M unlabelled images, achieving impressive zero‑shot depth prediction.
- **Novel view synthesis:** **NeRF** (Neural Radiance Fields) represents a scene as a continuous volumetric function parameterised by a multi‑layer perceptron. Given a sparse set of input views, NeRF can render photorealistic images from arbitrary camera poses, a breakthrough that has spawned an entire sub‑field.

### 6. Image‑to‑Image Translation and Restoration

The course highlights **pix2pix** (Isola et al.) as a general framework for image‑to‑image translation using conditional generative adversarial networks (GANs). Applications include:

- Day‑to‑night conversion, black‑and‑white colourisation, and map‑to‑satellite translation.
- **Deblurring and super‑resolution:** Networks can recover a sharp, high‑resolution image from a blurry, low‑resolution input. The slides show an example where a 16×16 input is upscaled to 256×256 with convincing detail.

### 7. Generative Models and Image Synthesis

Generative models learn the underlying distribution of training images and can sample new, realistic images. The course covers:

- **Variational Autoencoders (VAEs) and Generative Adversarial Networks (GANs):** GANs, in particular, have produced stunningly photorealistic samples (e.g., Nvidia’s progressive GAN). They consist of a generator that creates images and a discriminator that tries to distinguish real from fake; the two are trained adversarially.
- **Large text‑to‑image models:** Starting around 2022, models such as **DALL‑E 2, Imagen, Midjourney, and Stable Diffusion** use diffusion processes or autoregressive transformers conditioned on text prompts to generate high‑fidelity images. The slides show examples like “a panda mad scientist mixing sparkling chemicals, artstation” and “a propaganda poster depicting a cat dressed as French emperor Napoleon holding a piece of cheese.”
- **Video synthesis:** Extensions to video (e.g., SORA, VEO) and talking‑head avatars (e.g., Synthesia) are pushing the boundary toward fully synthetic media.

### 8. Image Manipulation and Editing

Beyond generating images from scratch, deep networks enable sophisticated editing of existing photographs:

- **Instruct Pix2Pix** allows users to edit an image by giving a textual instruction (e.g., “put on a pair of sunglasses” or “make her look 100 years old”).
- **Hairstyle transfer** and other attribute manipulations are achieved by learning disentangled representations.
- **Neural Style Transfer** (Gatys et al.) separates and recombines the *content* of one image with the *style* of another. The style is captured by the Gram matrix of feature correlations in lower network layers, while the content is represented by higher‑level feature responses. The result is a photorealistic or artistic rendering that preserves the scene layout but adopts the texture and colour palette of a style image. The slides illustrate this with examples reminiscent of Dalí and Bosch.

### 9. Adversarial Examples and Network Interpretability

The course devotes a segment to “Deeper Insight into the Deep Nets,” which is both a cautionary tale and a set of analysis tools:

- **Adversarial examples:** Small, imperceptible perturbations — found by gradient ascent on the input — can cause a well‑trained network to misclassify an image with high confidence. Physical adversarial attacks (stickers, T‑shirts, glasses) demonstrate that this vulnerability extends to the real world.
- **Visualisation and interpretability:** Techniques such as **Grad‑CAM** use the gradient of a class score with respect to the last convolutional feature map to produce a coarse heatmap highlighting the image regions most influential for the prediction. For transformers, **attention rollout** and gradient‑attention combinations reveal which image patches the model attends to. These methods help verify that the network is “looking” at the right things.
- **Deep Dream** amplifies the features detected by a network by iteratively modifying the input image to maximise the activations of chosen layers, producing hallucinogenic, dream‑like imagery.
- **Feature inversion:** Starting from random noise, one can reconstruct an image that produces the same internal feature representation as a target image, demonstrating that the network’s representation discards some information but retains semantic content.

### 10. Foundation Models and the Shift Toward Generalist Vision

The final part of the course introduces **foundation models** — large models pre‑trained on vast, often weakly supervised or self‑supervised data, which can be adapted to a wide range of downstream tasks with little or no fine‑tuning. Key examples include:

- **CLIP** (Contrastive Language–Image Pre‑training) learns a joint embedding space for images and text from 400 M image–caption pairs. It enables zero‑shot classification by comparing an image embedding to text embeddings of class names (e.g., “a photo of a cat”). CLIP’s embeddings are also powerful for retrieval and as a backbone for other tasks.
- **DINO** (self‑Distillation with NO labels) trains a Vision Transformer using a student–teacher framework on unlabelled images. The self‑attention maps of the class token spontaneously segment objects, demonstrating that semantic grouping emerges without explicit supervision. DINO features achieve competitive results on ImageNet with a simple k‑NN classifier.
- **Segment Anything (SAM)** and **Depth Anything** have already been mentioned; they exemplify the trend of building promptable, generalist models that can be applied out‑of‑the‑box to new domains.
- **FARL** (FAcial Representation Learning) applies contrastive text–image learning to faces, creating a universal face representation that transfers to landmark detection, age estimation, and segmentation.

These foundation models signal a paradigm shift: instead of training a specialised network from scratch for each task, practitioners increasingly fine‑tune or prompt a single large model that already encapsulates rich visual and linguistic knowledge.

### Summary

The applications of deep neural networks in computer vision span the entire spectrum from low‑level pixel tasks to high‑level semantic understanding and content creation. The course slides illustrate this breadth with dozens of examples, many of which have moved from research curiosities to commercial products in just a few years. Underpinning all these successes are the core principles covered in earlier sections: hierarchical feature learning, end‑to‑end differentiability, scalable optimisation with SGD, and regularisation techniques such as dropout and batch normalisation. As the field moves toward ever larger foundation models, the boundary between different vision tasks continues to blur, promising a future where a single model can perceive, reason about, and generate visual content with unprecedented flexibility.

---

### Self-Test

1. CLIP achieves zero-shot image classification by comparing image embeddings to text embeddings of class names — why does this work without any task-specific training, and what property of the pre-training objective makes it possible?
2. Neural Style Transfer represents style via the Gram matrix of feature correlations rather than the feature activations directly. Why does the Gram matrix capture "style" while higher-level activations capture "content"?
3. Adversarial examples are often transferable — a perturbation crafted for one model can fool a different model. What does this suggest about the geometry of decision boundaries learned by deep networks, and does it undermine or support the view that these networks learn meaningful representations?
4. DINO learns to segment objects without any segmentation labels, while SAM was trained on over 1 B labelled masks. Under what conditions would you expect DINO's unsupervised segmentation to fail where SAM succeeds, and vice versa?

### Answer Key

1. CLIP is pre-trained on 400 M image–caption pairs using a contrastive objective that forces images and their textual descriptions to share a common embedding space. Because class names are natural language phrases, they already live in this same space at inference time, so comparing image embeddings to class-name text embeddings is a direct application of the learned alignment — no additional supervision is needed. The key property is that the contrastive objective maximises similarity between matched image–text pairs globally, giving the representations cross-modal semantic structure rather than task-specific labels.

2. The Gram matrix $G_{ij} = \sum_k F_{ik} F_{jk}$ measures the co-occurrence (correlation) of different feature channels $i$ and $j$ across all spatial positions $k$, discarding positional information entirely. This spatial averaging is what makes it a style descriptor: textures and colour statistics repeat across an image independently of where objects sit, so the Gram matrix captures their frequency and co-occurrence without encoding object layout. Higher-level activations, by contrast, retain which features fire *where*, encoding the specific arrangement of parts that defines the scene's content.

3. Transferability implies that different networks, despite being independently initialised and trained, converge to decision boundaries with similar orientations in the high-dimensional input space. This suggests that adversarial directions are not idiosyncratic artefacts of a single model but reflect genuine structural properties of the image-to-label mapping learned from the data. The phenomenon is somewhat double-edged: it supports the view that networks learn consistent, data-driven features (otherwise transferability would be near chance), yet also reveals that these shared representations share a common geometric fragility rather than the robust invariances one would hope for.

4. DINO's unsupervised segmentation emerges from self-attention on the class token and works well when objects are visually salient, well-separated, and consistent with the ImageNet-like distribution on which it was trained; it is likely to fail on cluttered scenes, fine-grained boundaries, novel domains (e.g., medical images), or when asked to segment arbitrary, user-specified regions. SAM, trained on over 1 B diverse labelled masks and designed to be promptable, excels precisely in these cases — handling arbitrary categories, fine boundaries, and out-of-distribution imagery given explicit point or box prompts. Conversely, DINO may identify semantically meaningful object regions without any prompt in familiar natural scenes, where SAM without a prompt would not know *which* objects to segment.