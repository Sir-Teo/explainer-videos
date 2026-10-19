"""AlphaZero for Connect Four, small enough to train on the CPU that renders Part 26.

    python -m videos.ai.ai26.alphazero            # train (resumes from .cache/ai26/az/), about 5 hours on 4 cores
    python -m videos.ai.ai26.alphazero --gens 2   # a quick check

The recipe is Silver et al.'s (AlphaGo Zero 2017, AlphaZero 2018), at toy scale:

* one network f(s) = (p, v): a residual tower over the board, a policy head (a probability for each column) and a
  value head (the expected result for the player to move, in [-1, 1]);
* self-play: each move is chosen by a Monte Carlo tree search guided by the network (PUCT: Q + c P sqrt(N) / (1 + n)),
  with Dirichlet noise on the root's priors; the first moves are sampled in proportion to visit counts, later ones
  are the most visited;
* training on every position played: the policy learns the search's visit counts pi, the value learns the game's
  result z: loss (z - v)^2 - pi . log p, plus weight decay; boards are mirrored left-right for twice the data;
* repeat: the improved network makes the next generation's games.

Each generation's network is kept (``gen_NNN.pt``), with a log of losses and game statistics (``log.json``), so
compute.py can grade every generation against the perfect solver and rate them against each other.
"""

from __future__ import annotations

import argparse
import json
import math
import multiprocessing as mp
import os
import time
from pathlib import Path

import numpy as np

from explainer.tts import REPO_ROOT
from videos.ai.ai26.c4 import SIZE, W, Board, last_mover_won

OUT = REPO_ROOT / ".cache" / "ai26" / "az"
CHANNELS, BLOCKS = 32, 4
C_PUCT = 2.0
DIR_ALPHA, DIR_EPS = 1.0, 0.25
SIMS = 100
SAMPLE_MOVES = 8  # moves sampled from the visit counts before switching to the most visited
GAMES_PER_GEN = 400
TRAIN_STEPS = 300
BATCH = 512
WINDOW = 10  # generations of games kept in the replay buffer
LR, WD = 1e-3, 1e-4


def make_net():
    import torch
    import torch.nn as nn
    import torch.nn.functional as F

    class Res(nn.Module):
        def __init__(self, c):
            super().__init__()
            self.c1, self.b1 = nn.Conv2d(c, c, 3, padding=1, bias=False), nn.BatchNorm2d(c)
            self.c2, self.b2 = nn.Conv2d(c, c, 3, padding=1, bias=False), nn.BatchNorm2d(c)

        def forward(self, x):
            y = F.relu(self.b1(self.c1(x)))
            return F.relu(x + self.b2(self.c2(y)))

    class Net(nn.Module):
        def __init__(self, c=CHANNELS, blocks=BLOCKS):
            super().__init__()
            self.stem = nn.Sequential(nn.Conv2d(3, c, 3, padding=1, bias=False), nn.BatchNorm2d(c), nn.ReLU())
            self.tower = nn.Sequential(*[Res(c) for _ in range(blocks)])
            self.ph = nn.Sequential(nn.Conv2d(c, 2, 1, bias=False), nn.BatchNorm2d(2), nn.ReLU(), nn.Flatten(),
                                    nn.Linear(2 * SIZE, W))
            self.vh = nn.Sequential(nn.Conv2d(c, 1, 1, bias=False), nn.BatchNorm2d(1), nn.ReLU(), nn.Flatten(),
                                    nn.Linear(SIZE, 64), nn.ReLU(), nn.Linear(64, 1), nn.Tanh())

        def forward(self, x):
            h = self.tower(self.stem(x))
            return self.ph(h), self.vh(h).squeeze(-1)

    return Net()


def encode(boards: list[Board]) -> np.ndarray:
    """Input planes: the mover's stones, the opponent's, and a plane of ones (so the edges are visible)."""
    x = np.zeros((len(boards), 3, 6, 7), np.float32)
    for i, b in enumerate(boards):
        x[i, :2] = b.planes()
        x[i, 2] = 1.0
    return x


class Evaluator:
    """Batched network calls: priors over the legal columns and the value for the player to move."""

    def __init__(self, net):
        import torch

        self.torch = torch
        self.net = net.eval()

    def __call__(self, boards: list[Board]):
        torch = self.torch
        with torch.no_grad():
            logits, v = self.net(torch.from_numpy(encode(boards)))
        logits, v = logits.numpy().astype(np.float64), v.numpy().astype(np.float64)
        priors = []
        for b, lg in zip(boards, logits):
            legal = np.zeros(W, bool)
            legal[b.legal()] = True
            lg = np.where(legal, lg, -np.inf)
            p = np.exp(lg - lg[legal].max())
            priors.append(p / p.sum())
        return priors, v


