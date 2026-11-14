from __future__ import annotations

import numpy as np

from videos.psychology.psych8.common import *  # noqa: F403


class Bold(VoiceoverScene):
    def construct(self):
        self.card()
        self.blood()
        self.echo()
        self.linear()
        self.meaning()

    def card(self):
        card = chapter_card(5, r"Blood, and a slow echo", r"What does a functional scan measure?",
                            lit={1990: r"BOLD"}, part=PART, scale=("circuit", "brain"), marr=("tissue",))
        with self.voiceover(
            "Chapter five. Blood, and a slow echo."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def blood(self):
        head = heading(r"1990: \ the signal depends on oxygen in the blood")
        vessel = VGroup(Line([-6.6, 0.9, 0], [-1.2, 0.9, 0], color=GREY_B, stroke_width=3),
                        Line([-6.6, -0.3, 0], [-1.2, -0.3, 0], color=GREY_B, stroke_width=3))
        g = np.random.default_rng(5)
        cells = VGroup(*[Ellipse(width=0.48, height=0.3, stroke_width=0, fill_color=BAD if k % 2 else NOISE,
                                 fill_opacity=0.9).move_to([-6.3 + 0.52 * k, 0.3 + g.uniform(-0.3, 0.3), 0])
                         for k in range(10)])
        fresh = VGroup(*[Ellipse(width=0.48, height=0.3, stroke_width=0, fill_color=BAD, fill_opacity=0.9).move_to(
            [-6.3 + 0.52 * k, 0.3 + g.uniform(-0.3, 0.3), 0]) for k in range(10)])
        key = VGroup(
            VGroup(Ellipse(width=0.36, height=0.22, stroke_width=0, fill_color=BAD, fill_opacity=0.9),
                   label(r"carrying oxygen: \ invisible to the magnet", font_size=24, color=BAD)).arrange(RIGHT, buff=0.15),
            VGroup(Ellipse(width=0.36, height=0.22, stroke_width=0, fill_color=NOISE, fill_opacity=0.9),
                   label(r"oxygen given up: \ disturbs the field nearby", font_size=24, color=NOISE)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-3.9, -1.5, 0])
        rows = rows_of([
            (r"blood that has given up its oxygen is slightly magnetic; \ it blurs the signal around it", WHITE),
            (r"active tissue is sent more fresh blood than it uses", BLOOD),
            (r"so, where neurons work harder, \ the signal \emph{rises}, \ by a percent or so", BLOOD),
            (r"blood-oxygen-level-dependent: \ BOLD", THRESH),
        ], 5.6, 30).move_to([3.9, -0.2, 0])
        keep_in_frame(rows)
        src = historical_tag(archive.OGAWA_1990.cite)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "So far that's a picture of anatomy. To watch a brain work, you need something in the picture "
            "that changes when neurons are active. In 1990 Seiji Ogawa found it, in the blood. "
            "<bookmark mark='a'/> The molecule that carries oxygen in a red blood cell is magnetically "
            "quiet while it holds its oxygen. Once it's handed the oxygen over, it's slightly magnetic, and "
            "it disturbs the field around the vessel. That makes nearby protons drift out of step faster, "
            "the second kind of fading from the last chapter, and the signal there drops. "
            "<bookmark mark='b'/> Now the surprise. When a patch of brain becomes active, its vessels open "
            "and it's sent more fresh blood than it needs. The used-up blood is flushed out. "
            "<bookmark mark='c'/> So in active tissue the signal goes up, by something like one percent. "
            "<bookmark mark='d'/> It's called the blood-oxygen-level-dependent signal, BOLD. Two years "
            "later, two groups used it to watch a human brain respond to a flashing light. That's "
            "functional MRI, and it's what nearly every picture of a working brain you've seen is made of."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(vessel), FadeIn(cells), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeOut(cells, shift=RIGHT * 1.5), FadeIn(fresh, shift=RIGHT * 1.5), FadeIn(rows[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def echo(self):
        b = load("bold")
        head = heading(r"The echo: \ late, slow, and smeared")
        A = axes([0, 30], [-0.2, 1.1], x_length=7.4, y_length=4.2, xticks=[0, 5, 10, 15, 20, 25, 30],
                 yticks=[0, 0.5, 1.0], yfmt=lambda v: f"{v:.1f}", xlabel=r"seconds after a brief burst of neural activity",
                 ylabel=r"BOLD response", center=[-2.8, -0.6, 0])
        ax = A.ax
        c = curve(ax, b["t"], b["hrf"], BLOOD, stroke_width=5)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(30, 0), color=GREY_D, stroke_width=2)
        burst = Line(ax.c2p(0, 0), ax.c2p(0, 1.05), color=SPIKE, stroke_width=6)
        peak = VGroup(Dot(ax.c2p(b["peak_s"], 1.0), radius=0.08, color=WHITE),
                      label(rf"peak: \ {b['peak_s']:.0f} s", font_size=26).next_to(ax.c2p(b["peak_s"], 1.0), RIGHT, buff=0.25))
        under = label(r"a dip below the start", font_size=27, color=GREY_A).next_to(ax.c2p(22.5, 0.0), UP, buff=0.3)
        rows = rows_of([
            (r"the neurons are done in a fraction of a second", SPIKE),
            (rf"the blood's response peaks {b['peak_s']:.0f} seconds later", BLOOD),
            (r"and takes some 20 seconds to settle", BLOOD),
            (r"one image every second or two: \ fMRI sees \emph{where}, to millimetres, \ and \emph{when} "
             r"only to seconds", P.ACCENT),
        ], 4.4, 28, 0.3).move_to([4.8, -0.4, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: the canonical response")
        with self.voiceover(
            "And here's what that signal does in time. <bookmark mark='a'/> Suppose the neurons in a voxel "
            "fire a brief burst, over in a fraction of a second. <bookmark mark='b'/> For the first second "
            "or two, nothing. Then the fresh blood arrives, and the signal climbs to a peak about "
            f"{b['peak_s']:.0f} seconds after the neurons have finished. <bookmark mark='c'/> It falls "
            "back, dips a little below where it started, and takes twenty seconds or so to settle. "
            "<bookmark mark='d'/> So functional MRI doesn't see neurons. It sees a slow echo of them, in "
            "the plumbing. Compare the EEG: timing to the millisecond, and no secure place. This is the "
            "opposite bargain. Place to a few millimetres, and timing to a few seconds. There's no "
            "instrument yet that gives you both from outside the head."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(zero))
            vo.wait_until("a")
            self.play(Create(burst), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(c), run_time=6.0, rate_func=linear)
            self.play(FadeIn(peak), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(under), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def linear(self):
        b = load("bold")
        head = heading(r"The working assumption: \ responses add")
        A = axes([0, 100], [-0.3, 2.6], x_length=11.6, y_length=3.3, xticks=[0, 20, 40, 60, 80, 100], yticks=[0, 1, 2],
                 xlabel=r"time (s)", ylabel=r"predicted BOLD", center=[0.0, -0.35, 0])
        ax = A.ax
        sticks = VGroup(*[Line(ax.c2p(float(o), 0), ax.c2p(float(o), 0.7), color=SPIKE, stroke_width=5) for o in b["onsets"]])
        resp = curve(ax, b["scans"], b["response"], BLOOD, stroke_width=4.5)
        ghost = VGroup(*[curve(ax, b["t"] + float(o), b["hrf"], GREY_B, stroke_width=1.8) for o in b["onsets"]])
        lg = legend([(SPIKE, r"events"), (GREY_B, r"one echo for each"), (BLOOD, r"their sum: the prediction")], font_size=24)
        lg.next_to(A, UP, buff=0.15)
        eq = VGroup(label(r"prediction", font_size=32, color=BLOOD), label(r"$=$", font_size=34),
                    label(r"events", font_size=32, color=SPIKE), label(r"$\ast$", font_size=38),
                    label(r"the echo", font_size=32, color=GREY_A)).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.5)
        src = published_tag(archive.BOYNTON_1996.cite)
        tag = psyche_tag(r"computed")
        with self.voiceover(
            "To get from that echo to an experiment, you need one assumption, and it's a strong one. "
            "<bookmark mark='a'/> Suppose every event in the experiment, each picture, each word, sets "
            "off the same echo. <bookmark mark='b'/> And suppose echoes simply add. Then three events "
            "close together give a single hump, more than twice as high as one echo and smeared in time. "
            "<bookmark mark='c'/> If that's true, you can predict the whole time course of a voxel from "
            "nothing but the times of the events. Mathematically it's a convolution: the events, combined "
            "with the echo. <bookmark mark='d'/> Is it true? It was tested in the visual cortex in 1996, "
            "and it holds well, though not perfectly: very brief events give a bit more than their share. "
            "Nearly every functional imaging study rests on this line. It's the same move as Part 5's "
            "equations, a model of the instrument, and it deserves the same question. Does it predict what "
            "it wasn't fitted to?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(src), FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(s) for s in sticks], lag_ratio=0.3), FadeIn(ghost, lag_ratio=0.3), FadeIn(lg[0]),
                      FadeIn(lg[1]), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(resp), FadeIn(lg[2]), run_time=4.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(eq, shift=UP * 0.1))
            vo.wait_until("d")
        self.clear_scene()

    def meaning(self):
        head = heading(r"What the echo follows")
        ch = chain([r"input arriving at synapses", r"local processing", r"impulses sent out", r"blood flow", r"BOLD"],
                   [EEGC, EEGC, SPIKE, BLOOD, BLOOD], width=13.0, font_size=25, height=1.2).move_to([0, 1.3, 0])
        brace = VGroup(Line(ch.boxes[0].get_corner(DL) + DOWN * 0.15, ch.boxes[1].get_corner(DR) + DOWN * 0.15,
                            color=THRESH, stroke_width=5),
                       label(r"BOLD follows these most closely", font_size=26, color=THRESH))
        brace[1].next_to(brace[0], DOWN, buff=0.12)
        rows = rows_of([
            (r"2001: \ electrodes and a scanner on the same patch of a monkey's cortex", WHITE),
            (r"the signal tracked the currents of input and local processing better than the cells' output", THRESH),
            (r"So a bright voxel means: \ more synaptic work here. \ It does not say whether the region is "
             r"driving, being driven, or being held back.", P.ACCENT),
        ], 12.6, 30, 0.28).move_to([0, -2.0, 0])
        src = published_tag(archive.LOGOTHETIS_2001.cite)
        with self.voiceover(
            "One more link, and it's the one most often forgotten. What neural event does the blood "
            "follow? <bookmark mark='a'/> In 2001 Nikos Logothetis and his colleagues recorded with "
            "electrodes and a scanner at once, from the same patch of a monkey's visual cortex. "
            "<bookmark mark='b'/> The BOLD signal followed the slow currents, the ones that reflect input "
            "arriving at the synapses and being worked on locally, better than it followed the impulses "
            "the cells sent out. <bookmark mark='c'/> So a bright voxel means that more synaptic work is "
            "going on there, and synaptic work is what costs energy. It doesn't tell you that the region is "
            "sending a message. And inhibition is synaptic work too. A region that's being held down hard "
            "can light up. Keep that in mind when a headline says a region was activated."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(ch))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(brace), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2], shift=UP * 0.1))
        self.clear_scene()
