from __future__ import annotations

from videos.psychology.psych18.common import *  # noqa: F403


class Capacity(VoiceoverScene):
    def construct(self):
        self.card()
        self.race()
        self.report()

    def card(self):
        card = chapter_card(10, r"Capacity as a race", r"How much can one glance take in?",
                            lit={1960: r"Sperling", 1990: r"Bundesen"}, part=PART, scale=("mind",),
                            marr=("what", "how"))
        with self.voiceover("Chapter ten. Capacity as a race."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def race(self):
        head = heading(r"Bundesen's theory of visual attention")
        eq = MathTex(r"v(x, i)", r"=", r"\eta(x, i)\,\beta_i", r"\,\frac{w_x}{\sum_z w_z}", font_size=46)
        eq[0].set_color(ATT)
        eq[3].set_color(CONTROL)
        eq.move_to([0, 2.1, 0])
        notes = rows_of([
            (r"$v(x, i)$: \ the rate at which item $x$ is encoded as belonging to category $i$", ATT),
            (r"$\eta\,\beta$: \ the sensory evidence, \ and a bias toward the categories you are looking for", WHITE),
            (r"$w_x / \sum w$: \ item $x$'s share of attention; \ the shares add to one", CONTROL),
            (r"items race to be encoded; \ the winners fill a short-term store of about four slots", CUE),
            (r"two numbers per person: \ total processing capacity $C$, \ and storage $K$", MODEL),
        ], 12.4, 26, 0.32).move_to([0, -0.85, 0])
        tag = historical_tag(archive.BUNDESEN_1990.cite)
        with self.voiceover(
            "If attention selects, how much can it select at once, and how fast? <bookmark mark='a'/> Claus "
            "Bundesen's theory of visual attention, from 1990, answers with a race. Every item in a display races to "
            "be encoded into short-term memory, and the rate for item x as an instance of category i is written as one "
            "product. <bookmark mark='b'/> The sensory evidence that x looks like an i, times a bias toward the "
            "categories you care about, red things or letters. <bookmark mark='c'/> Times x's share of attention: "
            "each item gets a weight, and the shares are normalized to add to one, so attending to more items gives "
            "each one less. <bookmark mark='d'/> Encoding times are random, the fastest finish first, and the "
            "winners fill a short-term store of about four slots. <bookmark mark='e'/> The theory turns a person's "
            "attention into two numbers to measure: C, how many items per second they can process in total, and K, "
            "how many they can hold. It has been used to measure attention in patients with brain damage and in "
            "children with reading difficulties."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Write(eq))
            for m, r in zip("abcde", notes):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def report(self):
        d = load("tva")
        head = heading(r"Whole report: \ how many letters from a brief flash")
        A = axes([0, 300], [0, 4.4], x_length=6.0, y_length=3.4, xticks=[0, 100, 200, 300], yticks=[0, 2, 4],
                 xlabel=r"exposure, \ ms, \ then a mask", ylabel=r"letters reported", center=[-2.5, 0.5, 0],
                 font_size=17)
        ax = A.ax
        c6 = curve(ax, d["e"], d["six"], ATT, 4)
        c2 = curve(ax, d["e"], d["two"], CUE, 4)
        kline = DashedLine(ax.c2p(0, 4), ax.c2p(300, 4), color=GREY_C, stroke_width=1.5)
        kl = label(r"$K = 4$", font_size=18, color=GREY_B).next_to(ax.c2p(300, 4), UP, buff=0.05).align_to(
            ax.c2p(300, 4), RIGHT)
        t0 = DashedLine(ax.c2p(20, 0), ax.c2p(20, 4.4), color=GREY_D, stroke_width=1.5)
        t0l = label(r"$t_0$", font_size=18, color=GREY_B).next_to(ax.c2p(20, 4.4), UP, buff=0.05)
        lg = legend([(ATT, r"six letters shown"), (CUE, r"two letters shown")], font_size=19)
        lg.next_to(ax.c2p(150, 1.2), RIGHT, buff=0.2)
        rows = rows_of([
            (r"below a threshold time $t_0$, \ nothing is encoded", GREY_A),
            (r"the curve's initial slope is the capacity $C$, \ in items a second", ATT),
            (r"its ceiling is the storage $K$, \ when there are more items than slots", CUE),
            (r"fitted to a person's curve, \ the two numbers separate speed from storage", MODEL),
        ], 5.6, 24, 0.4).move_to([3.9, 0.2, 0])
        ptag = psyche_tag(r"\texttt{attention.tva\_whole\_report}: \ $C$ = 30 items/s, \ $t_0$ = 20 ms, \ $K$ = 4")
        tag = historical_tag(archive.BUNDESEN_1990.cite)
        with self.voiceover(
            "The measurement is old and simple. Flash some letters, then a mask, and ask for as many as you can "
            "report. George Sperling's work in 1960 showed that far more is briefly available than can be reported. "
            "<bookmark mark='a'/> In the race model, below a minimum exposure, t-zero, nothing gets encoded. "
            "<bookmark mark='b'/> After that, the number reported climbs, at first in proportion to the capacity C. "
            "<bookmark mark='c'/> Then it levels off at K, if there are more letters than slots; with only two "
            "letters, the curve tops out at two. <bookmark mark='d'/> Fit the curve for one person and you get their "
            "speed and their storage separately, two things that a single accuracy score mixes together."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(ptag))
            vo.wait_until("a")
            self.play(Create(t0), FadeIn(t0l), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(c6), Create(c2), FadeIn(lg), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(kline), FadeIn(kl), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
