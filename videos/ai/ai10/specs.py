"""Published numbers that Part 10 shows, each with its source.  Computed numbers are in ``compute.py``."""

# ---------------------------------------------------------------------------
# ImageNet (ILSVRC) classification: the winning top-5 error, by year
# ---------------------------------------------------------------------------
# 2010-2014: Russakovsky et al., "ImageNet Large Scale Visual Recognition Challenge", IJCV 115 (2015), Tables 5-7
#   (best entry per team; 2012 SuperVision 16.4% on the supplied data, 15.3% with the extra Fall 2011 images).
# 2015: He, Zhang, Ren & Sun, "Deep Residual Learning for Image Recognition" (arXiv 1512.03385): 3.57%.
# 2016 and 2017: Hu, Shen & Sun, "Squeeze-and-Excitation Networks" (arXiv 1709.01507): the 2016 winner 2.991%,
#   SENet (2017) 2.251%.
ILSVRC = [
    (2010, "NEC-UIUC", 28.2, "SIFT, LBP, coding, SVM"),
    (2011, "XRCE", 25.8, "Fisher vectors, linear SVM"),
    (2012, "SuperVision (AlexNet)", 16.4, "a deep CNN on two GPUs"),
    (2013, "Clarifai", 11.7, "CNNs (Zeiler & Fergus)"),
    (2014, "GoogLeNet", 6.7, "Inception, 22 layers"),
    (2015, "ResNet (MSRA)", 3.57, "152 layers, residual"),
    (2016, "Trimps-Soushen", 2.99, "ensembles"),
    (2017, "SENet", 2.25, "squeeze-and-excitation"),
]
ILSVRC_2012_SECOND = ("ISI", 26.2, "SIFT and other features, Fisher vectors")  # Russakovsky et al., Table 5
ALEXNET_EXTRA = 15.3  # with the extra ImageNet Fall 2011 data (Russakovsky et al.; Krizhevsky et al. 2012)
HUMAN_TOP5 = 5.1  # Andrej Karpathy, annotating 1,500 test images himself (Russakovsky et al. 2015, sec. 6.4)
VGG_2014 = 7.3  # Simonyan & Zisserman (2014): second in classification, ILSVRC 2014
ILSVRC_SIZES = dict(train=1_281_167, val=50_000, test=100_000, classes=1000)  # ILSVRC 2012-14 (Russakovsky et al.)

# ImageNet itself: Deng, Dong, Socher, Li, Li & Fei-Fei, "ImageNet: A Large-Scale Hierarchical Image Database",
# CVPR 2009; the first challenge, ILSVRC 2010, ran with the PASCAL VOC workshop.

# ---------------------------------------------------------------------------
# AlexNet (Krizhevsky, Sutskever & Hinton, NeurIPS 2012)
# ---------------------------------------------------------------------------
ALEXNET = dict(
    params="60 million", neurons="650,000", layers="five convolutional, three fully connected",
    gpus="two GTX 580, 3 GB each", days="five to six",
    relu_speedup=6,  # "a four-layer convolutional neural network with ReLUs reaches a 25% training error rate on
    # CIFAR-10 six times faster than an equivalent network with tanh neurons" (sec. 3.1, Figure 1)
    augment_factor=2048,  # random 224 x 224 crops of the 256 x 256 images, and reflections (sec. 4.1)
    dropout=0.5,  # in the first two fully connected layers; "without dropout, our network exhibits substantial
    # overfitting" (sec. 4.2)
    epochs=90,
)

# ---------------------------------------------------------------------------
# Digits
# ---------------------------------------------------------------------------
# LeCun, Bottou, Bengio & Haffner, "Gradient-Based Learning Applied to Document Recognition", Proc. IEEE 86 (1998):
# MNIST test error of LeNet-5 0.95% (0.8% trained with distorted copies); a linear classifier 12.0%; the check
# reader "is deployed commercially and reads several million checks per day" (abstract).
LENET5_1998 = 0.95
LENET5_DISTORT = 0.8
LINEAR_1998 = 12.0
# LeCun et al., "Backpropagation Applied to Handwritten Zip Code Recognition", Neural Computation 1 (1989):
# 7,291 training and 2,007 test digits from US mail, 16 x 16; 5.0% test error; about 9,760 free parameters
# (A. Karpathy's 2022 reproduction, karpathy.github.io/2022/03/14/lecun1989, gives these figures from the paper).
ZIP1989 = dict(train=7291, test=2007, error=5.0, params=9760, days=3)

# ---------------------------------------------------------------------------
# Adversarial examples
# ---------------------------------------------------------------------------
# Goodfellow, Shlens & Szegedy, "Explaining and Harnessing Adversarial Examples" (arXiv 1412.6572, ICLR 2015):
# the panda (57.7%) becomes a gibbon (99.3%) for GoogLeNet at eps = 0.007; on MNIST at eps = 0.25 a shallow softmax
# classifier errs on 99.9% of the adversarial examples, a maxout network on 89.4%; adversarial training brings the
# maxout network's adversarial error to 17.9%.
FGSM_PAPER = dict(panda=57.7, gibbon=99.3, eps=0.007, softmax=99.9, maxout=89.4, maxout_adv=17.9)

