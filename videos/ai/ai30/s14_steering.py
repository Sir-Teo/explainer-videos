from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai30.common import CTRL, FEAT, MONO, PART, context_line, load, spread_bar, ticks

PUSH = C.SURPRISE


def text_block(t: str, width_chars=56, font_size=18, color=GREY_A, hot="\"'!?") -> VGroup:
    """Generated text, wrapped into at most three lines, with the marks of speech lit."""
    t = " ".join(t.split())
    lines = [t[i:i + width_chars] for i in range(0, min(len(t), 3 * width_chars), width_chars)]
    return VGroup(*[data_text(ln, font=MONO, font_size=font_size, color=color, t2c={h: PUSH for h in hot}) for ln in lines]).arrange(
        DOWN, aligned_edge=LEFT, buff=0.12)


class Steering(VoiceoverScene):
    def construct(self):
        self.card()
        self.dial()
        self.vector()
        self.tradeoff()
        self.persona()

    def card(self):
        card = chapter_card(13, r"Reaching in", r"Can we change what the model thinks?", part=PART)
        with self.voiceover("Chapter thirteen. Reaching in."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def dial(self):
        st = load("steering")
        alphas = [float(a) for a in st["alphas"]]
        texts, speech = st["texts"], st["speech_mean"]
        feat = int(st["feature"])
        ctx = VGroup(*[context_line(c, 5.2, font_size=16, color=FEAT) for c in st["contexts"][:3]]).arrange(DOWN, buff=0.08)
        ch = label(rf"feature {feat}: \ where it fires hardest", font_size=20, color=FEAT).next_to(ctx, UP, buff=0.12).align_to(ctx, LEFT)
        fbox = VGroup(ch, ctx).to_corner(UL, buff=0.35)
        colors = {r"\alpha": PUSH, r"d_k": FEAT}
        f = cmath(r"h \;\leftarrow\; h + ", r"\alpha", r"\, ", r"d_k", colors=colors, font_size=40).to_corner(UR, buff=0.5).shift(LEFT * 0.4)
        fl = label(r"add the feature's direction \\ at every character, \ while it writes", font_size=20, color=GREY_A)
        fl.next_to(f, DOWN, buff=0.15)
        prompt = str(st["prompt"])
        pr = Text(prompt, font="DejaVu Serif", font_size=20, color=GREY_B).move_to([0, 0.75, 0])
        if pr.width > 12.5:
            pr.scale_to_fit_width(12.5)
        prl = label(r"our transformer is given this, \ and writes on", font_size=22, color=GREY_A).next_to(pr, UP, buff=0.35)
        rows = VGroup()
        for a in alphas:
            key = f"{a:g}"
            tb = text_block(texts[key][0])
            al = MathTex(rf"\alpha = {a:g}", font_size=30, color=PUSH)
            q = label(rf"${speech[key]:.1f}$ marks of speech \\ per $160$ characters", font_size=18, color=PUSH)
            rows.add(VGroup(al, tb, q))
        for i, r_ in enumerate(rows):
            y = -0.15 - i * 1.25
            r_[0].move_to([-5.9, y, 0])
            r_[1].move_to([-0.2, y, 0])
            r_[2].move_to([5.5, y, 0])
        hl = label(r"lit: \ quotes, \ apostrophes, \ ! \ and \ ?", font_size=18, color=PUSH)
        tag = note(rf"${len(st['seeds'])}$ samples at each strength, \ one shown; \ a random direction at "
                   rf"$\alpha = {alphas[-1]:g}$: \ ${np.mean(st['random_speech']):.1f}$").to_corner(DR, buff=0.2)
        hl.next_to(tag, UP, buff=0.1).align_to(tag, RIGHT)
        q0, q1 = float(speech[f"{alphas[0]:g}"]), float(speech[f"{alphas[-1]:g}"])
        qr = float(np.mean(st["random_speech"]))
        with self.voiceover(
            "If a feature is a direction, we can push on it. <bookmark mark='a'/> Take the feature that fires on "
            "quotation marks. <bookmark mark='b'/> While the model writes, add alpha times its direction to the "
            "vector at every character. <bookmark mark='c'/> With no push, the model's own continuation. "
            f"<bookmark mark='d'/> Turn the dial up, and the writing turns into talk: quote marks, apostrophes, "
            f"exclamations and questions, from {q0:.1f} to {q1:.1f} per hundred and sixty characters, averaged over "
            f"{len(st['seeds'])} samples; a random direction of the same length gives {qr:.1f}. The model now thinks it's inside "
            "someone's speech. We didn't train anything or change a weight; we moved one direction. In May 2024 "
            "Anthropic did the same to Claude 3 Sonnet with a Golden Gate Bridge feature, and for one day, as a demo, "
            "it brought every conversation round to the bridge."
        ) as vo:
            self.play(FadeIn(pr, shift=UP * 0.1), FadeIn(prl))  # the prompt the model will continue, from the first words
            vo.wait_until("a")
            self.play(FadeIn(fbox))
            vo.wait_until("b")
            self.play(Write(f), FadeIn(fl), FadeOut(prl))
            vo.wait_until("c")
            self.play(FadeIn(rows[0][0]), FadeIn(rows[0][1], lag_ratio=0.02), FadeIn(rows[0][2]), FadeIn(tag), FadeIn(hl), run_time=1.5)
            vo.wait_until("d")
            for r_ in rows[1:]:
                self.play(FadeIn(r_[0]), FadeIn(r_[1], lag_ratio=0.02), FadeIn(r_[2]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def vector(self):
        m = load("mood")
        pos, neg = list(m["pos_test"]), list(m["neg_test"])
        frames = list(m["frames"])
        ex = VGroup(*[data_text(frames[i].format(w), font=MONO, font_size=20, color=c_)
                      for i, (w, c_) in enumerate(((pos[0], C.TRUE_P), (neg[0], PUSH), (pos[1], C.TRUE_P), (neg[1], PUSH)))])
        ex.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-4.4, 1.6, 0])
        colors = {r"v": C.BITS}
        f = cmath(r"v", r" = \overline{h_3(\text{cheerful word})} - \overline{h_3(\text{gloomy word})}", colors=colors,
                  font_size=30).move_to([2.2, 2.7, 0])
        fl = label(rf"the same ${len(frames)}$ frames, \ ${len(m['words_fit']) // 2}$ words of each kind; \ the other half "
                   r"kept for testing", font_size=19, color=GREY_A).next_to(f, DOWN, buff=0.15)
        pc, pg = np.asarray(m["proj_cheer"]), np.asarray(m["proj_gloom"])
        lo, hi = float(min(pc.min(), pg.min())), float(max(pc.max(), pg.max()))
        e = np.linspace(lo, hi, 21)
        hc_, _ = np.histogram(pc, e)
        hg_, _ = np.histogram(pg, e)
        top = float(max(hc_.max(), hg_.max()))
        g = axes([lo, hi], [0, top * 1.1], x_length=6.0, y_length=2.6, xlabel=r"a sentence's largest projection on $v$",
                 ylabel=r"sentences", yticks=ticks(0, top, 2), center=[2.4, -1.4, 0])
        w = (e[1] - e[0]) / (hi - lo) * 6.0
        bc = VGroup(*[Rectangle(width=w * 0.85, height=max(v / (top * 1.1) * 2.6, 0.005), stroke_width=0, fill_color=C.TRUE_P,
                                fill_opacity=0.55).move_to(g.ax.c2p((a + b) / 2, 0), aligned_edge=DOWN) for v, a, b in zip(hc_, e, e[1:])])
        bg = VGroup(*[Rectangle(width=w * 0.85, height=max(v / (top * 1.1) * 2.6, 0.005), stroke_width=0, fill_color=PUSH,
                                fill_opacity=0.55).move_to(g.ax.c2p((a + b) / 2, 0), aligned_edge=DOWN) for v, a, b in zip(hg_, e, e[1:])])
        lg = legend([(C.TRUE_P, rf"cheerful sentences \ (${int(m['n_sent'])}$)"), (PUSH, r"gloomy sentences")], font_size=18)
        lg.move_to([-4.5, -0.9, 0])
        res = label(rf"held-out words: \ AUROC ${float(m['auroc_words']):.2f}$ \\ real sentences of the novels: \ AUROC "
                    rf"${float(m['auroc_sent']):.2f}$", font_size=20, color=WHITE).move_to([-4.5, -2.4, 0])
        aw, as_ = float(m["auroc_words"]), float(m["auroc_sent"])
        with self.voiceover(
            "Steering does not need a dictionary. A direction can come straight from a contrast. "
            "<bookmark mark='a'/> Put cheerful and gloomy words into the same little frames, take the novels model's "
            f"vector at the word after block {int(m['layer'])}, and subtract the averages. <bookmark mark='b'/> Is "
            "it a mood? As a monitor, it separates held-out words it never saw with an AUROC of "
            f"{aw:.2f}, where one is perfect and a half is chance, <bookmark mark='c'/> and real sentences from the "
            f"novels, cheerful against gloomy, with {as_:.2f}."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(x) for x in ex], lag_ratio=0.2))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(fl))
            vo.wait_until("b")
            self.play(FadeIn(g), FadeIn(lg), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bc], lag_ratio=0.02),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in bg], lag_ratio=0.02), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tradeoff(self):
        m = load("mood")
        al = [float(a) for a in m["alphas"]]

        def stats(nm, field):
            out = []
            for a in al:
                key = f"{nm}_{a:g}_{field}" if not (nm == "r" and a == 0) else f"v_0_{field}"
                v = np.asarray(m[key], float)
                out.append((float(v.mean()), float(v.std(ddof=1) / np.sqrt(len(v)))))
            return out

        mv, mr = stats("v", "mood"), stats("r", "mood")
        fv, fr = stats("v", "flu"), stats("r", "flu")
        lo = min(a - b for a, b in mv + mr)
        hi = max(a + b for a, b in mv + mr)
        pad = 0.1 * (hi - lo + 1e-6)
        g1 = axes([al[0] - 0.1, al[-1] + 0.1], [lo - pad, hi + pad], x_length=5.4, y_length=3.4,
                  xlabel=r"strength $\alpha$ \ (times the stream's typical length)", ylabel=r"cheerful minus gloomy words, \ per $100$",
                  xticks=al, yticks=ticks(lo - pad, hi + pad, 3), center=[-3.4, -0.4, 0])
        flo = min(a - b for a, b in fv + fr)
        fhi = max(a + b for a, b in fv + fr)
        fp = 0.1 * (fhi - flo + 1e-6)
        g2 = axes([al[0] - 0.1, al[-1] + 0.1], [flo - fp, fhi + fp], x_length=5.4, y_length=3.4,
                  xlabel=r"strength $\alpha$", ylabel=r"bits per token, \ under the unsteered model",
                  xticks=al, yticks=ticks(flo - fp, fhi + fp, 3), center=[3.4, -0.4, 0])

        def plot(ax, st_, col):
            pts = [ax.c2p(a, mu) for a, (mu, _) in zip(al, st_)]
            c = VMobject(color=col, stroke_width=3).set_points_as_corners(pts)
            bars_ = VGroup(*[Line(ax.c2p(a, mu - se), ax.c2p(a, mu + se), color=col, stroke_width=3) for a, (mu, se) in zip(al, st_)])
            return VGroup(c, bars_, *[Dot(p, radius=0.05, color=col) for p in pts])

        pv1, pr1 = plot(g1.ax, mv, C.BITS), plot(g1.ax, mr, CTRL)
        pv2, pr2 = plot(g2.ax, fv, C.BITS), plot(g2.ax, fr, CTRL)
        lg = legend([(C.BITS, r"the mood vector"), (CTRL, r"a random direction")], font_size=18).to_corner(UR, buff=0.3)
        tag = note(rf"computed: \ ${len(m['topics'])}$ prompts $\times$ ${len(m['seeds'])}$ seeds, \ ${int(m['n_new'])}$ "
                   r"tokens each; \ bars: $\pm$ one standard error").to_corner(DR, buff=0.2)
        i0 = al.index(0.0)
        d_up = mv[-1][0] - mv[i0][0]
        d_dn = mv[0][0] - mv[i0][0]
        se = max(mv[-1][1], mv[i0][1])
        works = d_up > 2 * se and d_dn < -2 * max(mv[0][1], mv[i0][1])
        r_dev = max(abs(mr[0][0] - mv[i0][0]), abs(mr[-1][0] - mv[i0][0]))
        r_quiet = r_dev < 2 * max(mr[0][1], mr[-1][1], mv[i0][1])
        if works and r_quiet:
            verdict = (f"Pushing along the mood vector moves the mood: {mv[i0][0]:+.1f} cheerful-minus-gloomy words per "
                       f"hundred unsteered, {mv[-1][0]:+.1f} at the strongest push, {mv[0][0]:+.1f} pulling the other "
                       "way, while the random direction does nothing comparable.")
        elif works:
            verdict = (f"The mood rises steadily with the push: {mv[0][0]:+.1f} cheerful-minus-gloomy words per hundred "
                       f"pulling one way, {mv[i0][0]:+.1f} unsteered, {mv[-1][0]:+.1f} pushing the other. But a random "
                       f"direction, pushed as hard, reached {mr[-1][0]:+.1f} at the strongest setting too: a hard push "
                       "disturbs the text whatever its direction, and at this sample size the vector's own effect is "
                       "real but modest.")
        else:
            verdict = (f"The mood barely follows: {mv[i0][0]:+.1f} words per hundred unsteered, {mv[-1][0]:+.1f} at the "
                       f"strongest push and {mv[0][0]:+.1f} the other way, within the noise. A direction that reads a "
                       "mood well need not write it, at least not in a model this small.")
        with self.voiceover(
            "Now write with it: add alpha times the direction at every position while the model continues 'The sea', "
            "'The night' and ten more openings. <bookmark mark='a'/> " + verdict + " <bookmark mark='b'/> Either way "
            f"there is a price. Unsteered text costs {fv[i0][0]:.2f} bits per token under the model's own judgement; "
            f"at the strongest push, {fv[-1][0]:.2f}, and a random push of the same length costs about as much. "
            "Steering trades fluency for control."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(lg), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(pr1), run_time=1.0)
            self.play(Create(pv1), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(g2), Create(pr2), Create(pv2), run_time=2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def persona(self):
        cards = VGroup(
            history_card(2023, r"A.~Turner et al.: \ activation addition", r"``Love'' minus ``Hate'', \ added to GPT-2's "
                         r"stream, \ makes it write lovingly", width=4.3, color=PUSH, font_size=20),
            history_card(2024, r"A.~Arditi et al.", r"refusal in $13$ chat models is one direction: \ remove it and "
                         r"they stop refusing, \ add it and they refuse harmless requests", width=4.3, color=PUSH, font_size=20),
            history_card(2025, r"R.~Chen, \ A.~Arditi, \ H.~Sleight, \ O.~Evans \& J.~Lindsey", r"persona vectors for evil, "
                         r"\ sycophancy and hallucination, \ in Qwen2.5 and Llama 3.1", width=4.3, color=PUSH, font_size=20),
        ).arrange(RIGHT, buff=0.25).to_edge(UP, buff=0.4)
        uses = VGroup(label(r"monitor: \ watch the projection drift during a conversation or a fine-tune", font_size=25),
                      label(r"flag: \ score training data by how far it would push the model along a trait", font_size=25),
                      label(r"prevent: \ steer \textit{toward} the trait while fine-tuning, \ so the weights need not move "
                            r"there", font_size=25),
                      label(r"Part 27 met them as a diagnosis of emergent misalignment", font_size=22, color=GREY_B))
        uses.arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(cards, DOWN, buff=0.6)
        uses.set_opacity(0.25)
        with self.voiceover(
            "This recipe has a short history. <bookmark mark='a'/> In 2023 Alex Turner and colleagues added the "
            "difference between 'Love' and 'Hate' to GPT-2's stream and it wrote lovingly. <bookmark mark='b'/> In "
            "2024 Andy Arditi and colleagues found that refusal in thirteen chat models is a single direction: remove "
            "it and they stop refusing harmful requests, add it and they refuse harmless ones. <bookmark mark='c'/> In 2025 Runjin Chen, "
            "Arditi and colleagues extracted persona vectors, for traits like evil, sycophancy and making things up, "
            "in Qwen 2.5 and Llama 3.1. <bookmark mark='d'/> They used them three ways: to monitor a model's "
            "personality as a conversation or a fine-tune shifts it; to flag training data before it is used; and, "
            "oddly, to prevent a trait by steering toward it during fine-tuning, so the weights need not go there "
            "themselves."
        ) as vo:
            self.play(FadeIn(uses))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
            vo.wait_until("d")
            self.play(LaggedStart(*[u.animate.set_opacity(1) for u in uses], lag_ratio=0.5), run_time=4)
        self.wait(0.3)
        self.clear_scene()
