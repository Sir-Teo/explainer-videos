from __future__ import annotations

import numpy as np

from videos.music.music56.common import *  # noqa: F403

PC = {"XY": TUNE, "Blumlein": BLUE, "ORTF": EAR, "NOS": "#A3E635", "AB": GREY_A}


class Arrays(SoundScene):
    def construct(self):
        chapter(self, 2, r"Stereo microphone pairs", r"Where on the loudspeakers does a pair put each instrument?")
        self.pairs()
        self.cues()
        self.images()
        self.heard()
        self.choosing()

    # ------------------------------------------------------------------
    def pairs(self):
        d = load("arrays")["pairs"]
        rows = VGroup(VGroup(label(r"pair", font_size=17, color=GREY_A), label(r"capsules", font_size=17, color=GREY_A),
                             label(r"angle between", font_size=17, color=GREY_A), label(r"spacing", font_size=17, color=GREY_A)))
        pat = {1.0: r"omnis", 0.5: r"cardioids", 0.0: r"figure-8s"}
        for k in ("XY", "Blumlein", "ORTF", "NOS", "AB"):
            v = d[k]
            rows.add(VGroup(label(k, font_size=20, color=PC[k]), label(pat[v["A"]], font_size=19, color=WHITE), label(rf"{2 * v['angle']:.0f}$^\circ$", font_size=19, color=WHITE),
                            label(rf"{100 * v['spacing']:.0f} cm", font_size=19, color=WHITE)))
        rows.arrange(DOWN, buff=0.28)
        for r in rows:
            for i, m in enumerate(r):
                m.set_x(-4.5 + 3.0 * i)
        rows.move_to(DOWN * 0.1)
        note = label(r"coincident pairs make level differences; \ spaced pairs, \ time differences; \ near-coincident pairs, \ both", font_size=18, color=TUNE).to_edge(DOWN, buff=0.4)
        head = label(r"five stereo pairs", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Part 55 named the stereo pairs; here they are computed. <bookmark mark='a'/> XY: two cardioids at the same point, "
            "ninety degrees apart. Blumlein's pair: two figure-8s, also ninety degrees apart. ORTF, French radio's choice: "
            "two cardioids a hundred and ten degrees apart and seventeen centimetres apart, about the width of a head. NOS, "
            "Dutch radio's: ninety degrees and thirty centimetres. And AB: two omnis sixty centimetres apart. "
            "<bookmark mark='b'/> Coincident pairs make only level differences; spaced pairs only time differences; "
            "near-coincident pairs both."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(ghost(rows[1:], 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:]], lag_ratio=0.25), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cues(self):
        d = load("arrays")
        th = np.array(d["theta"])
        k0 = (th >= 0)
        a1 = frame_axes(width=5.0, height=2.6, xlo=0, xhi=90, ylo=0, yhi=25, center=LEFT * 3.3 + DOWN * 0.3)
        a2 = frame_axes(width=5.0, height=2.6, xlo=0, xhi=90, ylo=0, yhi=2.0, center=RIGHT * 3.3 + DOWN * 0.3)
        c1 = VGroup(*[curve(th[k0], np.clip(np.array(d["pairs"][k]["dL"])[k0], 0, 25), a1.to, color=PC[k], width=2.5) for k in ("XY", "Blumlein", "ORTF", "NOS")])
        c2 = VGroup(*[curve(th[k0], np.array(d["pairs"][k]["dt"])[k0], a2.to, color=PC[k], width=2.5) for k in ("ORTF", "NOS", "AB")])
        t1 = label(r"level difference, \ dB", font_size=17, color=GREY_A).next_to(a1, UP, buff=0.15)
        t2 = label(r"time difference, \ ms", font_size=17, color=GREY_A).next_to(a2, UP, buff=0.15)
        xt = VGroup(*[label(f"{v}$^\\circ$", font_size=13, color=GREY_A).next_to(a.to(v, lo), DOWN, buff=0.08) for a, lo in ((a1, 0), (a2, 0)) for v in (0, 45, 90)])
        yt = VGroup(*[label(f"{v:g}", font_size=13, color=GREY_A).next_to(a1.to(0, v), LEFT, buff=0.08) for v in (0, 10, 20)],
                    *[label(f"{v:g}", font_size=13, color=GREY_A).next_to(a2.to(0, v), LEFT, buff=0.08) for v in (0, 1, 2)])
        key = VGroup(*[label(k, font_size=16, color=PC[k]) for k in ("XY", "Blumlein", "ORTF", "NOS", "AB")]).arrange(RIGHT, buff=0.6).to_edge(UP, buff=1.0)
        note = label(r"a source's angle off the centre line, \ left; \ the Blumlein pair's difference is infinite at 45$^\circ$, \ in one capsule's null", font_size=17, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"what each pair turns direction into", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "What does each pair turn a direction into? <bookmark mark='a'/> On the left, the level difference between its "
            "channels as a source moves from the centre to ninety degrees to one side. The coincident cardioids of XY reach "
            "only about fifteen decibels at the side; Blumlein's figure-8s shoot up, because at forty-five degrees the source "
            "sits in one capsule's null. <bookmark mark='b'/> On the right, the time difference: zero for coincident pairs; "
            "half a millisecond for ORTF, nearly one for NOS, and one point seven five for AB's sixty centimetres."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key), FadeIn(a1), FadeIn(a2), FadeIn(t1), FadeIn(t2), FadeIn(xt), FadeIn(yt), FadeIn(note), FadeIn(ghost(VGroup(c1, c2), 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c_) for c_ in c1], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c_) for c_ in c2], lag_ratio=0.3), run_time=1.8)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def images(self):
        d = load("arrays")
        th = np.array(d["theta"])
        k0 = th >= 0
        ax = frame_axes(width=7.4, height=3.0, xlo=0, xhi=90, ylo=0, yhi=1.05, center=LEFT * 1.6 + DOWN * 0.4)
        cs = VGroup(*[curve(th[k0], np.array(d["pairs"][k]["pos"])[k0], ax.to, color=PC[k], width=3) for k in ("XY", "Blumlein", "ORTF", "NOS", "AB")])
        xt = VGroup(*[label(f"{v}$^\\circ$", font_size=14, color=GREY_A).next_to(ax.to(v, 0), DOWN, buff=0.1) for v in (0, 30, 60, 90)])
        yt = VGroup(label(r"centre", font_size=14, color=GREY_A).next_to(ax.to(0, 0), LEFT, buff=0.1), label(r"one loudspeaker", font_size=14, color=GREY_A).next_to(ax.to(0, 1), LEFT, buff=0.1))
        sra = VGroup(label(r"recording angle", font_size=17, color=GREY_A))
        for k in ("Blumlein", "AB", "NOS", "ORTF", "XY"):
            v = d["pairs"][k]["sra"]
            sra.add(label(rf"{k}: \ {v:.0f}$^\circ$" if v < 179 else rf"{k}: \ 180$^\circ$ +", font_size=18, color=PC[k]))
        sra.arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.6)
        eq = MathTex(r"\text{image} \approx \frac{\Delta L}{15\,\text{dB}} + \frac{\Delta t}{1.1\,\text{ms}} \quad (\text{at most } 1)", font_size=30, color=TUNE).to_edge(UP, buff=1.0)
        note = label(r"a rule of thumb from listening tests \ (Simonsen; \ Williams); \ more careful charts give ORTF about 100$^\circ$", font_size=16, color=WHITE).to_edge(DOWN, buff=0.35)
        head = label(r"where the images fall", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Where does a listener hear each source? <bookmark mark='a'/> Listening tests, by Simonsen and others, collected "
            "by Michael Williams, found that about fifteen decibels of level difference, or about one point one milliseconds "
            "of time difference, puts an image fully in one loudspeaker, and that the two trade roughly in proportion. "
            "<bookmark mark='b'/> Apply the rule to each pair: the image's position against the source's angle. "
            "<bookmark mark='c'/> The angle at which a source reaches the loudspeaker, doubled, is the pair's recording angle: "
            f"the width of stage it spreads between the loudspeakers. Blumlein's pair, {say(d['pairs']['Blumlein']['sra'])} "
            f"degrees; AB, {say(d['pairs']['AB']['sra'])}; ORTF, {say(d['pairs']['ORTF']['sra'])}, though more careful charts "
            "say about a hundred; and XY never quite reaches the loudspeakers at all. A pair is chosen for the width of what it "
            "has to record."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(yt), FadeIn(ghost(cs, 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(eq), FadeIn(note))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c_) for c_ in cs], lag_ratio=0.25), run_time=2.2)
            vo.wait_until("c")
            self.play(FadeIn(sra))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("arrays")
        c = clip("arrays.three")
        order = d["order"]
        lines = VGroup()
        dots = []
        for i, k in enumerate(order):
            y = 1.2 - 1.3 * i
            ln = Line([-3.0, y, 0], [3.0, y, 0], color=GREY_D, stroke_width=2)
            spk = VGroup(Square(side_length=0.24, stroke_color=GREY_B, stroke_width=2).move_to([-3.2, y, 0]), Square(side_length=0.24, stroke_color=GREY_B, stroke_width=2).move_to([3.2, y, 0]))
            nm = label(k, font_size=20, color=PC[k]).move_to([-4.6, y, 0])
            ds = VGroup()
            for name, col in (("piano", BLUE), ("vox", TUNE), ("guitar", "#A3E635")):
                pos = d["stage_pos"][k][name]
                ds.add(Dot([-3.0 * pos, y, 0], radius=0.12, color=col))
            dots.append(ds)
            lines.add(VGroup(ln, spk, nm, ds))
        key = VGroup(label(r"piano, \ 40$^\circ$ left", font_size=16, color=BLUE), label(r"voice, \ centre", font_size=16, color=TUNE),
                     label(r"guitar, \ 40$^\circ$ right", font_size=16, color="#A3E635")).arrange(RIGHT, buff=0.7).to_edge(UP, buff=1.0)
        note = label(r"each row: \ the loudspeakers, \ and where the rule puts the three instruments", font_size=16, color=GREY_A).to_edge(DOWN, buff=1.25)
        head = label(r"one stage, \ three pairs", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Hear it, with headphones. Our piano forty degrees to the left, the voice in the centre, the guitar forty degrees to "
            "the right, recorded by an XY pair, an ORTF pair and an AB pair, and played on two loudspeakers. The rule puts the "
            "instruments where the dots are."
        ):
            self.play(FadeIn(head), FadeIn(key), FadeIn(lines), FadeIn(note))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"XY, \ ORTF, \ AB", kind="physical model", detail=r"three pairs, \ two loudspeakers, \ headphones", corner=DL, tag_corner=DR)
            for i, k in enumerate(order):
                end = st[order[i + 1]] - 0.3 if i + 1 < len(order) else c.duration
                pulse(snd, lines[i], st[k], end, buff=0.1)
        with self.voiceover(
            "XY keeps the instruments close together, a narrow stage, but sharply placed. ORTF spreads them most of the way. "
            "AB throws piano and guitar into the loudspeakers, and its images are wide and a little vague, because time "
            "differences are heard less precisely than level differences."
        ):
            self.play(Indicate(lines[1], color=EAR, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def choosing(self):
        items = [
            (r"coincident pairs: \ sharp images, \ and they sum to mono cleanly, \ with no time differences to comb", WHITE),
            (r"spaced pairs: \ spacious, \ enveloping, \ but vaguer, \ and they comb when summed to mono", WHITE),
            (r"the Decca tree \ (1950s): \ three omnis in a triangle over an orchestra, \ the centre one filling the middle", WHITE),
            (r"spot microphones close to soloists, \ delayed to match the main pair and mixed in a little", WHITE),
            (r"in pop, \ the pair is usually the room; \ the instruments get a close microphone each, \ and are placed by the mix", TUNE),
        ]
        rows_scene(self, r"choosing a pair", items,
                   "So how do engineers choose? <bookmark mark='b'/> Coincident pairs give sharp images, and sum to mono cleanly, "
                   "because there are no time differences to comb. <bookmark mark='c'/> Spaced pairs give spaciousness and "
                   "envelopment, but vaguer images, and they comb when summed. <bookmark mark='d'/> Decca's engineers in the 1950s "
                   "hung three omnis in a triangle over the orchestra, the centre one filling the middle: the Decca tree. "
                   "<bookmark mark='e'/> Spot microphones close to soloists are delayed to match the main pair and mixed in a "
                   "little. <bookmark mark='f'/> And in pop, the pair is usually the room: each instrument gets a close "
                   "microphone, and is placed by the mix.", marks="bcdef")