class Node:
    __slots__ = ("board", "P", "N", "Wsum", "children", "terminal", "tvalue")

    def __init__(self, board: Board):
        self.board = board
        self.P = None  # priors, set when the node is expanded
        self.N = np.zeros(W)
        self.Wsum = np.zeros(W)  # total value of each edge, from the view of the player to move here
        self.children: dict[int, Node] = {}
        self.terminal, self.tvalue = False, 0.0
        if board.moves and last_mover_won(board):
            self.terminal, self.tvalue = True, -1.0  # the player to move has lost
        elif board.full():
            self.terminal, self.tvalue = True, 0.0

    def select(self, c=C_PUCT) -> int:
        n = self.N.sum()
        q = np.where(self.N > 0, self.Wsum / np.maximum(self.N, 1), 0.0)
        u = c * self.P * math.sqrt(n + 1e-8) / (1 + self.N)
        score = np.where(self.P > 0, q + u, -np.inf)
        return int(np.argmax(score))


def search(roots: list[Node], evaluate, sims: int, rng, noise=True, c=C_PUCT):
    """Run ``sims`` simulations from each root, all roots advancing together so the network sees one batch."""
    fresh = [r for r in roots if r.P is None]
    if fresh:
        pri, _ = evaluate([r.board for r in fresh])
        for r, p in zip(fresh, pri):
            r.P = p
    if noise:
        for r in roots:
            legal = r.P > 0
            d = rng.dirichlet([DIR_ALPHA] * int(legal.sum()))
            P = r.P.copy()
            P[legal] = (1 - DIR_EPS) * P[legal] + DIR_EPS * d
            r.P = P
    for _ in range(sims):
        pending, paths = [], []
        for r in roots:
            node, path = r, []
            while True:
                a = node.select(c)
                path.append((node, a))
                child = node.children.get(a)
                if child is None:
                    child = Node(node.board.play(a))
                    node.children[a] = child
                    break
                if child.terminal:
                    break
                node = child
            if child.terminal:
                _backup(path, child.tvalue)
            else:
                pending.append(child)
                paths.append(path)
        if pending:
            pri, vals = evaluate([n.board for n in pending])
            for n, p, v, path in zip(pending, pri, vals, paths):
                n.P = p
                _backup(path, float(v))


def _backup(path, v_leaf):
    """``v_leaf`` is for the player to move at the leaf; each edge stores value for the player who chose it."""
    v = -v_leaf
    for node, a in reversed(path):
        node.N[a] += 1
        node.Wsum[a] += v
        v = -v


def play_games(net, n_games: int, sims: int, seed: int, sample_moves=SAMPLE_MOVES):
    """Self-play ``n_games`` at once. Returns training examples (planes, pi, z) and the games' move lists."""
    rng = np.random.default_rng(seed)
    ev = Evaluator(net)
    boards = [Board() for _ in range(n_games)]
    records: list[list] = [[] for _ in range(n_games)]
    done = [False] * n_games
    results = [0.0] * n_games  # +1 if the first player won
    while not all(done):
        idx = [i for i in range(n_games) if not done[i]]
        roots = [Node(boards[i]) for i in idx]
        search(roots, ev, sims, rng)
        for i, r in zip(idx, roots):
            pi = r.N / r.N.sum()
            records[i].append((encode([boards[i]])[0], pi, boards[i].moves % 2))
            if boards[i].moves < sample_moves:
                a = int(rng.choice(W, p=pi))
            else:
                a = int(np.argmax(r.N))
            boards[i] = boards[i].play(a)
            if last_mover_won(boards[i]):
                done[i], results[i] = True, (1.0 if boards[i].moves % 2 == 1 else -1.0)
            elif boards[i].full():
                done[i] = True
    X, P, Z = [], [], []
    for rec, res in zip(records, results):
        for planes, pi, side in rec:
            X.append(planes)
            P.append(pi)
            Z.append(res if side == 0 else -res)
    return np.array(X), np.array(P, np.float32), np.array(Z, np.float32), [list(b.history) for b in boards], results


def _worker(args):
    state, n_games, sims, seed = args
    import torch

    torch.set_num_threads(1)
    net = make_net()
    net.load_state_dict(state)
    return play_games(net, n_games, sims, seed)


