from __future__ import annotations

import numpy as np

from videos.psychology.psych16.common import *  # noqa: F403


class Choice(VoiceoverScene):
    def construct(self):
        self.card()
        self.matching()
        self.why()
        self.trap()

    def card(self):
        card = chapter_card(11, r"Choice", r"How do animals divide their time between two sources of reward?",
                            lit={1961: r"Herrnstein", 1979: r"Baum"}, part=PART, scale=("mind", "person"),
                            marr=("what", "how"))
        with self.voiceover("Chapter eleven. Choice."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def matching(self):
        d = load("choice")
        head = heading(r"The matching law, \ 1961")
        B, R = d["B"], d["R"]
        rb = R[:, 0] / R.sum(1)
        bb = B[:, 0] / B.sum(1)
        A = axes([0, 1], [0, 1], x_length=4.4, y_length=4.4, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                 xlabel=r"share of rewards from the left key", ylabel=r"share of pecks on the left",
                 center=[-3.6, 0.1, 0])
        ax = A.ax
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=GREY_B, stroke_width=2)
        pts = scatter(ax, rb, bb, CR, radius=0.08)
        eq = MathTex(r"\frac{B_L}{B_L + B_R} = \frac{R_L}{R_L + R_R}", font_size=42).move_to([3.4, 2.0, 0])
        rows = rows_of([
            (r"two keys, \ each paying on its own variable-interval schedule", WHITE),
            (r"pigeons divide their pecks in the proportion of the rewards each key gives", CR),
            (r"the generalized law, \ fitted on log ratios: \ sensitivity " + rf"{d['a']:.2f}" +
             r" here; \ in real data often about 0.8, \ undermatching", YOU),
        ], 5.6, 24, 0.32).move_to([3.4, -0.9, 0])
        keep_in_frame(rows)
        tag = historical_tag(archive.HERRNSTEIN_1961.cite)
        tag2 = psyche_tag(r"computed: \ \texttt{conditioning.concurrent}, \ seven pairs of schedules")
        with self.voiceover(
            "So far one response, one reward. Real animals choose. <bookmark mark='a'/> In 1961 Richard Herrnstein "
            "gave pigeons two keys, each paying off on its own variable-interval schedule, and varied how rich each "
            "one was. <bookmark mark='b'/> The pigeons divided their pecks between the keys in the same proportion as "
            "the rewards: a key giving seventy percent of the food got about seventy percent of the pecks. That's "
            "the matching law. Here it is on Psyche, for seven pairs of schedules: the points lie along the "
            "diagonal. <bookmark mark='c'/> Fitted on log ratios, the slope is the sensitivity to reward. William Baum "
            "surveyed over a hundred data sets in 1979: matching on average, with slopes often a little below one, "
            "which is called undermatching, as if the animals spread their bets a little too evenly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(diag), FadeIn(tag), FadeIn(tag2))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(eq), LaggedStart(*[FadeIn(p, scale=1.5) for p in pts], lag_ratio=0.3), FadeIn(rows[1]),
                      run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def why(self):
        d = load("choice")
        head = heading(r"Why match? \ Melioration")
        rows = rows_of([
            (r"local rate on a key: \ rewards per response there, \ $R_L / B_L$", WHITE),
            (r"melioration: \ shift your responses toward whichever key is paying better per response", CR),
            (r"you stop shifting when the local rates are equal: \ $R_L/B_L = R_R/B_R$", YOU),
            (r"and that equation is the matching law, \ rearranged", CR),
            (r"on two variable-ratio keys, \ the local rates never equalize: \ Psyche goes " +
             rf"{100 * d['B_vr'][0] / d['B_vr'].sum():.0f}" + r"\% to the richer, \ as pigeons do", US),
        ], 12.4, 28, 0.4).move_to([0, -0.1, 0])
        tag = psyche_tag(r"computed: \ \texttt{conditioning.concurrent}, \ a meliorating chooser")
        with self.voiceover(
            "Why would an animal match? Herrnstein's answer was a process he called melioration. "
            "<bookmark mark='a'/> Each key has a local rate of return: rewards per response spent on it. "
            "<bookmark mark='b'/> A meliorator moves its responses toward whichever key is paying better per "
            "response, right now. <bookmark mark='c'/> It stops moving only when the two local rates are equal. "
            "<bookmark mark='d'/> Write that down, rewards over pecks on the left equal to rewards over pecks on the "
            "right, and rearrange: it's the matching law. Psyche's chooser knows nothing about matching. It just "
            "meliorates, and matches. <bookmark mark='e'/> The same chooser on two ratio keys, where each response has "
            "a fixed chance of paying, finds that the local rates can never be equal, and drifts to the richer key "
            "almost entirely. Pigeons do that too."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def trap(self):
        d = load("choice")
        head = heading(r"When melioration is a trap")
        A = axes([0, 400], [0, 3.3], x_length=6.6, y_length=3.4, xticks=[0, 100, 200, 300, 400], yticks=[0, 1, 2, 3],
                 xlabel=r"choice", ylabel=r"payoff", center=[-2.7, 0.6, 0])
        ax = A.ax
        x = np.arange(400)
        k = np.ones(15) / 15
        sm = np.convolve(d["trap_mel"], k, mode="same")
        mel = curve(ax, x[10:-10], sm[10:-10], INHIB, 4)
        mx = curve(ax, x, d["trap_max"], CR, 4)
        lg = legend([(INHIB, rf"meliorate: \ average {d['trap_mel_mean']:.2f}"),
                     (CR, rf"always B: \ average {d['trap_max_mean']:.2f}")], font_size=20).next_to(A, DOWN, buff=0.25)
        rules = VGroup(
            MathTex(r"\text{A pays } 1 + 3f, \qquad \text{B pays } 3f", font_size=32),
            label(r"$f$: \ the share of B in your last 10 choices", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.2).move_to([3.9, 2.0, 0])
        rows = rows_of([
            (r"A always pays one more, \ right now", INHIB),
            (r"but every A lowers what both will pay", WHITE),
            (r"a meliorator chooses A, \ and ends near 1; \ choosing B every time earns 3", CR),
            (r"Herrnstein and Prelec: \ a model of addiction, \ where each dose is locally better", YOU),
        ], 4.8, 24, 0.32).move_to([3.9, -0.7, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ \texttt{conditioning.melioration\_trap}; \ 50 runs averaged")
        with self.voiceover(
            "Melioration usually works. Sometimes it's a trap. <bookmark mark='a'/> Here are two options. A always "
            "pays one point more than B, at that moment. <bookmark mark='b'/> But both pay according to f, the share "
            "of your recent choices that were B. Every time you choose A, you lower what both options will pay "
            "later. <bookmark mark='c'/> A meliorator follows the better local return, chooses A again and again, and "
            "slides down to about one point a choice. Choosing B every time, which always feels worse in the moment, "
            "earns three. <bookmark mark='d'/> Herrnstein and Drazen Prelec proposed this as a model of addiction: "
            "each drink or dose is better than the alternative at the time it's taken, while the habit lowers the "
            "value of everything, including the drug. Part 17 builds learners that look further ahead, Part 26 returns "
            "to choices over time, and Part 41 to addiction."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rules[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rules[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(mel), Create(mx), FadeIn(lg), FadeIn(rows[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
