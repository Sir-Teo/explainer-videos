from __future__ import annotations

from videos.psychology.psych47.common import *  # noqa: F403


class Stimuli(VoiceoverScene):
    def construct(self):
        self.card()
        self.power()
        self.grid()
        self.crisis()

    def card(self):
        card = chapter_card(5, r"Stimuli are a sample too", r"How many faces does a claim about faces need?",
                            lit={2012: r"Judd et al.", 2022: r"Yarkoni"}, part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter five. Stimuli are a sample too."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def power(self):
        d = load("stimpower")
        head = heading(r"Power comes from stimuli too")
        A = axes([0, 52], [0, 1], x_length=5.6, y_length=3.2, xticks=[8, 20, 32, 48], yticks=[0, 0.5, 0.8, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"words in the study",
                 ylabel=r"power", center=[-3.3, 0.3, 0], font_size=13)
        c = curve(A.ax, d["n_items"], d["power"], GOOD, stroke_width=4)
        dots = VGroup(*[Dot(A.ax.c2p(n, p), radius=0.07, color=GOOD) for n, p in zip(d["n_items"], d["power"])])
        rows = rows_of([
            (r"Psyche: \ a real priming effect, \ 30 participants, \ and studies with 8 to 48 words", WHITE),
            (rf"with 20 words the effect is found {100 * d['power'][2]:.0f}\% of the time; \ with 48, "
             rf"{100 * d['power'][-1]:.0f}\%", GOOD),
            (r"adding participants cannot fix this: \ the uncertainty about the words stays, \ however many people see "
             r"them", AUTH),
            (r"Judd, \ Westfall and Kenny, \ 2012: \ plan the number of stimuli as carefully as the number of "
             r"participants", MODEL),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{within.stimulus\_power}")
        with self.voiceover(
            "Stimuli limit power too. <bookmark mark='a'/> Psyche runs a real priming effect with thirty "
            "participants, in studies with eight to forty-eight words. <bookmark mark='b'/> With twenty words, the "
            "effect is found less than a third of the time. With forty-eight, about two thirds. "
            "<bookmark mark='c'/> Adding participants can't fix this. The uncertainty about the words stays, however "
            "many people see them. <bookmark mark='d'/> Charles Judd, Jacob Westfall and David Kenny made the point "
            "in 2012: plan the number of stimuli as carefully as the number of participants."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(c), FadeIn(dots))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def crisis(self):
        head = heading(r"The generalizability crisis")
        rows = rows_of([
            (r"Yarkoni, \ 2022: \ a study of ``ego depletion'' with one task, \ or of ``faces'' with twelve photographs, "
             r"\ supports a claim about that task and those photographs", WHITE),
            (r"the verbal claim is far broader than the statistical model that tests it", AUTH),
            (r"so either widen the model, \ sampling tasks, \ stimuli, \ experimenters and settings, \ and treating "
             r"them as random", GOOD),
            (r"or narrow the claim to what was sampled", PERSON),
            (r"Part 43's replications varied labs; \ few studies vary their stimuli", YOU),
        ], 12.4, 22, 0.42).move_to([0, -0.3, 0])
        tag = published_tag(r"Yarkoni (2022)")
        with self.voiceover(
            "Tal Yarkoni pushed the point further in 2022. <bookmark mark='a'/> A study of ego depletion with one "
            "task, or of faces with twelve photographs, supports a claim about that task and those photographs. "
            "<bookmark mark='b'/> The verbal claim is far broader than the statistical model that tests it. "
            "<bookmark mark='c'/> So either widen the model, sampling tasks, stimuli, experimenters and settings, and "
            "treating them as random. <bookmark mark='d'/> Or narrow the claim to what was sampled. "
            "<bookmark mark='e'/> Part 43's replications varied the labs. Few studies vary their stimuli."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def grid(self):
        d = load("powergrid")
        head = heading(r"People or items?")
        P = np.asarray(d["power"])
        cell = 1.0
        grid = VGroup()
        for i in range(P.shape[0]):
            for j in range(P.shape[1]):
                v = float(P[i, j])
                sq = Square(cell, stroke_width=1, stroke_color=BLACK,
                            fill_color=interpolate_color(ManimColor("#14181F"), ManimColor(GOOD), v / 0.7), fill_opacity=1)
                sq.move_to([-5.0 + j * cell, 1.2 - i * cell, 0])
                grid.add(VGroup(sq, label(f"{100 * v:.0f}\\%", font_size=16).move_to(sq)))
        rl = VGroup(*[label(rf"{s} people", font_size=14, color=GREY_A).next_to(grid[3 * i], LEFT, buff=0.1)
                      for i, s in enumerate(d["subj"])])
        cl = VGroup(*[label(rf"{k} words", font_size=14, color=GREY_A).next_to(grid[j], UP, buff=0.1)
                      for j, k in enumerate(d["items"])])
        rows = rows_of([
            (r"power for the same real effect, \ as participants and words both vary", WHITE),
            (r"down a column, \ more participants barely help: \ the words' variation is still there", AUTH),
            (r"along a row, \ more words help a lot", GOOD),
            (r"in designs like this, \ a study of 15 people and 40 words beats one of 120 people and 10 words", YOU),
        ], 5.6, 19, 0.38).move_to([3.6, -0.1, 0])
        tag = psyche_tag(r"\texttt{within.stimulus\_power}, \ 40 studies a cell")
        with self.voiceover(
            "So which should a study add, people or items? <bookmark mark='a'/> Here's power for the same real "
            "effect, as both vary. <bookmark mark='b'/> Down a column, more participants barely help. The words' "
            "variation is still there. <bookmark mark='c'/> Along a row, more words help a lot. <bookmark mark='d'/> "
            "In designs like this, a study of fifteen people and forty words beats one of a hundred and twenty people "
            "and ten words."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(grid), FadeIn(rl), FadeIn(cl))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
