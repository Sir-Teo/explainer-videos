"""Precompute everything numerical in Part 10 of the AI series ("Seeing and Remembering").

    python -m videos.ai.ai10.compute                  # everything missing: about two hours on two CPU cores
    python -m videos.ai.ai10.compute lenet cifar      # some items
    python -m videos.ai.ai10.compute --force memory

Results are cached in ``.cache/ai10/<name>.json`` (+ ``.npz``); trained weights in ``.cache/ai10/models/``; scenes
call ``load(name)``.  Every network here is trained on this computer (PyTorch on the CPU, two threads), seeded.  The
data: MNIST (60,000 + 10,000 handwritten digits) and CIFAR-10 (50,000 + 10,000 small colour photographs), downloaded
once and checked against SHA-256 (``data.py``); Part 1's thirty novels for the character LSTM, read through Part 1's
``compute``.  Published numbers (ImageNet results, architectures) are in ``specs.py``, cited there.

Every long job resumes after an interruption: LeNet and the CIFAR network save a checkpoint after every epoch, the
character LSTM every 100 steps, and the many short runs (memory task, seq2seq, comparisons) are kept run by run
(``CACHE.partial``).  Items that need a trained network train it themselves (or load it), so this module alone
rebuilds the part.

Items:
    data         the two datasets: checksums, counts, sample images
    hog          before deep learning: Sobel edges and histograms of oriented gradients (Dalal & Triggs 2005),
                 computed here; a linear classifier on raw pixels against the same classifier on HOG features
                 (MNIST and CIFAR-10, three seeds)
    lenet        LeNet-5's layout trained on MNIST, three seeds, 6 epochs; seed 0 replayed: first-layer filters,
                 feature maps of one digit and its prediction at checkpoints through training
    equivariance convolution commutes with shifts (circular padding: exact; zero padding: except at the border); a
                 dense layer does not; pooling breaks it for odd shifts; parameter counts
    receptive    receptive fields computed layer by layer for LeNet-5, AlexNet, VGG-16, ResNet-50 and our networks;
                 the effective receptive field (gradient of one unit) of our CIFAR network, trained and untrained
    mlp_cnn      LeNet against an MLP with the same number of parameters (three seeds): test error; on shifted
                 digits; and both retrained on digits whose pixels are shuffled by one fixed permutation
    activations  ReLU, tanh and sigmoid in the same 6-layer CNN, SGD with momentum, three seeds: training speed
    dropout      a 784-512-512-10 MLP on 5,000 digits for 60 epochs, with and without dropout (three seeds)
    datasize     LeNet on 500 ... 60,000 training digits, equal steps, with and without shifted copies (three seeds)
    alexnet      parameters and multiply-adds layer by layer, from the published architectures (AlexNet, VGG-16)
    cifar        the CIFAR-10 network, 10 epochs: curve, test accuracy, first-layer filters at checkpoints
    orientation  Hubel and Wiesel's experiment on our filters: responses to oriented gratings, tuning curves,
                 orientation selectivity of every first-layer filter, trained and untrained
    filters      deeper features of the CIFAR network: top-activating patches and images, class visualizations,
                 saliency maps, feature maps of one photograph
    adversarial  FGSM (Goodfellow, Shlens & Szegedy 2014) and PGD against a linear model, the MLP and LeNet on
                 MNIST, and against the CIFAR network; transfer between models; logits along the attack direction
    advtrain     LeNet trained on clean and adversarial digits (fast FGSM with a random start), three seeds
    depthwise    a standard 3x3 convolution against depthwise + pointwise, FLOPs and measured time on this CPU;
                 receptive fields of dilated stacks
    rnn_grad     products of Jacobians back through a random RNN (tanh and linear) at several spectral radii; the
                 cliff of a one-unit RNN's loss and gradient descent across it, with and without clipping
    memory       remember the first symbol across T = 10, 30, 100 steps: RNN, LSTM, GRU and minGRU, three seeds;
                 the gradient reaching each time step during training
    charlstm     a character LSTM (512 cells) on Part 1's thirty novels: curve, bits per character on the
                 scoreboard's passage, samples at checkpoints, a cell that tracks quotation marks, greedy against
                 beam search (checkpointed every 100 steps)
    seq2seq      reversing strings with an RNN encoder-decoder, with and without Bahdanau attention (three seeds):
                 accuracy by length, alignments at checkpoints through training, greedy against beam search
    scan         the linear recurrence h_t = a_t h_{t-1} + b_t sequentially and by a parallel scan: equal answers,
                 rounds, and time on this CPU
    teaser       Part 11's preview: gradient descent, momentum and Adam on one valley
"""

from __future__ import annotations

import math
import os
import time
from pathlib import Path

if __name__ == "__main__":
    for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
        os.environ.setdefault(_v, "2")

import numpy as np  # noqa: E402

from explainer.ai.cache import Cache  # noqa: E402

CACHE = Cache("ai10")
load = CACHE.load
MODELS = CACHE.dir / "models"
THREADS = 2


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def _torch():
    import torch

    torch.set_num_threads(THREADS)
    return torch


def _save_torch(obj, path: Path) -> None:
    torch = _torch()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    torch.save(obj, tmp)
    tmp.replace(path)


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------
def mnist_t():
    """MNIST as float tensors in [0, 1], (n, 1, 28, 28), and int64 labels."""
    torch = _torch()
    from videos.ai.ai10 import data

    d = data.mnist()
    f = lambda a: torch.from_numpy(a.astype(np.float32) / 255.0)[:, None]  # noqa: E731
    return f(d["xtr"]), torch.from_numpy(d["ytr"].astype(np.int64)), f(d["xte"]), torch.from_numpy(
        d["yte"].astype(np.int64))


def cifar_u8():
    from videos.ai.ai10 import data

    return data.cifar()


def cifar_batch(x_u8: np.ndarray):
    """uint8 (n, 32, 32, 3) -> float tensor (n, 3, 32, 32) in [0, 1]."""
    torch = _torch()
    return torch.from_numpy(x_u8.astype(np.float32) / 255.0).permute(0, 3, 1, 2).contiguous()


def shift_images(x, dy: int, dx: int):
    """Shift a batch of images (n, c, H, W) by (dy, dx) pixels, filling with zeros (not wrapping)."""
    torch = _torch()
    out = torch.zeros_like(x)
    H, W = x.shape[-2:]
    ys, yd = (slice(0, H - dy), slice(dy, H)) if dy >= 0 else (slice(-dy, H), slice(0, H + dy))
    xs, xd = (slice(0, W - dx), slice(dx, W)) if dx >= 0 else (slice(-dx, W), slice(0, W + dx))
    out[..., yd, xd] = x[..., ys, xs]
    return out


def accuracy(model, X, Y, batch: int = 2000) -> float:
    torch = _torch()
    model.eval()
    right = 0
    with torch.no_grad():
        for i in range(0, len(X), batch):
            right += int((model(X[i:i + batch]).argmax(1) == Y[i:i + batch]).sum())
    model.train()
    return right / len(X)


def cifar_accuracy(model, x_u8, y, batch: int = 1000) -> float:
    torch = _torch()
    model.eval()
    right = 0
    with torch.no_grad():
        for i in range(0, len(x_u8), batch):
            right += int((model(cifar_batch(x_u8[i:i + batch])).argmax(1) == torch.from_numpy(
                y[i:i + batch].astype(np.int64))).sum())
    model.train()
    return right / len(x_u8)


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
def compute_data():
    from videos.ai.ai10 import data

    m, c = data.mnist(), data.cifar()
    # ten test digits of each class, in order of appearance, for the pictures
    grid = np.stack([m["xte"][np.flatnonzero(m["yte"] == k)[:10]] for k in range(10)])
    cgrid = np.stack([c["xte"][np.flatnonzero(c["yte"] == k)[:8]] for k in range(10)])
    return dict(
        mnist_sha256=data.MNIST_FILES, cifar_sha256=data.CIFAR_SHA256,
        mnist_train=int(len(m["ytr"])), mnist_test=int(len(m["yte"])), cifar_train=int(len(c["ytr"])),
        cifar_test=int(len(c["yte"])), mnist_counts=np.bincount(m["ytr"]).tolist(),
        cifar_classes=data.CIFAR_CLASSES, mnist_grid=grid, cifar_grid=cgrid,
        mnist_first=m["xte"][:64], mnist_first_labels=m["yte"][:64].astype(np.int64),
        cifar_first=c["xte"][:64], cifar_first_labels=c["yte"][:64].astype(np.int64))


# ---------------------------------------------------------------------------
# Before deep learning: edges and histograms of oriented gradients
# ---------------------------------------------------------------------------
def gradients(img: np.ndarray):
    """Centred differences [-1, 0, 1] along x and y (Dalal & Triggs' choice), zero at the border."""
    gx = np.zeros_like(img)
    gy = np.zeros_like(img)
    gx[..., :, 1:-1] = img[..., :, 2:] - img[..., :, :-2]
    gy[..., 1:-1, :] = img[..., 2:, :] - img[..., :-2, :]
    return gx, gy


def sobel(img: np.ndarray) -> np.ndarray:
    k = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], float)
    p = np.pad(img, 1, mode="edge")
    gx = sum(k[i, j] * p[i:i + img.shape[0], j:j + img.shape[1]] for i in range(3) for j in range(3))
    gy = sum(k.T[i, j] * p[i:i + img.shape[0], j:j + img.shape[1]] for i in range(3) for j in range(3))
    return np.hypot(gx, gy)


def hog_cells(imgs: np.ndarray, cell: int, nbins: int = 9) -> np.ndarray:
    """Per-cell histograms of gradient orientation (unsigned, 0-180 degrees), weighted by gradient magnitude and
    split linearly between the two nearest bins: (n, cells_y, cells_x, nbins)."""
    gx, gy = gradients(imgs)
    mag = np.hypot(gx, gy)
    ang = np.degrees(np.arctan2(gy, gx)) % 180.0
    pos = ang / (180.0 / nbins) - 0.5
    b0 = np.floor(pos).astype(int)
    w1 = pos - b0
    b0 %= nbins
    b1 = (b0 + 1) % nbins
    n, H, W = imgs.shape
    cy, cx = H // cell, W // cell
    out = np.zeros((n, cy, cx, nbins))
    for k in range(nbins):
        wk = mag * ((b0 == k) * (1 - w1) + (b1 == k) * w1)
        out[..., k] = wk[:, :cy * cell, :cx * cell].reshape(n, cy, cell, cx, cell).sum((2, 4))
    return out


def hog(imgs: np.ndarray, cell: int, nbins: int = 9, block: int = 2) -> np.ndarray:
    """HOG features: cell histograms grouped in overlapping 2 x 2 blocks, each L2-Hys normalized."""
    h = hog_cells(imgs, cell, nbins)
    n, cy, cx, _ = h.shape
    feats = []
    for by in range(cy - block + 1):
        for bx in range(cx - block + 1):
            v = h[:, by:by + block, bx:bx + block].reshape(n, -1)
            v = v / np.sqrt((v ** 2).sum(1, keepdims=True) + 1e-6)
            v = np.minimum(v, 0.2)
            v = v / np.sqrt((v ** 2).sum(1, keepdims=True) + 1e-6)
            feats.append(v)
    return np.concatenate(feats, 1).astype(np.float32)


