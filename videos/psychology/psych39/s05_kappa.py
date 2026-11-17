from __future__ import annotations

from videos.psychology.psych39.common import *  # noqa: F403


class Kappa(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.trials()
        self.cap()

    def card(self):
        card = chapter_card(4, r"Two clinicians, \ one patient", r"How often do diagnosticians agree?",
                            lit={1960: r"Cohen", 1980: r"DSM-III", 2013: r"Regier et al."}, part=PART,
                            scale=("person",), marr=("what",))
        with self.voiceover("Chapter four. Two clinicians, one patient."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def derive(self):
        head = heading(r"Agreement beyond chance")
        cells = VGroup()
        vals = {(0, 0): ("20", GOOD), (0, 1): ("5", AUTH), (1, 0): ("10", AUTH), (1, 1): ("65", GOOD)}
        for (i, j), (t, c) in vals.items():
            sq = Square(side_length=1.3, stroke_color=GREY_D, fill_color="#14181F", fill_opacity=1)
            sq.move_to([-4.3 + 1.3 * j, 0.9 - 1.3 * i, 0])
            cells.add(VGroup(sq, label(t, font_size=26, color=c).move_to(sq)))
        top = VGroup(label(r"B: yes", font_size=15, color=GREY_A).move_to([-4.3, 1.8, 0]),
                     label(r"B: no", font_size=15, color=GREY_A).move_to([-3.0, 1.8, 0]))
        side = VGroup(label(r"A: yes", font_size=15, color=GREY_A).move_to([-5.5, 0.9, 0]),
                      label(r"A: no", font_size=15, color=GREY_A).move_to([-5.5, -0.4, 0]))
        eq = MathTex(r"\kappa = \frac{p_o - p_e}{1 - p_e}", font_size=40, color=MODEL).move_to([-3.8, -1.8, 0])
        rows = rows_of([
            (r"100 patients, \ two clinicians: \ they agree on 20 + 65 = 85, \ so $p_o = 0.85$", WHITE),
            (r"but A says yes 25\% of the time and B 30\%: \ by chance alone they would agree "
             r"$p_e = 0.25 \times 0.30 + 0.75 \times 0.70 = 0.60$", AUTH),
            (r"Cohen's kappa scales the agreement beyond chance by the most there could be: \ "
             r"$\kappa = (0.85 - 0.60)/(1 - 0.60) = 0.625$", MODEL),
            (r"0 is chance; \ 1 is perfect agreement; \ raw agreement flatters, \ especially for rare "
             r"conditions", YOU),
        ], 6.4, 19, 0.36).move_to([3.2, -0.2, 0])
        with self.voiceover(
            "How do you measure whether two clinicians agree? <bookmark mark='a'/> Take a hundred patients. The two "
            "agree on twenty yeses and sixty-five noes: eighty-five percent agreement. <bookmark mark='b'/> But "
            "clinician A says yes a quarter of the time, and B thirty percent. Guessing at those rates, they'd agree "
            "sixty percent of the time by chance alone. <bookmark mark='c'/> Jacob Cohen's kappa takes the agreement "
            "beyond chance, and divides by the most there could be. Point eight five minus point six, over one minus "
            "point six: point six two five. <bookmark mark='d'/> Nought is chance and one is perfect. Raw agreement "
            "flatters, especially for rare conditions, where two people saying no to everyone agree almost always."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top), FadeIn(side), FadeIn(cells))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Indicate(cells[0]), Indicate(cells[3]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(eq))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def trials(self):
        head = heading(r"The DSM-5 field trials")
        names = [r"major neurocognitive", r"autism spectrum", r"alcohol use", r"major depression",
                 r"generalized anxiety"]
        vals = [0.78, 0.69, 0.40, 0.28, 0.20]
        cols = [GOOD, GOOD, PERSON, AUTH, AUTH]
        A = axes([0, 1], [-0.6, 4.6], x_length=4.8, y_length=3.6, xticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
                 yticks=None, xfmt=lambda v: f"{v:g}", xlabel=r"kappa", center=[-2.6, -0.3, 0], font_size=14)
        bs = VGroup()
        for k, (v, c) in enumerate(zip(vals, cols)):
            y = 4 - k
            lo, hi = A.ax.c2p(0, y), A.ax.c2p(v, y)
            bs.add(Rectangle(width=max(hi[0] - lo[0], 0.01), height=0.42, stroke_width=0, fill_color=c,
                             fill_opacity=0.85).move_to([(lo[0] + hi[0]) / 2, lo[1], 0]))
        labs = VGroup(*[label(n, font_size=15, color=GREY_A).next_to(A.ax.c2p(0, 4 - k), LEFT, buff=0.15)
                        for k, n in enumerate(names)])
        vl = VGroup(*[label(f"{v:.2f}", font_size=14, color=c).next_to(b, RIGHT, buff=0.08) for v, c, b in
                      zip(vals, cols, bs)])
        note = wrapped_label(r"reported values; \ estimates differ somewhat between reports", 4.6, 13,
                             GREY_B).next_to(A, DOWN, buff=0.35)
        rows = rows_of([
            (r"Regier and colleagues, \ 2013: \ pairs of clinicians in the United States and Canada interviewed the "
             r"same patients independently", WHITE),
            (r"some diagnoses were agreed well: \ major neurocognitive disorder about 0.78, \ autism about 0.69", GOOD),
            (r"two of the commonest were not: \ major depression near 0.3, \ generalized anxiety near 0.2", AUTH),
            (r"the trials' design differed from earlier ones, \ which had reported higher kappas under easier "
             r"conditions", YOU),
        ], 5.0, 19, 0.36).move_to([4.0, -0.2, 0])
        tag = published_tag(r"Regier et al.\ (2013)")
        with self.voiceover(
            "How reliable are diagnoses now? <bookmark mark='a'/> For the fifth edition, Darrel Regier and "
            "colleagues had pairs of clinicians interview the same patients independently, across sites in the "
            "United States and Canada. <bookmark mark='b'/> Some diagnoses were agreed well: major neurocognitive "
            "disorder at about point seven eight, autism at about point seven. <bookmark mark='c'/> Two of the "
            "commonest were not: major depression near point three, and generalized anxiety near point two. "
            "<bookmark mark='d'/> The trials were designed differently from earlier ones, which had reported higher "
            "kappas under easier conditions. Still, two clinicians often disagree about whether a person is "
            "depressed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(labs), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), *[GrowFromEdge(b, LEFT) for b in bs[:3]], FadeIn(vl[:3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), *[GrowFromEdge(b, LEFT) for b in bs[3:]], FadeIn(vl[3:]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def cap(self):
        d = load("kappa")
        head = heading(r"Unreliable cannot be valid")
        A = axes([0, 2.5], [0, 1], x_length=5.0, y_length=3.4, xticks=[0, 0.5, 1, 1.5, 2, 2.5],
                 yticks=[0, 0.5, 1], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}",
                 xlabel=r"each clinician's observation noise (SD)", ylabel=r"kappa", center=[-3.4, -0.2, 0],
                 font_size=14)
        k1 = curve(A.ax, d["noise"], d["kappa"], SYMP, stroke_width=4)
        k2 = curve(A.ax, d["noise"], d["validity"], GOOD, stroke_width=4)
        key = legend([(SYMP, r"clinician with clinician"), (GOOD, r"clinician with the truth")],
                     font_size=14).move_to(A.ax.c2p(1.75, 0.85))
        i3 = int(np.argmin(np.abs(d["kappa"] - 0.3)))
        dot = Dot(A.ax.c2p(d["noise"][i3], d["kappa"][i3]), radius=0.08, color=AUTH)
        rows = rows_of([
            (r"Psyche: \ 2{,}000 patients, \ 20\% truly above a severity threshold; \ two clinicians each see "
             r"severity through their own noise", WHITE),
            (rf"as the noise grows, \ the clinicians agree less: \ at a kappa near 0.3, \ each one agrees with "
             rf"the truth only to a kappa of {d['validity'][i3]:.2f}", SYMP),
            (r"a diagnosis two clinicians cannot agree on cannot agree well with anything else: \ reliability caps "
             r"validity", AUTH),
            (r"but the reverse fails: \ two clinicians can agree perfectly on the wrong thing", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{clinic.two\_clinicians}")
        with self.voiceover(
            "Why does agreement matter so much? <bookmark mark='a'/> In Psyche, two thousand patients, a fifth of "
            "them truly above a severity threshold. Two clinicians each see severity through their own noise. "
            "<bookmark mark='b'/> As the noise grows the clinicians agree less, and each agrees less with the truth. "
            f"At a kappa near point three between them, each agrees with the truth only to a kappa of "
            f"{d['validity'][i3]:.2f}. <bookmark mark='c'/> A diagnosis two clinicians can't agree on can't agree "
            "well with anything else. Reliability caps validity. <bookmark mark='d'/> But the reverse fails. Two "
            "clinicians can agree perfectly on the wrong thing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(k1), Create(k2), FadeIn(key), run_time=2.0)
            self.play(FadeIn(dot, scale=1.5))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
