"""The networks Part 10 trains on the CPU: LeNet-5 and an MLP of the same size for the digits, a small plain CNN for
the activation race, a CIFAR-10 network for the photographs, recurrent cells for the memory task (including minGRU,
trained through a parallel scan), a character LSTM for the novels, and an encoder-decoder with and without Bahdanau
attention.  Only ``compute.py`` imports this (scenes read cached results)."""

from __future__ import annotations

import math

import torch
import torch.nn as nn
import torch.nn.functional as F

ACT = {"relu": F.relu, "tanh": torch.tanh, "sigmoid": torch.sigmoid}


# ---------------------------------------------------------------------------
# Digits
# ---------------------------------------------------------------------------
class LeNet5(nn.Module):
    """LeNet-5's layout (LeCun, Bottou, Bengio & Haffner 1998): C1 six 5x5 maps, S2 pooling, C3 sixteen 5x5 maps,
    S4 pooling, then 120, 84 and 10 units; with today's ReLU, max pooling, full C3 connections and a softmax."""

    def __init__(self, act: str = "relu"):
        super().__init__()
        self.act = ACT[act]
        self.c1 = nn.Conv2d(1, 6, 5, padding=2)
        self.c3 = nn.Conv2d(6, 16, 5)
        self.f5 = nn.Linear(400, 120)
        self.f6 = nn.Linear(120, 84)
        self.out = nn.Linear(84, 10)

    def maps(self, x):
        a1 = self.act(self.c1(x))  # (n, 6, 28, 28)
        a3 = self.act(self.c3(F.max_pool2d(a1, 2)))  # (n, 16, 10, 10)
        return a1, a3

    def forward(self, x):
        a1, a3 = self.maps(x)
        z = F.max_pool2d(a3, 2).flatten(1)
        return self.out(self.act(self.f6(self.act(self.f5(z)))))


class MLP(nn.Module):
    """One hidden layer, sized to LeNet-5's parameter count (784 -> 78 -> 10: 62,020 against 61,706)."""

    def __init__(self, hidden: int = 78, dropout: float = 0.0, layers: int = 1):
        super().__init__()
        dims = [784] + [hidden] * layers
        self.hid = nn.ModuleList(nn.Linear(a, b) for a, b in zip(dims, dims[1:]))
        self.drop = dropout
        self.out = nn.Linear(hidden, 10)

    def forward(self, x):
        z = x.flatten(1)
        for lin in self.hid:
            z = F.dropout(F.relu(lin(z)), self.drop, self.training)
        return self.out(z)


class Linear(nn.Module):
    """Multinomial logistic regression: the 'shallow softmax' of Goodfellow et al. (2014), and the classifier on top
    of hand-made features."""

    def __init__(self, d: int, k: int = 10):
        super().__init__()
        self.lin = nn.Linear(d, k)

    def forward(self, x):
        return self.lin(x.flatten(1))


class PlainCNN(nn.Module):
    """Five 3x3 convolutions and a linear read-out, no normalization: deep enough for the activation to matter."""

    def __init__(self, act: str = "relu"):
        super().__init__()
        self.act = ACT[act]
        ch = [1, 16, 16, 32, 32, 32]
        self.convs = nn.ModuleList(nn.Conv2d(a, b, 3, padding=1) for a, b in zip(ch, ch[1:]))
        self.out = nn.Linear(32 * 7 * 7, 10)

    def forward(self, x):
        for i, c in enumerate(self.convs):
            x = self.act(c(x))
            if i in (1, 3):
                x = F.max_pool2d(x, 2)
        return self.out(x.flatten(1))


# ---------------------------------------------------------------------------
# Photographs
# ---------------------------------------------------------------------------
CIFAR_MEAN = (0.4914, 0.4822, 0.4465)
CIFAR_STD = (0.2470, 0.2435, 0.2616)