def fit_linear(Xtr, ytr, Xte, yte, seed: int, epochs: int = 10, batch: int = 256, lr: float = 3e-3) -> float:
    """Multinomial logistic regression (standardized features, Adam): test error."""
    torch = _torch()
    from videos.ai.ai10 import nets

    mu, sd = Xtr.mean(0, keepdims=True), Xtr.std(0, keepdims=True) + 1e-6
    A = torch.from_numpy(((Xtr - mu) / sd).astype(np.float32))
    B = torch.from_numpy(((Xte - mu) / sd).astype(np.float32))
    ya, yb = torch.from_numpy(ytr.astype(np.int64)), torch.from_numpy(yte.astype(np.int64))
    torch.manual_seed(seed)
    model = nets.Linear(A.shape[1], 10)
    opt = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=1e-5)
    g = rng(seed)
    for _ in range(epochs):
        order = g.permutation(len(A))
        for i in range(0, len(A), batch):
            ix = torch.from_numpy(order[i:i + batch])
            loss = torch.nn.functional.cross_entropy(model(A[ix]), ya[ix])
            opt.zero_grad()
            loss.backward()
            opt.step()
    return 1.0 - accuracy(model, B, yb)


def compute_hog():
    from videos.ai.ai10 import data

    m, c = data.mnist(), data.cifar()
    out = {}
    # the pictures: one digit's gradients and cell histograms; a photograph's Sobel edges
    k = int(np.flatnonzero(m["yte"] == 2)[0])
    d = m["xte"][k].astype(float) / 255.0
    gx, gy = gradients(d)
    out.update(digit=d, digit_label=2, digit_gx=gx, digit_gy=gy, digit_cells=hog_cells(d[None], 7)[0],
               digit_sobel=sobel(d))
    kc = int(np.flatnonzero(c["yte"] == 7)[2])  # a horse
    photo = c["xte"][kc].astype(float) / 255.0
    grey = photo @ np.array([0.299, 0.587, 0.114])
    out.update(photo=photo, photo_label=7, photo_sobel=sobel(grey), photo_cells=hog_cells(grey[None], 8)[0])
    # the comparison: the same linear classifier on raw pixels and on HOG features
    seeds = (0, 1, 2)
    mx_tr, mx_te = m["xtr"].reshape(60000, -1) / 255.0, m["xte"].reshape(10000, -1) / 255.0
    mh_tr, mh_te = hog(m["xtr"] / 255.0, 7), hog(m["xte"] / 255.0, 7)
    gtr = c["xtr"].astype(np.float32) @ np.array([0.299, 0.587, 0.114], np.float32) / 255.0
    gte = c["xte"].astype(np.float32) @ np.array([0.299, 0.587, 0.114], np.float32) / 255.0
    cx_tr, cx_te = c["xtr"].reshape(50000, -1) / 255.0, c["xte"].reshape(10000, -1) / 255.0
    ch_tr, ch_te = hog(gtr, 8), hog(gte, 8)
    res = {}
    for name, (a, ya, b, yb) in {"mnist_pixels": (mx_tr, m["ytr"], mx_te, m["yte"]),
                                 "mnist_hog": (mh_tr, m["ytr"], mh_te, m["yte"]),
                                 "cifar_pixels": (cx_tr, c["ytr"], cx_te, c["yte"]),
                                 "cifar_hog": (ch_tr, c["ytr"], ch_te, c["yte"])}.items():
        errs = [fit_linear(a.astype(np.float32), ya, b.astype(np.float32), yb, s) for s in seeds]
        res[name] = dict(errors=errs, mean=float(np.mean(errs)), dims=int(a.shape[1]))
        print(f"    {name}: {100 * np.mean(errs):.2f}% error ({a.shape[1]} features)", flush=True)
    out["linear"] = res
    out["hog_dims"] = dict(mnist=int(mh_tr.shape[1]), cifar=int(ch_tr.shape[1]))
    return out


# ---------------------------------------------------------------------------
# LeNet on MNIST: three seeds, the first replayed
# ---------------------------------------------------------------------------
LENET_EPOCHS = 6
LENET_BATCH = 64
LENET_SNAPS = (0, 10, 25, 50, 100, 200, 400, 800, 1600, 3200, 5625)
REPLAY_DIGIT = 0  # the first test digit, a 7


def train_mnist(model, seed: int, epochs: int, tag: str, X=None, Y=None, Xte=None, Yte=None, lr: float = 1e-3,
                snaps=(), snap_fn=None, augment: bool = False, steps: int | None = None, batch: int = LENET_BATCH,
                log_every: int = 10):
    """Adam on MNIST (or on (X, Y)) for ``epochs`` (or ``steps``), checkpointed after every epoch in
    models/<tag>.ckpt; returns the curves.  ``snap_fn(step)`` is called at the steps in ``snaps``."""
    torch = _torch()
    F = torch.nn.functional
    if X is None:
        X, Y, Xte, Yte = mnist_t()
    n = len(X)
    per_epoch = math.ceil(n / batch)
    total = steps if steps is not None else epochs * per_epoch
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    g = rng(seed)
    ck = MODELS / f"{tag}.ckpt"
    state = dict(step=0, curve=[], test=[], snaps={})
    if ck.exists():
        s = torch.load(ck, weights_only=False)
        model.load_state_dict(s["model"])
        opt.load_state_dict(s["opt"])
        g.bit_generator.state = s["rng"]
        torch.set_rng_state(s["torch_rng"])
        state = s["state"]
        print(f"    resuming {tag} at step {state['step']}", flush=True)
    step = state["step"]
    if step == 0 and 0 in snaps and snap_fn is not None:
        state["snaps"][0] = snap_fn(0)
    while step < total:
        order = g.permutation(n)
        for i in range(0, n, batch):
            if step >= total:
                break
            ix = torch.from_numpy(order[i:i + batch])
            x, y = X[ix], Y[ix]
            if augment:  # random shifts of up to two pixels, the cheapest "more data"
                dy, dx = (int(v) for v in g.integers(-2, 3, 2))
                x = shift_images(x, dy, dx)
            logits = model(x)
            loss = F.cross_entropy(logits, y)
            opt.zero_grad()
            loss.backward()
            opt.step()
            step += 1
            if step % log_every == 0:
                state["curve"].append([step, float(loss), float((logits.argmax(1) != y).float().mean())])
            if step in snaps and snap_fn is not None:
                state["snaps"][step] = snap_fn(step)
            if step % per_epoch == 0 or step == total:
                if Xte is not None:
                    state["test"].append([step, 1.0 - accuracy(model, Xte, Yte)])
                state["step"] = step
                _save_torch(dict(model=model.state_dict(), opt=opt.state_dict(), rng=g.bit_generator.state,
                                 torch_rng=torch.get_rng_state(), state=state), ck)
    return state


def lenet_run(seed: int, act: str = "relu") -> tuple:
    """Train (or load) LeNet-5 with this seed; returns (model, results).  The results of a finished run are kept in
    models/lenet_<act>_s<seed>.json, the weights next to it."""
    torch = _torch()
    import json

    from videos.ai.ai10 import nets

    tag = f"lenet_{act}_s{seed}"
    wpath, rpath = MODELS / f"{tag}.pt", MODELS / f"{tag}.json"
    torch.manual_seed(seed)
    model = nets.LeNet5(act)
    if wpath.exists() and rpath.exists():
        model.load_state_dict(torch.load(wpath, weights_only=False))
        return model, json.loads(rpath.read_text())
    X, Y, Xte, Yte = mnist_t()
    xd = Xte[REPLAY_DIGIT:REPLAY_DIGIT + 1]

    def snap(step):
        with torch.no_grad():
            model.eval()
            a1, a3 = model.maps(xd)
            p = model(xd).softmax(1)[0]
            err = 1.0 - accuracy(model, Xte, Yte)
            model.train()
        return dict(w1=model.c1.weight.detach()[:, 0].numpy().tolist(), a1=a1[0].numpy().tolist(),
                    a3=a3[0].numpy().tolist(), p=p.numpy().tolist(), test_error=err)

    t0 = time.time()
    st = train_mnist(model, seed, LENET_EPOCHS, tag, X, Y, Xte, Yte, snaps=LENET_SNAPS if seed == 0 else (),
                     snap_fn=snap if seed == 0 else None)
    model.eval()
    with torch.no_grad():
        pred = torch.cat([model(Xte[i:i + 2000]).argmax(1) for i in range(0, 10000, 2000)])
    wrong = torch.nonzero(pred != Yte).flatten()
    conf = np.zeros((10, 10), int)
    np.add.at(conf, (Yte.numpy(), pred.numpy()), 1)
    res = dict(seed=seed, act=act, curve=st["curve"], test=st["test"], snaps={str(k): v for k, v in st["snaps"].items()},
               test_error=float(st["test"][-1][1]), wrong=wrong[:24].tolist(), wrong_pred=pred[wrong[:24]].tolist(),
               n_wrong=int(len(wrong)), confusion=conf.tolist(), seconds=time.time() - t0, params=nets.count(model))
    _save_torch(model.state_dict(), wpath)
    rpath.write_text(json.dumps(res))
    (MODELS / f"{tag}.ckpt").unlink(missing_ok=True)
    return model, res


def compute_lenet():
    from videos.ai.ai10 import data

    runs = [lenet_run(s)[1] for s in (0, 1, 2)]
    r0 = runs[0]
    snaps = r0["snaps"]
    steps = sorted(int(k) for k in snaps)
    m = data.mnist()
    out = dict(params=r0["params"], epochs=LENET_EPOCHS, batch=LENET_BATCH, steps=steps,
               curve=np.asarray(r0["curve"]), test=[r["test"] for r in runs],
               test_error=[r["test_error"] for r in runs], seconds=[r["seconds"] for r in runs],
               w1=np.asarray([snaps[str(s)]["w1"] for s in steps]), a1=np.asarray([snaps[str(s)]["a1"] for s in steps]),
               a3=np.asarray([snaps[str(s)]["a3"] for s in steps]), p=np.asarray([snaps[str(s)]["p"] for s in steps]),
               snap_error=[snaps[str(s)]["test_error"] for s in steps], digit=m["xte"][REPLAY_DIGIT],
               digit_label=int(m["yte"][REPLAY_DIGIT]), wrong=r0["wrong"], wrong_pred=r0["wrong_pred"],
               wrong_true=[int(m["yte"][i]) for i in r0["wrong"]], wrong_img=m["xte"][r0["wrong"]],
               n_wrong=[r["n_wrong"] for r in runs], confusion=np.asarray(r0["confusion"]))
    return out


