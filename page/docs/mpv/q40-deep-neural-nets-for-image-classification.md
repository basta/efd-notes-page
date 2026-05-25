## Deep Neural Networks for Image Classification: Convolutional, Pooling, and Fully Connected Layers, and Non‑linearities

Deep neural networks have revolutionised image classification by learning hierarchical representations directly from raw pixels. The architecture that ignited the modern deep learning era – AlexNet – and its successors are built from a small set of fundamental layer types: **convolutional layers**, **pooling layers**, **fully connected layers**, and **non‑linear activation functions**. This section describes each of these building blocks, their roles within a classification network, and the design principles that make deep architectures trainable and effective.

### 1. The Overall Pipeline: From Pixels to Class Scores

A deep convolutional neural network (CNN) for image classification can be viewed as a directed acyclic computational graph that transforms an input image into a probability distribution over predefined categories. The typical structure, exemplified by AlexNet, consists of:

1. **Input layer** – an RGB image of size $W \times H \times 3$.
2. **Intermediate layers** – a sequence of convolutional layers, often interleaved with non‑linear activations and pooling layers.
3. **Fully connected layers** – one or more layers that aggregate the spatially distributed features into a fixed‑length vector.
4. **Output layer** – a softmax layer that produces a normalised probability vector over the $C$ classes.
5. **Loss function** – the cross‑entropy loss that compares the predicted distribution with the ground‑truth label during training.

The entire graph is **end‑to‑end differentiable**, meaning that the gradient of the loss with respect to every parameter can be computed by back‑propagation, enabling optimisation via stochastic gradient descent (SGD) or its adaptive variants such as ADAM.

### 2. Convolutional Layer

The convolutional layer is the core building block that exploits the spatial structure of images. Unlike a fully connected layer that connects every input to every output, a convolutional layer uses **local connectivity** and **weight sharing** to dramatically reduce the number of parameters and to make the network translationally equivariant.

#### 2.1 Input and Output Tensors

A convolutional layer operates on a 3D tensor (a multi‑channel feature map). Let the input be a tensor of size

$$
W \times H \times D,
$$

where $W$ and $H$ are the spatial width and height, and $D$ is the number of channels (e.g., $D=3$ for an RGB image, or $D=64$ for an intermediate feature map). The layer produces an output tensor of size

$$
W' \times H' \times D',
$$

where $D'$ is the number of filters (output channels) chosen by the architect.

#### 2.2 Filters (Kernels)

The layer contains a bank of $D'$ learnable filters. Each filter has spatial dimensions $K \times K$ and extends through the full depth $D$ of the input. Thus the total number of parameters per filter is $K \times K \times D$, and the whole layer has

$$
K \times K \times D \times D'
$$

parameters (plus one bias per output channel, if used). The filter is convolved with the input: at each spatial location, the element‑wise product between the filter weights and the corresponding input patch is computed and summed, yielding a single scalar in the output feature map. This operation is a **dot product** between the vectorised filter and the vectorised input patch.

#### 2.3 Stride and Padding

Two hyperparameters control the spatial dimensions of the output:

- **Stride $S$** – the step size with which the filter slides over the input. $S=1$ means the filter moves one pixel at a time; $S>1$ downsamples the feature map.
- **Zero padding $P$** – the number of zeros added to the border of the input. Padding is used to control the spatial size and to allow the filter to process the edges of the image.

The output spatial dimensions are given by

$$
W' = \left\lfloor \frac{W - K + 2P}{S} \right\rfloor + 1, \qquad
H' = \left\lfloor \frac{H - K + 2P}{S} \right\rfloor + 1.
$$

For example, a $3 \times 3$ filter with stride $1$ and padding $1$ preserves the spatial size ($W' = W$), a common design choice in modern architectures.

#### 2.4 Role in the Hierarchy

Early convolutional layers learn low‑level features such as oriented edges and colour blobs (resembling the receptive fields of simple cells in the primary visual cortex). Deeper layers combine these into mid‑level motifs (corners, textures, object parts) and eventually into high‑level, category‑specific patterns. Because the same filter is applied across all spatial locations, the network becomes **translationally equivariant**: if the input is shifted, the feature map shifts correspondingly.

### 3. Non‑linear Activation Functions

After each convolutional (or fully connected) layer, a non‑linear activation function is applied element‑wise to the output tensor. Without non‑linearities, the entire network would collapse into a single affine transformation, regardless of its depth. The choice of activation has a profound impact on training dynamics.

#### 3.1 Sigmoid and Tanh – Classical Saturating Non‑linearities

The **sigmoid** function

$$
\sigma(x) = \frac{1}{1 + e^{-x}}
$$

squashes each input into the interval $(0,1)$. The **hyperbolic tangent**

$$
\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}
$$

