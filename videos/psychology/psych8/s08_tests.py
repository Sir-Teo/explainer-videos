from __future__ import annotations

import numpy as np

from videos.psychology.psych8.common import *  # noqa: F403


class Tests(VoiceoverScene):
    def construct(self):
        self.card()
        self.nothing()
        self.rules()
        self.trade()
        self.cluster()

    def card(self):
        card = chapter_card(7, r"A hundred thousand tests", r"Where do you draw the line on a map?",
                            lit={2009: r"the salmon", 2016: r"cluster failure"}, part=PART, scale=("brain",),
                            marr=("how",))
        with self.voiceover(
            "Chapter seven. A hundred thousand tests."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def nothing(self):
        d, s = load("tests"), load("salmon")
        head = heading(r"A brain with nothing in it")
        tm = heat(np.clip(d["null_t"], 0, None), 3.6, 0.0, 8.0, mask=d["mask"], center=[-5.0, -0.2, 0])
        hm = hits_map(d["null_hit"], d["mask"], None, 3.6, center=[-5.0, -0.2, 0], color=THRESH)
        tl = label(r"its map of $t$", font_size=28, color=GREY_A).next_to(tm, UP, buff=0.12)
        hl = label(r"voxels with $p < 0.001$", font_size=28, color=THRESH).next_to(hm, UP, buff=0.12)
        A = axes([0, 5.2], [0, 1.05], x_length=4.6, y_length=3.3, xticks=[0, 1, 2, 3, 4, 5], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: rf"10^{{{int(v)}}}", yfmt=lambda v: pct(v), xlabel=r"number of tests",
                 ylabel=r"chance of at least one false alarm", center=[0.1, -0.45, 0])
        ax = A.ax
        c = curve(ax, np.log10(s["n"]), s["chance"], THRESH, stroke_width=4)
        here = VGroup(Dot(ax.c2p(np.log10(d["voxels"]), d["chance_formula"]), radius=0.08, color=WHITE),
                      label(r"this slice", font_size=26).next_to(ax.c2p(np.log10(d["voxels"]), d["chance_formula"]), DR, buff=0.06))
        rows = rows_of([
            (rf"{fmt_int(d['voxels'])} voxels of noise: \ expect {d['expected_false']:.1f} to pass", WHITE),
            (rf"1{{,}}000 such brains: \ {pct(d['rate_uncorrected'])} show at least one ``active'' voxel", THRESH),
            (r"a whole brain is about 100{,}000 voxels: \ about 100 false ones, every time", BAD),
        ], 4.0, 29, 0.3).move_to([5.0, -0.3, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"simulated: brains of noise (Psyche)")
        with self.voiceover(
            "Take the synthetic brain and switch its two patches off. Now it's a brain in which nothing "
            "responds to the task. A salmon. <bookmark mark='a'/> Fit the model in every voxel, and apply "
            "the rule that was common in 2009: a voxel is active if it passes at one in a thousand. "
            "<bookmark mark='b'/> This is the first such brain we generated, and there's a voxel lit. "
            f"With {d['voxels']:,} tests at one in a thousand you expect "
            f"{d['expected_false']:.1f} to pass by luck. <bookmark mark='c'/> We made a thousand of these "
            f"empty brains. {100 * d['rate_uncorrected']:.0f} percent of them show something. That's "
            "below what independent tests would give, because neighbouring voxels move together, but "
            "it's nowhere near the five percent a reader assumes. <bookmark mark='d'/> And this is one "
            "slice. A whole brain is about a hundred thousand voxels. At one in a thousand, that's about a "
            "hundred false voxels in every study, in every brain, dead or alive. The salmon wasn't a "
            "fluke. It was the expected result."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tm), FadeIn(tl))
            vo.wait_until("b")
            self.play(FadeOut(tm), FadeOut(tl), FadeIn(hm), FadeIn(hl), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(A), Create(c), FadeIn(here), FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[2], shift=UP * 0.1))
        self.clear_scene()

    def rules(self):
        d = load("tests")
        head = heading(r"Three ways to draw the line honestly")
        items = [
            (r"control the chance of \emph{any} false voxel", r"Bonferroni: \ test each voxel at $0.05 / N$",
             d["rate_bonferroni"], EEGC),
            (r"control the \emph{share} of coloured voxels that are false",
             r"false discovery rate: \ let the cut-off depend on how many pass", d["rate_fdr"], MODEL),
            (r"ask for a \emph{patch}, not a voxel", r"cluster inference: \ a low bar, \ but many neighbours must pass together",
             d["rate_cluster"], BLOOD),
        ]
        ask = label(r"Of 1{,}000 empty brains, \ how many show anything? \ \ Promised: \ 5\%", font_size=30,
                    color=GREY_A).move_to([0, 2.45, 0])
        rows = VGroup()
        for i, (what, how, rate, col) in enumerate(items):
            y = 1.15 - 1.4 * i
            left = VGroup(wrapped_label(what, 8.8, 31, col), wrapped_label(how, 8.8, 29, WHITE)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.1)
            left.move_to([0, y, 0]).align_to(np.array([-6.5, 0, 0]), LEFT)
            right = VGroup(label(pct(rate, 1), font_size=46, color=col),
                           label(r"of empty brains", font_size=27, color=GREY_A)).arrange(DOWN, buff=0.08)
            right.move_to([5.0, y, 0])
            rows.add(VGroup(left, right))
        base = wrapped_label(rf"with no correction: \ {pct(d['rate_uncorrected'])} of empty brains", 9.0, 31, BAD)
        base.move_to([-1.0, -2.95, 0])
        tag = psyche_tag(r"simulated: 1{,}000 brains of noise (Psyche)")
        with self.voiceover(
            "There are three standard ways to draw the line honestly, and each defines honest differently. "
            "<bookmark mark='a'/> The first says: I want only a five percent chance of even one false "
            "voxel in the whole map. The simplest version divides the threshold by the number of tests. "
            f"On our empty brains it lets something through {100 * d['rate_bonferroni']:.1f} percent of "
            "the time. <bookmark mark='b'/> The second accepts some false voxels, and controls their "
            "share: of everything I colour, no more than five percent should be wrong. That's the false "
            "discovery rate. <bookmark mark='c'/> The third changes the question. Real activity comes in "
            "patches, and noise mostly comes in specks. So set a lenient bar for each voxel, and then "
            "demand that a whole cluster of neighbours pass together. How big must the cluster be? That "
            "depends on how smooth the noise is, and we'll come back to that. <bookmark mark='d'/> All "
            "three hold the empty brains near five percent. With no correction, it was "
            f"{100 * d['rate_uncorrected']:.0f}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(ask))
            for k, mark_ in enumerate("abc"):
                vo.wait_until(mark_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(base, shift=UP * 0.1))
        self.clear_scene()

    def trade(self):
        d = load("tests")
        head = heading(r"The price: \ what each rule finds when something is there")
        names = [("uncorrected", r"no correction", BAD), ("bonferroni", r"Bonferroni", EEGC),
                 ("fdr", r"false discovery rate", MODEL), ("cluster", r"clusters", BLOOD)]
        maps = Group()
        for i, (key, name, col) in enumerate(names):
            x = -5.25 + 3.5 * i
            hm = hits_map(d[f"map_{key}"], d["mask"], d["truth"], 2.9, center=[x, 0.55, 0], color=col)
            cap = VGroup(label(name, font_size=28, color=col),
                         label(rf"{d[f'hits_{key}']} of {d['active']} found", font_size=29, color=WHITE)).arrange(
                DOWN, buff=0.08).next_to(hm, DOWN, buff=0.14)
            maps.add(Group(hm, cap))
        end = rows_of([
            (rf"The strictest rule misses {d['active'] - d['hits_bonferroni']} of the {d['active']} true voxels. "
             r"\ Every threshold trades false alarms for misses.", WHITE),
            (r"And a voxel below the line is not a voxel where nothing happens.", P.ACCENT),
        ], 12.6, 30, 0.18).to_edge(DOWN, buff=0.45)
        tag = psyche_tag(r"the synthetic brain (Psyche)")
        with self.voiceover(
            "Corrections aren't free. Put the two patches back, and apply each rule to the same data. "
            "<bookmark mark='a'/> The lenient threshold finds nearly all of the truly active voxels, "
            f"{d['hits_uncorrected']} of {d['active']}. On this brain it happened to add none that were "
            "false. On others it adds one or two. <bookmark mark='b'/> The strictest rule is safe, and it "
            f"finds {d['hits_bonferroni']}. It's missed {d['active'] - d['hits_bonferroni']}. "
            "<bookmark mark='c'/> The false discovery rate and the cluster rule sit between. "
            "<bookmark mark='d'/> This is Part 4's trade, false alarms against misses, made a hundred "
            "thousand times at once. And it's the reason for a habit worth dropping. A voxel that didn't "
            "pass isn't a voxel where nothing happened. A map shows where the evidence cleared a bar. The "
            "blank parts are mostly where it didn't, and say little about what's there."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mark_ in enumerate("ab"):
                vo.wait_until(mark_)
                self.play(FadeIn(maps[k]))
            vo.wait_until("c")
            self.play(FadeIn(maps[2]), FadeIn(maps[3]))
            vo.wait_until("d")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def cluster(self):
        c = load("cluster")
        e = archive.EKLUND_2016.data
        head = heading(r"2016: \ the cluster rule, checked against real noise")
        A = axes([0, 15], [-0.05, 1.05], x_length=5.3, y_length=3.5, xticks=[0, 5, 10, 15], yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{v:.1f}", xlabel=r"distance between two voxels", ylabel=r"how alike their noise is",
                 center=[-3.85, -0.3, 0])
        ax = A.ax
        cg = curve(ax, c["lags"], c["acf_gauss"], NOISE, stroke_width=4)
        ct = curve(ax, c["lags"], c["acf_tail"], BAD, stroke_width=4)
        lg = legend([(NOISE, r"assumed: a bell curve"), (BAD, r"real scans: a long tail")], font_size=27)
        lg.next_to(ax.c2p(15, 1.0), DL, buff=0.1)
        bars = VGroup()
        vals = [(r"noise as assumed", c["gaussian"], NOISE), (r"noise with a long tail", c["long_tail"], BAD)]
        for i, (name, v, col) in enumerate(vals):
            bar = Rectangle(width=14.0 * v, height=0.45, stroke_width=0, fill_color=col, fill_opacity=0.9)
            bar.move_to([0.4 + 7.0 * v, 1.8 - 0.75 * i, 0])
            bars.add(VGroup(bar, label(rf"{name}: \ {pct(v, 1)}", font_size=28, color=col).next_to(bar, RIGHT, buff=0.18)))
        nominal = DashedLine([0.4 + 14.0 * 0.05, 2.15, 0], [0.4 + 14.0 * 0.05, 0.7, 0], color=WHITE, stroke_width=2)
        nl = label(r"promised: \ 5\%", font_size=26).next_to(nominal, DOWN, buff=0.08).align_to(nominal, LEFT)
        bl = label(r"empty brains with at least one cluster", font_size=28, color=GREY_A).move_to([3.4, 2.6, 0])
        bl.align_to(np.array([0.4, 0, 0]), LEFT)
        rows = rows_of([
            (rf"{e['controls']} people at rest, \ cut into {e['analyses'] // 1_000_000} million fake "
             r"experiments: \ up to 70\% found a cluster", DATA),
            (r"70\% of null studies with a false cluster; \ not 70\% of findings false", WHITE),
            (r"what held up: \ thresholds set by shuffling the data itself", MODEL),
        ], 6.5, 28, 0.22).move_to([3.65, -1.55, 0])
        keep_in_frame(rows)
        src = published_tag(archive.EKLUND_2016.cite)
        tag = psyche_tag(r"plot and bars: simulated (Psyche)")
        with self.voiceover(
            "The cluster rule needs to know how big a cluster of noise can get, and for years the software "
            "worked that out from a formula. The formula assumes something about the noise: that how alike "
            "two voxels are falls off with distance like a bell curve. <bookmark mark='a'/> Real scanner "
            "noise doesn't. Its resemblance falls off more slowly, with a long tail, so noise makes "
            "bigger clumps than the formula expects. <bookmark mark='b'/> Here's that in miniature. Set the "
            f"cluster size on bell-curve noise, and empty brains pass {100 * c['gaussian']:.0f} percent of the "
            "time, close to the five that was promised. Use the same size on noise with a long tail, and "
            f"{100 * c['long_tail']:.0f} percent pass. <bookmark mark='c'/> In 2016 Anders Eklund and his "
            "colleagues ran the real test. They "
            f"took resting scans of {e['controls']} people, in whom no task was happening, and analysed "
            "them as if there'd been one, three million times, with the three most used programs. With "
            "common settings, up to seventy percent of those empty analyses found a cluster. "
            "<bookmark mark='d'/> Read that number carefully. It's the share of empty studies with at "
            "least one false cluster. It isn't the share of published findings that are false. "
            "<bookmark mark='e'/> And one method came through at five percent: shuffling the labels of "
            "the real data to find out what its own noise does. That's Part 2's permutation test. The "
            "programs, and the settings they recommend, were changed afterwards."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(A), Create(cg), FadeIn(lg[0]))
            vo.wait_until("a")
            self.play(Create(ct), FadeIn(lg[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(bl), FadeIn(bars[0]), FadeIn(nominal), FadeIn(nl))
            self.play(FadeIn(bars[1], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2], shift=UP * 0.1))
        self.clear_scene()