class CifarNet(nn.Module):
    """A small CIFAR-10 network with an AlexNet-like first layer: 48 filters of 7 x 7 x 3 at stride 2, then three 3x3
    stages (64, 128, 128 channels), batch normalization, global average pooling.  Inputs in [0, 1]; the per-channel
    normalization is the first operation, so perturbations are measured in pixel units."""

    def __init__(self, c1: int = 48):
        super().__init__()
        self.register_buffer("mean", torch.tensor(CIFAR_MEAN).view(1, 3, 1, 1))
        self.register_buffer("std", torch.tensor(CIFAR_STD).view(1, 3, 1, 1))
        self.c1 = nn.Conv2d(3, c1, 7, stride=2, padding=3)
        self.b1 = nn.BatchNorm2d(c1)
        self.c2 = nn.Conv2d(c1, 64, 3, padding=1)
        self.b2 = nn.BatchNorm2d(64)
        self.c3 = nn.Conv2d(64, 128, 3, padding=1)
        self.b3 = nn.BatchNorm2d(128)
        self.c4 = nn.Conv2d(128, 128, 3, padding=1)
        self.b4 = nn.BatchNorm2d(128)
        self.fc = nn.Linear(128, 10)

    def maps(self, x):
        x = (x - self.mean) / self.std
        a1 = F.relu(self.b1(self.c1(x)))  # 16 x 16
        a2 = F.relu(self.b2(self.c2(a1)))  # 16 x 16
        a3 = F.relu(self.b3(self.c3(F.max_pool2d(a2, 2))))  # 8 x 8
        a4 = F.relu(self.b4(self.c4(F.max_pool2d(a3, 2))))  # 4 x 4
        return a1, a2, a3, a4

    def forward(self, x):
        return self.fc(self.maps(x)[3].mean((2, 3)))