def mirror(X, P):
    return X[..., ::-1].copy(), P[:, ::-1].copy()


def train(gens: int, workers: int = 4):
    import torch
    import torch.nn.functional as F

    OUT.mkdir(parents=True, exist_ok=True)
    torch.manual_seed(0)
    log_path = OUT / "log.json"
    log = json.loads(log_path.read_text()) if log_path.exists() else []
    net = make_net()
    opt = torch.optim.AdamW(net.parameters(), lr=LR, weight_decay=WD)
    start = len(log)
    if start:
        ck = torch.load(OUT / f"gen_{start:03d}.pt")
        net.load_state_dict(ck["net"])
        opt.load_state_dict(ck["opt"])
    else:
        torch.save({"net": net.state_dict(), "opt": opt.state_dict()}, OUT / "gen_000.pt")
    buffer = []
    for g in range(max(0, start - WINDOW), start):  # rebuild the replay window from saved games
        z = np.load(OUT / f"games_{g + 1:03d}.npz")
        buffer.append((z["X"], z["P"], z["Z"]))
    ctx = mp.get_context("fork" if os.name == "posix" and "fork" in mp.get_all_start_methods() else "spawn")
    for g in range(start, gens):
        t0 = time.time()
        state = {k: v.clone() for k, v in net.state_dict().items()}
        per = GAMES_PER_GEN // workers
        jobs = [(state, per, SIMS, 1000 * g + w) for w in range(workers)]
        with ctx.Pool(workers) as pool:
            outs = pool.map(_worker, jobs)
        X = np.concatenate([o[0] for o in outs])
        P = np.concatenate([o[1] for o in outs])
        Z = np.concatenate([o[2] for o in outs])
        games = [h for o in outs for h in o[3]]
        res = [r for o in outs for r in o[4]]
        np.savez_compressed(OUT / f"games_{g + 1:03d}.npz", X=X, P=P, Z=Z,
                            lengths=np.array([len(h) for h in games]), results=np.array(res))
        buffer.append((X, P, Z))
        buffer = buffer[-WINDOW:]
        t1 = time.time()
        BX = np.concatenate([b[0] for b in buffer])
        BP = np.concatenate([b[1] for b in buffer])
        BZ = np.concatenate([b[2] for b in buffer])
        MX, MP = mirror(BX, BP)
        BX, BP, BZ = np.concatenate([BX, MX]), np.concatenate([BP, MP]), np.concatenate([BZ, BZ])
        torch.set_num_threads(2)  # more threads spin against the self-play and other jobs (10x slower at 4)
        net.train()
        rng = np.random.default_rng(g)
        lp = lv = 0.0
        for s in range(TRAIN_STEPS):
            i = rng.integers(0, len(BX), BATCH)
            x, p, z = torch.from_numpy(BX[i]), torch.from_numpy(BP[i]), torch.from_numpy(BZ[i])
            logits, v = net(x)
            loss_p = -(p * F.log_softmax(logits, -1)).sum(-1).mean()
            loss_v = F.mse_loss(v, z)
            opt.zero_grad()
            (loss_p + loss_v).backward()
            opt.step()
            lp += loss_p.item() / TRAIN_STEPS
            lv += loss_v.item() / TRAIN_STEPS
        net.eval()
        torch.save({"net": net.state_dict(), "opt": opt.state_dict()}, OUT / f"gen_{g + 1:03d}.pt")
        res = np.array(res)
        log.append({"gen": g + 1, "loss_policy": lp, "loss_value": lv, "positions": int(len(X)),
                    "first_wins": float((res > 0).mean()), "second_wins": float((res < 0).mean()),
                    "draws": float((res == 0).mean()), "mean_length": float(np.mean([len(h) for h in games])),
                    "selfplay_s": t1 - t0, "train_s": time.time() - t1})
        log_path.write_text(json.dumps(log, indent=1))
        print(f"gen {g + 1}: policy {lp:.3f} value {lv:.3f} | first {log[-1]['first_wins']:.2f} "
              f"draws {log[-1]['draws']:.2f} len {log[-1]['mean_length']:.1f} | "
              f"{t1 - t0:.0f}s play {time.time() - t1:.0f}s train", flush=True)


def load_gen(g: int):
    import torch

    net = make_net()
    net.load_state_dict(torch.load(OUT / f"gen_{g:03d}.pt")["net"])
    return net.eval()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--gens", type=int, default=40)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    train(a.gens, a.workers)
