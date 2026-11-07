from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs55.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, mono

# Saltzer and Schroeder, "The Protection of Information in Computer Systems", Proc. IEEE 1975: the eight design
# principles (two more -- work factor and compromise recording -- are listed in the narration).
PRINCIPLES = [
    (r"economy of mechanism", r"keep the design small enough to inspect"),
    (r"fail-safe defaults", r"deny by default; \ grant access on purpose"),
    (r"complete mediation", r"check every access, \ every time"),
    (r"open design", r"security must not rest on secrecy of the design"),
    (r"separation of privilege", r"need two keys, \ not one, \ to act"),
    (r"least privilege", r"each part gets only the rights it needs"),
    (r"least common mechanism", r"share as little as possible between users"),
    (r"psychological acceptability", r"if it is unusable, \ it will be bypassed"),
]

# Events whose dates this series states with confidence.
HISTORY = [
    (1988, r"the Morris worm: \ a buffer overflow in \texttt{fingerd}", NO),
    (1996, r"Aleph One, \ ``Smashing the Stack for Fun and Profit''", HEAD),
    (2014, r"Rowhammer \ (Kim et al.)", NO),
    (2018, r"Spectre and Meltdown", NO),
    (2024, r"the xz-utils backdoor", NO),
]


class Threats(VoiceoverScene):
    def construct(self):
        self.card()
        self.triad()
        self.model()
        self.history()
        self.principles()
        self.asymmetry()

    def card(self):
        card = chapter_card(1, r"Threat models and principles", r"What are we defending, \ and against whom?",
                            lit=(1975, 2024), extra=((1975, r"Saltzer \& Schroeder"), (1988, r"the Morris worm"),
                                                     (2024, r"xz-utils")), part=PART)
        with self.voiceover("Chapter one. Threat models, and principles."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def triad(self):
        head = label(r"Security is three promises", font_size=36).to_edge(UP, buff=0.3)
        items = [(r"confidentiality", r"only the right people read it", DATA),
                 (r"integrity", r"only the right people change it", YES),
                 (r"availability", r"it is there when it is needed", HEAD)]
        tiles = VGroup()
        for name, body, col in items:
            box = RoundedRectangle(width=3.8, height=2.0, corner_radius=0.15, stroke_color=col, stroke_width=2.2,
                                   fill_color=BG, fill_opacity=1)
            t = label(name, font_size=26, color=col)
            b = wrapped_label(body, 3.4, font_size=20, color=GREY_A)
            VGroup(t, b).arrange(DOWN, buff=0.3).move_to(box)
            tiles.add(VGroup(box, t, b))
        tiles.arrange(RIGHT, buff=0.4).next_to(head, DOWN, buff=0.7)
        foot = wrapped_label(r"a breach is any one of the three broken; \ different systems weigh them differently: \ "
                             r"a bank fears a forged transfer, \ a hospital fears the records being gone",
                             12.4, font_size=21, color=WHITE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Before any attack or defence, one question: what does it mean for a system to be secure? "
            "<bookmark mark='a'/> The classic answer is three promises. Confidentiality: only the people who should "
            "read something can read it. Integrity: only the people who should change it can change it. "
            "Availability: it is there when it is needed. <bookmark mark='b'/> A breach is any one of the three "
            "broken, and different systems weigh them differently. A bank fears a forged transfer more than a leak; "
            "a hospital may fear its records being gone more than being read. Security is never absolute; it is "
            "always security of something, against someone."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tiles], lag_ratio=0.3), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def model(self):
        head = label(r"A threat model", font_size=36).to_edge(UP, buff=0.3)
        boundary = DashedVMobject(RoundedRectangle(width=5.6, height=3.4, corner_radius=0.2, stroke_color=YES,
                                                   stroke_width=2.5), num_dashes=60).move_to([-2.4, -0.1, 0])
        bl = label(r"trust boundary", font_size=18, color=YES).next_to(boundary, UP, buff=0.1)
        assets = VGroup(*[VGroup(RoundedRectangle(width=1.7, height=0.55, corner_radius=0.1, stroke_color=DATA,
                                                  fill_color=DATA, fill_opacity=0.12),
                                 label(t, font_size=17, color=WHITE)) for t in (r"login", r"the files", r"the keys")])
        for g in assets:
            g[1].move_to(g[0])
        assets.arrange(DOWN, buff=0.35).move_to(boundary)
        tcb = label(r"the trusted computing base: \ what must be correct", font_size=16,
                    color=GREY_A).next_to(assets, DOWN, buff=0.2)
        attacker = VGroup(Circle(radius=0.3, color=NO, fill_color=NO, fill_opacity=0.2),
                          label(r"adversary", font_size=18, color=NO))
        attacker[1].next_to(attacker[0], DOWN, buff=0.1)
        attacker.move_to([4.3, 1.2, 0])
        surface = VGroup(*[Arrow(attacker[0].get_center(), assets[i][0].get_right() + RIGHT * 0.05,
                                 buff=0.35, stroke_width=2.5, color=NO, max_tip_length_to_length_ratio=0.06)
                           for i in range(3)])
        sl = label(r"attack surface: \ every way in", font_size=18, color=NO).move_to([4.2, -1.8, 0])
        notes = wrapped_label(r"name the assets, \ the adversary and their powers, \ and where trust changes hands; \ "
                              r"what you leave out of the model is what will be attacked", 12.6, font_size=20,
                              color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "To defend a system you first describe the fight. That description is a threat model. "
            "<bookmark mark='a'/> It names the assets worth protecting: here, a login program, the files, the keys. "
            "<bookmark mark='b'/> It draws a trust boundary around the part that must be correct, the trusted "
            "computing base, and admits that everything inside it is trusted whether it deserves to be or not. "
            "<bookmark mark='c'/> It names the adversary and what they can do: can they send packets, run a program, "
            "sit on the same machine, bribe a maintainer? <bookmark mark='d'/> And it maps the attack surface, every "
            "way in. The danger is always what the model leaves out, because that is exactly where the attacker will "
            "look."
        ) as vo:
            self.play(FadeIn(head), Create(boundary), FadeIn(bl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(a) for a in assets], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(tcb))
            vo.wait_until("c")
            self.play(FadeIn(attacker))
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowArrow(a) for a in surface], lag_ratio=0.2), FadeIn(sl), FadeIn(notes))
        self.wait(0.4)
        self.clear_scene()

    def history(self):
        head = label(r"The attacks this part meets", font_size=36).to_edge(UP, buff=0.3)
        x0, x1 = -6.0, 6.0
        y = 1.6
        spine = Line([x0, y, 0], [x1, y, 0], color=GREY_C, stroke_width=2)

        def xof(yr):
            return x0 + (yr - 1985) / (2025 - 1985) * (x1 - x0)
        rows = VGroup()
        up = True
        for yr, txt, col in HISTORY:
            x = xof(yr)
            dot = Dot([x, y, 0], radius=0.09, color=col)
            yl = label(str(yr), font_size=20, color=HEAD).next_to(dot, DOWN if up else UP, buff=0.12)
            tx = wrapped_label(txt, 3.4, font_size=18, color=col)
            tx.next_to(dot, UP if up else DOWN, buff=0.5 if up else 0.55)
            tick = Line([x, y - 0.12, 0], [x, y + 0.12, 0], color=col, stroke_width=2)
            rows.add(VGroup(dot, tick, yl, tx))
            up = not up
        foot = wrapped_label(r"four decades, \ and every layer of the tower: \ a program, \ the hardware, \ the "
                             r"microarchitecture, \ the supply chain", 12.4, font_size=21,
                             color=WHITE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "This part is a tour of attacks, so here are the landmarks, with the dates this series is sure of. "
            "<bookmark mark='a'/> In 1988 the Morris worm spread across the early internet, partly through a buffer "
            "overflow in a network service, and brought the idea of a self-replicating attack into the open. "
            "<bookmark mark='b'/> In 1996 an article by the author who wrote as Aleph One explained the stack "
            "overflow carefully enough that anyone could follow it. <bookmark mark='c'/> In 2014 Rowhammer showed "
            "that software could flip bits in memory it never touched; in 2018 Spectre and Meltdown showed that "
            "speculation leaks secrets; and in 2024 a backdoor was found hidden in a widely used compression "
            "library. <bookmark mark='d'/> Four decades, and every layer of the tower we built."
        ) as vo:
            self.play(FadeIn(head), Create(spine))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[2:]], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def principles(self):
        head = label(r"Saltzer and Schroeder, 1975", font_size=36).to_edge(UP, buff=0.3)
        cells = VGroup()
        cols = (DATA, YES, HEAD, LAM, KERN, DATA, YES, HEAD)
        for i, (name, body) in enumerate(PRINCIPLES):
            box = RoundedRectangle(width=6.0, height=0.92, corner_radius=0.1, stroke_color=cols[i], stroke_width=1.6,
                                   fill_color=BG, fill_opacity=1)
            t = label(name, font_size=20, color=cols[i])
            b = wrapped_label(body, 5.6, font_size=15, color=GREY_A)
            VGroup(t, b).arrange(DOWN, buff=0.07).move_to(box)
            cells.add(VGroup(box, t, b))
        cells.arrange_in_grid(rows=4, cols=2, buff=(0.3, 0.18), flow_order="dr").next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "Fifty years ago Jerome Saltzer and Michael Schroeder distilled the whole subject into a handful of "
            "design principles, and they have barely aged. <bookmark mark='a'/> Keep the mechanism small enough to "
            "inspect. Deny by default, and grant access deliberately. Check every access, every time, with no fast "
            "path that skips the check. <bookmark mark='b'/> Do not rest security on keeping the design secret, an "
            "idea older than them, from Kerckhoffs in the nineteenth century: assume the enemy knows the system. "
            "Require more than one key for the most dangerous actions. <bookmark mark='c'/> Give each part only the "
            "privileges it needs; share as little machinery as possible between users; and, above all, make it "
            "usable, because a control people cannot live with is a control they will switch off. They listed two "
            "more: raise the attacker's work factor, and record compromises when you cannot prevent them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(cells[i]) for i in (0, 1, 2)], lag_ratio=0.3), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(cells[i]) for i in (3, 4)], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(cells[i]) for i in (5, 6, 7)], lag_ratio=0.3), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def asymmetry(self):
        head = label(r"The defender's hard problem", font_size=36).to_edge(UP, buff=0.3)
        left = VGroup(label(r"attacker", font_size=24, color=NO),
                      wrapped_label(r"needs \textbf{one} way in", 4.6, font_size=22, color=NO))
        left.arrange(DOWN, buff=0.2)
        right = VGroup(label(r"defender", font_size=24, color=YES),
                       wrapped_label(r"must hold \textbf{every} layer", 4.6, font_size=22, color=YES))
        right.arrange(DOWN, buff=0.2)
        VGroup(left, right).arrange(RIGHT, buff=2.4).next_to(head, DOWN, buff=0.6)
        layers = VGroup(*[Rectangle(width=8.0, height=0.42, stroke_color=GREY_B, stroke_width=1.4, fill_color=BG,
                                    fill_opacity=1) for _ in range(5)])
        labs = [r"hardware", r"the kernel", r"the program", r"the web", r"the supply chain"]
        for r, t in zip(layers, labs):
            r.add(label(t, font_size=17, color=WHITE).move_to(r))
        layers.arrange(UP, buff=0.08).move_to(DOWN * 1.3)
        foot = wrapped_label(r"so: \ defence in depth \ (many weak walls beat one strong one), \ a small trusted base, "
                             r"\ and the assumption that you have already been breached", 12.6, font_size=20,
                             color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "There is a deep asymmetry underneath all of this. <bookmark mark='a'/> The attacker needs to find one "
            "way in. The defender must hold every layer at once, from the hardware to the supply chain, and a single "
            "weak one is enough. <bookmark mark='b'/> That is why the practical answers are modest. Defence in "
            "depth: many imperfect walls, so that breaching one does not win the game. A trusted computing base kept "
            "as small as you can bear, because everything in it is a thing that must be right. And the working "
            "assumption of modern security, that you have already been breached, so you also plan to detect it and "
            "recover. The rest of this part walks the layers, one at a time, and shows each one leaking."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left), FadeIn(right), FadeIn(layers))
            self.play(Indicate(layers[2], color=NO, scale_factor=1.05))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES, PART, mono)
