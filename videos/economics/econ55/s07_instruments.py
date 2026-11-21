from __future__ import annotations

from videos.economics.econ55.common import *  # noqa: F403


class Instruments(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Narrative and high-frequency shocks", r"Where do good instruments come from?",
             "Chapter six. Narrative and high-frequency shocks.",
             lit={2004: r"Romer and Romer", 2015: r"Gertler and Karadi", 2018: r"Nakamura and Steinsson"},
             scale=("nation",), horizon=("a day", "a decade"))
        self.sources()
        self.cure()

    def sources(self):
        cards = point_cards([
            (r"narrative", r"read the central bank's own records; \ keep the part of each decision its forecasts "
             r"cannot explain \ (Romer and Romer, \ Part 31)", EST),
            (r"high frequency", r"the move in futures prices in the minutes around an announcement: \ nothing "
             r"else happened in that window \ (Kuttner; \ G\"urkaynak, \ Sack and Swanson)", GAIN),
            (r"the catch", r"an announcement also reveals what the bank knows: \ the information effect "
             r"\ (Nakamura and Steinsson)", MODEL),
        ], width=12.6, cols=3, font_size=20).move_to(UP * 0.4)
        foot = label(r"either can be the outside instrument of Chapter 3: \ Gertler and Karadi's proxy VAR",
                     font_size=21, color=E.ACCENT).to_edge(DOWN, buff=0.8)
        tag = published_tag(r"Romer and Romer, \ AER (2004); \ Gertler and Karadi, \ AEJ: Macro (2015); \ Nakamura "
                            r"and Steinsson, \ QJE (2018)", corner=DR, font_size=12)
        with self.voiceover(
            "The outside instrument did best on the Island. Where do good instruments come from in the world? Part "
            "thirty-one met two sources. <bookmark mark='a'/> Christina and David Romer read the Federal Reserve's "
            "own records and kept only the part of each decision that its staff's forecasts could not explain: "
            "the surprise, purged of foresight. <bookmark mark='b'/> Others look at the minutes around an "
            "announcement. The move in interest-rate futures in that window can only be news about policy, because "
            "nothing else happened. <bookmark mark='c'/> There is a catch. An announcement can also tell markets "
            "what the bank knows about the economy, so part of the surprise is news about the economy itself. Emi "
            "Nakamura and Jón Steinsson called it the information effect. <bookmark mark='d'/> Either series can be "
            "the outside instrument of Chapter three; Mark Gertler and Peter Karadi used market surprises that way "
            "in an autoregression."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def cure(self):
        I = load("instruments")
        h = np.arange(len(I["truth"]["pi"]))
        ax = plane([0, 16], [-0.5, 1.0], center=LEFT * 1.8 + DOWN * 0.35, x_length=7.6, y_length=4.8,
                   xticks=[0, 4, 8, 12, 16], yticks=[-0.4, 0, 0.4, 0.8], xlabel=r"quarters after a one-point rise",
                   ylabel=r"inflation, \ points", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:+.1f}".replace("-", "{-}") if v else "0", font_size=14)
        z = DashedLine(ax.ax.c2p(0, 0), ax.ax.c2p(16, 0), color=GREY_D, stroke_width=1)
        truth = path(ax, h, I["truth"]["pi"], TRUTHC, 3.0)
        lines = {m: path(ax, h, I["methods"][m]["pi"]["mean"], METHOD[m], 2.6, yr=(-0.5, 1.0))
                 for m in ("var", "var_news", "narrative", "hf_clean", "hf_info")}
        mx = max(I["methods"]["var"]["pi"]["mean"])
        side = VGroup(
            label(r"Part 31's Island: \ the bank \\ sees news about costs \\ before it sets its rate", font_size=18,
                  color=WHITE),
            label(rf"grey: \ timing: \ the price \\ puzzle, \ up to $+{mx:.2f}$", font_size=18,
                  color=METHOD["var"]),
            label(r"blue: \ add a noisy signal \\ of the bank's news", font_size=18, color=METHOD["var_news"]),
            label(r"gold: \ narrative shocks \\ green: \ clean market surprises", font_size=18,
                  color=METHOD["narrative"]),
            label(r"purple: \ surprises with \\ an information effect", font_size=18, color=METHOD["hf_info"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = island_tag(rf"simulated: \ {I['reps']} histories", corner=DR, font_size=13)
        with self.voiceover(
            "Part thirty-one's Island reproduces the price puzzle on purpose: its bank sees news about coming cost "
            f"shocks before it sets its rate. Averaged over {I['reps']} histories, <bookmark mark='a'/> the truth: "
            "inflation falls, slowly. <bookmark mark='b'/> A recursive autoregression says it rises, by up to "
            f"{mx:.2f} points: the puzzle, made by the bank's foresight. <bookmark mark='c'/> Give the model a noisy "
            "signal of the bank's news, as Sims gave his commodity prices, and the puzzle shrinks but does not "
            "vanish. <bookmark mark='d'/> Narrative shocks and clean market surprises both recover the truth. "
            "<bookmark mark='e'/> Surprises contaminated by an information effect understate it: part of what looks "
            "like policy is the bank's news about the economy. The cure for the price puzzle was never a cleverer "
            "regression. It was a better account of why the rate moved."
        ) as vo:
            self.play(FadeIn(ax), Create(z), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(truth))
            vo.wait_until("b")
            self.play(Create(lines["var"]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(lines["var_news"]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(lines["narrative"]), Create(lines["hf_clean"]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(lines["hf_info"]), FadeIn(side[4]))
        self.clear_scene()