squashes into $(-1,1)$. Both were widely used in early neural networks. However, they suffer from the **vanishing gradient** problem: for large positive or negative inputs, the function saturates (its derivative approaches zero). During back‑propagation, gradients are multiplied by these tiny derivatives, causing the gradient signal to decay exponentially as it flows backward through many layers. This makes deep networks extremely difficult to train with saturating non‑linearities.

#### 3.2 ReLU – Rectified Linear Unit

The **ReLU** activation, defined as

$$
\text{ReLU}(x) = \max(0, x),
$$

is the simplest non‑linearity and was a key enabler of deep network training in AlexNet. Its derivative is $1$ for positive inputs and $0$ for negative inputs. The non‑saturating nature for $x>0$ prevents the vanishing gradient, allowing gradients to flow freely through many layers. ReLU is computationally cheap and often serves as a strong baseline. A potential issue is that neurons can “die” if they consistently receive negative inputs, causing their gradient to be zero and never recovering. Variants such as **Leaky ReLU** ($\max(0.1x, x)$) and **ELU** (Exponential Linear Unit) address this by allowing a small, non‑zero slope for negative inputs.

#### 3.3 Other Activation Functions

The slides also mention **Maxout**, which takes the maximum over a set of linear responses, and more recent activations like **GELU** (Gaussian Error Linear Unit), a smooth approximation used in transformers and modern CNNs (e.g., ConvNeXt). The general trend is toward non‑saturating, smooth functions that facilitate optimisation.

### 4. Pooling Layer

Pooling layers reduce the spatial dimensions of feature maps, thereby decreasing the number of parameters and computation in the network, and providing a degree of **local translation invariance**. The most common type is **max‑pooling**.

#### 4.1 Max‑Pooling Operation

A max‑pooling layer takes an input tensor of size $W \times H \times D$ and produces an output of size $W' \times H' \times D$ (the depth is unchanged). It operates independently on each channel. A spatial window of size $K \times K$ slides over the input with stride $S$, and at each position the maximum value within the window is taken. Padding $P$ can be applied similarly to convolution.

For example, with $K=2$, $S=2$, and $P=0$, the spatial resolution is halved. The output dimensions follow the same formula as for convolution.

#### 4.2 Properties

- **No learnable parameters** – max‑pooling is a fixed, non‑linear operation.
- **Dimensionality reduction** – by downsampling, it reduces the computational load for subsequent layers and enlarges the effective receptive field.
- **Local translation invariance** – small shifts in the input may not change the maximum within a pooling window, making the representation robust to minor spatial perturbations.

In modern architectures, pooling is sometimes replaced by strided convolutions, but the principle of gradual spatial reduction remains essential.

### 5. Fully Connected Layer

After several convolutional and pooling stages, the spatial dimensions of the feature maps are typically small (e.g., $6 \times 6$ or $7 \times 7$) while the depth is large (e.g., $256$ or $512$). At this point, the 3D tensor is **flattened** into a 1D vector and fed into one or more **fully connected (FC) layers**.

An FC layer connects every input neuron to every output neuron via a weight matrix $\mathbf{W}$ and a bias vector $\mathbf{b}$:

$$
\mathbf{y} = \mathbf{W}\mathbf{x} + \mathbf{b}.
$$

The number of parameters in an FC layer is the product of the input and output dimensions, which can be enormous. For instance, in AlexNet the first FC layer takes a flattened vector of size $9216$ ($6 \times 6 \times 256$) and maps it to $4096$ units, resulting in over $37$ million parameters. This is why modern architectures (e.g., GoogLeNet, ResNet) often avoid large FC layers altogether, using global average pooling instead to produce a compact feature vector.

The final FC layer produces a vector of raw scores (logits) of length $C$, the number of classes. These logits are then passed through a **softmax** function to obtain a probability distribution:

$$
p_i = \frac{e^{z_i}}{\sum_{j=1}^{C} e^{z_j}},
$$

where $z_i$ is the logit for class $i$. The network is trained by minimising the **cross‑entropy loss** between the predicted distribution $\mathbf{p}$ and the one‑hot encoded ground‑truth label $\mathbf{y}$:

$$
L = -\sum_{i=1}^{C} y_i \log p_i.
$$

### 6. Putting It All Together: The AlexNet Example

