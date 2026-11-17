from __future__ import annotations

import numpy as np

from videos.psychology.psych13.common import *  # noqa: F403


class Retina(VoiceoverScene):
    def construct(self):
        self.card()
        self.rate()
        self.kuffler()
        self.dog()
        self.mach()
        self.why()

    def card(self):
        card = chapter_card(4, r"The retina sends differences", r"What does one fibre of the optic nerve report?",
                            lit={1926: r"Adrian", 1953: r"Kuffler"}, part=PART, scale=("neuron", "circuit"), marr=("how",))
        with self.voiceover("Chapter four. The retina sends differences."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def rate(self):
        d = load("rate")
        head = heading(r"The code of a single fibre")
        A = axes([0, 1], [0, 3.6], x_length=6.0, y_length=2.6, xticks=[0, 0.5, 1], yticks=None,
                 xlabel=r"time (s)", center=[-3.2, 0.7, 0])
        ax = A.ax
        trains = VGroup()
        for i, (L, ts) in enumerate(d["trains"].items()):
            y0 = 0.4 + 1.1 * i
            trains.add(VGroup(*[Line(ax.c2p(float(t), y0), ax.c2p(float(t), y0 + 0.75), color=CENTRE, stroke_width=2)
                                for t in ts]))
            trains.add(label(rf"load {float(L):g}", font_size=20, color=GREY_A).next_to(ax.c2p(0, y0 + 0.37), LEFT, buff=0.15))
        B = axes([0, 10], [0, 110], x_length=4.6, y_length=2.4, xticks=[0, 5, 10], yticks=[0, 50, 100],
                 xlabel=r"seconds of steady stretch", ylabel=r"impulses/s", center=[3.9, 0.7, 0])
        bx = B.ax
        ad = VGroup(*[curve(bx, d["t"], v, c, stroke_width=4) for (k, v), c in zip(d["adapt"].items(), (GREY_B, CENTRE))])
        rows = rows_of([
            (r"Adrian and Zotterman, \ 1926: \ one stretch receptor in a frog's muscle, \ weights hung from it", WHITE),
            (r"every impulse the same size: \ a heavier weight makes them more frequent, \ not bigger", CENTRE),
            (r"and while the weight stays on, \ the rate falls: \ the fibre reports change more than state", GREY_A),
        ], 12.4, 27, 0.26).to_edge(DOWN, buff=0.95)
        tags = VGroup(historical_tag(archive.ADRIAN_1926.cite), psyche_tag(r"schematic: \ spikes drawn from a rate"))
        with self.voiceover(
            "First, what is there to send? <bookmark mark='a'/> In 1926 Edgar Adrian and Yngve Zotterman cut a "
            "frog's muscle down until a single stretch receptor was left in it, hung weights from it, and recorded "
            "its nerve fibre. <bookmark mark='b'/> Every impulse was the same size. A heavier weight made them more "
            "frequent, not bigger. Strength is coded as a rate. <bookmark mark='c'/> And while the weight stayed on, "
            "the rate fell away. The fibre reported change more faithfully than it reported a steady state. Six "
            "years later, Haldan Keffer Hartline found the same rate code in a single fibre from the eye of a "
            "horseshoe crab. Part 5 told this as history; today it enters the Ledger."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tags))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(A))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t) for t in trains], lag_ratio=0.3), FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(B), LaggedStart(*[Create(c) for c in ad], lag_ratio=0.4), FadeIn(rows[2]), run_time=2.5)
        self.clear_scene()

    def kuffler(self):
        head = heading(r"Kuffler's cat, \ 1953: \ a centre and a surround")

        def field(on: bool):
            c = CENTRE if on else SURROUND
            s = SURROUND if on else CENTRE
            ring = Annulus(inner_radius=0.7, outer_radius=1.5, fill_color=s, fill_opacity=0.25, stroke_width=0)
            mid = Circle(radius=0.7, fill_color=c, fill_opacity=0.45, stroke_width=0)
            sign_c = MathTex("+" if on else "-", font_size=48, color=c)
            sign_s = VGroup(*[MathTex("-" if on else "+", font_size=30, color=s).move_to(1.1 * np.array([np.cos(a), np.sin(a), 0]))
                              for a in np.linspace(0, TAU, 8, endpoint=False)])
            return VGroup(ring, mid, sign_c, sign_s)

        on, off = field(True).move_to([-4.2, 0.6, 0]), field(False).move_to([-1.0, 0.6, 0])
        lon = label(r"on-centre", font_size=26, color=CENTRE).next_to(on, DOWN, buff=0.2)
        loff = label(r"off-centre", font_size=26, color=SURROUND).next_to(off, DOWN, buff=0.2)
        rows = rows_of([
            (r"a spot of light in the centre: \ the on-centre cell fires faster", CENTRE),
            (r"in the ring around it: \ it falls silent", SURROUND),
            (r"light everywhere: \ the two cancel, \ and the cell barely changes", WHITE),
            (r"off-centre cells are the mirror image; \ together they report brighter-than and darker-than", GREY_A),
        ], 5.6, 27, 0.32).move_to([3.7, 0.2, 0])
        keep_in_frame(rows)
        tag = published_tag(archive.KUFFLER_1953.cite)
        with self.voiceover(
            "In 1953 Stephen Kuffler recorded from single ganglion cells, the retina's output neurons, whose fibres "
            "form the optic nerve, in the eyes of cats. Each cell watches a small patch of the visual field, its "
            "receptive field, and the patch has two parts. <bookmark mark='a'/> A spot of light in the centre made "
            "an on-centre cell fire faster. <bookmark mark='b'/> The same spot in a ring around the centre made it "
            "fall silent. <bookmark mark='c'/> Light the whole field evenly, and centre and surround cancel: the cell "
            "hardly changes. <bookmark mark='d'/> Off-centre cells are the mirror image. Between them they report "
            "where a patch is brighter, or darker, than its surroundings."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(on), FadeIn(lon))
            vo.wait_until("a")
            self.play(Indicate(on[1], color=CENTRE), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Indicate(on[0], color=SURROUND), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(off), FadeIn(loff), FadeIn(rows[3]))
        self.clear_scene()

    def dog(self):
        d = load("retina")
        head = heading(r"A centre minus a surround: \ the difference of Gaussians")
        A = axes([-12, 12], [-0.12, 0.3], x_length=5.6, y_length=2.8, xticks=[-10, 0, 10], yticks=[0, 0.2],
                 xlabel=r"position", ylabel=r"weight", center=[-3.5, 0.85, 0])
        ax = A.ax
        x = d["x"]
        cen = curve(ax, x, np.exp(-x ** 2 / (2 * 1.5 ** 2)) / (1.5 * np.sqrt(2 * np.pi)), CENTRE, stroke_width=3)
        sur = curve(ax, x, -np.exp(-x ** 2 / (2 * 4.5 ** 2)) / (4.5 * np.sqrt(2 * np.pi)), SURROUND, stroke_width=3)
        dog = curve(ax, x, d["prof"], WHITE, stroke_width=5)
        B = axes([np.log10(0.005), np.log10(0.5)], [0, 1.05], x_length=5.0, y_length=2.8,
                 xticks=[np.log10(v) for v in (0.01, 0.1)], yticks=[0, 0.5, 1], xfmt=lambda v: f"{10 ** v:g}",
                 xlabel=r"spatial frequency (cycles per unit)", ylabel=r"gain", center=[3.6, 0.85, 0])
        bx = B.ax
        c_only = curve(bx, np.log10(d["f"]), d["centre_only"], CENTRE, stroke_width=3)
        band = curve(bx, np.log10(d["f"]), d["resp"], WHITE, stroke_width=5)
        eq = MathTex(r"w(x) = \underbrace{G_{\sigma_c}(x)}_{\text{centre}} - \underbrace{G_{\sigma_s}(x)}_{\text{surround}}",
                     font_size=34).to_edge(DOWN, buff=1.65)
        rows = rows_of([
            (r"low frequencies (broad, even light): \ centre and surround cancel; \ high frequencies: \ blurred by the "
             r"centre. \ What passes is a band in between", WHITE),
        ], 12.4, 26, 0.3).to_edge(DOWN, buff=0.7)
        tag = psyche_tag(r"computed: \ Rodieck's model (1965)")
        with self.voiceover(
            "There's a neat mathematical description, due to Robert Rodieck in 1965. <bookmark mark='a'/> Model the "
            "centre as a narrow bell curve of positive weight, <bookmark mark='b'/> the surround as a wider, shallower "
            "bell of negative weight, <bookmark mark='c'/> and the cell's receptive field as their difference: a "
            "Mexican hat. The cell's response is the light weighted by this profile and summed. "
            "<bookmark mark='d'/> Now ask how such a filter treats gratings of different fineness. A centre alone "
            "passes coarse patterns and blurs fine ones. <bookmark mark='e'/> Subtract the surround, and coarse "
            "patterns, broad even light, cancel too. What passes is a band of middle frequencies. The retina is a "
            "band-pass filter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(cen))
            vo.wait_until("b")
            self.play(Create(sur))
            vo.wait_until("c")
            self.play(Create(dog), FadeIn(eq))
            vo.wait_until("d")
            self.play(FadeIn(B), Create(c_only))
            vo.wait_until("e")
            self.play(Create(band), FadeIn(rows[0]))
        self.clear_scene()

    def mach(self):
        d = load("retina")
        head = heading(r"Mach bands, \ computed")
        n = len(d["m_in"])
        strip = np.tile(d["m_in"][None, :], (60, 1))
        img = picture(strip, 1.3, smooth=True).move_to([0, 2.2, 0]).stretch_to_fit_width(10.0)
        A = axes([0, n - 1], [0, 1], x_length=10.0, y_length=2.2, xticks=None, yticks=[0, 0.5, 1],
                 xlabel=r"position", center=[0, -0.35, 0])
        ax = A.ax
        xs = np.arange(n)
        lum = curve(ax, xs, d["m_in"], GREY_B, stroke_width=4)
        out = d["m_out"]
        sc = (out - out[200]) / (out.max() - out.min()) * 0.8 + 0.5
        resp = curve(ax, xs, sc, CENTRE, stroke_width=5)
        lg = legend([(GREY_B, r"the light"), (CENTRE, r"the filter's output (scaled)")], font_size=21).move_to(ax.c2p(60, 0.85))
        rows = rows_of([
            (r"a dark plateau, \ a ramp, \ a light plateau: \ most people see a darker stripe at the ramp's foot and a "
             r"brighter one at its top \ (Ernst Mach, \ 1865)", WHITE),
            (r"the filter overshoots at exactly those corners: \ the bands are the code showing through", CENTRE),
        ], 12.4, 25, 0.22).to_edge(DOWN, buff=0.75)
        tag = psyche_tag(r"computed: \ the light through a difference of Gaussians")
        with self.voiceover(
            "You can see this filter at work. <bookmark mark='a'/> Here is a dark plateau, a ramp, and a light "
            "plateau. Most people see a narrow stripe at the foot of the ramp that's darker than the plateau, and one "
            "at the top that's brighter. Ernst Mach described them in 1865. They are not in the light: the light, in "
            "grey, has no dips or peaks. <bookmark mark='b'/> Pass it through the difference of Gaussians, and the "
            "output overshoots at exactly those two corners. The bands you see are the code showing through. Part 6 "
            "drew them with lateral inhibition; this is the same idea written as a filter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(img), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lum), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(resp), FadeIn(lg), FadeIn(rows[1]))
        self.clear_scene()

    def why(self):
        d = load("retina")
        head = heading(r"Why send differences?")
        a = picture(d["img"], 3.0, smooth=True, lo=-2.5, hi=2.5).move_to([-4.6, 0.5, 0])
        b = picture(d["out"], 3.0, smooth=True, lo=-2.5, hi=2.5).move_to([-1.0, 0.5, 0])
        la = label(rf"neighbours two apart: \ $r = {d['corr_in']:.2f}$", font_size=22, color=GREY_A).next_to(a, DOWN, buff=0.15)
        lb = label(rf"after the filter: \ $r = {d['corr_out']:.2f}$", font_size=22, color=CENTRE).next_to(b, DOWN, buff=0.15)
        rows = rows_of([
            (r"natural images are redundant: \ a point is usually much like its neighbours", WHITE),
            (r"sending every point's brightness wastes the optic nerve's million fibres on what could be predicted", GREY_A),
            (r"subtract the neighbourhood, \ and what is left is the surprise: \ edges, \ textures, \ change", CENTRE),
            (r"the same idea compresses images and sound (Part 58 returns to it, \ as efficient coding)", LIGHT),
        ], 5.4, 26, 0.32).move_to([4.0, 0.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ a texture with natural images' $1/f$ spectrum")
        with self.voiceover(
            "Why would an eye do this? <bookmark mark='a'/> Because natural images are redundant. In this texture, "
            "built with the statistics of natural scenes, points two pixels apart are correlated at about point six. "
            "Knowing one, you can largely guess the other. <bookmark mark='b'/> Sending every point's brightness "
            "would spend the optic nerve's million or so fibres largely on things that could be predicted. "
            "<bookmark mark='c'/> Subtract the neighbourhood, and what's left is the surprise: edges, textures, "
            "change. After the filter, the correlation falls to about point one. <bookmark mark='d'/> It's the "
            "principle behind most of the compression of images and sound you use every day. Part 58 returns to it "
            "under its proper name, efficient coding."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(a), FadeIn(la))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(b), FadeIn(lb), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
