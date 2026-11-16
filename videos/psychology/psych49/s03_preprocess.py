from __future__ import annotations

from videos.psychology.psych49.common import *  # noqa: F403


class Preprocess(VoiceoverScene):
    def construct(self):
        self.card()
        self.steps()
        self.motion()
        self.smoothing()

    def card(self):
        card = chapter_card(2, r"Preprocessing", r"What is done to a scan before it is analysed?", lit=(), part=PART,
                            scale=("brain",), marr=("how",))
        with self.voiceover("Chapter two. Preprocessing."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def steps(self):
        head = heading(r"Four steps before any statistics")
        items = [
            (r"slice timing", r"a volume is taken slice by slice over a second or two; \ shift each slice's series "
                              r"to a common time", SYMP),
            (r"motion correction", r"realign every volume to the first; \ the movement estimates are kept, \ because "
                                   r"realignment cannot undo all of what motion did", AUTH),
            (r"registration", r"map each brain onto a template, \ so that voxel $v$ means the same place in "
                              r"everyone", MODEL),
            (r"smoothing", r"blur with a Gaussian kernel a few millimetres wide: \ less noise, \ better overlap "
                           r"between people, \ coarser maps", PERSON),
        ]
        rows = VGroup()
        for name, what, col in items:
            rows.add(VGroup(word_chip(name, col, 22, width=3.4), wrapped_label(what, 8.6, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, -0.2, 0])
        tag = published_tag(r"Poldrack, \ Mumford \& Nichols (2011)")
        with self.voiceover(
            "Before any statistics, four steps. <bookmark mark='a'/> Slice timing. A volume is taken slice by slice, "
            "over a second or two, so each slice's series is shifted to a common time. <bookmark mark='b'/> Motion "
            "correction. Every volume is realigned to the first, and the movement estimates are kept, because "
            "realignment can't undo everything motion did. <bookmark mark='c'/> Registration. Each brain is mapped "
            "onto a template, so that a voxel means the same place in everyone. <bookmark mark='d'/> And smoothing: a "
            "blur a few millimetres wide, which cuts noise and helps people overlap, at the price of coarser maps. "
            "Every step has options, and each option is a fork."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def motion(self):
        d = load("motion")
        head = heading(r"Head motion makes connections")
        A = axes([0, 1], [-0.02, 0.06], x_length=5.6, y_length=3.0, xticks=[0, 0.5, 1], yticks=[0, 0.02, 0.04],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"distance between two regions",
                 ylabel=r"connectivity, \ movers minus still", center=[-3.3, 0.3, 0], font_size=12)
        zero = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(1, 0), color=GREY_B, stroke_width=1.5)
        c_raw = curve(A.ax, d["dist"], d["diff_raw"], AUTH, stroke_width=4)
        c_cen = curve(A.ax, d["dist"], d["diff_censored"], GOOD, stroke_width=4)
        key = VGroup(label(r"all scans", font_size=13, color=AUTH),
                     label(r"moving scans removed", font_size=13, color=GOOD)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.3)
        rows = rows_of([
            (r"Psyche: \ 80 people with identical brains; \ half move their heads more, \ in brief jerks", WHITE),
            (r"a jerk changes the signal in nearby regions together: \ near pairs look more connected in the movers, "
             r"\ far pairs less", AUTH),
            (r"a group that moves more (children, \ patients, \ older adults) shows a ``finding'' that is only motion",
             PERSON),
            (r"remove the moving scans, \ and the difference vanishes; \ Power and colleagues found exactly this "
             r"pattern in 2012", GOOD),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{neurodata.motion\_connectivity}")
        tag2 = published_tag(r"Power et al.\ (2012)").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Motion matters most where people differ. <bookmark mark='a'/> Psyche makes eighty people with identical "
            "brains. Half move their heads more, in brief jerks. <bookmark mark='b'/> A jerk changes the signal in "
            "nearby regions together, so near pairs look more connected in the movers, and far pairs a little less. "
            "<bookmark mark='c'/> Any group that moves more, such as children, patients, or older adults, shows a "
            "finding that's only motion. <bookmark mark='d'/> Remove the moving scans, and the difference vanishes. "
            "Jonathan Power and colleagues found exactly this pattern in real data in 2012, and some published "
            "differences in connectivity had to be revisited."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), FadeIn(A), FadeIn(zero), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(c_raw))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), Create(c_cen))
        self.clear_scene()

    def smoothing(self):
        d = load("multiverse")
        head = heading(r"How wide a blur?")
        S = np.asarray(d["by_smoothing"])
        A = axes([0.3, 5.7], [0, 1.05], x_length=6.2, y_length=3.0, xticks=None, yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"pipelines saying yes", center=[-3.0, 0.3, 0],
                 font_size=12)
        cols = [SYMP, MODEL, PERSON]
        groups = VGroup()
        for h in range(5):
            groups.add(bars(A.ax, [h + 1 - 0.22, h + 1, h + 1 + 0.22], [S[k, h] for k in range(3)], cols, width=0.2))
        names = VGroup(*[label(rf"H{h + 1}", font_size=14, color=GREY_A).next_to(A.ax.c2p(h + 1, 0), DOWN, buff=0.1)
                         for h in range(5)])
        key = VGroup(*[label(rf"{float(s):g} voxels", font_size=13, color=c) for s, c in zip(d["smoothings"], cols)])
        key.arrange(RIGHT, buff=0.4).next_to(A, UP, buff=0.3)
        rows = rows_of([
            (r"the same 72 pipelines, \ split by how much they smooth; \ the regions are discs eight voxels across",
             WHITE),
            (r"no smoothing finds the mid-sized effects most often here", SYMP),
            (r"a blur wider than the region spreads its signal into the silent tissue around it, \ and the largest "
             r"effect is found by fewer than a third of the widest-blur pipelines", PERSON),
            (r"the right kernel depends on the size of what you look for: \ the matched-filter rule", YOU),
        ], 5.6, 19, 0.38).move_to([3.7, -0.1, 0])
        with self.voiceover(
            "How wide should the blur be? <bookmark mark='a'/> Take the same seventy-two pipelines, split by how much "
            "they smooth. The planted regions are discs eight voxels across, and the blur is measured in voxels too. <bookmark mark='b'/> Here, no smoothing "
            "finds the middle-sized effects most often. <bookmark mark='c'/> A blur wider than the region spreads its "
            "signal into the silent tissue around it, and even the largest effect is found by fewer than a third of "
            "the widest-blur pipelines. <bookmark mark='d'/> The right kernel depends on the size of what you're "
            "looking for. It's the matched-filter rule from signal processing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(names), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(g) for g in groups], lag_ratio=0.2), run_time=2.0)
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
