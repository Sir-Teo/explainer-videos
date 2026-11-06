from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs21.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class Rsync(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.rsync()
        self.cdc()

    def card(self):
        card = chapter_card(14, r"Rolling hashes at scale: \ rsync and chunking", r"How do you send only what "
                            r"changed?", lit=(1996,), extra=((1996, r"rsync"),), part=PART)
        with self.voiceover("Chapter fourteen. Rolling hashes at scale: rsync and chunking."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def problem(self):
        d = load("rsync")
        head = label(r"Twenty-four bytes inserted in the middle", font_size=34).to_edge(UP, buff=0.35)
        n = 40
        W = 11.6
        old = VGroup(*[Rectangle(width=W / n - 0.02, height=0.45, stroke_width=0, fill_color=DATA, fill_opacity=0.75)
                       for _ in range(n)]).arrange(RIGHT, buff=0.02).move_to(UP * 1.4)
        new = old.copy().move_to(UP * 0.4)
        for k in range(n // 2, n):
            new[k].set_fill(NO, 0.75)
        ins = Rectangle(width=0.08, height=0.6, stroke_width=0, fill_color=HEAD, fill_opacity=1).move_to(new[n // 2]
                                                                                                    .get_left())
        lo = label(r"the old file, \ cut into fixed 2 KB blocks", font_size=19, color=GREY_A).next_to(old, UP, buff=0.15)
        ln = label(r"the new file: \ every block after the insertion has shifted", font_size=19, color=GREY_A
                   ).next_to(new, DOWN, buff=0.15)
        res = label(rf"\textit{{Moby-Dick}}: \ only {d['fixed_reused']} of {d['fixed_blocks']} fixed blocks are "
                    r"unchanged", font_size=24, color=NO).to_edge(DOWN, buff=1.2)
        with self.voiceover(
            "You have last week's copy of a large file, and the server has today's, which differs by a sentence "
            "inserted in the middle. How do you update your copy without downloading all of it? <bookmark "
            "mark='a'/> The obvious plan cuts both files into fixed blocks and sends only the blocks whose hashes "
            "differ. <bookmark mark='b'/> But an insertion shifts everything after it. We inserted twenty-four "
            "bytes into the middle of Moby-Dick: <bookmark mark='c'/> half of the fixed blocks now differ, though "
            "almost nothing changed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(old), FadeIn(lo))
            vo.wait_until("a")
            self.play(FadeIn(new))
            vo.wait_until("b")
            self.play(FadeIn(ins), *[new[k].animate.set_fill(NO, 0.75) for k in range(n // 2, n)], FadeIn(ln))
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    def rsync(self):
        d = load("rsync")
        head = label(r"rsync: \ look for the old blocks at \textit{every} offset", font_size=32).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"the receiver sends a weak and a strong hash of each of its blocks", font_size=22, color=WHITE),
            label(r"the sender slides a window over the new file, \ one byte at a time", font_size=22, color=WHITE),
            MathTex(r"a_{k+1} = a_k - t_k + t_{k+B}, \qquad b_{k+1} = b_k - B\,t_k + a_{k+1}", font_size=34, color=LAM),
            label(r"the weak checksum rolls in $O(1)$; \ only on a weak match is the strong hash computed", font_size=22,
                  color=YES),
            label(rf"\textit{{Moby-Dick}}: \ {d['rsync_matched']} blocks found, \ {words(d['rsync_literal'])} literal "
                  rf"bytes sent", font_size=24, color=HEAD),
            label(r"Tridgell and Mackerras (1996); \ the same idea as Rabin--Karp, \ chapter 2", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.26).next_to(head, DOWN, buff=0.4)
        n, W = 40, 11.6
        bw = W / n - 0.02
        blocks = VGroup(*[Rectangle(width=bw, height=0.4, stroke_width=0, fill_color=DATA, fill_opacity=0.75)
                          for _ in range(n)]).arrange(RIGHT, buff=0.02)
        lit = Rectangle(width=0.1, height=0.4, stroke_width=0, fill_color=HEAD, fill_opacity=1)
        bar = VGroup(*blocks[:n // 2], lit, *blocks[n // 2:]).arrange(RIGHT, buff=0.02).move_to(DOWN * 2.55)
        win = Rectangle(width=bw + 0.06, height=0.56, stroke_color=YES, stroke_width=3).move_to(blocks[0])
        win.shift(LEFT * 0.12)
        cap = label(r"the new file: \ every old block found again \ (blue), \ plus a few literal bytes \ (yellow)",
                    font_size=19, color=GREY_A).next_to(bar, DOWN, buff=0.15)
        with self.voiceover(
            "Andrew Tridgell and Paul Mackerras's rsync, from 1996, fixes this with a rolling hash. <bookmark "
            "mark='a'/> The receiver hashes each of its blocks twice, once weakly and once strongly, and sends the "
            "list. <bookmark mark='b'/> The sender slides a window over its new file one byte at a time, looking "
            "for any old block at any offset. <bookmark mark='c'/> The weak checksum, two running sums, updates in "
            "constant time as the window slides, like chapter two's fingerprints. <bookmark mark='d'/> Only when "
            "the weak checksum matches is the expensive strong hash checked. <bookmark mark='e'/> For our edited "
            f"Moby-Dick, {d['rsync_matched']} of the old blocks were found in place or shifted, and only about "
            "three kilobytes had to be sent as literal text."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(lines[1], shift=UP * 0.1), FadeIn(bar[:n // 2]), FadeIn(bar[n // 2 + 1:]),
                      FadeIn(win))
            self.play(win.animate.shift(RIGHT * 0.12), run_time=0.6)
            self.play(Indicate(blocks[0], color=YES), win.animate.move_to(blocks[1]), run_time=0.8)
            self.play(win.animate.move_to(blocks[2]), run_time=0.5)
            for mk, ln in zip("cd", lines[2:4]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(win.animate.move_to(lit).stretch_to_fit_width(0.5), FadeIn(lit), FadeIn(lines[4]), FadeIn(cap))
            self.play(FadeOut(win), FadeIn(lines[5]))
        self.wait(0.3)
        self.clear_scene()

    def cdc(self):
        d = load("rsync")
        head = label(r"Content-defined chunking", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"rsync needs the old file's hashes; \ a backup of a million files can't afford them", font_size=22,
                  color=WHITE),
            label(r"instead, \ let the \textbf{content} choose the cut points: \\ cut wherever a rolling hash of the "
                  r"last few bytes ends in 13 zeros", font_size=22, color=LAM),
            label(r"an insertion moves only the cuts near it: \ the chunks after it are cut in the same places",
                  font_size=22, color=YES),
            label(rf"\textit{{Moby-Dick}}: \ {d['cdc_chunks']} chunks \ (mean {d['cdc_mean'] / 1000:.1f} KB); \ after "
                  rf"the edit, \ {d['cdc_new']} new chunk \ ({d['cdc_new_bytes'] / 1000:.0f} KB)", font_size=24,
                  color=HEAD),
            label(r"store each chunk once, \ by its hash: \ LBFS (2001), \ restic, \ Borg, \ Dropbox, \ and data "
                  r"deduplication everywhere", font_size=21, color=GREY_A),
        )
        lines[:3].arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.45)
        lines[3:].arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.45)
        W = 12.4

        def chunks(sizes, red=()):
            tot = sum(sizes)
            g = VGroup()
            for k, z in enumerate(sizes):
                col = NO if k in red else DATA
                g.add(Rectangle(width=max(W * z / tot - 0.012, 0.006), height=0.45, stroke_width=0, fill_color=col,
                                fill_opacity=1.0 if k in red else (0.85 if k % 2 else 0.5)))
            return g.arrange(RIGHT, buff=0.012)
        old_c = chunks(d["cdc_sizes_old"]).move_to(DOWN * 0.45)
        new_c = chunks(d["cdc_sizes_new"], set(d["cdc_new_idx"])).move_to(DOWN * 1.45)
        lo = label(r"the old file, \ cut where the content says", font_size=18, color=GREY_A).next_to(old_c, UP,
                                                                                                  buff=0.1)
        ln = label(r"the new file: \ the same cuts, \ except around the insertion", font_size=18,
                   color=GREY_A).next_to(new_c, DOWN, buff=0.1)
        with self.voiceover(
            "rsync needs the old file's block hashes, and a backup system with millions of files can't afford to "
            "keep them all. <bookmark mark='a'/> Content-defined chunking turns the idea around. Let the content "
            "choose where to cut: run a rolling hash over the bytes, and cut wherever its value ends in thirteen "
            "zeros, which with a minimum chunk size comes about every ten kilobytes. <bookmark mark='b'/> An insertion changes the hash only "
            "near it, so the cuts after it fall in the same places as before. <bookmark mark='c'/> Moby-Dick cut "
            f"into {d['cdc_chunks']} chunks; after our edit, exactly one chunk was new, fourteen kilobytes. "
            "<bookmark mark='d'/> Store each chunk once, under its hash, and a thousand nightly backups of a "
            "slowly changing disk cost little more than one. This is how deduplicating backup tools and cloud "
            "file sync work."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(FadeIn(lines[1], shift=UP * 0.1), FadeIn(lo),
                      LaggedStart(*[FadeIn(c) for c in old_c], lag_ratio=0.02), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(lines[2], shift=UP * 0.1), FadeIn(new_c), FadeIn(ln))
            vo.wait_until("c")
            self.play(FadeIn(lines[3], shift=UP * 0.1), *[Indicate(new_c[k], color=NO, scale_factor=1.6)
                                                         for k in d["cdc_new_idx"]])
            vo.wait_until("d")
            self.play(FadeIn(lines[4], shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
