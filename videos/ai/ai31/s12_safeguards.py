from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai31.common import CI, EST, JUDGE, LEAK, PART, TRUTH, node_box, tagline

THRESH = C.PENALTY
GUARD = C.INTERVAL


class Safeguards(VoiceoverScene):
    def construct(self):
        self.card()
        self.frameworks()
        self.crossings()
        self.classifiers()
        self.adaptive()

    def card(self):
        card = chapter_card(11, r"Dangerous capabilities and safeguards",
                            r"What if a model could help cause serious harm?", lit=(2025, 2026), part=PART)
        with self.voiceover("Chapter eleven. Dangerous capabilities and safeguards."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def frameworks(self):
        g = axes([0, 10], [0, 10], x_length=5.4, y_length=4.4, xlabel=r"time", ylabel=r"measured capability",
                 center=[-3.6, -0.5, 0])
        t = np.linspace(0, 10, 100)
        cap = curve(g.ax, t, 1.0 + 0.08 * t ** 2, EST, 4)
        lines = VGroup()
        for y, name in ((4.0, r"threshold 1: \ stronger safeguards"), (7.5, r"threshold 2: \ stronger still, \ or stop")):
            lines.add(VGroup(DashedLine(g.ax.c2p(0, y), g.ax.c2p(10, y), color=THRESH, dash_length=0.08),
                             label(name, font_size=18, color=THRESH).next_to(g.ax.c2p(0.2, y), UP, buff=0.06,
                                                                            aligned_edge=LEFT)))
        sch = note(r"schematic").next_to(g, DOWN, buff=0.1).align_to(g, RIGHT)
        domains = VGroup(*[node_box(t_, c_, font_size=20) for t_, c_ in (
            (r"biological and chemical weapons", LEAK), (r"cyberattacks", LEAK), (r"AI research done by AI", JUDGE),
            (r"manipulation, \ loss of control", JUDGE))]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        domains.move_to([3.4, 1.6, 0])
        dl = label(r"what dangerous-capability evaluations test", font_size=22, color=GREY_A).next_to(domains, UP, buff=0.15)
        fw = VGroup(
            label(r"Anthropic: \ Responsible Scaling Policy \ (2023; \ rewritten 2026)", font_size=20, color=GREY_A),
            label(r"OpenAI: \ Preparedness Framework \ (2023; \ v2, April 2025: \ High, Critical)", font_size=20,
                  color=GREY_A),
            label(r"Google DeepMind: \ Frontier Safety Framework \ (2024; \ v3, September 2025)", font_size=20,
                  color=GREY_A),
            label(r"California SB 53 \ (signed September 2025): \\ the largest developers must publish theirs", font_size=20,
                  color=CI),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.4, -1.7, 0])
        if lines.get_right()[0] > 6.9:
            lines.shift(LEFT * (lines.get_right()[0] - 6.9))
        with self.voiceover(
            "Some abilities matter because of what they could help someone do. Labs now test every frontier model "
            "for a few of them: <bookmark mark='a'/> help with biological or chemical weapons, with cyberattacks, with "
            "doing AI research itself, and with manipulation or escaping control. <bookmark mark='b'/> Each lab "
            "publishes a framework that ties capability thresholds to safeguards: cross the first line, and stronger "
            "protections are required before release; cross the next, and stronger still, or stop. "
            "<bookmark mark='c'/> Anthropic's Responsible Scaling Policy came first, in 2023; OpenAI's Preparedness "
            "Framework and Google DeepMind's Frontier Safety Framework followed. Since January 2026, a California law "
            "requires the largest developers to publish theirs."
        ) as vo:
            self.play(FadeIn(g), Create(cap), FadeIn(sch))
            vo.wait_until("a")
            self.play(FadeIn(dl), LaggedStart(*[FadeIn(d_) for d_ in domains], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in lines], lag_ratio=0.5))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(f_) for f_ in fw], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def crossings(self):
        events = [
            ("May 2025", r"Claude Opus 4 released under ASL-3 protections: \ ``clearly ruling out ASL-3 risks is not "
                         r"possible''", LEAK),
            ("Jul 2025", r"ChatGPT agent, \ then GPT-5: \ treated as High in biology, \ as a precaution", LEAK),
            ("Feb 2026", r"GPT-5.3-Codex: \ OpenAI's first launch treated as High in cybersecurity", LEAK),
            ("Apr 2026", r"Claude Mythos Preview: \ zero-days in every major operating system and browser; \ not made "
                         r"generally available; \ given to defenders \ (Project Glasswing)", THRESH),
            ("Jun 2026", r"GPT-5.6: \ at the US government's request, \ a limited preview for trusted partners first",
             THRESH),
            ("Sep 2026", r"GPT-6 Astra: \ OpenAI's first model at its Critical level in cybersecurity", THRESH),
        ]
        rows = VGroup()
        for when, what, col in events:
            d = label(when, font_size=22, color=col)
            w = wrapped_label(what, 10.6, 21, WHITE)
            rows.add(VGroup(d, w).arrange(RIGHT, buff=0.35, aligned_edge=UP))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        xw = max(r_[0].width for r_ in rows)
        for r_ in rows:
            r_[1].next_to(r_[0], RIGHT, buff=0.35 + xw - r_[0].width, aligned_edge=UP)
        rows.move_to(DOWN * 0.25)
        head = label(r"Thresholds crossed", font_size=36).to_edge(UP, buff=0.35)
        fire = history_card(2026, r"a benchmark of working exploits for Firefox", r"Claude Opus 4.6: \ $2$ working "
                            r"exploits in several hundred attempts; \ Mythos Preview: \ $181$", width=5.0, color=THRESH,
                            font_size=18)
        fire.to_corner(DR, buff=0.25)
        cite_ = cite(r"Anthropic (2025, 2026); \ OpenAI system cards (2025, 2026)", font_size=18)
        with self.voiceover(
            "In 2025 the lines started to be crossed. <bookmark mark='a'/> In May, Anthropic released Claude Opus 4 "
            "under its stricter ASL-3 protections, because it could no longer rule out the risk. <bookmark mark='b'/> "
            "In July OpenAI treated its ChatGPT agent, and then GPT-5, as High in biology, also as a precaution. "
            "<bookmark mark='c'/> In February 2026 came the first model OpenAI treated as High in cybersecurity. "
            "<bookmark mark='d'/> In April Anthropic announced Claude Mythos Preview, which found and exploited "
            "unknown vulnerabilities in every major operating system and browser; it went to defenders first, not to "
            "the public. On a Firefox exploit benchmark its predecessor managed two working exploits in several "
            "hundred attempts; Mythos, a hundred and eighty-one. <bookmark mark='e'/> In June, at the US government's "
            "request, OpenAI previewed its next models to trusted partners first. <bookmark mark='f'/> And in "
            "September it released GPT-6 Astra, the first model it rates at its highest level, Critical, in "
            "cybersecurity, with its strongest safeguards yet."
        ) as vo:
            full = rows.copy()
            rows.fade(0.8)
            self.play(FadeIn(head), FadeIn(cite_), FadeIn(rows))
            for k, m in enumerate("abcdef"):
                vo.wait_until(m)
                self.play(Transform(rows[k], full[k]))
                if m == "d":
                    self.play(FadeIn(fire, shift=UP * 0.15))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def classifiers(self):
        flow = VGroup(*[node_box(t, c, font_size=22) for t, c in (
            (r"request", GREY_B), (r"input \\ classifier", GUARD), (r"model", EST), (r"output \\ classifier", GUARD),
            (r"answer", GREY_B))]).arrange(RIGHT, buff=0.45).move_to([0, 2.3, 0])
        arr = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.06, color=GREY_B, stroke_width=2.5)
                       for a, b in zip(flow, flow[1:])])
        c1 = history_card(2025, r"Constitutional Classifiers \ (Anthropic, January)", r"trained on synthetic examples "
                          r"written from a ``constitution'' of what is allowed; \ $183$ red-teamers, \ over $3{,}000$ hours: "
                          r"\ no universal jailbreak; \ automated attacks: \ $86\% \to$ under $5\%$ succeed; \ cost: "
                          r"\ $+0.38\%$ refusals, \ $+23.7\%$ compute", width=6.4, color=GUARD, font_size=19)
        c2 = history_card(2026, r"\dots the next generation \ (January)", r"one classifier reads the request and the "
                          r"answer together; \ a linear probe on the model's own activations screens all traffic, \ "
                          r"passing the suspicious few on: \ about $1\%$ compute, \ $0.05\%$ refusals", width=6.4,
                          color=CI, font_size=19)
        c3 = history_card(2026, r"probes in production \ (OpenAI, June)", r"GPT-5.6 served with ``activation "
                          r"classifiers'': \ Part 30's probes, \ guarding a frontier model", width=6.4, color=CI,
                          font_size=19)
        VGroup(c1, c2).arrange(RIGHT, buff=0.3).move_to([0, -0.2, 0])
        c3.next_to(VGroup(c1, c2), DOWN, buff=0.25)
        sch = note(r"schematic").next_to(flow, DOWN, buff=0.1).align_to(flow, RIGHT)
        with self.voiceover(
            "The safeguards themselves are layered. The model is trained to refuse, and around it sit classifiers "
            "that read what goes in and what comes out. <bookmark mark='a'/> Anthropic's Constitutional Classifiers, "
            "in January 2025, were trained on synthetic examples written from a short constitution of what is and "
            "isn't allowed. A hundred and eighty-three red-teamers spent over three thousand hours without finding a "
            "universal jailbreak; on automated attacks, success fell from eighty-six percent to under five, for a "
            "small rise in refusals and a quarter more compute. <bookmark mark='b'/> A year later the next version "
            "cut the cost to about one percent, partly by putting a linear probe on the model's own activations in "
            "front. <bookmark mark='c'/> OpenAI now serves its models with activation classifiers too: the probes of "
            "Part 30, standing guard."
        ) as vo:
            cards_ = VGroup(c1, c2, c3)
            full = cards_.copy()
            cards_.fade(0.8)
            self.play(FadeIn(flow), FadeIn(arr), FadeIn(sch), FadeIn(cards_))
            vo.wait_until("a")
            self.play(Transform(c1, full[0]))
            vo.wait_until("b")
            self.play(Transform(c2, full[1]))
            vo.wait_until("c")
            self.play(Transform(c3, full[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def adaptive(self):
        layers = VGroup()
        rng_ = np.random.default_rng(5)
        for k in range(3):
            slab = RoundedRectangle(width=0.35, height=4.2, corner_radius=0.08, stroke_color=GUARD, stroke_width=2,
                                    fill_color=GUARD, fill_opacity=0.18).move_to([-3.9 + 1.6 * k, 0.0, 0])
            holes = VGroup(*[Ellipse(width=0.22, height=0.38, stroke_width=0, fill_color=BACKGROUND, fill_opacity=1)
                             .move_to(slab.get_center() + UP * y) for y in rng_.uniform(-1.7, 1.7, 3)])
            layers.add(VGroup(slab, holes))
        ys = [h.get_y() for h in layers[0][1]]
        fixed = Arrow([-6.3, -0.9, 0], [layers[0][0].get_left()[0] - 0.05, -0.9, 0], buff=0, color=GREY_B,
                      stroke_width=3)
        stop = Cross(scale_factor=0.18, stroke_color=GUARD).move_to(layers[0][0].get_center() + DOWN * 0.9)
        path = VMobject(stroke_color=LEAK, stroke_width=4).set_points_smoothly(
            [[-6.3, 1.2, 0]] + [[l_[1][0].get_x(), l_[1][0].get_y(), 0] for l_ in layers] + [[-0.3, layers[-1][1][0].get_y(), 0]])
        tip = Triangle(fill_color=LEAK, fill_opacity=1, stroke_width=0).scale(0.12).rotate(-PI / 2).move_to(path.get_end())
        l1 = label(r"a fixed set \\ of attacks: \ stopped", font_size=18, color=GREY_A).next_to(fixed, DOWN, buff=0.12)
        l1.align_to(fixed, LEFT)
        l2 = label(r"an attacker who adapts: \ finds the holes that line up", font_size=20, color=LEAK)
        l2.next_to(layers, UP, buff=0.15)
        sch = note(r"schematic").next_to(layers, DOWN, buff=0.15)
        hc = history_card(2025, r"\textit{The Attacker Moves Second} \ (Nasr, Carlini et al., October)", r"$12$ recent "
                          r"defenses against jailbreaks and prompt injection, \ most reported near-zero attack success; "
                          r"\ adaptive attacks, \ by gradient, \ RL, \ search and people, \ got through most of them over "
                          r"$90\%$ of the time", width=6.0, color=LEAK, font_size=19).move_to([3.5, 0.6, 0])
        lesson = label(r"test a defense against an attacker who knows it", font_size=24, color=CI).move_to([3.5, -2.4, 0])
        with self.voiceover(
            "How should such defenses be judged? <bookmark mark='a'/> Against a fixed list of known attacks, most look "
            "excellent. <bookmark mark='b'/> But an attacker moves second. In October 2025 researchers from several "
            "labs and universities took twelve recently published defenses, most reporting near-zero attack success, "
            "and attacked each one adaptively: with gradients, reinforcement learning, search, and people. They got "
            "through most of them more than ninety percent of the time. <bookmark mark='c'/> It is the oldest lesson "
            "of security: a defense is only as good as the strongest attacker who knows it is there."
        ) as vo:
            self.play(FadeIn(layers), FadeIn(sch))
            vo.wait_until("a")
            self.play(GrowArrow(fixed), FadeIn(l1))
            self.play(FadeIn(stop))
            vo.wait_until("b")
            self.play(Create(path), FadeIn(tip), FadeIn(l2), FadeIn(hc), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(lesson, shift=UP * 0.1))
        self.wait(0.4)
        self.clear_scene()
