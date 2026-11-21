from __future__ import annotations

from videos.economics.econ55.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 14, r"Frontier: \ micro data and expectations", r"What will identify the next generation of "
             r"models?", "Chapter fourteen. Frontier: micro data and expectations.",
             lit={2018: r"Coibion, Gorodnichenko and Kamdar", 2024: r"Bayer, Born and Luetticke"},
             scale=("household", "nation"), horizon=("a decade",))
        self.open_()

    def open_(self):
        cards = point_cards([
            (r"heterogeneous agents, estimated", r"Part 52's HANK models fitted to aggregate series and to "
             r"household data at once, \ so the spending of the poor and the rich both discipline them", EST),
            (r"micro moments in macro models", r"marginal propensities to spend from rebates and lotteries \ (Part "
             r"22) \ as targets, \ not afterthoughts", DATA),
            (r"expectations as data", r"surveys of households, \ firms and forecasters, \ so beliefs are measured "
             r"rather than assumed rational", MODEL),
            (r"new instruments", r"surprises cleaned of the information effect; \ narrative series for other "
             r"countries; \ shocks shared across regions", GAIN),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.15)
        head = label(r"what remains open", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Coibion, \ Gorodnichenko and Kamdar, \ JEL 56(4) (2018); \ Bayer, \ Born and "
                            r"Luetticke, \ AER 114(5) (2024)", corner=DR, font_size=12)
        with self.voiceover(
            "What remains open. <bookmark mark='a'/> Heterogeneous-agent models, Part fifty-two's, are now "
            "estimated on aggregate series and household data together; Christian Bayer, Benjamin Born and Ralph "
            "Luetticke estimated one for the American business cycle. <bookmark mark='b'/> Micro moments, like how "
            "much of a windfall people spend, from Part twenty-two, are becoming targets that models must hit, not "
            "afterthoughts. <bookmark mark='c'/> Expectations are measured rather than assumed: Olivier Coibion, "
            "Yuriy Gorodnichenko and Rupal Kamdar argued that surveys of what households, firms and forecasters "
            "expect should discipline the Phillips curve. <bookmark mark='d'/> And instruments keep improving: "
            "surprises cleaned of the information effect, narrative series for other countries, and shocks that "
            "hit regions differently. Each new source of variation is a new restriction, and a new chance to find "
            "out which of the old ones were wrong."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
