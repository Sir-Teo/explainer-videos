from __future__ import annotations

from videos.economics.econ27.common import *  # noqa: F403


class Critics(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Keynes's critics", r"Who disagreed, \ and who turned out right about what?",
             "Chapter twelve. Keynes's critics.", lit={1919: r"\emph{Economic Consequences}", 1963: r"Friedman and "
             r"Schwartz", 1979: r"Lucas and Sargent"}, scale=("nation",), horizon=("decades",))
        self.critics()
        self.called()

    def critics(self):
        cards = point_cards([
            (r"Hayek (1931)", r"the slump repairs a boom built \\ on cheap credit; \ stimulus \\ only delays it",
             INVEST),
            (r"the monetarists", r"Friedman and Schwartz (1963): \\ the Fed let money fall a third; \\ a monetary "
                                 r"failure", COUPON),
            (r"the new classicals", r"Lucas and Sargent (1979): \\ models without expectations \\ failed in the "
                                    r"1970s", RATE),
            (r"what each kept", r"Hayek: \ booms matter; \\ Friedman: \ money matters; \\ Lucas: \ expectations "
                                r"matter", OUTPUT),
        ], width=12.6, cols=2, font_size=22).move_to(DOWN * 0.1)
        head = label(r"the critics", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Hayek, \emph{Prices and Production} (1931); \ Friedman and Schwartz, \emph{A Monetary "
                            r"History} (1963); \ Lucas and Sargent (1979)", corner=DR, font_size=12)
        with self.voiceover(
            "Keynes had critics from the start, and each one won something. <bookmark mark='a'/> Friedrich Hayek "
            "argued in 1931 that a slump is the economy repairing the damage of a boom built on cheap credit, in "
            "which too much was invested in the wrong things. Stimulus only delays the repair. "
            "<bookmark mark='b'/> The monetarists, led by Milton Friedman and Anna Schwartz, argued in 1963 that "
            "the Depression was a failure of monetary policy: the Federal Reserve let the money stock fall by about "
            "a third, as banks failed. Part twenty-six showed how. <bookmark mark='c'/> And in the 1970s the new "
            "classicals, Robert Lucas and Thomas Sargent, argued that Keynesian models had failed when inflation "
            "and unemployment rose together, because they ignored how people's expectations respond to policy. "
            "<bookmark mark='d'/> Each left a mark on what came next: booms matter, money matters, and expectations "
            "matter. Parts twenty-eight to thirty-one build the economics that took all three on board."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["keynes_peace"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.4,
                       font_size=18).move_to(UP * 0.1)
        tag = published_tag(r"Keynes (1919), \ ch.\ 6; \ Mantoux (1946); \ Clavin, \ Corsetti, \ Obstfeld and Tooze "
                            r"(eds., \ 2023)", corner=DR, font_size=12)
        with self.voiceover(
            "Keynes himself made one of economics' most famous forecasts. Called it? <bookmark mark='a'/> In 1919, "
            "after resigning from the British delegation at the peace conference in Paris, he wrote The Economic "
            "Consequences of the Peace. He argued that the reparations the Allies meant to take from Germany were "
            "more than it could pay, and that pressing them would impoverish Central Europe. If we aim deliberately "
            "at the impoverishment of Central Europe, he wrote, vengeance, I dare predict, will not limp. "
            "<bookmark mark='b'/> The bill was set only in 1921, cut in 1924 and 1929, suspended in 1931 and "
            "abandoned in 1932: it was never paid in full. Germany suffered hyperinflation and then depression, and "
            "the peace ended in war. But Etienne Mantoux argued in 1946 that Germany could have paid, as the sums "
            "it later spent on rearmament showed. <bookmark mark='c'/> Partly right: about the peace, tragically; "
            "about what Germany could pay, still argued over."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()