# ---------------------------------------------------------------------------
# Recurrence
# ---------------------------------------------------------------------------
def linear_scan(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    """h_t = a_t * h_{t-1} + b_t from h_0 = 0, for every t at once: the Hillis-Steele scan of the associative pair
    (a, b) o (a', b') = (a a', a' b + b'), log2(T) rounds of elementwise products (time is dim 1)."""
    A, B = a, b
    d, T = 1, a.shape[1]
    while d < T:
        A_prev = torch.cat([torch.ones_like(A[:, :d]), A[:, :-d]], 1)
        B_prev = torch.cat([torch.zeros_like(B[:, :d]), B[:, :-d]], 1)
        B = A * B_prev + B
        A = A * A_prev
        d *= 2
    return B


class MinGRU(nn.Module):
    """minGRU (Feng, Tung, Ahmed, Bengio & Hajimirsadeghi 2024): the gate and the candidate see only the input,
    z_t = sigmoid(W_z x_t), h~_t = W_h x_t, h_t = (1 - z_t) h_{t-1} + z_t h~_t: a linear recurrence, so a scan."""

    def __init__(self, d_in: int, hidden: int):
        super().__init__()
        self.z = nn.Linear(d_in, hidden)
        self.h = nn.Linear(d_in, hidden)

    def forward(self, x, sequential: bool = False):
        z = torch.sigmoid(self.z(x))
        a, b = 1 - z, z * self.h(x)
        if not sequential:
            return linear_scan(a, b)
        h, out = torch.zeros_like(b[:, 0]), []
        for t in range(x.shape[1]):
            h = a[:, t] * h + b[:, t]
            out.append(h)
        return torch.stack(out, 1)


class SeqClassifier(nn.Module):
    """Read a sequence of symbols with one recurrent cell and classify from the last hidden state."""

    def __init__(self, cell: str, vocab: int, classes: int, hidden: int = 64, emb: int = 16):
        super().__init__()
        self.kind = cell
        self.emb = nn.Embedding(vocab, emb)
        if cell == "rnn":
            self.rnn = nn.RNN(emb, hidden, batch_first=True, nonlinearity="tanh")
        elif cell == "lstm":
            self.rnn = nn.LSTM(emb, hidden, batch_first=True)
        elif cell == "gru":
            self.rnn = nn.GRU(emb, hidden, batch_first=True)
        elif cell == "mingru":
            self.rnn = MinGRU(emb, hidden)
        else:
            raise ValueError(cell)
        self.out = nn.Linear(hidden, classes)

    @torch.no_grad()
    def chrono_init(self, t_max: int, generator=None):
        """Tallec & Ollivier (2018), 'chrono' initialization: each unit's gate starts so that it keeps its memory for
        a time drawn between 1 and t_max steps (forget/update gate bias log U(1, t_max - 1); LSTM input gate the
        opposite).  Only the gated cells have such a gate; the plain RNN is left as it is."""
        H = self.out.in_features
        u = torch.empty(H).uniform_(1.0, max(t_max - 1.0, 1.0 + 1e-3), generator=generator)
        b = torch.log(u)
        if self.kind == "lstm":  # PyTorch gate order: input, forget, cell, output
            self.rnn.bias_ih_l0[H:2 * H] = b
            self.rnn.bias_hh_l0[H:2 * H] = 0.0
            self.rnn.bias_ih_l0[:H] = -b
            self.rnn.bias_hh_l0[:H] = 0.0
        elif self.kind == "gru":  # reset, update, new; h' = (1 - z) n + z h: z near 1 keeps the state
            self.rnn.bias_ih_l0[H:2 * H] = b
            self.rnn.bias_hh_l0[H:2 * H] = 0.0
        elif self.kind == "mingru":  # h = (1 - z) h + z h~: z near 0 keeps the state
            self.rnn.z.bias[:] = -b

    def forward(self, x, keep_inputs: bool = False):
        e = self.emb(x)
        if keep_inputs:  # the inputs as leaves, so the gradient reaching each time step can be read
            e = e.detach().requires_grad_(True)
            self.inputs = e
        h = self.rnn(e) if self.kind == "mingru" else self.rnn(e)[0]
        return self.out(h[:, -1])


class CharLSTM(nn.Module):
    """A character-level LSTM language model: a learned vector per character, one LSTM layer, a softmax read-out."""

    def __init__(self, vocab: int, hidden: int = 512, emb: int = 64):
        super().__init__()
        self.emb = nn.Embedding(vocab, emb)
        self.lstm = nn.LSTM(emb, hidden, batch_first=True)
        self.out = nn.Linear(hidden, vocab)

    def forward(self, x, state=None):
        h, state = self.lstm(self.emb(x), state)
        return self.out(h), state

    @torch.no_grad()
    def trace(self, x: torch.Tensor):
        """Run one sequence (1-D) step by step with the same weights, returning every cell state c_t, hidden h_t and
        forget gate f_t (for reading what single cells track)."""
        W_ih, W_hh = self.lstm.weight_ih_l0, self.lstm.weight_hh_l0
        b = self.lstm.bias_ih_l0 + self.lstm.bias_hh_l0
        H = W_hh.shape[1]
        h = torch.zeros(H)
        c = torch.zeros(H)
        xs = self.emb(x) @ W_ih.T + b  # input contributions for all steps at once
        cs, hs, fs = [], [], []
        for t in range(len(x)):
            g = xs[t] + W_hh @ h
            i, f, gg, o = g[:H].sigmoid(), g[H:2 * H].sigmoid(), g[2 * H:3 * H].tanh(), g[3 * H:].sigmoid()
            c = f * c + i * gg
            h = o * c.tanh()
            cs.append(c.clone())
            hs.append(h.clone())
            fs.append(f.clone())
        return torch.stack(cs), torch.stack(hs), torch.stack(fs)


class Seq2Seq(nn.Module):
    """An RNN encoder-decoder for strings.  The encoder is a bidirectional GRU.  Without attention the decoder sees
    one fixed summary c of the whole input at every step (Cho et al. 2014); with attention it recomputes c_i at each
    step as a weighted average of the encoder's states, weights from Bahdanau, Cho & Bengio's additive score
    e_ij = v . tanh(W s_{i-1} + U h_j) (2014)."""

    PAD, SOS, EOS = 0, 1, 2

    def __init__(self, vocab: int, attention: bool, hidden: int = 128, emb: int = 32):
        super().__init__()
        self.attention, self.H = attention, hidden
        self.src_emb = nn.Embedding(vocab, emb, padding_idx=0)
        self.tgt_emb = nn.Embedding(vocab, emb, padding_idx=0)
        self.enc = nn.GRU(emb, hidden // 2, batch_first=True, bidirectional=True)
        self.init = nn.Linear(hidden, hidden)
        self.cell = nn.GRUCell(emb + hidden, hidden)
        if attention:
            self.W = nn.Linear(hidden, hidden, bias=False)
            self.U = nn.Linear(hidden, hidden, bias=False)
            self.v = nn.Linear(hidden, 1, bias=False)
        self.out = nn.Linear(2 * hidden + emb, vocab)

    def encode(self, src, lengths):
        packed = nn.utils.rnn.pack_padded_sequence(self.src_emb(src), lengths.cpu(), batch_first=True,
                                                   enforce_sorted=False)
        out, last = self.enc(packed)
        hs, _ = nn.utils.rnn.pad_packed_sequence(out, batch_first=True, total_length=src.shape[1])
        summary = torch.cat([last[0], last[1]], -1)  # forward state at the end, backward state at the start
        return hs, summary, src != self.PAD

    def context(self, s, hs, mask, Uh):
        if not self.attention:
            return None, None
        e = self.v(torch.tanh(self.W(s)[:, None] + Uh)).squeeze(-1)
        alpha = e.masked_fill(~mask, -1e9).softmax(-1)
        return (alpha[:, :, None] * hs).sum(1), alpha

    def step(self, y_prev, s, hs, summary, mask, Uh):
        c, alpha = self.context(s, hs, mask, Uh)
        if c is None:
            c = summary
        e = self.tgt_emb(y_prev)
        s = self.cell(torch.cat([e, c], -1), s)
        return self.out(torch.cat([s, c, e], -1)), s, alpha

    def forward(self, src, lengths, tgt_in):
        """Teacher forcing: the decoder is fed the true previous symbol at every step."""
        hs, summary, mask = self.encode(src, lengths)
        s = torch.tanh(self.init(summary))
        Uh = self.U(hs) if self.attention else None
        logits = []
        for t in range(tgt_in.shape[1]):
            lo, s, _ = self.step(tgt_in[:, t], s, hs, summary, mask, Uh)
            logits.append(lo)
        return torch.stack(logits, 1)

    @torch.no_grad()
    def greedy(self, src, lengths, max_len: int):
        hs, summary, mask = self.encode(src, lengths)
        s = torch.tanh(self.init(summary))
        Uh = self.U(hs) if self.attention else None
        y = torch.full((src.shape[0],), self.SOS, dtype=torch.long)
        out, alphas = [], []
        for _ in range(max_len):
            lo, s, a = self.step(y, s, hs, summary, mask, Uh)
            y = lo.argmax(-1)
            out.append(y)
            if a is not None:
                alphas.append(a)
        return torch.stack(out, 1), (torch.stack(alphas, 1) if alphas else None)

    @torch.no_grad()
    def beam(self, src, length, max_len: int, width: int = 4):
        """Beam search for one input: keep the ``width`` most probable prefixes at every step."""
        hs, summary, mask = self.encode(src[None], length[None])
        s0 = torch.tanh(self.init(summary))
        Uh = self.U(hs) if self.attention else None
        beams = [(0.0, [self.SOS], s0, False)]
        for _ in range(max_len):
            cand = []
            for lp, seq, s, done in beams:
                if done:
                    cand.append((lp, seq, s, True))
                    continue
                lo, s2, _ = self.step(torch.tensor([seq[-1]]), s, hs, summary, mask, Uh)
                logp = lo.log_softmax(-1)[0]
                top = logp.topk(width)
                for v, i in zip(top.values.tolist(), top.indices.tolist()):
                    cand.append((lp + v, seq + [i], s2, i == self.EOS))
            beams = sorted(cand, key=lambda b: -b[0])[:width]
            if all(b[3] for b in beams):
                break
        return beams[0][1][1:], beams[0][0]


def count(model: nn.Module) -> int:
    return sum(p.numel() for p in model.parameters())


def bits(loss_nats: float) -> float:
    return loss_nats / math.log(2)