# ---------------------------------------------------------------------------
# Convolution and shifts
# ---------------------------------------------------------------------------
def compute_equivariance():
    torch = _torch()
    F = torch.nn.functional
    from videos.ai.ai10 import data

    model, _ = lenet_run(0)
    W = model.c1.weight.detach()  # (6, 1, 5, 5)
    m = data.mnist()
    x = torch.from_numpy(m["xte"][REPLAY_DIGIT].astype(np.float32) / 255.0)[None, None]
    sy, sx = 3, -2

    def conv_circ(z):
        return F.conv2d(F.pad(z, (2, 2, 2, 2), mode="circular"), W)

    def roll(z, a, b):
        return torch.roll(z, shifts=(a, b), dims=(-2, -1))

    ref = conv_circ(x)
    scale = float(ref.abs().max())
    e_circ = float((conv_circ(roll(x, sy, sx)) - roll(ref, sy, sx)).abs().max()) / scale
    # zero padding: the same away from the border
    zz = F.conv2d(x, W, padding=2)
    diff = (F.conv2d(shift_images(x, sy, sx), W, padding=2) - shift_images(zz, sy, sx)).abs()[0].amax(0)
    inner = diff[2 + abs(sy):-2 - abs(sy), 2 + abs(sx):-2 - abs(sx)]
    e_zero_inside, e_zero_all = float(inner.max()) / scale, float(diff.max()) / scale
    # a dense layer with the same number of outputs: no such identity
    g = torch.Generator().manual_seed(0)
    D = torch.randn(6 * 784, 784, generator=g) / 28.0
    dense = lambda z: (D @ z.flatten()).view(6, 28, 28)  # noqa: E731
    e_dense = float((dense(roll(x, sy, sx)) - roll(dense(x), sy, sx)).abs().max() / dense(x).abs().max())
    # max pooling (stride 2): a shift by 2 pixels is a shift by 1 in the pooled map; a shift by 1 is no shift at all
    pooled = F.max_pool2d(F.relu(ref), 2)

    def pool_err(s):
        p2 = F.max_pool2d(F.relu(conv_circ(roll(x, s, 0))), 2)
        cands = [roll(pooled, k, 0) for k in (s // 2, (s + 1) // 2)]
        return min(float((p2 - c).abs().max()) for c in cands) / float(pooled.abs().max())

    # the picture of the sweep: one learned filter over the digit
    k = int(np.argmax([float(W[i].abs().sum()) for i in range(6)]))
    fmap = F.conv2d(x, W[k:k + 1], padding=2)[0, 0].numpy()
    shifted = shift_images(x, sy, sx)
    fmap_shift = F.conv2d(shifted, W[k:k + 1], padding=2)[0, 0].numpy()
    return dict(shift=[sy, sx], err_circular=e_circ, err_zero_inside=e_zero_inside, err_zero_all=e_zero_all,
                err_dense=e_dense, err_pool_1=pool_err(1), err_pool_2=pool_err(2), err_pool_3=pool_err(3),
                err_pool_4=pool_err(4), kernel_index=k, kernel=W[k, 0].numpy(), digit=x[0, 0].numpy(), fmap=fmap,
                digit_shift=shifted[0, 0].numpy(), fmap_shift=fmap_shift,
                params_conv=6 * (25 + 1), params_local=28 * 28 * 6 * (25 + 1), params_dense=784 * 4704 + 4704)


# ---------------------------------------------------------------------------
# Receptive fields
# ---------------------------------------------------------------------------
def rf_table(layers):
    """layers: [(name, kernel, stride, dilation)]; r_l = r_{l-1} + (k_eff - 1) j_{l-1}, j_l = j_{l-1} s_l."""
    r, j, rows = 1, 1, []
    for name, k, s, *d in layers:
        dil = d[0] if d else 1
        keff = dil * (k - 1) + 1
        r = r + (keff - 1) * j
        j = j * s
        rows.append([name, k, s, dil, r, j])
    return rows


def resnet50_layers():
    L = [("conv1", 7, 2), ("pool1", 3, 2)]
    for stage, (blocks, first_stride) in enumerate(((3, 1), (4, 2), (6, 2), (3, 2)), start=2):
        for b in range(blocks):
            s = first_stride if b == 0 else 1
            # the original ResNet puts the stride on the block's first 1x1 convolution
            L += [(f"conv{stage}_{b + 1}a", 1, s), (f"conv{stage}_{b + 1}b", 3, 1), (f"conv{stage}_{b + 1}c", 1, 1)]
    return L


def compute_receptive():
    torch = _torch()
    from videos.ai.ai10 import specs

    tables = {name: rf_table(layers) for name, layers in specs.RF_LAYERS.items()}
    tables["ResNet-50"] = rf_table(resnet50_layers())
    # the effective receptive field of the CIFAR network's last layer: |d unit / d input|, averaged over images
    from videos.ai.ai10 import nets

    c = cifar_u8()
    x = cifar_batch(c["xte"][:64]).requires_grad_(True)

    def erf(model):
        model.eval()
        a4 = model.maps(x)[3]  # (64, 128, 4, 4)
        a4[:, :, 2, 2].sum().backward()
        g = x.grad.abs().sum(1).mean(0).numpy()
        x.grad = None
        return g / g.max()

    trained = cifar_model()
    torch.manual_seed(12345)
    fresh = nets.CifarNet()
    out = dict(tables=tables, erf_trained=erf(trained), erf_untrained=erf(fresh))
    for key in ("erf_trained", "erf_untrained"):
        e = out[key]
        tot = e.sum()
        yy, xx = np.mgrid[:32, :32]
        cy, cx = (e * yy).sum() / tot, (e * xx).sum() / tot
        out[key + "_radius"] = float(np.sqrt((e * ((yy - cy) ** 2 + (xx - cx) ** 2)).sum() / tot))
    # LeNet's: one unit of C3 (16 maps of 10 x 10), the unit at (5, 5)
    model, _ = lenet_run(0)
    X = mnist_t()[2][:256].clone().requires_grad_(True)
    a1, a3 = model.maps(X)
    a3[:, :, 5, 5].sum().backward()
    g = X.grad.abs()[:, 0].mean(0).numpy()
    out["erf_lenet"] = g / g.max()
    out["dilated"] = dict(plain=[2 * L + 1 for L in range(1, 11)], dilated=[2 ** (L + 1) - 1 for L in range(1, 11)])
    return out


# ---------------------------------------------------------------------------
# The inductive bias: LeNet against an MLP of the same size
# ---------------------------------------------------------------------------
SHIFTS = (0, 1, 2, 3, 4, 5, 6)


def shifted_error(model, Xte, Yte, d: int) -> float:
    if d == 0:
        return 1.0 - accuracy(model, Xte, Yte)
    errs = [1.0 - accuracy(model, shift_images(Xte, dy, dx), Yte) for dy, dx in ((d, 0), (-d, 0), (0, d), (0, -d))]
    return float(np.mean(errs))


def mlp_run(seed: int, perm=None, epochs: int = LENET_EPOCHS):
    torch = _torch()
    import json

    from videos.ai.ai10 import nets

    tag = f"mlp_s{seed}" + ("_perm" if perm is not None else "") + (f"_e{epochs}" if epochs != LENET_EPOCHS else "")
    wpath, rpath = MODELS / f"{tag}.pt", MODELS / f"{tag}.json"
    torch.manual_seed(seed)
    model = nets.MLP(78)
    if wpath.exists() and rpath.exists():
        model.load_state_dict(torch.load(wpath, weights_only=False))
        return model, json.loads(rpath.read_text())
    X, Y, Xte, Yte = mnist_t()
    if perm is not None:
        X, Xte = permute(X, perm), permute(Xte, perm)
    st = train_mnist(model, seed, epochs, tag, X, Y, Xte, Yte)
    res = dict(test=st["test"], test_error=float(st["test"][-1][1]), params=nets.count(model))
    _save_torch(model.state_dict(), wpath)
    rpath.write_text(json.dumps(res))
    (MODELS / f"{tag}.ckpt").unlink(missing_ok=True)
    return model, res


def permute(X, perm):
    return X.flatten(1)[:, perm].view_as(X)


PERM_EPOCHS = 3


def compute_mlp_cnn():
    torch = _torch()
    import json

    from videos.ai.ai10 import nets

    X, Y, Xte, Yte = mnist_t()
    seeds = (0, 1, 2)
    out = dict(seeds=list(seeds), shifts=list(SHIFTS))
    cnn = [lenet_run(s) for s in seeds]
    mlp = [mlp_run(s) for s in seeds]
    out["params"] = dict(cnn=nets.count(cnn[0][0]), mlp=nets.count(mlp[0][0]))
    out["test"] = dict(cnn=[r["test"] for _, r in cnn], mlp=[r["test"] for _, r in mlp])
    out["error"] = dict(cnn=[r["test_error"] for _, r in cnn], mlp=[r["test_error"] for _, r in mlp])
    out["shifted"] = dict(cnn=[[shifted_error(m_, Xte, Yte, d) for d in SHIFTS] for m_, _ in cnn],
                          mlp=[[shifted_error(m_, Xte, Yte, d) for d in SHIFTS] for m_, _ in mlp])
    # shuffled pixels: one fixed permutation of the 784 positions, the same for training and test
    perm = torch.from_numpy(rng(1998).permutation(784))
    cp, mp = [], []
    for s in seeds:
        tag = f"lenet_perm_s{s}"
        rpath = MODELS / f"{tag}.json"
        if rpath.exists():
            cp.append(json.loads(rpath.read_text()))
        else:
            torch.manual_seed(s)
            model = nets.LeNet5()
            st = train_mnist(model, s, PERM_EPOCHS, tag, permute(X, perm), Y, permute(Xte, perm), Yte)
            r = dict(test=st["test"], test_error=float(st["test"][-1][1]))
            rpath.write_text(json.dumps(r))
            (MODELS / f"{tag}.ckpt").unlink(missing_ok=True)
            cp.append(r)
        mp.append(mlp_run(s, perm=perm, epochs=PERM_EPOCHS)[1])
    # the unshuffled runs after the same number of epochs, from their per-epoch test errors
    per_epoch = math.ceil(60000 / LENET_BATCH)
    at = lambda test: next(e for st_, e in test if st_ >= PERM_EPOCHS * per_epoch)  # noqa: E731
    out["perm_epochs"] = PERM_EPOCHS
    out["perm"] = dict(cnn=[r["test_error"] for r in cp], mlp=[r["test_error"] for r in mp],
                       cnn_plain=[at(r["test"]) for _, r in cnn], mlp_plain=[at(r["test"]) for _, r in mlp])
    d = mnist_t()[2][REPLAY_DIGIT, 0].numpy()
    out["perm_digit"] = d.flatten()[perm.numpy()].reshape(28, 28)
    out["digit"] = d
    for k in ("cnn", "mlp"):
        print(f"    {k}: {100 * np.mean(out['error'][k]):.2f}%; shuffled {100 * np.mean(out['perm'][k]):.2f}%",
              flush=True)
    return out


# ---------------------------------------------------------------------------
# Why AlexNet worked, in miniature: the activation, dropout, data
# ---------------------------------------------------------------------------
ACT_STEPS = 800


def compute_activations():
    torch = _torch()
    F = torch.nn.functional
    from videos.ai.ai10 import nets

    X, Y, Xte, Yte = mnist_t()
    part = CACHE.partial("activations", dict(steps=ACT_STEPS, v=1))
    for act in ("relu", "tanh", "sigmoid"):
        for seed in (0, 1, 2):
            key = f"{act}-{seed}"
            if key in part:
                continue
            torch.manual_seed(seed)
            model = nets.PlainCNN(act)
            for mod in model.modules():  # each activation with its usual initialization
                if isinstance(mod, (torch.nn.Conv2d, torch.nn.Linear)):
                    if act == "relu":
                        torch.nn.init.kaiming_normal_(mod.weight, nonlinearity="relu")
                    else:
                        torch.nn.init.xavier_normal_(mod.weight, gain=torch.nn.init.calculate_gain(act))
                    torch.nn.init.zeros_(mod.bias)
            opt = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
            g = rng(seed)
            curve, ema = [], None
            for step in range(1, ACT_STEPS + 1):
                ix = torch.from_numpy(g.integers(0, 60000, 64))
                logits = model(X[ix])
                loss = F.cross_entropy(logits, Y[ix])
                opt.zero_grad()
                loss.backward()
                opt.step()
                e = float((logits.argmax(1) != Y[ix]).float().mean())
                ema = e if ema is None else 0.95 * ema + 0.05 * e
                if step % 10 == 0:
                    curve.append([step, float(loss), ema])
            part[key] = dict(curve=curve, test_error=1.0 - accuracy(model, Xte, Yte))
            print(f"    {key}: test error {100 * part[key]['test_error']:.2f}%", flush=True)
    out = dict(steps=ACT_STEPS, runs={k: part[k] for k in part.done})
    # steps for the smoothed training error to fall below a threshold that ReLU and tanh both reach
    thr = 0.10
    reach = {}
    for k, r in out["runs"].items():
        c = np.asarray(r["curve"])
        hit = np.flatnonzero(c[:, 2] < thr)
        reach[k] = int(c[hit[0], 0]) if len(hit) else None
    out["threshold"], out["reach"] = thr, reach
    return out


DROP_N, DROP_EPOCHS = 5000, 60


def compute_dropout():
    torch = _torch()
    F = torch.nn.functional
    from videos.ai.ai10 import nets

    X, Y, Xte, Yte = mnist_t()
    idx = torch.from_numpy(rng(5000).permutation(60000)[:DROP_N])
    Xs, Ys = X[idx], Y[idx]
    part = CACHE.partial("dropout", dict(n=DROP_N, epochs=DROP_EPOCHS, v=1))
    for p in (0.0, 0.5):
        for seed in (0, 1, 2):
            key = f"{p}-{seed}"
            if key in part:
                continue
            torch.manual_seed(seed)
            model = nets.MLP(512, dropout=p, layers=2)
            opt = torch.optim.Adam(model.parameters(), lr=1e-3)
            g = rng(seed)
            rows = []
            for ep in range(1, DROP_EPOCHS + 1):
                order = torch.from_numpy(g.permutation(DROP_N))
                for i in range(0, DROP_N, 64):
                    ix = order[i:i + 64]
                    loss = F.cross_entropy(model(Xs[ix]), Ys[ix])
                    opt.zero_grad()
                    loss.backward()
                    opt.step()
                rows.append([ep, 1.0 - accuracy(model, Xs, Ys), 1.0 - accuracy(model, Xte, Yte)])
            part[key] = rows
            print(f"    dropout {key}: train {100 * rows[-1][1]:.2f}%, test {100 * rows[-1][2]:.2f}%", flush=True)
    return dict(n=DROP_N, epochs=DROP_EPOCHS, runs={k: part[k] for k in part.done})


DATA_SIZES = (500, 2000, 8000, 30000, 60000)
DATA_STEPS = 1200


def compute_datasize():
    torch = _torch()
    from videos.ai.ai10 import nets

    X, Y, Xte, Yte = mnist_t()
    order = torch.from_numpy(rng(2009).permutation(60000))
    part = CACHE.partial("datasize", dict(sizes=DATA_SIZES, steps=DATA_STEPS, v=1))
    for aug in (False, True):
        for n in DATA_SIZES:
            if aug and n > 8000:
                continue
            for seed in (0, 1, 2):
                key = f"{n}-{int(aug)}-{seed}"
                if key in part:
                    continue
                torch.manual_seed(seed)
                model = nets.LeNet5()
                tag = f"datasize_{key}"
                st = train_mnist(model, seed, 0, tag, X[order[:n]], Y[order[:n]], None, None, steps=DATA_STEPS,
                                 augment=aug)
                (MODELS / f"{tag}.ckpt").unlink(missing_ok=True)
                part[key] = dict(test_error=1.0 - accuracy(model, Xte, Yte), train_error=1.0 - accuracy(
                    model, X[order[:n]], Y[order[:n]]))
                print(f"    n={n} aug={aug} seed={seed}: {100 * part[key]['test_error']:.2f}%", flush=True)
    return dict(sizes=list(DATA_SIZES), steps=DATA_STEPS, runs={k: part[k] for k in part.done})


# ---------------------------------------------------------------------------
# AlexNet and VGG by the numbers, from their published architectures
# ---------------------------------------------------------------------------
def conv_row(name, cin, cout, k, out_hw, groups=1):
    params = cout * (k * k * cin // groups) + cout
    macs = out_hw * out_hw * cout * k * k * cin // groups
    return [name, params, macs]


def compute_alexnet():
    alex = [conv_row("conv1", 3, 96, 11, 55), conv_row("conv2", 96, 256, 5, 27, groups=2),
            conv_row("conv3", 256, 384, 3, 13), conv_row("conv4", 384, 384, 3, 13, groups=2),
            conv_row("conv5", 384, 256, 3, 13, groups=2),
            ["fc6", 9216 * 4096 + 4096, 9216 * 4096], ["fc7", 4096 * 4096 + 4096, 4096 * 4096],
            ["fc8", 4096 * 1000 + 1000, 4096 * 1000]]
    vgg, hw, cin = [], 224, 3
    for stage, (n, c) in enumerate(((2, 64), (2, 128), (3, 256), (3, 512), (3, 512)), start=1):
        for i in range(n):
            vgg.append(conv_row(f"conv{stage}_{i + 1}", cin, c, 3, hw))
            cin = c
        hw //= 2
    vgg += [["fc6", 25088 * 4096 + 4096, 25088 * 4096], ["fc7", 4096 * 4096 + 4096, 4096 * 4096],
            ["fc8", 4096 * 1000 + 1000, 4096 * 1000]]

    def summ(rows):
        p = sum(r[1] for r in rows)
        m = sum(r[2] for r in rows)
        pc = sum(r[1] for r in rows if r[0].startswith("conv"))
        mc = sum(r[2] for r in rows if r[0].startswith("conv"))
        return dict(params=p, macs=m, conv_param_share=pc / p, conv_mac_share=mc / m)

    # LeNet-5 as published (1998): C3's 60 of 96 connections (the partial table), the RBF output
    lenet98 = dict(C1=156, S2=12, C3=1516, S4=32, C5=48120, F6=10164, out=84 * 10)
    return dict(alexnet=alex, vgg16=vgg, alexnet_sum=summ(alex), vgg16_sum=summ(vgg), lenet98=lenet98,
                lenet98_total=sum(lenet98.values()))


# ---------------------------------------------------------------------------
# The CIFAR-10 network
# ---------------------------------------------------------------------------
CIFAR_EPOCHS = 10
CIFAR_BATCH = 128
CIFAR_SNAPS = (0, 20, 50, 100, 200, 400, 800, 1600, 2400, 3910)


def cifar_augment(x, g):
    """Random crops of the image padded by 4 pixels (reflected) and random horizontal flips."""
    torch = _torch()
    F = torch.nn.functional
    n = x.shape[0]
    p = F.pad(x, (4, 4, 4, 4), mode="reflect")
    oy, ox = g.integers(0, 9, n), g.integers(0, 9, n)
    flip = g.random(n) < 0.5
    out = torch.empty_like(x)
    for i in range(n):
        crop = p[i, :, oy[i]:oy[i] + 32, ox[i]:ox[i] + 32]
        out[i] = crop.flip(-1) if flip[i] else crop
    return out


def cifar_train():
    """Train the CIFAR network (resuming from its per-epoch checkpoint); return (model, results)."""
    torch = _torch()
    F = torch.nn.functional
    import json

    from videos.ai.ai10 import nets

    wpath, rpath, ck = MODELS / "cifar.pt", MODELS / "cifar.json", MODELS / "cifar.ckpt"
    torch.manual_seed(2012)
    model = nets.CifarNet()
    if wpath.exists() and rpath.exists():
        model.load_state_dict(torch.load(wpath, weights_only=False))
        model.eval()
        return model, json.loads(rpath.read_text())
    c = cifar_u8()
    n = len(c["ytr"])
    per_epoch = math.ceil(n / CIFAR_BATCH)
    total = CIFAR_EPOCHS * per_epoch
    decay = [p for nm, p in model.named_parameters() if p.dim() > 1]
    rest = [p for nm, p in model.named_parameters() if p.dim() <= 1]
    opt = torch.optim.SGD([dict(params=decay, weight_decay=5e-4), dict(params=rest, weight_decay=0.0)], lr=0.05,
                          momentum=0.9, nesterov=True)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=0.1, total_steps=total, pct_start=0.15)
    g = rng(2012)
    st = dict(step=0, curve=[], test=[], snaps={})
    test_x, test_y = c["xte"][:2000], c["yte"][:2000]

    def snap(step):
        return dict(w1=model.c1.weight.detach().numpy().tolist(), acc=cifar_accuracy(model, test_x, test_y))

    if ck.exists():
        s = torch.load(ck, weights_only=False)
        model.load_state_dict(s["model"])
        opt.load_state_dict(s["opt"])
        sched.load_state_dict(s["sched"])
        g.bit_generator.state = s["rng"]
        torch.set_rng_state(s["torch_rng"])
        st = s["state"]
        print(f"    resuming cifar at step {st['step']}", flush=True)
    else:
        st["snaps"][0] = snap(0)
    t0 = time.time() - st.get("seconds", 0.0)
    ytr = torch.from_numpy(c["ytr"].astype(np.int64))
    step = st["step"]
    while step < total:
        order = g.permutation(n)
        for i in range(0, n, CIFAR_BATCH):
            ix = order[i:i + CIFAR_BATCH]
            x = cifar_augment(cifar_batch(c["xtr"][ix]), g)
            logits = model(x)
            loss = F.cross_entropy(logits, ytr[ix])
            opt.zero_grad()
            loss.backward()
            opt.step()
            sched.step()
            step += 1
            if step % 10 == 0:
                st["curve"].append([step, float(loss), float((logits.argmax(1) != ytr[ix]).float().mean())])
            if step in CIFAR_SNAPS:
                st["snaps"][step] = snap(step)
            if step % 100 == 0:
                print(f"    cifar step {step}/{total} loss {float(loss):.3f} "
                      f"({(time.time() - t0) / max(step, 1):.2f}s/step)", flush=True)
        st["test"].append([step, cifar_accuracy(model, c["xte"], c["yte"])])
        st["step"], st["seconds"] = step, time.time() - t0
        print(f"    cifar epoch {step // per_epoch}: test accuracy {100 * st['test'][-1][1]:.1f}%", flush=True)
        _save_torch(dict(model=model.state_dict(), opt=opt.state_dict(), sched=sched.state_dict(),
                         rng=g.bit_generator.state, torch_rng=torch.get_rng_state(), state=st), ck)
    res = dict(curve=st["curve"], test=st["test"], snaps={str(k): v for k, v in st["snaps"].items()},
               seconds=st["seconds"], params=nets.count(model), total_steps=total)
    _save_torch(model.state_dict(), wpath)
    rpath.write_text(json.dumps(res))
    ck.unlink(missing_ok=True)
    model.eval()
    return model, res


def cifar_model():
    return cifar_train()[0]


def compute_cifar():
    _, r = cifar_train()
    steps = sorted(int(k) for k in r["snaps"])
    return dict(params=r["params"], epochs=CIFAR_EPOCHS, batch=CIFAR_BATCH, total_steps=r["total_steps"],
                curve=np.asarray(r["curve"]), test=r["test"], test_acc=float(r["test"][-1][1]),
                seconds=r["seconds"], steps=steps, w1=np.asarray([r["snaps"][str(s)]["w1"] for s in steps]),
                snap_acc=[r["snaps"][str(s)]["acc"] for s in steps])


# ---------------------------------------------------------------------------
# Hubel and Wiesel's experiment, on our filters
# ---------------------------------------------------------------------------
N_ORI = 16


def gratings(size: int, freqs, n_ori: int = N_ORI, n_phase: int = 8) -> np.ndarray:
    """Sinusoidal gratings (luminance), (n_ori, n_freq, n_phase, size, size), unit RMS."""
    yy, xx = np.mgrid[:size, :size] - (size - 1) / 2
    out = np.zeros((n_ori, len(freqs), n_phase, size, size))
    for a in range(n_ori):
        th = math.pi * a / n_ori
        u = xx * math.cos(th) + yy * math.sin(th)
        for b, f in enumerate(freqs):
            for c in range(n_phase):
                out[a, b, c] = math.sqrt(2) * np.cos(2 * math.pi * f * u + 2 * math.pi * c / n_phase)
    return out


def tuning(filters: np.ndarray, colour: bool) -> dict:
    """Each filter's best response to a grating at each orientation (over frequency and phase); the orientation
    selectivity index (R_pref - R_orth) / (R_pref + R_orth); and, for colour filters, how much of the filter is
    'colour' (the part that differs between channels) rather than 'luminance'."""
    k = filters.shape[-1]
    G = gratings(k, freqs=(1 / 8, 1 / 6, 1 / 4.5, 1 / 3.5, 1 / 2.5))
    W = filters if colour else filters[:, None]
    lum = W.mean(1)  # the luminance part of each filter (gratings are the same in every channel)
    resp = np.einsum("nyx,abcyx->nabc", lum * W.shape[1], G)
    R = resp.max(axis=(2, 3))  # (n, orientations)
    R = np.maximum(R, 0)
    pref = R.argmax(1)
    orth = (pref + N_ORI // 2) % N_ORI
    rp, ro = R[np.arange(len(R)), pref], R[np.arange(len(R)), orth]
    osi = (rp - ro) / (rp + ro + 1e-9)
    out = dict(R=R, pref_deg=(180.0 * pref / N_ORI), osi=osi)
    if colour:
        chroma = W - lum[:, None]
        out["colour_share"] = (chroma ** 2).sum((1, 2, 3)) / ((W ** 2).sum((1, 2, 3)) + 1e-12)
    return out


def compute_orientation():
    torch = _torch()
    from videos.ai.ai10 import nets

    model = cifar_model()
    W = model.c1.weight.detach().numpy()
    torch.manual_seed(2012)  # the same initialization the training started from
    W0 = nets.CifarNet().c1.weight.detach().numpy()
    t, t0 = tuning(W, True), tuning(W0, True)
    lw = lenet_run(0)[0].c1.weight.detach().numpy()[:, 0]
    tl = tuning(lw, False)
    sel = 0.5
    oriented = (t["osi"] >= sel) & (t["colour_share"] < 0.5)
    colour = t["colour_share"] >= 0.5
    order = np.argsort(-t["osi"] * (1 - t["colour_share"]))
    return dict(n=int(len(W)), R=t["R"], osi=t["osi"], pref_deg=t["pref_deg"], colour_share=t["colour_share"],
                R0=t0["R"], osi0=t0["osi"], colour_share0=t0["colour_share"], selective=sel,
                n_oriented=int(oriented.sum()), n_colour=int(colour.sum()),
                n_oriented0=int(((t0["osi"] >= sel) & (t0["colour_share"] < 0.5)).sum()),
                n_colour0=int((t0["colour_share"] >= 0.5).sum()), best=order[:6].tolist(),
                median_osi=float(np.median(t["osi"])), median_osi0=float(np.median(t0["osi"])),
                lenet_osi=tl["osi"], lenet_R=tl["R"], w1=W, w0=W0, angles=(180.0 * np.arange(N_ORI) / N_ORI))


# ---------------------------------------------------------------------------
# Deeper features of the CIFAR network
# ---------------------------------------------------------------------------
def compute_filters():
    torch = _torch()
    F = torch.nn.functional
    model = cifar_model()
    c = cifar_u8()
    X = c["xte"]
    acts3, acts4 = [], []
    with torch.no_grad():
        for i in range(0, len(X), 500):
            _, _, a3, a4 = model.maps(cifar_batch(X[i:i + 500]))
            acts3.append(a3.numpy())
            acts4.append(a4.mean((2, 3)).numpy())
    a3 = np.concatenate(acts3)  # (10000, 128, 8, 8)
    a4 = np.concatenate(acts4)  # (10000, 128)
    # layer 3 (receptive field 21 pixels): for 12 channels, the 9 image patches that excite them most
    peak = a3.reshape(len(X), 128, -1).max(2)
    spread = peak.max(0) / (peak.mean(0) + 1e-6)
    chans3 = np.argsort(-spread)[:12].tolist()
    pad = np.pad(X, ((0, 0), (10, 10), (10, 10), (0, 0)), mode="constant")
    patches3 = []
    for ch in chans3:
        flat = a3[:, ch].reshape(len(X), -1)
        best = np.argsort(-flat.max(1))[:9]
        row = []
        for i in best:
            p = int(flat[i].argmax())
            y, x = divmod(p, 8)
            cy, cx = 4 * y + 2, 4 * x + 2  # the unit's centre in the image (jump 4)
            row.append(pad[i, cy + 10 - 10:cy + 10 + 11, cx + 10 - 10:cx + 10 + 11])
        patches3.append(row)
    # layer 4 (sees the whole image): the 6 images that excite each of 8 channels most, and their classes
    spread4 = a4.max(0) / (a4.mean(0) + 1e-6)
    chans4 = np.argsort(-spread4)[:8].tolist()
    top4 = [np.argsort(-a4[:, ch])[:6].tolist() for ch in chans4]
    imgs4 = np.asarray([[X[i] for i in row] for row in top4])
    cls4 = [[int(c["yte"][i]) for i in row] for row in top4]
    # what the network 'wants' for each class: gradient ascent on the class score from a grey image, with jitter,
    # blur and a small penalty on the pixels (Simonyan et al. 2013; Olah et al. 2017)
    dreams = []
    for k in range(10):
        g = torch.Generator().manual_seed(k)
        x = (0.5 + 0.02 * torch.randn(1, 3, 32, 32, generator=g)).requires_grad_(True)
        opt = torch.optim.Adam([x], lr=0.02)
        for it in range(300):
            dy, dx = (int(v) for v in torch.randint(-2, 3, (2,), generator=g))
            xj = torch.roll(x, (dy, dx), (2, 3))
            score = model(xj.clamp(0, 1))[0, k] - 0.05 * ((x - 0.5) ** 2).sum()
            opt.zero_grad()
            (-score).backward()
            opt.step()
            if it % 4 == 3:
                with torch.no_grad():
                    x.copy_(F.avg_pool2d(F.pad(x, (1, 1, 1, 1), mode="replicate"), 3, 1) * 0.3 + x * 0.7)
        with torch.no_grad():
            p = model(x.clamp(0, 1)).softmax(1)[0, k]
        dreams.append(dict(img=x.detach().clamp(0, 1)[0].permute(1, 2, 0).numpy(), p=float(p)))
    # saliency: which pixels the class score is most sensitive to
    sal_ix = [int(np.flatnonzero(c["yte"] == k)[0]) for k in (0, 3, 6, 7, 8, 9)]
    sal = []
    for i in sal_ix:
        x = cifar_batch(X[i:i + 1]).requires_grad_(True)
        lo = model(x)
        k = int(c["yte"][i])
        lo[0, k].backward()
        s = x.grad.abs().amax(1)[0].numpy()
        sal.append(dict(img=X[i], sal=s / s.max(), label=k, pred=int(lo.argmax()),
                        p=float(lo.softmax(1)[0, k])))
    # one photograph through the layers
    k = int(np.flatnonzero(c["yte"] == 8)[1])  # a ship
    with torch.no_grad():
        m1, m2, m3, m4 = model.maps(cifar_batch(X[k:k + 1]))
    return dict(chans3=chans3, patches3=np.asarray(patches3), chans4=chans4, imgs4=imgs4, cls4=cls4,
                dreams=np.asarray([d["img"] for d in dreams]), dream_p=[d["p"] for d in dreams],
                sal_img=np.asarray([s["img"] for s in sal]), sal=np.asarray([s["sal"] for s in sal]),
                sal_label=[s["label"] for s in sal], sal_pred=[s["pred"] for s in sal], sal_p=[s["p"] for s in sal],
                photo=X[k], photo_label=8, maps1=m1[0, :16].numpy(), maps2=m2[0, :16].numpy(),
                maps3=m3[0, :16].numpy(), maps4=m4[0, :16].numpy())


# ---------------------------------------------------------------------------
# Adversarial examples
# ---------------------------------------------------------------------------
EPS = (0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3)


def fgsm(model, x, y, eps):
    torch = _torch()
    x = x.clone().requires_grad_(True)
    loss = torch.nn.functional.cross_entropy(model(x), y)
    g, = torch.autograd.grad(loss, x)
    return (x + eps * g.sign()).clamp(0, 1).detach()


def pgd(model, x, y, eps, steps: int = 20, alpha=None, seed: int = 0):
    torch = _torch()
    alpha = alpha or 2.5 * eps / steps
    gen = torch.Generator().manual_seed(seed)
    d = (torch.rand(x.shape, generator=gen) * 2 - 1) * eps
    xa = (x + d).clamp(0, 1)
    for _ in range(steps):
        xa.requires_grad_(True)
        loss = torch.nn.functional.cross_entropy(model(xa), y)
        g, = torch.autograd.grad(loss, xa)
        xa = (x + (xa.detach() + alpha * g.sign() - x).clamp(-eps, eps)).clamp(0, 1)
    return xa.detach()


def attack_error(model, X, Y, eps, kind="fgsm", batch=1000, source=None):
    """Error of ``model`` on attacked test images (made against ``source``, by default the model itself), and the
    mean probability it gives its (wrong) answers."""
    torch = _torch()
    model.eval()
    src = source or model
    wrong, conf = 0, []
    for i in range(0, len(X), batch):
        x, y = X[i:i + batch], Y[i:i + batch]
        xa = x if eps == 0 else (fgsm(src, x, y, eps) if kind == "fgsm" else pgd(src, x, y, eps))
        with torch.no_grad():
            p = model(xa).softmax(1)
        bad = p.argmax(1) != y
        wrong += int(bad.sum())
        conf += p.max(1).values[bad].tolist()
    return wrong / len(X), (float(np.mean(conf)) if conf else 0.0)


def linear_model():
    torch = _torch()
    import json

    from videos.ai.ai10 import nets

    wpath, rpath = MODELS / "linear.pt", MODELS / "linear.json"
    torch.manual_seed(0)
    model = nets.Linear(784)
    if wpath.exists():
        model.load_state_dict(torch.load(wpath, weights_only=False))
        return model
    X, Y, Xte, Yte = mnist_t()
    st = train_mnist(model, 0, 5, "linear", X, Y, Xte, Yte)
    _save_torch(model.state_dict(), wpath)
    rpath.write_text(json.dumps(dict(test=st["test"])))
    (MODELS / "linear.ckpt").unlink(missing_ok=True)
    return model


def compute_adversarial():
    torch = _torch()
    X, Y, Xte, Yte = mnist_t()
    lin = linear_model()
    lenets = [lenet_run(s)[0].eval() for s in (0, 1, 2)]
    mlps = [mlp_run(s)[0].eval() for s in (0, 1, 2)]
    out = dict(eps=list(EPS))
    out["fgsm"] = dict(linear=[attack_error(lin, Xte, Yte, e)[0] for e in EPS],
                       mlp=[[attack_error(m, Xte, Yte, e)[0] for e in EPS] for m in mlps],
                       lenet=[[attack_error(m, Xte, Yte, e)[0] for e in EPS] for m in lenets])
    out["fgsm_conf"] = dict(linear=attack_error(lin, Xte, Yte, 0.25)[1], lenet=attack_error(lenets[0], Xte, Yte,
                                                                                              0.25)[1])
    sub = slice(0, 2000)
    out["pgd"] = dict(lenet=[[attack_error(m, Xte[sub], Yte[sub], e, "pgd")[0] for e in EPS] for m in lenets[:1]])
    e_t = 0.2
    out["transfer_eps"] = e_t
    out["transfer"] = dict(
        mlp_to_lenet=attack_error(lenets[0], Xte, Yte, e_t, source=mlps[0])[0],
        lenet_to_mlp=attack_error(mlps[0], Xte, Yte, e_t, source=lenets[0])[0],
        lenet_to_lenet=attack_error(lenets[1], Xte, Yte, e_t, source=lenets[0])[0],
        linear_to_lenet=attack_error(lenets[0], Xte, Yte, e_t, source=lin)[0])
    # one digit: the attack, and the logits all along the attack direction (Goodfellow et al.'s figure 4)
    i = REPLAY_DIGIT
    x, y = Xte[i:i + 1], Yte[i:i + 1]
    m = lenets[0]
    xx = x.clone().requires_grad_(True)
    gsign, = torch.autograd.grad(torch.nn.functional.cross_entropy(m(xx), y), xx)
    gsign = gsign.sign()
    es = np.linspace(-0.5, 0.5, 101)
    with torch.no_grad():
        logits = torch.cat([m((x + float(e) * gsign).clamp(0, 1)) for e in es]).numpy()
        logits_noclamp = torch.cat([m(x + float(e) * gsign) for e in es]).numpy()
        steps = []
        for e in (0.0, 0.1, 0.2, 0.3):
            p = m((x + e * gsign).clamp(0, 1)).softmax(1)[0]
            steps.append(dict(eps=e, pred=int(p.argmax()), p=float(p.max()), p_true=float(p[y])))
    # the linear model's arithmetic: the score gap it must close, and how fast eps closes it (eps times an L1 norm)
    W = lin.lin.weight.detach().numpy()
    with torch.no_grad():
        z = lin(Xte).numpy()
    yt = Yte.numpy()
    zs = np.sort(z, 1)
    gap = z[np.arange(len(z)), yt] - np.where(z.argmax(1) == yt, zs[:, -2], zs[:, -1])
    runner = np.argsort(-z, 1)[:, :2]
    other = np.where(runner[:, 0] == yt, runner[:, 1], runner[:, 0])
    l1 = np.abs(W[yt] - W[other]).sum(1)
    right = gap > 0
    need = gap[right] / l1[right]
    # the same picture for a photograph: CIFAR at a few eps (in steps of 1/255, the smallest change of a pixel)
    cm = cifar_model()
    c = cifar_u8()
    cx = cifar_batch(c["xte"][:2000])
    cy = torch.from_numpy(c["yte"][:2000].astype(np.int64))
    ceps = (0.0, 0.5, 1.0, 2.0, 4.0, 8.0)
    out["cifar_eps"] = list(ceps)
    out["cifar_fgsm"] = [attack_error(cm, cx, cy, e / 255, batch=500)[0] for e in ceps]
    out["cifar_pgd"] = [attack_error(cm, cx, cy, e / 255, "pgd", batch=500)[0] for e in ceps]
    ex = []
    with torch.no_grad():
        pc = cm(cx[:200]).softmax(1)
    for j in range(200):
        if len(ex) == 4:
            break
        if int(pc[j].argmax()) != int(cy[j]) or float(pc[j].max()) < 0.9:
            continue
        xa = pgd(cm, cx[j:j + 1], cy[j:j + 1], 2 / 255)
        with torch.no_grad():
            pa = cm(xa).softmax(1)[0]
        if int(pa.argmax()) == int(cy[j]):
            continue
        ex.append(dict(img=c["xte"][j], adv=(xa[0].permute(1, 2, 0).numpy() * 255).round().astype(np.uint8),
                       label=int(cy[j]), p=float(pc[j].max()), pred=int(pa.argmax()), p_adv=float(pa.max())))
    out.update(digit=x[0, 0].numpy(), sign=gsign[0, 0].numpy(), digit_label=int(y), digit_steps=steps,
               line_eps=es, line_logits=logits, line_logits_noclamp=logits_noclamp,
               linear_gap_median=float(np.median(gap[right])), linear_l1_median=float(np.median(l1)),
               linear_need_median=float(np.median(need)), linear_need_q90=float(np.quantile(need, 0.9)),
               cifar_ex_img=np.asarray([e["img"] for e in ex]), cifar_ex_adv=np.asarray([e["adv"] for e in ex]),
               cifar_ex=[{k: v for k, v in e.items() if k not in ("img", "adv")} for e in ex])
    return out


ADV_EPS, ADV_EPOCHS = 0.2, 3


def compute_advtrain():
    torch = _torch()
    F = torch.nn.functional
    from videos.ai.ai10 import nets

    X, Y, Xte, Yte = mnist_t()
    part = CACHE.partial("advtrain", dict(eps=ADV_EPS, epochs=ADV_EPOCHS, v=1))
    for seed in (0, 1, 2):
        key = str(seed)
        if key in part:
            continue
        torch.manual_seed(seed)
        model = nets.LeNet5()
        opt = torch.optim.Adam(model.parameters(), lr=1e-3)
        g = rng(seed)
        gen = torch.Generator().manual_seed(seed)
        curve, step = [], 0
        for ep in range(ADV_EPOCHS):
            order = torch.from_numpy(g.permutation(60000))
            for i in range(0, 60000, LENET_BATCH):
                ix = order[i:i + LENET_BATCH]
                x, y = X[ix], Y[ix]
                # fast FGSM with a random start (Wong, Rice & Kolter 2020), mixed half and half with clean digits
                d = ((torch.rand(x.shape, generator=gen) * 2 - 1) * ADV_EPS).requires_grad_(True)
                lg = F.cross_entropy(model((x + d).clamp(0, 1)), y)
                gd, = torch.autograd.grad(lg, d)
                d = (d + 1.25 * ADV_EPS * gd.sign()).clamp(-ADV_EPS, ADV_EPS).detach()
                xa = (x + d).clamp(0, 1)
                loss = 0.5 * F.cross_entropy(model(x), y) + 0.5 * F.cross_entropy(model(xa), y)
                opt.zero_grad()
                loss.backward()
                opt.step()
                step += 1
                if step % 100 == 0 or step == 1:
                    model.eval()
                    ce = 1.0 - accuracy(model, Xte[:1000], Yte[:1000])
                    ae = attack_error(model, Xte[:1000], Yte[:1000], ADV_EPS)[0]
                    model.train()
                    curve.append([step, ce, ae])
        model.eval()
        part[key] = dict(curve=curve, clean=1.0 - accuracy(model, Xte, Yte),
                         fgsm=[attack_error(model, Xte, Yte, e)[0] for e in EPS],
                         pgd=[attack_error(model, Xte[:2000], Yte[:2000], e, "pgd")[0] for e in EPS])
        print(f"    advtrain seed {seed}: clean {100 * part[key]['clean']:.2f}%, fgsm@0.2 "
              f"{100 * part[key]['fgsm'][4]:.1f}%, pgd@0.2 {100 * part[key]['pgd'][4]:.1f}%", flush=True)
    # the same curve for ordinary training (seed 0, its first epochs), for comparison
    return dict(eps=ADV_EPS, epochs=ADV_EPOCHS, eps_grid=list(EPS), runs={k: part[k] for k in part.done})


# ---------------------------------------------------------------------------
# Cheaper convolutions
# ---------------------------------------------------------------------------
def compute_depthwise():
    torch = _torch()
    F = torch.nn.functional

    def best(fn, reps=7):
        fn()
        ts = []
        for _ in range(reps):
            t = time.perf_counter()
            fn()
            ts.append(time.perf_counter() - t)
        return min(ts)

    rows = []
    g = torch.Generator().manual_seed(0)
    hw = 28
    for C in (32, 64, 128, 256, 512):
        x = torch.randn(8, C, hw, hw, generator=g)
        w = torch.randn(C, C, 3, 3, generator=g) * 0.05
        wd = torch.randn(C, 1, 3, 3, generator=g) * 0.3
        wp = torch.randn(C, C, 1, 1, generator=g) * 0.05
        with torch.no_grad():
            t_std = best(lambda: F.conv2d(x, w, padding=1))
            t_dw = best(lambda: F.conv2d(x, wd, padding=1, groups=C))
            t_pw = best(lambda: F.conv2d(x, wp))
        macs_std = 8 * hw * hw * C * C * 9
        macs_dw, macs_pw = 8 * hw * hw * C * 9, 8 * hw * hw * C * C
        rows.append(dict(C=C, t_std=t_std, t_dw=t_dw, t_pw=t_pw, macs_std=macs_std, macs_dw=macs_dw, macs_pw=macs_pw,
                         flop_ratio=(macs_dw + macs_pw) / macs_std, time_ratio=(t_dw + t_pw) / t_std,
                         gflops_std=2 * macs_std / t_std / 1e9, gflops_dw=2 * macs_dw / t_dw / 1e9,
                         gflops_pw=2 * macs_pw / t_pw / 1e9))
        print(f"    C={C}: FLOPs x{rows[-1]['flop_ratio']:.3f}, time x{rows[-1]['time_ratio']:.3f}", flush=True)
    return dict(rows=rows, hw=hw, batch=8, threads=THREADS, loadavg=list(os.getloadavg()))


# ---------------------------------------------------------------------------
# Gradients through time
# ---------------------------------------------------------------------------
RHOS = (0.8, 1.0, 1.25, 2.0)


def compute_rnn_grad():
    n, n_in, T, K, draws = 100, 10, 160, 100, 20
    out = dict(rhos=list(RHOS), K=K, n=n)
    for kind in ("tanh", "linear"):
        med, lo, hi, bound = [], [], [], []
        for rho in RHOS:
            logs, bounds = [], []
            for d in range(draws):
                g = rng(1000 * d + int(100 * rho))
                W = g.normal(0, 1 / math.sqrt(n), (n, n))
                W *= rho / np.abs(np.linalg.eigvals(W)).max()
                U = g.normal(0, 1 / math.sqrt(n_in), (n, n_in))
                h = np.zeros(n)
                hs = []
                for t in range(T):
                    pre = W @ h + U @ g.normal(0, 1, n_in)
                    h = np.tanh(pre) if kind == "tanh" else pre
                    hs.append(h)
                P = np.eye(n)
                row = [0.0]
                smax = np.linalg.norm(W, 2)
                for k in range(1, K + 1):
                    hk = hs[T - k]
                    J = (1 - hk ** 2)[:, None] * W if kind == "tanh" else W
                    P = P @ J
                    row.append(math.log10(max(np.linalg.norm(P, 2), 1e-300)))
                logs.append(row)
                bounds.append([k * math.log10(smax) for k in range(K + 1)])
            logs = np.asarray(logs)
            med.append(np.median(logs, 0))
            lo.append(np.quantile(logs, 0.1, 0))
            hi.append(np.quantile(logs, 0.9, 0))
            bound.append(np.median(np.asarray(bounds), 0))
        out[kind] = dict(median=np.asarray(med), lo=np.asarray(lo), hi=np.asarray(hi), bound=np.asarray(bound))
    # a one-unit RNN, h_t = tanh(w h_{t-1} + b) from h_0 = 0.5 for 50 steps, loss (h_50 - 0.7)^2: the cliff
    # (after Pascanu, Mikolov & Bengio 2013), and gradient descent from one point near it, with and without clipping

    def run(w, b, T=50, h0=0.5):
        h = np.full(np.broadcast(w, b).shape, h0, float)
        gw = np.zeros_like(h)
        gb = np.zeros_like(h)
        for _ in range(T):
            hn = np.tanh(w * h + b)
            dd = 1 - hn ** 2
            gw = dd * (h + w * gw)
            gb = dd * (1 + w * gb)
            h = hn
        return (h - 0.7) ** 2, 2 * (h - 0.7) * gw, 2 * (h - 0.7) * gb

    ws, bs = np.linspace(-1, 4, 201), np.linspace(-3, 1, 161)
    Wg, Bg = np.meshgrid(ws, bs)
    L, GW, GB = run(Wg, Bg)

    def descend(w, b, lr, steps, clip=None):
        path, norms = [(w, b)], []
        for _ in range(steps):
            _, gw, gb = run(w, b)
            nrm = math.hypot(gw, gb)
            norms.append(nrm)
            if clip and nrm > clip:
                gw, gb = gw * clip / nrm, gb * clip / nrm
            w, b = w - lr * gw, b - lr * gb
            path.append((w, b))
        return np.asarray(path), norms

    start, lr = (2.4, -0.4), 0.5
    p_raw, n_raw = descend(*start, lr, 40)
    p_clip, n_clip = descend(*start, lr, 40, clip=1.0)
    out["cliff"] = dict(ws=ws, bs=bs, loss=L, grad=np.hypot(GW, GB), start=list(start), lr=lr, clip=1.0,
                        path_raw=p_raw, path_clip=p_clip, norm_raw=n_raw, norm_clip=n_clip,
                        loss_raw=[float(run(w, b)[0]) for w, b in p_raw], loss_clip=[float(run(w, b)[0])
                                                                                    for w, b in p_clip])
    return out


# ---------------------------------------------------------------------------
# The memory task: RNN, LSTM, GRU, minGRU
# ---------------------------------------------------------------------------
MEM_T = (10, 30, 100)
MEM_STEPS = {10: 500, 30: 1000, 100: 1200}
MEM_CELLS = ("rnn", "lstm", "gru", "mingru")
MEM_SYMBOLS = 8


def memory_batch(g, B, T):
    """First token: the symbol to remember (marked, 8-15); then T - 2 distractors (0-7); last: the query (16)."""
    s = g.integers(0, MEM_SYMBOLS, B)
    x = g.integers(0, MEM_SYMBOLS, (B, T))
    x[:, 0] = s + MEM_SYMBOLS
    x[:, -1] = 2 * MEM_SYMBOLS
    return x, s


def compute_memory():
    torch = _torch()
    F = torch.nn.functional
    from videos.ai.ai10 import nets

    part = CACHE.partial("memory", dict(T=MEM_T, steps=MEM_STEPS, cells=MEM_CELLS, v=1))
    for T in MEM_T:
        tx, ts = memory_batch(rng(777), 1024, T)
        tx, ts = torch.from_numpy(tx), torch.from_numpy(ts)
        for cell in MEM_CELLS:
            for seed in (0, 1, 2):
                key = f"{cell}-{T}-{seed}"
                if key in part:
                    continue
                torch.manual_seed(seed)
                model = nets.SeqClassifier(cell, 2 * MEM_SYMBOLS + 1, MEM_SYMBOLS)
                opt = torch.optim.Adam(model.parameters(), lr=2e-3)
                g = rng(seed)
                curve, prof = [], []
                t0 = time.time()
                for step in range(MEM_STEPS[T] + 1):
                    if step % 50 == 0:
                        model.eval()
                        with torch.no_grad():
                            acc = float((model(tx).argmax(1) == ts).float().mean())
                        curve.append([step, acc])
                        if step % 200 == 0 and seed == 0:
                            lo = model(tx[:256], keep_inputs=True)
                            F.cross_entropy(lo, ts[:256]).backward()
                            gn = model.inputs.grad.norm(dim=-1).mean(0).numpy()
                            prof.append([step] + gn.tolist())
                            model.zero_grad()
                        model.train()
                    if step == MEM_STEPS[T]:
                        break
                    x, s = memory_batch(g, 64, T)
                    loss = F.cross_entropy(model(torch.from_numpy(x)), torch.from_numpy(s))
                    opt.zero_grad()
                    loss.backward()
                    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                    opt.step()
                part[key] = dict(curve=curve, profile=prof, final=curve[-1][1], params=nets.count(model),
                                 seconds=time.time() - t0)
                print(f"    memory {key}: accuracy {100 * curve[-1][1]:.1f}% ({time.time() - t0:.0f}s)", flush=True)
    return dict(T=list(MEM_T), steps={str(k): v for k, v in MEM_STEPS.items()}, cells=list(MEM_CELLS),
                chance=1 / MEM_SYMBOLS, runs={k: part[k] for k in part.done})


# ---------------------------------------------------------------------------
# The character LSTM on the thirty novels
# ---------------------------------------------------------------------------
LSTM_H, LSTM_EMB, LSTM_B, LSTM_T, LSTM_STEPS = 512, 64, 64, 128, 2400
LSTM_SNAPS = (0, 100, 200, 400, 800, 1600, 2400)
LSTM_PROMPT = "Spade sat down in the armchair, and "  # Part 9's prompt


def novels():
    """Part 1's texts and the character table (as Part 9 builds it: every character of train, valid and passage)."""
    from videos.ai.ai1 import compute as c1

    texts = {k: c1.text(k) for k in ("train", "valid", "passage")}
    chars = sorted(set("".join(texts.values())))
    cp = np.array([ord(ch) for ch in chars])

    def enc(t):
        a = np.frombuffer(t.encode("utf-32-le"), dtype=np.uint32)
        return np.searchsorted(cp, a).astype(np.int64)

    return texts, chars, enc


def lstm_bits(model, seq: np.ndarray, streams: int = 1) -> float:
    """Bits per character over ``seq``, read in ``streams`` contiguous pieces, each from a zero state."""
    torch = _torch()
    model.eval()
    n = (len(seq) - 1) // streams * streams
    x = torch.from_numpy(seq[:n].reshape(streams, -1))
    y = torch.from_numpy(seq[1:n + 1].reshape(streams, -1))
    with torch.no_grad():
        lo, _ = model(x)
        nats = float(torch.nn.functional.cross_entropy(lo.flatten(0, 1), y.flatten(), reduction="sum"))
    model.train()
    return nats / y.numel() / math.log(2)


def lstm_sample(model, enc, chars, prompt: str, n: int, seed: int, temperature: float = 1.0) -> str:
    torch = _torch()
    model.eval()
    g = torch.Generator().manual_seed(seed)
    with torch.no_grad():
        lo, st = model(torch.from_numpy(enc(prompt))[None])
        out = []
        z = lo[0, -1]
        for _ in range(n):
            c = int(torch.multinomial((z / temperature).softmax(0), 1, generator=g))
            out.append(chars[c])
            lo, st = model(torch.tensor([[c]]), st)
            z = lo[0, -1]
    model.train()
    return "".join(out)


def charlstm_train():
    torch = _torch()
    F = torch.nn.functional
    import json

    from videos.ai.ai10 import nets

    wpath, rpath, ck = MODELS / "charlstm.pt", MODELS / "charlstm.json", MODELS / "charlstm.ckpt"
    texts, chars, enc = novels()
    K = len(chars)
    torch.manual_seed(1997)  # Hochreiter & Schmidhuber
    model = nets.CharLSTM(K, LSTM_H, LSTM_EMB)
    if wpath.exists() and rpath.exists():
        model.load_state_dict(torch.load(wpath, weights_only=False))
        return model, json.loads(rpath.read_text()), (texts, chars, enc)
    tr = enc(texts["train"])
    ps = enc(texts["passage"])
    va = enc(texts["valid"])[:200_000]
    per = len(tr) // LSTM_B
    streams = tr[:per * LSTM_B].reshape(LSTM_B, per)  # 64 contiguous readers, each through its own stretch of books
    opt = torch.optim.Adam(model.parameters(), lr=2e-3)

    def lr_at(step):
        if step < 100:
            return 2e-3 * (step + 1) / 100
        t = (step - 100) / max(1, LSTM_STEPS - 100)
        return 2e-4 + (2e-3 - 2e-4) * 0.5 * (1 + math.cos(math.pi * t))

    st = dict(step=0, curve=[], evals=[], snaps={}, clipped=0, seconds=0.0)
    state = None
    if ck.exists():
        s = torch.load(ck, weights_only=False)
        model.load_state_dict(s["model"])
        opt.load_state_dict(s["opt"])
        torch.set_rng_state(s["torch_rng"])
        state, st = s["hidden"], s["state"]
        print(f"    resuming charlstm at step {st['step']}", flush=True)
    t0 = time.time() - st["seconds"]
    step = st["step"]
    if step == 0:
        st["evals"].append([0, lstm_bits(model, ps), lstm_bits(model, va, 32)])
        st["snaps"]["0"] = lstm_sample(model, enc, chars, LSTM_PROMPT, 200, 1)
    while step < LSTM_STEPS:
        for gq in opt.param_groups:
            gq["lr"] = lr_at(step)
        a = step * LSTM_T
        x = torch.from_numpy(streams[:, a:a + LSTM_T])
        y = torch.from_numpy(streams[:, a + 1:a + LSTM_T + 1])
        lo, state = model(x, state)
        state = tuple(s_.detach() for s_ in state)  # truncated backpropagation through time: carry the state on
        loss = F.cross_entropy(lo.flatten(0, 1), y.flatten())
        opt.zero_grad()
        loss.backward()
        gn = float(torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0))
        st["clipped"] += int(gn > 1.0)
        opt.step()
        step += 1
        if step % 10 == 0:
            st["curve"].append([step, float(loss) / math.log(2), gn])
        if step % 100 == 0:
            st["evals"].append([step, lstm_bits(model, ps), lstm_bits(model, va, 32) if step % 400 == 0 else None])
            print(f"    charlstm step {step}/{LSTM_STEPS}: train {float(loss) / math.log(2):.3f}  passage "
                  f"{st['evals'][-1][1]:.3f} bits/char ({(time.time() - t0) / step:.2f}s/step)", flush=True)
        if step in LSTM_SNAPS:
            st["snaps"][str(step)] = lstm_sample(model, enc, chars, LSTM_PROMPT, 200, 1)
        if step % 100 == 0 or step == LSTM_STEPS:
            st["step"], st["seconds"] = step, time.time() - t0
            _save_torch(dict(model=model.state_dict(), opt=opt.state_dict(), torch_rng=torch.get_rng_state(),
                             hidden=state, state=st), ck)
    res = dict(st, chars_seen=LSTM_STEPS * LSTM_T * LSTM_B, train_chars=int(len(tr)), K=K, params=nets.count(model))
    _save_torch(model.state_dict(), wpath)
    rpath.write_text(json.dumps(res))
    ck.unlink(missing_ok=True)
    return model, res, (texts, chars, enc)


def beam_lm(model, enc, chars, prompt: str, n: int, width: int):
    """Beam search under the LSTM: keep the ``width`` most probable continuations, character by character."""
    torch = _torch()
    model.eval()
    with torch.no_grad():
        lo, st = model(torch.from_numpy(enc(prompt))[None])
        beams = [(0.0, [], lo[0, -1].log_softmax(0), st)]
        for _ in range(n):
            cand = []
            for lp, seq, logp, s in beams:
                top = logp.topk(width)
                for v, i in zip(top.values.tolist(), top.indices.tolist()):
                    cand.append((lp + v, seq + [i], s))
            cand.sort(key=lambda c: -c[0])
            cand = cand[:width]
            xs = torch.tensor([[c[1][-1]] for c in cand])
            hs = torch.cat([c[2][0] for c in cand], 1)
            cs = torch.cat([c[2][1] for c in cand], 1)
            lo, (h2, c2) = model(xs, (hs, cs))
            beams = [(cand[k][0], cand[k][1], lo[k, -1].log_softmax(0), (h2[:, k:k + 1], c2[:, k:k + 1]))
                     for k in range(len(cand))]
    best = beams[0]
    return "".join(chars[i] for i in best[1]), -best[0] / math.log(2)


def continuation_bits(model, enc, prompt: str, text: str) -> float:
    torch = _torch()
    model.eval()
    ids = enc(prompt + text)
    with torch.no_grad():
        lo, _ = model(torch.from_numpy(ids[:-1])[None])
        lp = lo[0].log_softmax(-1)
    k = len(enc(prompt))
    tot = -float(sum(lp[t - 1, ids[t]] for t in range(k, len(ids))))
    return tot / math.log(2)


def compute_charlstm():
    torch = _torch()
    model, r, (texts, chars, enc) = charlstm_train()
    ps = enc(texts["passage"])
    va = enc(texts["valid"])
    passage_bits = lstm_bits(model, ps)
    valid_bits = lstm_bits(model, va, 64)
    # per-character surprise over the passage
    with torch.no_grad():
        lo, _ = model(torch.from_numpy(ps[:-1])[None])
        surprise = (-lo[0].log_softmax(-1).gather(1, torch.from_numpy(ps[1:])[:, None])[:, 0] / math.log(2)).numpy()
    # what single cells track: correlation of every cell state with "inside a quotation" over the passage
    c_, h_, f_ = model.trace(torch.from_numpy(ps))
    C = c_.numpy()
    txt = texts["passage"]
    inside, q = np.zeros(len(txt)), 0
    for i, ch in enumerate(txt):
        if ch == '"':
            q ^= 1
        inside[i] = q
    z = (C - C.mean(0)) / (C.std(0) + 1e-6)
    corr = (z * ((inside - inside.mean()) / inside.std())[:, None]).mean(0)
    qcell = int(np.argmax(np.abs(corr)))
    # a stretch of dialogue to show it on (a paragraph that opens a quotation)
    start = txt.find('"', 2000)
    start = txt.rfind("\n", 0, start) + 1
    span = slice(start, start + 360)
    # samples, and greedy against beam search from the prompt
    samples = [[p, lstm_sample(model, enc, chars, p, 300, sd)] for sd, p in
               ((1, LSTM_PROMPT), (2, "It was the best of times, "), (3, "The telephone rang. "),
                (4, '"I don\'t know," he said. ')]]
    cool = lstm_sample(model, enc, chars, LSTM_PROMPT, 300, 1, temperature=0.6)
    greedy = lstm_sample(model, enc, chars, LSTM_PROMPT, 120, 1, temperature=1e-4)
    beam, beam_b = beam_lm(model, enc, chars, LSTM_PROMPT, 120, 8)
    sampled = samples[0][1][:120]
    return dict(params=r["params"], hidden=LSTM_H, emb=LSTM_EMB, batch=LSTM_B, bptt=LSTM_T, steps=LSTM_STEPS,
                chars_seen=r["chars_seen"], train_chars=r["train_chars"], K=r["K"], seconds=r["seconds"],
                clipped=r["clipped"], curve=np.asarray(r["curve"]),
                evals=[[e[0], e[1], e[2] if e[2] is not None else float("nan")] for e in r["evals"]],
                passage_bits=passage_bits, valid_bits=valid_bits, prompt=LSTM_PROMPT,
                snaps=[[int(k), v] for k, v in sorted(r["snaps"].items(), key=lambda kv: int(kv[0]))],
                surprise=surprise, quote_cell=qcell, quote_corr=float(corr[qcell]),
                quote_corr_next=float(np.sort(np.abs(corr))[-2]), quote_text=txt[span],
                quote_trace=C[span, qcell], forget_mean=float(f_.numpy().mean()),
                samples=samples, cool=cool, greedy=greedy,
                greedy_bits=continuation_bits(model, enc, LSTM_PROMPT, greedy), beam=beam, beam_bits=beam_b,
                sampled=sampled, sampled_bits=continuation_bits(model, enc, LSTM_PROMPT, sampled))


# ---------------------------------------------------------------------------
# Sequence to sequence, with and without attention
# ---------------------------------------------------------------------------
S2S_TRAIN = (3, 20)
S2S_TEST = tuple(range(3, 31))
S2S_STEPS, S2S_BATCH = 1200, 64
S2S_SNAPS = (0, 50, 100, 200, 400, 800, 1200)
S2S_SHOW = "attentionworks"  # the string whose alignment is replayed (14 letters)
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def s2s_encode(words):
    torch = _torch()
    L = max(len(w) for w in words)
    src = torch.zeros(len(words), L, dtype=torch.long)
    for i, w in enumerate(words):
        src[i, :len(w)] = torch.tensor([3 + LETTERS.index(ch) for ch in w])
    return src, torch.tensor([len(w) for w in words])


def s2s_batch(g, B, lo, hi):
    lens = g.integers(lo, hi + 1, B)
    words = ["".join(LETTERS[i] for i in g.integers(0, 26, n)) for n in lens]
    return words


def s2s_target(words):
    torch = _torch()
    L = max(len(w) for w in words) + 1
    tgt = torch.zeros(len(words), L, dtype=torch.long)
    for i, w in enumerate(words):
        tgt[i, :len(w) + 1] = torch.tensor([3 + LETTERS.index(ch) for ch in w[::-1]] + [2])
    tin = torch.cat([torch.ones(len(words), 1, dtype=torch.long), tgt[:, :-1]], 1)
    return tin, tgt


def s2s_decode(ids):
    out = []
    for i in ids:
        if i == 2:
            break
        out.append(LETTERS[i - 3] if i >= 3 else "?")
    return "".join(out)


def compute_seq2seq():
    torch = _torch()
    F = torch.nn.functional
    from videos.ai.ai10 import nets

    part = CACHE.partial("seq2seq", dict(train=S2S_TRAIN, steps=S2S_STEPS, v=1))
    test_words = {n: s2s_batch(rng(10_000 + n), 100, n, n) for n in S2S_TEST}
    for att in (False, True):
        for seed in (0, 1, 2):
            key = f"{int(att)}-{seed}"
            if key in part:
                continue
            torch.manual_seed(seed)
            model = nets.Seq2Seq(29, att)
            opt = torch.optim.Adam(model.parameters(), lr=2e-3)
            g = rng(seed)
            curve, losses, snaps = [], [], {}
            t0 = time.time()
            for step in range(S2S_STEPS + 1):
                if att and seed == 0 and step in S2S_SNAPS:
                    src, lens = s2s_encode([S2S_SHOW])
                    model.eval()
                    _, al = model.greedy(src, lens, len(S2S_SHOW) + 1)
                    model.train()
                    snaps[str(step)] = al[0].numpy().tolist()
                if step % 100 == 0:
                    model.eval()
                    accs = []
                    for n in (10, 20):
                        src, lens = s2s_encode(test_words[n][:50])
                        ys, _ = model.greedy(src, lens, n + 1)
                        accs.append(float(np.mean([s2s_decode(y.tolist()) == w[::-1] for y, w in
                                                   zip(ys, test_words[n][:50])])))
                    model.train()
                    curve.append([step] + accs)
                if step == S2S_STEPS:
                    break
                words = s2s_batch(g, S2S_BATCH, *S2S_TRAIN)
                src, lens = s2s_encode(words)
                tin, tgt = s2s_target(words)
                logits = model(src, lens, tin)
                loss = F.cross_entropy(logits.flatten(0, 1), tgt.flatten(), ignore_index=0)
                opt.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                opt.step()
                if step % 10 == 0:
                    losses.append([step, float(loss)])
            model.eval()
            exact, chars = [], []
            for n in S2S_TEST:
                src, lens = s2s_encode(test_words[n])
                ys, _ = model.greedy(src, lens, n + 1)
                preds = [s2s_decode(y.tolist()) for y in ys]
                exact.append(float(np.mean([p == w[::-1] for p, w in zip(preds, test_words[n])])))
                chars.append(float(np.mean([sum(a == b for a, b in zip(p, w[::-1])) / n
                                            for p, w in zip(preds, test_words[n])])))
            beam = {}
            if seed == 0:
                for n in (8, 14, 20):
                    ok_g = ok_b = 0
                    for w in test_words[n][:40]:
                        src, lens = s2s_encode([w])
                        yg, _ = model.greedy(src, lens, n + 1)
                        yb, _ = model.beam(src[0], lens[0], n + 1, width=4)
                        ok_g += s2s_decode(yg[0].tolist()) == w[::-1]
                        ok_b += s2s_decode(yb) == w[::-1]
                    beam[str(n)] = [ok_g / 40, ok_b / 40]
            src, lens = s2s_encode([S2S_SHOW])
            ys, al = model.greedy(src, lens, len(S2S_SHOW) + 1)
            part[key] = dict(curve=curve, losses=losses, exact=exact, chars=chars, snaps=snaps, beam=beam,
                             show_out=s2s_decode(ys[0].tolist()),
                             show_alpha=(al[0].numpy().tolist() if al is not None else None),
                             params=nets.count(model), seconds=time.time() - t0)
            print(f"    seq2seq att={att} seed={seed}: exact@10 {exact[7]:.2f} @20 {exact[17]:.2f} @30 {exact[-1]:.2f}"
                  f" ({time.time() - t0:.0f}s)", flush=True)
    return dict(train=list(S2S_TRAIN), test=list(S2S_TEST), steps=S2S_STEPS, batch=S2S_BATCH, show=S2S_SHOW,
                snap_steps=list(S2S_SNAPS), runs={k: part[k] for k in part.done})


# ---------------------------------------------------------------------------
# The parallel scan
# ---------------------------------------------------------------------------
def compute_scan():
    def sequential(a, b):
        h = np.zeros(a.shape[1])
        out = np.empty_like(b)
        for t in range(a.shape[0]):
            h = a[t] * h + b[t]
            out[t] = h
        return out

    def parallel(a, b):
        A, B = a.copy(), b.copy()
        d, rounds = 1, 0
        T = a.shape[0]
        while d < T:
            B[d:] = A[d:] * B[:-d] + B[d:]
            A[d:] = A[d:] * A[:-d]
            d *= 2
            rounds += 1
        return B, rounds

    def best(fn, reps=3):
        ts = []
        for _ in range(reps):
            t = time.perf_counter()
            r = fn()
            ts.append(time.perf_counter() - t)
        return min(ts), r

    rows = []
    for e in range(6, 17, 2):
        T, d = 2 ** e, 256
        g = rng(e)
        a, b = g.uniform(0.9, 1.0, (T, d)), g.normal(0, 1, (T, d))
        ts, hs = best(lambda: sequential(a, b))
        tp, (hp, rounds) = best(lambda: parallel(a, b))
        rows.append(dict(T=T, d=d, seq=ts, par=tp, rounds=rounds, err=float(np.abs(hs - hp).max()),
                         work_seq=T, work_par=sum(T - 2 ** k for k in range(rounds))))
        print(f"    T={T}: sequential {ts * 1e3:.1f} ms, scan {tp * 1e3:.1f} ms in {rounds} rounds", flush=True)
    return dict(rows=rows)


# ---------------------------------------------------------------------------
# Next time: optimizers in one valley
# ---------------------------------------------------------------------------
def compute_teaser():
    def f(x, y):
        return 0.5 * (x ** 2 / 9 + 4 * y ** 2) + 0.15 * np.sin(2 * x) * np.cos(1.5 * y)

    def grad(x, y):
        return np.array([x / 9 + 0.3 * np.cos(2 * x) * np.cos(1.5 * y), 4 * y - 0.225 * np.sin(2 * x) * np.sin(1.5 * y)])

    start = np.array([-4.2, 1.1])
    paths = {}
    p = start.copy()
    path = [p.copy()]
    for _ in range(120):
        p = p - 0.22 * grad(*p)
        path.append(p.copy())
    paths["gd"] = path
    p, v = start.copy(), np.zeros(2)
    path = [p.copy()]
    for _ in range(120):
        v = 0.85 * v + grad(*p)
        p = p - 0.06 * v
        path.append(p.copy())
    paths["momentum"] = path
    p, m, s = start.copy(), np.zeros(2), np.zeros(2)
    path = [p.copy()]
    for t in range(1, 121):
        gg = grad(*p)
        m = 0.9 * m + 0.1 * gg
        s = 0.999 * s + 0.001 * gg ** 2
        p = p - 0.12 * (m / (1 - 0.9 ** t)) / (np.sqrt(s / (1 - 0.999 ** t)) + 1e-8)
        path.append(p.copy())
    paths["adam"] = path
    xs, ys = np.linspace(-5, 5, 61), np.linspace(-2, 2, 41)
    X, Y = np.meshgrid(xs, ys)
    return dict(xs=xs, ys=ys, Z=f(X, Y), paths={k: np.asarray(v) for k, v in paths.items()},
                final={k: float(f(*np.asarray(v)[-1])) for k, v in paths.items()})


ITEMS = {
    "data": compute_data,
    "lenet": compute_lenet,
    "equivariance": compute_equivariance,
    "hog": compute_hog,
    "mlp_cnn": compute_mlp_cnn,
    "activations": compute_activations,
    "dropout": compute_dropout,
    "datasize": compute_datasize,
    "alexnet": compute_alexnet,
    "cifar": compute_cifar,
    "receptive": compute_receptive,
    "orientation": compute_orientation,
    "filters": compute_filters,
    "adversarial": compute_adversarial,
    "advtrain": compute_advtrain,
    "depthwise": compute_depthwise,
    "rnn_grad": compute_rnn_grad,
    "memory": compute_memory,
    "seq2seq": compute_seq2seq,
    "scan": compute_scan,
    "teaser": compute_teaser,
    "charlstm": compute_charlstm,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
