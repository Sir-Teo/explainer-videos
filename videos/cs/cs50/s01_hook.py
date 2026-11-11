from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs50.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


def postmortem(title, when, what, lesson, col, w=4.2, h=3.6):
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=col, stroke_width=2, fill_color=BG,
                             fill_opacity=1)
    t = label(title, font_size=24, color=col)
    d = label(when, font_size=17, color=GREY_B)
    body = wrapped_label(what, w - 0.4, font_size=17, color=GREY_A)
    les = wrapped_label(lesson, w - 0.4, font_size=17, color=YES)
    VGroup(t, d, body, les).arrange(DOWN, buff=0.2).move_to(frame)
    return VGroup(frame, t, d, body, les)


class Hook(VoiceoverScene):
    def construct(self):
        self.three()
        self.worst_hour()
        self.plan()

    def three(self):
        head = label(r"Three post-mortems", font_size=36).to_edge(UP, buff=0.3)
        cards = VGroup(
            postmortem(r"one mistyped input", r"Amazon S3, \ 28 February 2017",
                       r"a command meant to remove a few servers removed many more, \ including two subsystems the "
                       r"whole region's storage needed; \ restarting them took hours",
                       r"lesson: \ tools that remove capacity must do it slowly, \ and refuse to go below a floor",
                       HEAD),
            postmortem(r"one regular expression", r"Cloudflare, \ 2 July 2019",
                       r"a new firewall rule's pattern backtracked catastrophically \ (Part 12); \ pushed everywhere "
                       r"at once, \ it pinned every CPU serving web traffic",
                       r"lesson: \ roll out in stages, \ and bound the work any input can cause", NO),
            postmortem(r"one content update", r"CrowdStrike, \ 19 July 2024",
                       r"a configuration file for a security sensor made its kernel driver read out of bounds; \ about "
                       r"8.5 million Windows machines crashed and could not boot",
                       r"lesson: \ configuration is code: \ validate it, \ stage it, \ be able to roll it back", LAM),
        ).arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.45)
        src = note(r"from the companies' own public reports \ (AWS 2017, \ Cloudflare 2019, \ CrowdStrike 2024); "
                   r"\ the 8.5 million is Microsoft's estimate", font_size=16).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Three post-mortems. <bookmark mark='a'/> In February 2017 an engineer at Amazon ran a command to take a "
            "few servers out of the billing system of its storage service, S3. One input was mistyped. The command "
            "removed far more servers, including two subsystems that every request in the region depended on, and "
            "restarting them took hours. Amazon changed the tool to remove capacity slowly, and never below a "
            "safe floor. <bookmark mark='b'/> In July 2019 Cloudflare deployed a new firewall rule whose regular "
            "expression backtracked catastrophically, the failure Part 12 warned about. Pushed to every machine at "
            "once, it drove every processor serving web traffic to one hundred percent. <bookmark mark='c'/> And in "
            "July 2024 a content update for CrowdStrike's security sensor made its Windows kernel driver read memory "
            "out of bounds. About eight and a half million machines crashed, and would not boot until someone "
            "repaired each one by hand. <bookmark mark='d'/> None of these was exotic. Each was a routine change, "
            "pushed too far, too fast, with nothing to stop it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for mk, c in zip("abc", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(*[Indicate(c[4], color=YES, scale_factor=1.05) for c in cards])
        self.wait(0.4)
        self.clear_scene()

    def worst_hour(self):
        rows = {round(r["availability"], 5): r for r in load("nines")["rows"]}
        head = label(r"A year has 525{,}960 minutes", font_size=36).to_edge(UP, buff=0.3)
        W = 12.0
        bars = VGroup()
        specs = [(0.99, r"99\%", NO), (0.999, r"99.9\%", HEAD), (0.9999, r"99.99\%", YES),
                 (0.99999, r"99.999\%", DATA)]
        for a, name, col in specs:
            r = rows[a]
            year = Rectangle(width=W, height=0.42, stroke_color=GREY_C, stroke_width=1, fill_color=GREY_E,
                             fill_opacity=1)
            frac = r["per_year_min"] / 525960
            red = Rectangle(width=max(0.012, W * frac), height=0.42, stroke_width=0, fill_color=col,
                            fill_opacity=1).align_to(year, RIGHT)
            mins = r["per_year_min"]
            txt = (rf"{mins / 1440:.1f} days a year" if mins > 2880
                   else rf"{mins / 60:.1f} hours a year" if mins > 120
                   else rf"{mins:.0f} minutes a year" if mins > 3
                   else rf"{mins:.1f} minutes a year")
            name_l = label(name, font_size=22, color=col).next_to(year, LEFT, buff=0.2)
            cap = label(txt + rf", \ {r['per_month_min']:.1f} min a month" if mins < 120 else txt, font_size=19,
                        color=GREY_A).next_to(year, DOWN, buff=0.1).align_to(year, RIGHT)
            bars.add(VGroup(year, red, name_l, cap))
        bars.arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.5).shift(RIGHT * 0.5)
        foot = wrapped_label(r"each nine costs about ten times more and allows ten times less; \ a system is judged by "
                             r"its worst hours, \ so reliability is engineered as arithmetic", 12.4, font_size=20,
                             color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A system is only as good as its worst hour, so reliability is counted in minutes. A year has five "
            "hundred and twenty-five thousand, nine hundred and sixty of them. <bookmark mark='a'/> Ninety-nine "
            "percent availability allows about three and a half days of downtime a year. <bookmark mark='b'/> Three "
            "nines allows under nine hours. <bookmark mark='c'/> Four nines, under an hour, about four minutes a "
            "month. <bookmark mark='d'/> Five nines, about five minutes a year, less than the time it takes to "
            "notice a problem. <bookmark mark='e'/> Each nine costs about ten times as much as the last, and this "
            "part is about how to buy them: the arithmetic of availability, budgets for failure, defences against "
            "overload, and the instruments that tell you what actually happened."
        ) as vo:
            self.play(FadeIn(head))
            for mk, b in zip("abcd", bars):
                vo.wait_until(mk)
                self.play(FadeIn(b[0]), FadeIn(b[2]))
                self.play(GrowFromEdge(b[1], RIGHT), FadeIn(b[3]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Keeping It Running", font_size=36).to_edge(UP, buff=0.3)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"availability in series and in parallel",
            r"error budgets, \ and alerts that page only when it matters",
            r"retries that melt a system, \ and jitter that saves it",
            r"breakers, \ bulkheads, \ shedding and redundancy",
            r"metrics, \ traces and profiles that do not lie",
            r"incidents, \ chaos experiments, \ and the Job under faults",
        ], font_size=25).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 50 of Computer Science, Built. <bookmark mark='a'/> We will compose availability in series "
            "and in parallel; turn reliability into an error budget and derive the alerts that guard it; watch "
            "retries melt a system and jitter rescue it; build breakers, bulkheads and load shedding; measure with "
            "metrics, traces and profiles that do not lie; learn how incidents are run and studied; and break the "
            "Job's own service on purpose, to see what it survives."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()


_ = (KERN, LAM, NO, YES)
