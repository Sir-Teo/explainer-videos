from __future__ import annotations

from videos.economics.econ62.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 16, r"Frontier: \ firms of people and models", r"What happens to a firm's hierarchy when a "
             r"model can answer the workers' questions?", "Chapter sixteen. Frontier: firms of people and models.",
             lit={2023: r"Generative AI at Work"}, scale=("person", "firm"), horizon=("a decade",))
        self.agents()
        self.open_questions()

    def agents(self):
        ax = plane([-0.6, 1.6], [0, 40], center=LEFT * 3.0 + DOWN * 0.4, x_length=5.2, y_length=4.4, xticks=[],
                   yticks=[0, 10, 20, 30, 40], ylabel=r"issues resolved per hour, \ change \%",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        b = bars(ax, [0, 1], [14, 34], [OWN, GAIN], width=0.55)
        labs = VGroup(label(r"all agents", font_size=15, color=OWN).next_to(ax.ax.c2p(0, 0), DOWN, buff=0.1),
                      label(r"novice and \\ low-skilled", font_size=15, color=GAIN).next_to(ax.ax.c2p(1, 0), DOWN,
                                                                                         buff=0.1))
        vl = VGroup(label(r"+14\%", font_size=16, color=OWN).next_to(b[0], UP, buff=0.06),
                    label(r"+34\%", font_size=16, color=GAIN).next_to(b[1], UP, buff=0.06))
        side = VGroup(
            label(r"a customer-support firm gives its agents an AI assistant, \ in stages", font_size=19,
                  color=WHITE),
            label(r"the least experienced gain most; \ the most skilled gain a little speed \\ and lose a little "
                  r"quality", font_size=19, color=GAIN),
            label(r"in Garicano's terms: \ knowledge became cheap \ (chapter ten), \\ so the bottom of the "
                  r"hierarchy can solve more", font_size=19, color=MGR),
            label(r"the assistant learned from the best agents' answers: \\ are they paid for teaching it?",
                  font_size=19, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        if side.width > 6.2:
            side.width = 6.2
            side.to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Brynjolfsson, \ Li and Raymond, \ NBER Working Paper 31161 (2023); \ QJE 140(2) "
                            r"(2025)", corner=DL, font_size=12)
        with self.voiceover(
            "The frontier: firms that organize people and models together. <bookmark mark='a'/> Erik Brynjolfsson, "
            "Danielle Li and Lindsey Raymond studied a customer-support firm that gave its agents an AI assistant, "
            "in stages, so that some had it before others. Issues resolved per hour rose fourteen percent on "
            "average in the working-paper version, and thirty-four percent for novice and low-skilled agents. "
            "<bookmark mark='b'/> The most experienced and skilled gained a little speed and lost a little quality. "
            "<bookmark mark='c'/> In chapter ten's terms, knowledge became cheap, so the bottom of the hierarchy "
            "can solve problems it used to pass up. <bookmark mark='d'/> And a question for personnel economics: "
            "the assistant learned from the best agents' answers. Are they paid for teaching it?"
        ) as vo:
            self.play(FadeIn(ax), FadeIn(labs), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowFromEdge(b[0], DOWN), FadeIn(vl[0]), GrowFromEdge(b[1], DOWN), FadeIn(vl[1]),
                      FadeIn(side[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(FadeIn(side[1 + k]))
        self.clear_scene()

    def open_questions(self):
        cards = point_cards([
            (r"flatter firms?", r"if workers can solve more, \ managers can supervise more: \ wider spans, \ fewer "
             r"layers", MGR),
            (r"management as software", r"targets, \ monitoring and scheduling done by systems: \ chapter two's "
             r"practices, \ installed rather than taught", PLANT),
            (r"who gains", r"the novices gain most at first; \ whether wages follow depends on who can capture the "
             r"gain", WORK),
            (r"what remains hard", r"measuring management's effect in firms that change faster than any experiment "
             r"can run", COST),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.2)
        head = label(r"what remains open", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "What remains open? <bookmark mark='a'/> Whether firms flatten: if workers can solve more, managers can "
            "support more of them, with wider spans and fewer layers. <bookmark mark='b'/> Whether management "
            "becomes software: targets, monitoring and scheduling done by systems, chapter two's practices "
            "installed rather than taught. <bookmark mark='c'/> Who gains: the novices first, but whether their "
            "wages follow depends on who can capture the gain. <bookmark mark='d'/> And what remains hard: "
            "measuring management's effect in firms that change faster than any experiment can run."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()
