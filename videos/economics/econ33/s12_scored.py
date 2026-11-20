from __future__ import annotations

from videos.economics.econ33.common import *  # noqa: F403
from videos.economics.econ33.s02_playit import boom_minis


class Scored(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Your guesses, \ scored", r"Which booms ended in crises, and could a model have told?",
             "Chapter ten. Your guesses, scored.", lit={1990: r"Sweden", 2007: r"Ireland and Spain"},
             scale=("nation",), horizon=("a decade",))
        self.reveal()
        self.table()

    def reveal(self):
        B = load("booms")
        cards = boom_minis(B, reveal=True).move_to(DOWN * 0.1)
        head = label(rf"the answers: \ {B['crises']} of the 8 ended in a crisis within three years", font_size=24,
                     color=E.ACCENT).to_edge(UP, buff=0.25)
        crisis = [b for b in B["booms"] if b["crisis"]]
        calm = [b for b in B["booms"] if not b["crisis"]]
        with self.voiceover(
            "Here are your eight booms, with their names and what came after. <bookmark mark='a'/> "
            + ", ".join(f"{b['letter']}, {b['name']} in {b['year']}" for b in crisis[:-1])
            + f", and {crisis[-1]['letter']}, {crisis[-1]['name']} in {crisis[-1]['year']}, ended in banking "
            "crises within three years. <bookmark mark='b'/> "
            + ", ".join(f"{b['letter']}, {b['name']} in {b['year']}" for b in calm[:-1])
            + f", and {calm[-1]['letter']}, {calm[-1]['name']} in {calm[-1]['year']}, did not, though Portugal "
            "and the Netherlands both had crises in 2008, seven and eight years after their booms. Australia, "
            "after a boom of forty points, had none. <bookmark mark='c'/> If you marked every one of them a crisis, "
            f"you were right {B['crises']} times in eight. That is the first lesson: the biggest credit booms end "
            "in crises far more often than ordinary times do, about six times in ten here against one in ten."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c.box) for c in cards], lag_ratio=0.1),
                      LaggedStart(*[FadeIn(VGroup(*c.g[:3])) for c in cards], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c.g.outcome) for c, b in zip(cards, B["booms"]) if b["crisis"]],
                                  lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c.g.outcome) for c, b in zip(cards, B["booms"]) if not b["crisis"]],
                                  lag_ratio=0.3), run_time=1.5)
            vo.wait_until("c")
            self.play(*[Indicate(c.box, color=CRISIS, scale_factor=1.02) for c, b in zip(cards, B["booms"])
                        if b["crisis"]])
        self.clear_scene()

    def table(self):
        B = load("booms")
        rows = VGroup()
        head = VGroup(*[label(t, font_size=20, color=GREY_B) for t in (r"boom", r"loans, \ 5 years",
                                                                       r"model's chance", r"what happened")])
        rows.add(head)
        order = sorted(B["booms"], key=lambda b: -b["p"])
        for b in order:
            col = CRISIS if b["crisis"] else CALM
            cells = VGroup(label(rf"{b['letter']}: \ {tex_safe(b['name'])} {b['year']}", font_size=21, color=WHITE),
                           label(rf"+{b['rise']:.0f} points", font_size=21, color=CREDIT),
                           label(rf"{100 * b['p']:.0f}\%", font_size=21, color=HOUSE),
                           label(r"crisis" if b["crisis"] else r"no crisis", font_size=21, color=col))
            rows.add(cells)
        widths = [4.2, 2.4, 2.6, 2.4]
        for r in rows:
            x = -5.8
            for c, w in zip(r, widths):
                c.move_to([x + w / 2, 0, 0])
                x += w
        rows.arrange(DOWN, buff=0.22).move_to(UP * 0.35)
        for r in rows:
            x = -5.8
            for c, w in zip(r, widths):
                c.set_x(x + w / 2)
                x += w
        foot = VGroup(
            label(rf"ranked by the model's chance: \ area under the curve {B['auc8']:.2f} \ (0.5 is a coin)",
                  font_size=21, color=HOUSE),
            label(r"the model was fitted only on the years before each boom ended", font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.65)
        tag = data_tag(r"Jord\`a, \ Schularick and Taylor, \ Macrohistory Database R6; \ this film's model", corner=DR,
                       font_size=12)
        with self.voiceover(
            "Could a model have done better than you? <bookmark mark='a'/> For each boom, here is the chance of a "
            "crisis in the next three years from the simple model of chapter nine, fitted only on the history "
            "before that boom ended, ordered from most to least alarmed. <bookmark mark='b'/> It put Ireland and "
            "Spain at the top, rightly. It also put Portugal third, wrongly, and Switzerland in 1989, which did "
            f"have a crisis, at the bottom. <bookmark mark='c'/> Its ranking scores {B['auc8']:.2f}, where a coin "
            "scores one half. That is the second lesson. Credit booms are the best single warning sign we have, "
            "but among large booms, telling which will break, and when, is far harder. The Queen's question has a "
            "partial answer: the warning signs were there, but signs like them appear in many booms that end "
            "quietly, and in the fastest fifth of credit growth, four times in five no crisis follows."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r[:3])) for r in rows[1:]], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r[3]) for r in rows[1:]], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
