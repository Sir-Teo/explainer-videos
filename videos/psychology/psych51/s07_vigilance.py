from __future__ import annotations

from videos.psychology.psych51.common import *  # noqa: F403


class Vigilance(VoiceoverScene):
    def construct(self):
        card_section(self, 6, r"The watch", r"Why does attention fail over a long watch?")
        self.decline()
        self.sdt()
        self.one()

    def decline(self):
        d = load("vigilance")
        head = heading(r"Two hours at the clock")
        A = axes([0, 130], [0, 1.0], x_length=5.6, y_length=3.0, xticks=[30, 60, 90, 120], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"minutes into the watch",
                 ylabel=r"share detected", center=[-3.3, 0.3, 0], font_size=12)
        x = np.asarray(d["block_end"]) - 15
        c = curve(A.ax, x, d["hit"], PERSON, stroke_width=4)
        dots = VGroup(*[Dot(A.ax.c2p(t, h), radius=0.08, color=PERSON) for t, h in zip(x, d["hit"])])
        rows = rows_of([
            (r"Psyche's watchers: \ 60 of them, \ two hours each, \ a double jump about one time in eighty", WHITE),
            (rf"first half hour: \ {100 * d['hit'][0]:.0f}\% of signals detected; \ last half hour: \ "
             rf"{100 * d['hit'][-1]:.0f}\%", AUTH),
            (r"Mackworth found the fall begins within the first half hour; \ later work found it in radar, \ sonar, \ "
             r"airport screening and quality control", PERSON),
            (r"it is not boredom alone: \ watching for rare signals is hard, \ stressful work (Warm and colleagues)", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.vigilance}, \ 60 simulated watchers")
        with self.voiceover(
            "Here's the decrement Mackworth found. <bookmark mark='a'/> Psyche's sixty watchers spend two hours each "
            "at the clock, with a double jump about one time in eighty. <bookmark mark='b'/> In the first half hour "
            "they detect about seventy-three percent of the signals. In the last half hour, under half. "
            "<bookmark mark='c'/> Mackworth found the fall begins within the first half hour, and later work found it "
            "in radar, sonar, airport screening and quality control. <bookmark mark='d'/> And it isn't boredom alone. "
            "Watching for rare signals is hard, stressful work."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(c), FadeIn(dots))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def sdt(self):
        d = load("vigilance")
        head = heading(r"Sensitivity, \ or criterion?")
        x = np.asarray(d["block_end"]) - 15
        A1 = axes([0, 130], [1.8, 2.8], x_length=4.2, y_length=2.4, xticks=[30, 60, 90, 120], yticks=[2, 2.5],
                  xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"minutes", ylabel=r"$d'$",
                  center=[-4.2, 0.5, 0], font_size=12)
        A2 = axes([0, 130], [0.4, 1.3], x_length=4.2, y_length=2.4, xticks=[30, 60, 90, 120], yticks=[0.5, 1.0],
                  xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"minutes", ylabel=r"criterion $c$",
                  center=[0.6, 0.5, 0], font_size=12)
        cd = curve(A1.ax, x, d["d"], MODEL, stroke_width=4)
        cc = curve(A2.ax, x, d["c"], AUTH, stroke_width=4)
        rows = rows_of([
            (r"Part 12's tools on each half hour: \ hits and false alarms give $d'$ and $c$", WHITE),
            (rf"$d'$ falls from {d['d'][0]:.2f} to {d['d'][-1]:.2f}: \ the watcher discriminates less well", MODEL),
            (rf"$c$ rises from {d['c'][0]:.2f} to {d['c'][-1]:.2f}: \ the watcher also says ``signal'' less readily; \ "
             rf"false alarms fall", AUTH),
            (r"the meta-analysis of See and colleagues: \ which one moves depends on the task; \ the remedies differ "
             r"(rest and aids for sensitivity, \ feedback and expectations for criterion)", YOU),
        ], 12.4, 19, 0.28).move_to([0, -2.4, 0])
        tag = published_tag(r"See et al.\ (1995)").to_corner(UR, buff=0.3)
        with self.voiceover(
            "Is it sensitivity or criterion? Part 12's tools can tell. <bookmark mark='a'/> For each half hour, hits "
            "and false alarms give d prime and the criterion. <bookmark mark='b'/> Here d prime falls: the watcher "
            "discriminates less well. <bookmark mark='c'/> And the criterion rises: the watcher also says signal less "
            "readily, so false alarms fall too. In Psyche, both were planted. <bookmark mark='d'/> In real watches, the "
            "meta-analysis by Joel See and colleagues found that which one moves depends on the task, and the remedies "
            "differ: rest and aids for sensitivity, feedback and expectations for criterion."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A1), FadeIn(A2))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(cd))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(cc))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def one(self):
        d = load("onewatch")
        rows_section(self, r"One watcher's record", [
            (rf"the same watch for a single watcher: \ detections by half hour {', '.join(f'{100 * h:.0f}' for h in d['hit'])}\%",
             WHITE),
            (r"with about seven signals per half hour, \ one record jumps around: \ the decline is real, \ but one "
             r"person's curve cannot show it reliably", AUTH),
            (r"Part 47's lesson again: \ group curves describe the task; \ individual curves need many more signals", MODEL),
            (r"which is why fitness-for-duty tests from a few minutes of data are weak", YOU),
        ], "One caution. <bookmark mark='a'/> Here's the same watch for a single watcher, by half hour. "
           "<bookmark mark='b'/> With about seven signals per half hour, one record jumps around. The decline is real, "
           "but one person's curve can't show it reliably. <bookmark mark='c'/> It's Part 47's lesson again. Group "
           "curves describe the task, and individual curves need many more signals. <bookmark mark='d'/> That's why "
           "fitness-for-duty tests from a few minutes of data are weak.", tag=psyche_tag(r"\texttt{work.vigilance}, \ "
                                                                                          r"one watcher"))
