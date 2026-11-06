from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs29.common import (BG, DATA, HEAD, NO, PART, YES, grid_table, load, mono)


class HashUses(VoiceoverScene):
    def construct(self):
        self.card()
        self.merkle()
        self.commit()
        self.passwords()

    def card(self):
        card = chapter_card(13, r"Hashes at work", r"What can a fingerprint prove?", lit=(1979, 2005, 2013),
                            extra=((1979, r"Merkle's trees"), (2005, r"git"), (2013, r"Certificate Transparency"),
                                   (2015, r"Argon2")), part=PART)
        with self.voiceover("Chapter thirteen. Hashes at work."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def merkle(self):
        m = load("merkle")
        head = label(r"A Merkle tree over eight commits", font_size=34).to_edge(UP, buff=0.3)
        levels = m["levels"]
        leaf = 2
        nodes = []
        pos = []
        ys = [-0.6, 0.4, 1.4, 2.4]
        for d, lvl in enumerate(levels):
            n = len(lvl)
            row, prow = [], []
            for i, h in enumerate(lvl):
                x = -5.9 + 11.8 * (i + 0.5) / n
                box = RoundedRectangle(width=1.25, height=0.42, corner_radius=0.08, stroke_color=GREY_B,
                                       stroke_width=1.3, fill_color=BG, fill_opacity=1).move_to([x, ys[d], 0])
                row.append(VGroup(box, mono(h, 15, WHITE).move_to(box)))
                prow.append(np.array([x, ys[d], 0]))
            nodes.append(row)
            pos.append(prow)
        edges = VGroup()
        for d in range(1, len(levels)):
            for i in range(len(levels[d])):
                for c in (2 * i, 2 * i + 1):
                    edges.add(Line(pos[d][i] + DOWN * 0.21, pos[d - 1][c] + UP * 0.21, color=GREY_D, stroke_width=1.4))
        leaves = VGroup(*[label(t.split(": ")[1], font_size=15, color=GREY_A).next_to(nodes[0][i], DOWN, buff=0.4)
                          for i, t in enumerate(m["leaves"])])
        lw = VGroup(*[Line(lf.get_top(), nodes[0][i].get_bottom(), color=GREY_D, stroke_width=1.2)
                      for i, lf in enumerate(leaves)])
        path, sibs = [], []
        i = leaf
        for d in range(len(levels)):
            path.append(nodes[d][i])
            if d < len(levels) - 1:
                sibs.append(nodes[d][i ^ 1])
            i //= 2
        hp = VGroup(*[SurroundingRectangle(p, color=YES, buff=0.04) for p in path])
        hs = VGroup(*[SurroundingRectangle(s, color=HEAD, buff=0.04) for s in sibs])
        bad = VGroup(*[SurroundingRectangle(p, color=NO, buff=0.04) for p in path])
        lines = VGroup(
            label(r"each node is the hash of its two children; \ the \textbf{root} commits to everything below it",
                  font_size=21, color=WHITE),
            label(rf"to prove \textit{{fix overflow}} is in the history: \ give its {m['proof_len']} siblings \ "
                  r"(gold); \ the verifier rehashes up to the root", font_size=21, color=HEAD),
            label(rf"$\log_2 n$ hashes for $n$ items: \ proof checks: \ {'valid' if m['valid'] else 'invalid'}; "
                  rf"\ change the commit: \ {'valid' if m['tampered'] else 'rejected'}", font_size=21, color=YES),
            label(r"git \ (Part 41), \ Certificate Transparency \ (Part 30), \ ZFS \ (Part 34), \ blockchains \ "
                  r"(Part 38)", font_size=21, color=DATA),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Collision resistance turns a hash into a commitment: whoever publishes a hash is bound to the data "
            "behind it. Ralph Merkle's trees, from 1979, extend this to many items. <bookmark mark='a'/> Hash each "
            "item; then hash the hashes in pairs; and so on up to a single root. The root fixes every item below it: "
            "changing any one would change the root, unless you can find a collision. <bookmark mark='b'/> Now a "
            "server holding the tree can prove that one item, the commit that fixed an overflow, is in it, by "
            "sending only the three sibling hashes along its path. The verifier, who knows only the root, rehashes "
            "upward and compares. <bookmark mark='c'/> The proof is the logarithm of the number of items. Ours "
            "verifies; change one character of the commit, and the rebuilt root no longer matches. <bookmark "
            "mark='d'/> This structure is everywhere later in the series: git names every commit by such a hash, "
            "Certificate Transparency logs every web certificate in one, file systems like ZFS checksum every block "
            "with one, and blockchains chain them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(leaves), Create(lw), FadeIn(VGroup(*nodes[0])))
            vo.wait_until("a")
            self.play(Create(edges), FadeIn(VGroup(*[n for row in nodes[1:] for n in row])), FadeIn(lines[0]),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(Create(hp), Create(hs), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            self.play(ReplacementTransform(hp, bad), leaves[leaf].animate.set_color(NO))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def commit(self):
        head = label(r"Commit now, \ reveal later", font_size=34).to_edge(UP, buff=0.3)
        A = label(r"Alice", font_size=24, color=DATA).move_to([-4.2, 2.0, 0])
        B = label(r"Bob", font_size=24, color=HEAD).move_to([4.2, 2.0, 0])
        steps = [(1.2, r"$c = H(r \,\|\, \textrm{heads})$", "R", DATA),
                 (0.4, r"Bob's call: \ \textrm{tails}", "L", HEAD),
                 (-0.4, r"$r$, \ \textrm{heads}", "R", DATA)]
        arrows = VGroup()
        for y, t, d, c in steps:
            a, b = ([-3.6, y, 0], [3.6, y, 0]) if d == "R" else ([3.6, y, 0], [-3.6, y, 0])
            ar = Arrow(a, b, buff=0, stroke_width=2.5, color=c, max_tip_length_to_length_ratio=0.03)
            arrows.add(VGroup(ar, label(t, font_size=21, color=WHITE).next_to(ar, UP, buff=0.06)))
        check = label(r"Bob checks $H(r \,\|\, \textrm{heads}) = c$: \ Alice won, \ fairly", font_size=21,
                      color=YES).move_to([0, -1.1, 0])
        lines = VGroup(
            label(r"\textbf{hiding}: \ $c$ reveals nothing about the choice \ (the random $r$ makes guessing useless)",
                  font_size=21, color=WHITE),
            label(r"\textbf{binding}: \ Alice cannot open $c$ as tails \ (that would be a collision)", font_size=21,
                  color=HEAD),
            label(r"coin flipping by telephone \ (Blum, 1981); \ sealed bids; \ zero-knowledge proofs \ (Part 27)",
                  font_size=21, color=DATA),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The same binding works for a single secret. <bookmark mark='a'/> Alice and Bob want to flip a coin by "
            "telephone. Alice chooses heads, and sends the hash of a long random string followed by her choice. "
            "<bookmark mark='b'/> Bob calls tails. <bookmark mark='c'/> Alice reveals the random string and her "
            "choice; Bob hashes them and checks. <bookmark mark='d'/> The commitment is hiding: the random string "
            "keeps Bob from simply hashing both possible choices. <bookmark mark='e'/> And it is binding: to claim "
            "tails afterwards, Alice would need a collision. <bookmark mark='f'/> Manuel Blum described coin "
            "flipping by telephone in 1981. Commitments run through sealed-bid auctions and the zero-knowledge proofs "
            "of Part 27."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(B))
            vo.wait_until("a")
            self.play(FadeIn(arrows[0]))
            vo.wait_until("b")
            self.play(FadeIn(arrows[1]))
            vo.wait_until("c")
            self.play(FadeIn(arrows[2]))
            self.play(FadeIn(check))
            for mk, ln in zip("def", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def passwords(self):
        p = load("passwords")
        h = load("hashes")
        head = label(r"Storing passwords", font_size=34).to_edge(UP, buff=0.3)
        space = p["space_8_lower"]
        rows_ = {r["scheme"]: r for r in p["rows"]}
        data = [(r"SHA-256, \ once", h["hashlib_us"] * 1e-6, r"--"),
                (r"PBKDF2-SHA256 $\times$ 100{,}000", rows_["PBKDF2-SHA256 x 100,000"]["seconds"], r"--"),
                (r"PBKDF2-SHA256 $\times$ 600{,}000", rows_["PBKDF2-SHA256 x 600,000"]["seconds"], r"--"),
                (r"scrypt, \ $N = 2^{14}$", rows_["scrypt N=2^14, r=8"]["seconds"], r"16 MB")]

        def dur(s):
            if s < 3 * 86400:
                return rf"{s / 3600:.0f} hours"
            if s < 3 * 3.156e7:
                return rf"{s / 86400:.0f} days"
            return rf"{s / 3.156e7:,.0f} years".replace(",", "{,}")

        def per(s):
            return rf"{s * 1e6:.2f} $\mu$s" if s < 1e-3 else rf"{s * 1e3:.0f} ms"
        tab = grid_table([r"scheme", r"per guess", r"memory", r"every 8-letter password"],
                         [[n, per(s), m, dur(s * space)] for n, s, m in data],
                         widths=[4.2, 1.8, 1.4, 3.4], row_h=0.55, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5)
        for r in range(1, 5):
            tab.cells[r][3].set_color(NO if r == 1 else YES)
        tn = label(rf"measured on one CPU core; \ {space:,} lowercase 8-letter passwords".replace(",", "{,}"),
                   font_size=17, color=GREY_A).next_to(tab, DOWN, buff=0.15)
        lines = VGroup(
            label(r"never store passwords: \ store a random \textbf{salt} and $\mathrm{slow}(\mathit{salt}, "
                  r"\mathit{password})$", font_size=21, color=WHITE),
            label(r"salt: \ one hash per guess per user, \ and no precomputed tables \ (LinkedIn, 2012: \ unsalted "
                  r"SHA-1, \ most cracked)", font_size=21, color=HEAD),
            label(r"slow: \ an iteration count the defender pays once per login, \ and the attacker per guess",
                  font_size=21, color=DATA),
            label(r"memory-hard \ (scrypt, 2009; \ Argon2, 2015): \ GPUs have thousands of cores but little memory "
                  r"each", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Hashes also guard passwords, and here the danger is not a clever attack but a fast one. <bookmark "
            "mark='a'/> A server should never store passwords, only a random salt and a deliberately slow hash of the "
            "salt and password. <bookmark mark='b'/> The salt means each guess must be hashed separately for each "
            "user, and makes precomputed tables useless. In 2012 LinkedIn lost six and a half million unsalted SHA-1 "
            "hashes, and most were cracked. <bookmark mark='c'/> Slowness is a dial. We measured: one SHA-256 takes "
            "under half a microsecond, so every lowercase eight-letter password can be tried in about a day on one "
            "core. PBKDF2, which iterates a hash six hundred thousand times as current guidance recommends, takes a "
            "sixth of a second per guess: imperceptible at login, and over a thousand years for that search. "
            "<bookmark mark='d'/> But attackers use graphics cards with thousands of cores. Memory-hard functions, "
            "scrypt and the competition winner Argon2, need megabytes of memory per guess, which those cores do not "
            "have. Use one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(tn), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()