AlexNet, the architecture that won the ILSVRC 2012 challenge by a large margin, is a canonical illustration of these building blocks. It consists of:

- **5 convolutional layers**, each followed by a ReLU non‑linearity. The first, second, and fifth convolutional layers are followed by max‑pooling layers that reduce spatial resolution.
- **3 fully connected layers**: two with 4096 units each (with ReLU and dropout), and a final softmax layer with 1000 outputs for the ImageNet classes.
- **60 million parameters** in total, trained on 1.2 million labelled images.

Key design choices that enabled its success include:

- **ReLU** instead of sigmoid/tanh to mitigate vanishing gradients.
- **Dropout** – randomly omitting 50% of hidden units during training to prevent over‑fitting, effectively averaging many subnetworks.
- **Data augmentation** – artificially enlarging the training set by random crops and horizontal flips.
- **GPU implementation** – exploiting the massive parallelism of convolutional operations.

### 7. Why Deep Networks Work Now

The slide material highlights several reasons why deep CNNs became feasible and dominant after decades of scepticism:

- **Large labelled datasets** (e.g., ImageNet with 1.2M images) provide enough supervision to train millions of parameters without severe over‑fitting.
- **Weight sharing** in convolutional layers drastically reduces the parameter count compared to fully connected networks, making deep architectures practical.
- **Non‑saturating activations (ReLU)** and **batch normalisation** (later developments) stabilise gradient flow, allowing networks with tens or hundreds of layers to be trained.
- **Powerful parallel hardware (GPUs)** delivers the computational throughput needed for both training and inference.

### 8. Summary

A deep neural network for image classification is composed of a hierarchy of layers:

- **Convolutional layers** extract local features through learnable filters, exploiting spatial structure and weight sharing.
- **Non‑linear activation functions** (most commonly ReLU and its variants) introduce the non‑linearity necessary for learning complex mappings, while avoiding the vanishing gradient problem that plagued earlier saturating functions.
- **Pooling layers** (typically max‑pooling) progressively reduce spatial resolution, increasing the receptive field and providing local translation invariance.
- **Fully connected layers** aggregate the spatially distributed features into a global representation and produce the final class scores, with a softmax output and cross‑entropy loss driving supervised training.

This modular, differentiable architecture, combined with large datasets and GPU acceleration, forms the foundation of modern image classification and has been extended to countless other vision tasks.

---

### Self-Test

1. ReLU solves the vanishing gradient problem for positive activations, but neurons can "die" permanently during training. Under what conditions does this happen, and why does Leaky ReLU prevent it?
2. A convolutional layer and a fully connected layer can both learn linear mappings followed by a non-linearity — how does weight sharing in convolution change what the layer can and cannot represent compared to a fully connected layer?
3. If you replace all max-pooling layers in a CNN with strided convolutions (same stride and kernel size), what do you gain and what do you lose relative to the original design?
4. Global average pooling collapses each channel's spatial map to a single value before the final classifier, replacing large FC layers. When might this design choice hurt classification accuracy compared to using FC layers?

### Answer Key

1. A ReLU neuron dies when it receives a consistently large negative input, so its output is always zero and its gradient is always zero — the weight update is therefore zero and the neuron never recovers. Leaky ReLU prevents this by using $\max(0.1x, x)$ instead of $\max(0, x)$, giving a small but non-zero gradient for negative inputs so that the weight can still be updated and the neuron can recover.

2. Weight sharing means every spatial position uses the same filter, so a convolutional layer can only detect features that are the same regardless of where they appear in the image — it is translationally equivariant but cannot learn position-specific patterns. A fully connected layer has independent weights for every input-output pair, so it can represent arbitrary position-dependent mappings but loses the parameter efficiency and translational structure that make convolutions effective for images.

3. Replacing max-pooling with strided convolutions adds learnable parameters (the kernel weights), allowing the network to learn a data-driven downsampling rather than a fixed maximum operation; this can improve representational power and performance. However, you lose the guaranteed local translation invariance that max-pooling provides, since a learned strided convolution is not constrained to pick the locally dominant activation, and you add parameters and computation that may increase overfitting risk on small datasets.

4. Global average pooling discards all spatial layout information within each channel map, so if the classification task depends on fine-grained spatial relationships or the precise configuration of parts (e.g., distinguishing faces with different expressions, or fine-grained species recognition), collapsing to a single scalar per channel can lose discriminative information that FC layers — operating on the full flattened feature map — could exploit. It can also hurt when the network's final feature maps are too coarse or semantically entangled for a simple channel-wise average to form a clean linear boundary between classes.