from __future__ import annotations

from videos.psychology.psych42.common import *  # noqa: F403


class Dose(VoiceoverScene):
    def construct(self):
        self.card()
        self.curve_()
        self.gap()

    def card(self):
        card = chapter_card(11, r"How much therapy?", r"Is there a dose-response curve?", lit={1986: r"Howard et al."},
                            part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter eleven. How much therapy?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def curve_(self):
        d = load("dose")
        head = heading(r"The dose-response curve")
        A = axes([0, 52], [0, 1], x_length=5.6, y_length=3.2, xticks=[0, 8, 26, 52], yticks=[0, 0.5, 0.75, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"sessions",
                 ylabel=r"clients improved", center=[-3.3, 0.4, 0], font_size=13)
        c = curve(A.ax, d["sessions"], d["share"], GOOD, stroke_width=3)
        guides = VGroup(DashedLine(A.ax.c2p(8, 0), A.ax.c2p(8, 0.5), color=GREY_B, stroke_width=1.5),
                        DashedLine(A.ax.c2p(0, 0.5), A.ax.c2p(8, 0.5), color=GREY_B, stroke_width=1.5),
                        DashedLine(A.ax.c2p(26, 0), A.ax.c2p(26, 0.75), color=GREY_B, stroke_width=1.5),
                        DashedLine(A.ax.c2p(0, 0.75), A.ax.c2p(26, 0.75), color=GREY_B, stroke_width=1.5))
        rows = rows_of([
            (r"Howard and colleagues, \ 1986: \ across many samples, \ about half of clients had improved by 8 "
             r"sessions, \ and three quarters by 26", WHITE),
            (r"Psyche draws it as a log-normal curve through those two points: \ each extra session adds less", MODEL),
            (r"later work suggests clients often stop when they are ``good enough'', \ so the curve partly reflects "
             r"who stays", PERSON),
            (r"and some do not respond at all, \ which is where monitoring and a change of plan matter", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Howard et al.\ (1986)")
        with self.voiceover(
            "How much therapy is enough? <bookmark mark='a'/> In 1986 Kenneth Howard and colleagues pooled many "
            "samples. About half of clients had improved by eight sessions, and three quarters by twenty-six. "
            "<bookmark mark='b'/> Psyche draws it as a log-normal curve through those two points. Each extra session "
            "adds less. <bookmark mark='c'/> Later work suggests that clients often stop when they feel good enough, "
            "so the curve partly reflects who stays. <bookmark mark='d'/> And some don't respond at all, which is "
            "where monitoring and a change of plan matter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(guides))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(c), run_time=2.0)
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def gap(self):
        head = heading(r"Most people get none")
        rows = rows_of([
            (r"Part 39's treatment gap: \ most people with a common mental disorder receive no treatment, \ and few "
             r"receive therapy that matches the trials", WHITE),
            (r"trained therapists are scarce and expensive; \ waits are long", AUTH),
            (r"responses: \ guided self-help, \ group and digital programmes, \ and lay counsellors trained to "
             r"deliver simple therapies, \ tested in trials of their own", GOOD),
            (r"how well these scale, \ and for whom, \ is Part 57's question", YOU),
        ], 12.4, 24, 0.48).move_to([0, -0.3, 0])
        with self.voiceover(
            "And most people get none. <bookmark mark='a'/> Part 39's treatment gap: most people with a common mental "
            "disorder receive no treatment, and few receive therapy that matches what the trials tested. "
            "<bookmark mark='b'/> Trained therapists are scarce and expensive, and waits are long. "
            "<bookmark mark='c'/> The responses include guided self-help, group and digital programmes, and lay "
            "counsellors trained to deliver simple therapies, each tested in trials of its own. "
            "<bookmark mark='d'/> How well these scale, and for whom, is Part 57's question."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