# ---------------------------------------------------------------------------
# Efficient networks
# ---------------------------------------------------------------------------
# Howard et al., "MobileNets" (arXiv 1704.04861), Table 8: ImageNet top-1, mult-adds (millions), parameters (millions)
MOBILENET = [("1.0 MobileNet-224", 70.6, 569, 4.2), ("GoogLeNet", 69.8, 1550, 6.8), ("VGG 16", 71.5, 15300, 138)]
# Liu et al., "A ConvNet for the 2020s" (arXiv 2201.03545), Figure 2: ResNet-50 modernized step by step, ImageNet-1K
# top-1 at about 4.5 GFLOPs; Swin-T 81.3%; ConvNeXt-XL with ImageNet-22K pre-training 87.8%.
CONVNEXT_STEPS = [("ResNet-50", 76.1), ("modern training recipe", 78.8), ("stage ratio", 79.4),
                  ("patchify stem", 79.5), ("depthwise conv, wider", 80.5), ("inverted bottleneck", 80.6),
                  ("7x7 kernels", 80.6), ("GELU, fewer activations and norms, LayerNorm", 81.5),
                  ("separate downsampling: ConvNeXt-T", 82.0)]
SWIN_T = 81.3
CONVNEXT_XL_22K = 87.8

# ---------------------------------------------------------------------------
# Machine translation
# ---------------------------------------------------------------------------
# Sutskever, Vinyals & Le, "Sequence to Sequence Learning with Neural Networks" (arXiv 1409.3215): WMT'14
# English-French; an ensemble of 5 deep LSTMs (4 layers, 1,000 cells, 384M parameters each) 34.81 BLEU; the
# phrase-based baseline 33.30; rescoring its 1,000-best lists 36.5; reversing the source: BLEU 25.9 -> 30.6.
SEQ2SEQ = dict(ensemble=34.81, smt=33.30, rescore=36.5, reverse_before=25.9, reverse_after=30.6, layers=4,
               cells=1000)
# Bahdanau, Cho & Bengio, "Neural Machine Translation by Jointly Learning to Align and Translate" (arXiv 1409.0473),
# Table 1, BLEU on all test sentences: RNNencdec-50 17.82, RNNsearch-50 26.75, RNNsearch-50* 28.45, Moses 33.30;
# on sentences without unknown words: 26.71, 34.16, 36.15, 35.63.
BAHDANAU = dict(encdec=17.82, search=26.75, search_long=28.45, moses=33.30, encdec_nounk=26.71,
                search_nounk=34.16, search_long_nounk=36.15, moses_nounk=35.63)
# Wu et al., "Google's Neural Machine Translation System" (arXiv 1609.08144): 8-layer LSTMs with attention and
# residual connections; human side-by-side evaluation: translation errors reduced by an average of 60% compared to
# Google's phrase-based production system.
GNMT = dict(layers=8, error_cut=60)

# ---------------------------------------------------------------------------
# Recurrent networks return
# ---------------------------------------------------------------------------
# Feng, Tung, Ahmed, Bengio & Hajimirsadeghi, "Were RNNs All We Needed?" (arXiv 2410.01201): minGRU and minLSTM
# train 175x and 235x faster per step than GRU and LSTM at sequence length 512 (GPU), 1,324x and 1,361x at 4,096.
MINRNN = dict(gru512=175, lstm512=235, gru4096=1324, lstm4096=1361)

# ---------------------------------------------------------------------------
# Receptive fields: published layer lists (name, kernel, stride[, dilation])
# ---------------------------------------------------------------------------
RF_LAYERS = {
    "LeNet-5": [("C1", 5, 1), ("S2", 2, 2), ("C3", 5, 1), ("S4", 2, 2), ("C5", 5, 1)],
    "AlexNet": [("conv1", 11, 4), ("pool1", 3, 2), ("conv2", 5, 1), ("pool2", 3, 2), ("conv3", 3, 1),
                ("conv4", 3, 1), ("conv5", 3, 1), ("pool5", 3, 2)],
    "VGG-16": [("conv1_1", 3, 1), ("conv1_2", 3, 1), ("pool1", 2, 2), ("conv2_1", 3, 1), ("conv2_2", 3, 1),
               ("pool2", 2, 2), ("conv3_1", 3, 1), ("conv3_2", 3, 1), ("conv3_3", 3, 1), ("pool3", 2, 2),
               ("conv4_1", 3, 1), ("conv4_2", 3, 1), ("conv4_3", 3, 1), ("pool4", 2, 2), ("conv5_1", 3, 1),
               ("conv5_2", 3, 1), ("conv5_3", 3, 1), ("pool5", 2, 2)],
    "our CIFAR network": [("conv1", 7, 2), ("conv2", 3, 1), ("pool", 2, 2), ("conv3", 3, 1), ("pool", 2, 2),
                          ("conv4", 3, 1)],
}
