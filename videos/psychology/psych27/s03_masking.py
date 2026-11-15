from __future__ import annotations

from videos.psychology.psych27.common import *  # noqa: F403


class Masking(VoiceoverScene):
    def construct(self):
        self.card()
        self.curves()
        self.criterion()
        self.measures()

    def card(self):
        card = chapter_card(2, r"Masking and the criterion problem", r"When is an unseen stimulus really unseen?",
                            lit={1960: r"Eriksen", 2004: r"Ramsøy \& Overgaard", 2007: r"Del Cul et al."},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter two. Masking and the criterion problem."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def curves(self):
        d = load("masking")
        head = heading(r"One representation, \ read twice")
        A = axes([0, 150], [0, 1], x_length=6.0, y_length=3.8, xticks=[0, 50, 100, 150], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"target-to-mask interval, \ ms",
                 ylabel=r"proportion", center=[-3.2, -0.3, 0], font_size=16)
        soa = d["soa"]
        acc = curve(A.ax, soa, d["middle_acc"], WHITE, 4)
        seen = curve(A.ax, soa, d["middle_p_seen"], SEEN, 4)
        uns = curve(A.ax, soa[1:], d["middle_acc_unseen"][1:], UNSEEN, 4)
        half = DashedLine(A.ax.c2p(0, 0.5), A.ax.c2p(150, 0.5), color=GREY_D, stroke_width=1.5)
        key = legend([(WHITE, r"forced choice: \ correct"), (SEEN, r"reported seen"),
                      (UNSEEN, r"correct on ``unseen'' trials")], font_size=17).move_to(A.ax.c2p(100, 0.22))
        rows = rows_of([
            (r"Psyche: \ a masked arrow gives one noisy signal; \ the longer before the mask, \ the stronger", MODEL),
            (r"a forced choice reads its sign; \ a report of seeing needs its size to pass a criterion", WHITE),
            (rf"at {d['ex_soa']:.0f} ms: \ seen on {100 * d['ex_p_seen']:.0f}\% of trials, \ yet "
             rf"{100 * d['ex_acc_unseen']:.0f}\% correct on the trials called unseen", UNSEEN),
            (r"perception without awareness, \ from one representation and a strict criterion", GNW),
        ], 5.6, 22, 0.3).move_to([3.5, -0.1, 0])
        tag = psyche_tag(r"\texttt{workspace.masking}, \ \texttt{visibility\_curve}")
        with self.voiceover(
            "Here is the logic of most masking experiments, run on Psyche. <bookmark mark='a'/> A masked arrow "
            "points left or right, and leaves one noisy signal; the longer the interval before the mask, the "
            "stronger it is. <bookmark mark='b'/> Asked to guess the direction, Psyche reads the signal's sign. "
            "Asked whether it saw anything, it says yes only when the signal's size passes a criterion. In white, "
            "accuracy rises with the interval; in blue, reports of seeing rise more slowly. "
            f"<bookmark mark='c'/> At {d['ex_soa']:.0f} milliseconds, the arrow is reported seen on only "
            f"{100 * d['ex_p_seen']:.0f} percent of trials, but on the trials called unseen, guesses are "
            f"{100 * d['ex_acc_unseen']:.0f} percent correct. <bookmark mark='d'/> That looks like perception without "
            "awareness. But there is only one representation here, and no unconscious system at all: just a strict "
            "standard for saying yes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(half))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(acc), Create(seen), FadeIn(key[:2]), FadeIn(rows[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(uns), FadeIn(key[2]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def criterion(self):
        d = load("masking")
        head = heading(r"The criterion problem")
        A = axes([0, 150], [0.45, 1.0], x_length=6.0, y_length=3.8, xticks=[0, 50, 100, 150],
                 yticks=[0.5, 0.75, 1.0], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}",
                 xlabel=r"target-to-mask interval, \ ms", ylabel=r"correct on ``unseen'' trials",
                 center=[-3.2, -0.3, 0], font_size=16)
        soa = d["soa"][1:]
        cs = VGroup(*[curve(A.ax, soa, d[f"{n}_acc_unseen"][1:], col, 4)
                      for n, col in (("strict", HOT), ("middle", UNSEEN), ("lax", SEEN))])
        key = legend([(HOT, rf"strict: \ seen if $|x| > {d['strict_c']:.1f}$"),
                      (UNSEEN, rf"middle: \ $|x| > {d['middle_c']:.1f}$"),
                      (SEEN, rf"lax: \ $|x| > {d['lax_c']:.1f}$")], font_size=17).move_to(A.ax.c2p(100, 0.58))
        rows = rows_of([
            (r"the same signal, \ three standards for saying ``seen''", WHITE),
            (rf"at {d['ex_soa']:.0f} ms, \ ``unseen'' accuracy runs from {100 * d['ex_lax_unseen']:.0f}\% to "
             rf"{100 * d['ex_strict_unseen']:.0f}\%: \ the stricter the criterion, \ the more ``unconscious "
             r"perception''", HOT),
            (r"Part 12's lesson: \ a report mixes sensitivity with a criterion; \ above-chance guessing on "
             r"unseen trials can be a strict criterion, \ not a second system", MODEL),
        ], 5.6, 22, 0.32).move_to([3.5, 0.0, 0])
        tag = psyche_tag(r"\texttt{workspace.masking}: \ three criteria")
        with self.voiceover(
            "So the size of the effect depends on how people decide to say they saw something. "
            "<bookmark mark='a'/> Here's the same signal with three standards for saying seen. "
            f"<bookmark mark='b'/> At {d['ex_soa']:.0f} milliseconds, accuracy on the unseen trials ranges from "
            f"{100 * d['ex_lax_unseen']:.0f} to {100 * d['ex_strict_unseen']:.0f} percent, depending only on the "
            "criterion. A cautious person, who calls anything faint unseen, will produce plenty of unconscious "
            "perception. <bookmark mark='c'/> It's Part 12's lesson again: a report mixes sensitivity with a "
            "criterion. Above-chance guessing on unseen trials can be a strict criterion, not a second system. "
            "This is the criterion problem, and every claim of perception without awareness has to answer it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(cs), FadeIn(key), FadeIn(rows[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def measures(self):
        head = heading(r"Measuring awareness")
        boxes = VGroup()
        for name, txt, col in [
            (r"objective", r"can you discriminate it? \ sensitivity $d'$ at chance means no information, \ "
                           r"conscious or not", SEEN),
            (r"subjective", r"did you see it? \ a graded scale: \ no experience, \ a brief glimpse, \ almost "
                            r"clear, \ clear", GNW),
            (r"metacognitive", r"does your confidence track your accuracy? \ meta-$d'$, \ Part 12; \ "
                               r"zero means guesses without insight", HOT),
        ]:
            box = RoundedRectangle(corner_radius=0.12, width=4.0, height=2.8, stroke_color=col, stroke_width=2,
                                   fill_color=BLACK, fill_opacity=0.5)
            body = VGroup(label(name, font_size=25, color=col), wrapped_label(txt, 3.5, 20, WHITE)).arrange(
                DOWN, buff=0.3).move_to(box)
            boxes.add(VGroup(box, body))
        boxes.arrange(RIGHT, buff=0.3).move_to([0, 0.8, 0])
        rows = rows_of([
            (r"Eriksen, \ 1960: \ a stimulus the observer can discriminate has not been shown to be unperceived", WHITE),
            (r"Ramsøy and Overgaard, \ 2004: \ the Perceptual Awareness Scale; \ graded reports find more glimpses "
             r"and fewer truly unseen trials than a yes or no", GNW),
            (r"Del Cul and colleagues, \ 2007: \ visibility rises steeply, \ like a threshold, \ around 50 ms", SEEN),
        ], 12.0, 23, 0.3).move_to([0, -1.8, 0])
        tag = published_tag(r"Eriksen (1960); \ Ramsøy \& Overgaard (2004); \ Del Cul, \ Baillet \& Dehaene (2007)")
        with self.voiceover(
            "There are three ways to measure awareness, and they disagree. <bookmark mark='a'/> Objective measures "
            "ask whether you can discriminate the stimulus. If sensitivity is at chance, there's no information "
            "there at all, conscious or not, so nothing unconscious is left to explain. Subjective measures ask what "
            "you saw, ideally on a graded scale. And metacognitive measures ask whether your confidence tracks your "
            "accuracy, with Part 12's meta d prime. <bookmark mark='b'/> Charles Eriksen made the sceptic's case in "
            "1960: if people can discriminate a stimulus, it hasn't been shown to be unperceived. "
            "<bookmark mark='c'/> Graded scales help. With Morten Overgaard's Perceptual Awareness Scale, people "
            "report brief glimpses that a yes-or-no question would have counted as unseen. "
            "<bookmark mark='d'/> And when Antoine Del Cul, Sylvain Baillet and Dehaene varied the masking interval "
            "finely in 2007, visibility rose steeply around fifty milliseconds, like a threshold, which brings us "
            "to blindsight."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in boxes], lag_ratio=0.7), run_time=5)
            for m, r in zip("bcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
