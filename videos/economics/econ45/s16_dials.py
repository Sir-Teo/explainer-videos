from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ45.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 14, r"The Dials: \ loss aversion, \ present bias, \ defaults", r"What do the numbers say?",
             "Chapter fourteen. The Dials: loss aversion, present bias, and the effect of a default.",
             lit={2019: r"Jachimowicz et al.", 2024: r"Brown et al.; \ Walasek et al."}, scale=("person",),
             horizon=("a year",))
        self.dial_loss()
        self.dial_beta()
        self.dial_default()

    def _show(self, dial, title, lo, hi, ticks, unit, say, marks, fmt="{:.2f}"):
        head = status_head(dial, title)
        frame, rows = dial_rows(dial, lo, hi, ticks, unit, top=2.1, step=0.55, fmt=fmt)
        meaning = wrapped_label(tex_safe(dial.meaning), 11.2, 15, GREY_A).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"explainer.economics.dials, \ checked 2026-11-21", corner=DR, font_size=12)
        with self.voiceover(say) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip(marks, rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("z")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def dial_loss(self):
        C = load("c13k")
        self._show(dials.DIALS["loss_aversion"], r"loss aversion \ (new)", 0.8, 2.6, [1.0, 1.5, 2.0, 2.5],
                   r"lambda: \ how many times a loss outweighs an equal gain",
                   "The first dial is new: loss aversion, lambda, how many times more a loss is felt than an equal "
                   "gain. Tversky and Kahneman's 1992 estimate from laboratory gambles is two and a quarter. "
                   "<bookmark mark='a'/> A 2024 meta-analysis by Alexander Brown, Taisuke Imai, Ferdinand Vieider and "
                   "Colin Camerer, pooling estimates from economics, psychology and neuroscience, finds about two. "
                   "<bookmark mark='b'/> Another 2024 meta-analysis, by Lukasz Walasek, Timothy Mullett and Neil "
                   "Stewart, restricted to choices between risky prospects, finds 1.31. <bookmark mark='c'/> And "
                   f"prospect theory fitted to choices13k's gamble problems gives {C['params']['lam']:.2f}. "
                   "<bookmark mark='z'/> The status: contested. Losses usually weigh more than gains, but how much "
                   "depends on the setting and the method, and the card-show traders of chapter three suggest "
                   "experience can shrink it toward one.", "abc", fmt="{:.2f}")

    def dial_beta(self):
        self._show(dials.DIALS["present_bias"], r"present bias \ (new)", 0.4, 1.05, [0.4, 0.6, 0.8, 1.0],
                   r"beta: \ the weight on everything after today \ (1 = none)",
                   "The second, also new: present bias, beta. David Laibson, Andrea Repetto and Jeremy Tobacman fitted "
                   "a life-cycle model to American households' wealth and credit-card borrowing, and found a beta of "
                   "about one half: people who save for retirement and borrow at high interest at the same time. "
                   "<bookmark mark='a'/> In laboratory tasks where people choose how much tedious work to do today "
                   "against a future day, a recent study finds betas of 0.70 to 0.79. <bookmark mark='b'/> But over "
                   "money paid on different dates, Ned Augenblick, Muriel Niederle and Charles Sprenger found "
                   "virtually none: money can be saved or borrowed, so its date matters less than when it is spent. "
                   "<bookmark mark='c'/> The Island's gym members are planted between one half and 0.95. "
                   "<bookmark mark='z'/> The status: depends on the setting. Present bias is clearest over effort and "
                   "consumption, and a meta-analysis of over two hundred laboratory estimates finds it on average, "
                   "with wide variation.", "abc", fmt="{:.2f}")

    def dial_default(self):
        self._show(dials.DIALS["default_effect"], r"the effect of a default \ (new)", -5, 60, [0, 20, 40, 60],
                   r"percentage points more people at the default outcome",
                   "The third: the effect of a default. Madrian and Shea's company saw participation among new hires "
                   "rise from 37 to 86 percent when enrollment became automatic: 49 percentage points. "
                   "<bookmark mark='a'/> On the Island, naive new hires gain 35 points after a year. "
                   "<bookmark mark='b'/> Time-consistent ones, none. <bookmark mark='z'/> The status: depends on "
                   "the setting. Across fifty-eight studies, a meta-analysis by Jon Jachimowicz and coauthors finds a "
                   "large average effect with wide variation: defaults matter most when people put decisions off or "
                   "read the default as advice.", "ab", fmt="{:.0f}")
