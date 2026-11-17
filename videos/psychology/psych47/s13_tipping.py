from __future__ import annotations

from videos.psychology.psych47.common import *  # noqa: F403


class Tipping(VoiceoverScene):
    def construct(self):
        self.card()
        self.slowing()
        self.rates()
        self.windows()

    def card(self):
        card = chapter_card(12, r"Tipping points", r"Can a mind warn before it tips?",
                            lit={2009: r"Scheffer et al.", 2014: r"van de Leemput et al."}, part=PART,
                            scale=("person",), marr=("how",))
        with self.voiceover("Chapter twelve. Tipping points."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def slowing(self):
        d = load("tipping")
        head = heading(r"Critical slowing down")
        T = len(d["x"])
        A = axes([0, T], [-1.8, 1.8], x_length=6.0, y_length=1.9, xticks=None, yticks=[-1, 0, 1],
                 yfmt=lambda v: f"{v:g}", ylabel=r"state", center=[-3.0, 1.4, 0], font_size=12)
        B = axes([0, T], [0.6, 1.0], x_length=6.0, y_length=1.6, xticks=None, yticks=[0.7, 0.9],
                 yfmt=lambda v: f"{v:g}", ylabel=r"autocorrelation", center=[-3.0, -1.2, 0], font_size=12)
        step = 4
        xs = np.arange(0, T, step)
        cx = curve(A.ax, xs, d["x"][::step], PERSON, stroke_width=2)
        ok = np.isfinite(d["ac"])
        idx = np.arange(T)[ok][::step]
        idx = idx[idx < d["tip"]]
        ca = curve(B.ax, idx, d["ac"][idx], AUTH, stroke_width=3)
        tip = DashedLine(A.ax.c2p(d["tip"], -1.8), A.ax.c2p(d["tip"], 1.8), color=GREY_B, stroke_width=1.5)
        rows = rows_of([
            (r"Psyche: \ a mood that sits in a low valley; \ slowly, \ the valley flattens, \ until the state tips "
             r"into another", WHITE),
            (r"before the tip, \ the system recovers more slowly from each nudge: \ moments resemble the moments "
             r"before them", MODEL),
            (rf"so autocorrelation and variance rise: \ Kendall's $\tau$ for the trend, \ {d['tau_ac']:.2f} and "
             rf"{d['tau_var']:.2f}", AUTH),
            (r"Scheffer and colleagues found the signature in lakes, \ climates and fisheries; \ van de Leemput and "
             r"colleagues, \ 2014, \ looked for it in mood", GOOD),
        ], 5.6, 19, 0.38).move_to([3.6, -0.1, 0])
        tag = psyche_tag(r"\texttt{within.double\_well}, \ \texttt{rolling\_indicators}")
        with self.voiceover(
            "Some changes are not gradual. <bookmark mark='a'/> Psyche builds a mood that sits in a low valley. "
            "Slowly, the valley flattens, until the state tips into another. <bookmark mark='b'/> Before the tip, "
            "the system recovers more slowly from each small nudge, so each moment resembles the ones before it. "
            "<bookmark mark='c'/> Autocorrelation and variance rise. It's called critical slowing down. "
            "<bookmark mark='d'/> Marten Scheffer and colleagues found the signature before transitions in lakes, "
            "climates and fisheries. In 2014 Ingrid van de Leemput and colleagues looked for it in mood."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(B), Create(cx), FadeIn(tip))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(ca))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def rates(self):
        d = load("tipping")
        head = heading(r"Warnings, \ and false alarms")
        A = axes([0.3, 4.7], [0, 0.7], x_length=5.4, y_length=3.0, xticks=None, yticks=[0, 0.25, 0.5],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"share warned", center=[-3.3, 0.3, 0], font_size=13)
        b = bars(A.ax, [1, 2, 3, 4], [d["hit"], d["false_alarm"], d["diary_hit"], d["diary_false"]],
                 [GOOD, AUTH, GOOD, AUTH], width=0.6)
        names = VGroup(*[wrapped_label(t, 1.3, 11, GREY_A).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.1) for i, t in
                         enumerate((r"tipped, \ continuous record", r"never tipped, \ continuous record",
                                    r"tipped, \ daily diary", r"never tipped, \ daily diary"))])
        rows = rows_of([
            (rf"with a long continuous record, \ a rising autocorrelation warns before {100 * d['hit']:.0f}\% of "
             rf"tips, \ and almost never when nothing tips", GOOD),
            (rf"with a noisy daily diary of the same lives, \ warnings come before {100 * d['diary_hit']:.0f}\% of "
             rf"tips, \ and in {100 * d['diary_false']:.0f}\% of people who never tip", AUTH),
            (r"a single person followed through a relapse showed the signal (Wichers and colleagues); \ prospective "
             r"tests in many people have found it weak", PERSON),
            (r"the theory is sound; \ whether a mood is such a system, \ and whether diaries can see it in time, \ is "
             r"open: \ the Ledger says contested", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{within.warning\_rates}, \ 100 simulated lives each")
        with self.voiceover(
            "Can it warn in time? <bookmark mark='a'/> With a long, continuous record, a rising autocorrelation "
            "warns before more than half of the tips, and almost never when nothing tips. <bookmark mark='b'/> With a "
            "noisy daily diary of the same lives, warnings come before a quarter of the tips, and in about one in six "
            "people who never tip. <bookmark mark='c'/> A single person followed through a relapse showed the "
            "signal. Prospective tests in many people have found it weak. <bookmark mark='d'/> The theory is sound. "
            "Whether a mood is such a system, and whether diaries can see the signal in time, is open. The Ledger "
            "says contested."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(b[0]), FadeIn(b[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[2]), FadeIn(b[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def windows(self):
        d = load("windows")
        head = heading(r"The analyst's window")
        A = axes([0, 540], [0, 0.8], x_length=5.6, y_length=3.0, xticks=[100, 200, 300, 500], yticks=[0, 0.25, 0.5, 0.75],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"rolling window (time steps)",
                 ylabel=r"", center=[-3.3, 0.3, 0], font_size=13)
        ch = curve(A.ax, d["window"], d["hit"], GOOD, stroke_width=4)
        cf = curve(A.ax, d["window"], d["false_alarm"], AUTH, stroke_width=4)
        key = VGroup(label(r"warnings before a tip", font_size=13, color=GOOD),
                     label(r"false alarms", font_size=13, color=AUTH)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.3)
        rows = rows_of([
            (r"a fresh set of 60 lives that tip and 60 that never do; \ only the width of the rolling window changes", WHITE),
            (rf"a narrow window (100 steps) warns before {100 * d['hit'][0]:.0f}\% of tips; \ a wide one (500) before "
             rf"{100 * d['hit'][-1]:.0f}\%", GOOD),
            (rf"but false alarms rise too, \ from {100 * d['false_alarm'][0]:.0f}\% to "
             rf"{100 * d['false_alarm'][-1]:.0f}\%", AUTH),
            (r"window, \ detrending and threshold are forks: \ fix them before the data, \ or the warning is found "
             r"after the fact", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{within.warning\_rates}, \ continuous records")
        with self.voiceover(
            "One choice the analyst makes changes the answer. <bookmark mark='a'/> A fresh set of sixty lives that tip, and "
            "sixty that never do. Only the width of the rolling window changes. <bookmark mark='b'/> A narrow window "
            "warns before almost no tips. A wide one before seven in ten. <bookmark mark='c'/> But false alarms rise "
            "too, from about two percent to about twelve. <bookmark mark='d'/> The window, the detrending and the "
            "threshold are all forks in the garden. Fix them before the data, or the warning is found after the fact."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(ch))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(cf))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
