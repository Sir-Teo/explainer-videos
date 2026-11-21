from __future__ import annotations

from videos.economics.econ65.common import *  # noqa: F403

# (study, setting, measured gain in %, colour): as reported; time saved counts as a gain, extra time as a loss
STUDIES = [
    (r"Noy and Zhang \ (Science, 2023)", r"writing tasks, \ about 450 professionals", 40, r"time per task $-40\%$; "
     r"quality $+18\%$", TEXT),
    (r"Peng et al. \ (2023)", r"coding an HTTP server, \ 95 programmers", 55.8, r"time $-55.8\%$", MACH),
    (r"Dell'Acqua et al. \ (2023)", r"consulting tasks inside the frontier, \ 758 consultants", 25.1,
     r"25.1\% faster, \ 12.2\% more tasks", IDEA),
    (r"Brynjolfsson, \ Li and Raymond \ (QJE, 2025)", r"customer support, \ 5,172 agents", 14,
     r"resolutions per hour $+14\%$", GDP),
    (r"METR \ (2025)", r"experienced open-source developers, \ their own repositories", -19,
     r"time $+19\%$ \ (expected $-24\%$)", NAIVE),
]


class Experiments(VoiceoverScene):
    def construct(self):
        card(self, 5, r"What the experiments find", r"When people are given an AI assistant, \ how much faster or "
             r"better is their work, \ and whose?", "Chapter five. What the experiments find.",
             lit={2023: "Noy and Zhang", 2025: "Brynjolfsson, Li and Raymond"}, scale=("person", "firm"),
             horizon=("a day", "a year"))
        self.studies()
        self.desk()
        self.frontier()

    def studies(self):
        ax = plane([-30, 65], [-0.6, len(STUDIES) - 0.4], center=RIGHT * 2.2 + DOWN * 0.3, x_length=6.4,
                   y_length=5.0, xticks=[-20, 0, 20, 40, 60], yticks=[], xlabel=r"measured gain, \ \% \ (as reported)",
                   xfmt=lambda v: f"{v:.0f}".replace("-", "{-}"), font_size=14)
        zero = vline(ax, 0, -0.6, len(STUDIES) - 0.4, GREY_B)
        rows = VGroup()
        for k, (who, what, v, note_, c) in enumerate(STUDIES):
            y = len(STUDIES) - 1 - k
            p0, p1 = ax.ax.c2p(0, y - 0.25), ax.ax.c2p(v, y + 0.25)
            bar = Rectangle(width=abs(p1[0] - p0[0]), height=abs(p1[1] - p0[1]), fill_color=c, fill_opacity=0.8,
                            stroke_width=0).move_to((p0 + p1) / 2)
            lab = VGroup(label(who, font_size=15, color=c), label(what, font_size=13, color=GREY_A)).arrange(
                DOWN, aligned_edge=RIGHT, buff=0.04).next_to(ax.ax.c2p(-30, y), LEFT, buff=0.2)
            nt = label(note_, font_size=13, color=c).next_to(bar, RIGHT if v > 0 else LEFT, buff=0.1)
            if v < 0:
                nt.next_to(ax.ax.c2p(0, y), RIGHT, buff=0.15)
            rows.add(VGroup(bar, lab, nt))
        tag = published_tag(r"Noy and Zhang, \ Science 381 (2023); \ Peng, \ Kalliamvakou, \ Cihon and Demirer "
                            r"(2023); \ Dell'Acqua et al., \ HBS 24-013 (2023); \ Brynjolfsson, \ Li and Raymond, \ "
                            r"QJE 140(2) (2025); \ Becker et al., \ METR (2025)", corner=DL, font_size=11)
        with self.voiceover(
            "Since 2023 economists have run randomized experiments with AI assistants. <bookmark mark='a'/> Shakked "
            "Noy and Whitney Zhang gave ChatGPT to half of about four hundred and fifty professionals writing "
            "press releases, reports and emails: time per task fell forty percent, and graders rated the work "
            "eighteen percent better. <bookmark mark='b'/> Programmers given GitHub's Copilot built a small web "
            "server fifty-six percent faster. <bookmark mark='c'/> Consultants at Boston Consulting Group, on "
            "tasks the model could do well, finished a quarter faster and did twelve percent more of them. "
            "<bookmark mark='d'/> At a software firm's customer support desk, five thousand agents given an "
            "assistant resolved fourteen percent more problems per hour. <bookmark mark='e'/> And in 2025 METR "
            "randomized real issues for sixteen experienced open-source developers, in code they knew well. With "
            "AI allowed, they took nineteen percent longer, while believing it had made them faster. Short, "
            "well-defined tasks show large gains; long work in a familiar, complicated setting, so far, may not. "
            "METR has since said its estimate is probably out of date, as the tools have improved."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag))
            for k, (mk, r_) in enumerate(zip("abcde", rows)):
                vo.wait_until(mk)
                self.play(GrowFromEdge(r_[0], LEFT if STUDIES[k][2] > 0 else RIGHT), FadeIn(r_[1]), FadeIn(r_[2]))
        self.clear_scene()

    def desk(self):
        D = load("desk")
        F = D["fifths"]
        ax = plane([0.4, 5.6], [-0.1, 0.42], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.6, y_length=4.6,
                   xticks=[1, 2, 3, 4, 5], yticks=[0, 0.1, 0.2, 0.3, 0.4],
                   xlabel=r"fifth of agents by skill \ (1 = least skilled)",
                   ylabel=r"the assistant's effect on resolutions per hour", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        zero = seg(ax, 0.4, 0, 5.6, 0, GREY_C, 1.5)
        est = VGroup()
        for r in F:
            est.add(VGroup(seg(ax, r["fifth"], r["lo"], r["fifth"], r["hi"], TEXT, 3.0),
                           dot(ax, r["fifth"], r["est"], TEXT, 0.09)))
        tru = VGroup(*[dot(ax, r["fifth"] + 0.18, r["truth"], TRUTHC, 0.07) for r in F])
        avg = seg(ax, 0.4, D["est"], 5.6, D["est"], GDP, 2.4, dashed=True)
        alab = label(rf"average: \ +{100 * D['est']:.0f}\% \ ({100 * D['lo']:.0f} to {100 * D['hi']:.0f})",
                     font_size=16, color=GDP).next_to(ax.ax.c2p(5.6, D["est"]), UP, buff=0.1).shift(LEFT * 1.0)
        side = VGroup(
            label(rf"{D['n']:,} agents; \ half given the assistant at random".replace(",", "{,}"), font_size=17,
                  color=GREY_A),
            legend_rows([(TEXT, "estimate, with a 95% interval"), (TRUTHC, "the planted truth")], font_size=15),
            label(rf"top fifth over bottom fifth: \ {D['gap_control']:.2f} $\to$ {D['gap_treated']:.2f}",
                  font_size=17, color=WORK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ax.ax, RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ agora.automation.support\_desk \ (after Brynjolfsson, \ Li and Raymond)",
                         corner=DL, font_size=12)
        with self.voiceover(
            "The most striking pattern is who gains. <bookmark mark='a'/> On the Island we built a support desk "
            f"like Brynjolfsson, Li and Raymond's: {D['n']:,} agents of differing skill, half given an assistant "
            "at random, with an effect we planted. <bookmark mark='b'/> The experiment recovers the average: about "
            f"{100 * D['est']:.0f} percent more resolutions per hour. <bookmark mark='c'/> And it recovers the "
            f"pattern: the least skilled fifth gains about {100 * F[0]['est']:.0f} percent, the most skilled "
            f"almost nothing. In the real study, the newest and least skilled agents gained about a third, and "
            "the best saw small gains in speed and small falls in quality. The assistant had learned "
            "from the best agents' conversations, and passed their know-how to the rest. <bookmark mark='d'/> So "
            f"the gap between the top and bottom fifths shrinks, from {D['gap_control']:.2f} to "
            f"{D['gap_treated']:.2f}. Noy and Zhang found the same compression in writing. Within a job, at least "
            "at first, these tools are levellers."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(avg), FadeIn(alab))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(e) for e in est], lag_ratio=0.2), FadeIn(side[1]), run_time=1.6)
            self.play(LaggedStart(*[FadeIn(t) for t in tru], lag_ratio=0.2))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def frontier(self):
        cards = point_cards([
            (r"inside the frontier", r"tasks the model does well: \ consultants with GPT-4 faster, \ more "
             r"productive, \ and rated much higher in quality", NEWT),
            (r"outside the frontier", r"a task chosen to look easy but trip the model: \ consultants with it 19 "
             r"points less likely to get the right answer", NAIVE),
            (r"the jagged frontier", r"which side a task falls on is hard to see in advance, \ and it moves with "
             r"every new model", IDEA),
            (r"what is measured", r"time on a set task, \ not the value of the work, \ not learning, \ not what "
             r"happens to the jobs", GREY_B),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"Dell'Acqua et al.: \ the jagged technological frontier", font_size=28,
                     color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Dell'Acqua, \ McFowland, \ Mollick et al., \ Harvard Business School 24-013 (2023)",
                            corner=DL, font_size=12)
        with self.voiceover(
            "The consulting study adds a warning. <bookmark mark='a'/> On tasks inside what its authors called the "
            "frontier of the model's abilities, consultants with GPT-4 were faster and more productive, and graders "
            "rated their work much better. <bookmark mark='b'/> But they also set a task chosen to look easy while "
            "lying just outside the frontier. There, consultants using the model were nineteen percentage points "
            "less likely to get the right answer than those without it. They trusted it where they should not "
            "have. <bookmark mark='c'/> Fabrizio Dell'Acqua and coauthors call it a jagged frontier: which side a "
            "task falls on is hard to see in advance, and it moves with every new model. <bookmark mark='d'/> And "
            "all these studies measure time on a set task. They do not measure the value of the work, what people "
            "learn or stop learning, or what happens to the jobs. For that we need the aggregates."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
