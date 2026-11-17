from __future__ import annotations

import numpy as np

from videos.psychology.psych10.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.why()
        self.wash()
        self.open()

    def card(self):
        card = chapter_card(14, r"Frontier: \ why do we sleep?", r"A third of life, \ and no agreed purpose", lit=(),
                            part=PART, scale=("molecule", "brain", "mind"), marr=("what",))
        with self.voiceover(
            "Chapter fourteen. The frontier: why do we sleep?"
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def why(self):
        head = heading(r"Every animal studied does it. \ Nobody knows why")
        facts = rows_of([
            (r"flies, \ worms, \ even jellyfish, which have no brain: \ all have sleep, or something very like it", WHITE),
            (r"an animal asleep cannot eat, \ cannot mate, \ and cannot watch for what eats it", BAD),
        ], 12.4, 30, 0.2).move_to([0, 2.15, 0])
        ideas = [
            (r"to fix memories", SLEEPC, r"chapter seven: \ real, and small"),
            (r"to turn synapses back down", CLOCKC, r"a day of learning strengthens them; \ sleep scales them back. \ The "
                                                    r"pressure would be the bill"),
            (r"to clear waste", HORM, r"found in mice in 2013; \ disputed in 2024"),
            (r"to save energy", LIGHTC, r"the oldest idea"),
        ]
        cards = VGroup()
        for i, (name, col, what) in enumerate(ideas):
            x = -5.1 + 3.4 * i
            box = RoundedRectangle(width=3.15, height=2.9, corner_radius=0.15, color=col, stroke_width=2.5, fill_color=col,
                                   fill_opacity=0.07).move_to([x, -0.55, 0])
            a = wrapped_label(name, 2.8, 30, col)
            a.move_to([x, 0.35, 0])
            b = wrapped_label(what, 2.8, 26, WHITE)
            b.next_to(a, DOWN, buff=0.25)
            cards.add(VGroup(box, a, b))
        end = wrapped_label(r"Not rivals: \ sleep may do all four. \ None has been shown to be the reason an animal cannot "
                            r"do without it.", 12.4, 30, THRESH).move_to([0, -2.85, 0])
        third = big_number(r"$\tfrac{1}{3}$", r"of a life, \ asleep", SLEEPC, 110, 4.0, 34).move_to([0, -0.6, 0])
        tag = note(r"the four proposals, as the reviews give them").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Here's the frontier, and it's a strange one. A third of this part has been about sleep: its "
            "stages, its timing, the cost of losing it. And nobody can say what it's for. "
            "<bookmark mark='a'/> It isn't an accident. Every animal that has been studied closely "
            "sleeps, or does something very like it: flies, worms, even jellyfish, which have no brain. "
            "And it's dangerous. An animal asleep can't eat, can't mate, and can't watch for whatever "
            "eats it. Evolution keeps nothing that costly without a reason. <bookmark mark='b'/> There "
            "are four main candidates. To fix memories: that's chapter seven, real and small. "
            "<bookmark mark='c'/> To turn synapses back down. On this idea, a day of learning "
            "strengthens synapses across the brain, which costs energy and room, and sleep scales them "
            "back while keeping their differences. The pressure of chapter four would be the bill. "
            "<bookmark mark='d'/> To clear waste. We'll look at that one next. <bookmark mark='e'/> And "
            "to save energy, which is the oldest idea. <bookmark mark='f'/> They aren't rivals, "
            "necessarily. Sleep may do all four. But none of them has been shown to be the reason an "
            "animal can't do without it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(third, scale=1.1))
            vo.wait_until("a")
            self.play(FadeIn(facts[0]))
            self.wait(7.0)
            self.play(FadeIn(facts[1]))
            vo.wait_until("b")
            self.play(FadeOut(third), *[FadeIn(c[0]) for c in cards], FadeIn(cards[0][1]), FadeIn(cards[0][2]))
            for mark_, c in zip("cde", cards[1:]):
                vo.wait_until(mark_)
                self.play(FadeIn(c[1]), FadeIn(c[2]))
            vo.wait_until("f")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def wash(self):
        x = archive.XIE_2013.data
        wider = round(100 * x["space_increase"])
        head = heading(r"Does sleep wash the brain?")

        def card(title, body, verdict, col, cx):
            t = label(title, font_size=32, color=col)
            b = wrapped_label(body, 5.6, 28, WHITE)
            v = wrapped_label(verdict, 5.6, 30, col)
            inner = VGroup(t, b, v).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
            box = RoundedRectangle(width=6.3, height=inner.height + 0.5, corner_radius=0.14, color=col, stroke_width=2.5,
                                   fill_color=col, fill_opacity=0.07)
            inner.move_to(box)
            g = VGroup(box, inner)
            return g.move_to([cx, 0, 0])

        a = card(r"2013: \ mice", rf"asleep or anaesthetized, \ the space between brain cells widened by {wider}\%, \ and "
                 r"fluid carried waste away faster", r"sleep is when the brain takes out the rubbish", MODEL, -3.4)
        b = card(r"2024: \ mice", r"clearance measured another way: \ slower in sleep, \ and slower still under "
                 r"anaesthesia", r"the opposite", BAD, 3.4)
        VGroup(a, b).set_y(1.25)
        a.align_to(b, UP)
        rows = rows_of([
            (r"the argument: \ what counts as clearance, \ and how to measure fluid in a living brain without changing how "
             r"it moves", WHITE),
            (r"both in mice; \ in people the evidence is thin", GREY_A),
            (r"a finding and a counter-finding, \ with no verdict: \ not in the Ledger yet. \ A claim can be in every "
             r"popular book, and still be open", THRESH),
        ], 12.6, 29, 0.22).move_to([0, -2.0, 0])
        src = published_tag(archive.XIE_2013.cite)
        tag = note(r"the second study: Miao et al.\ (2024), in the same Archive entry").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Take the third, because you've met it in headlines: sleep washes the brain. "
            "<bookmark mark='a'/> In 2013 a team in Rochester reported that in mice, asleep or "
            f"anaesthetized, the space between brain cells widened by {wider} percent, and that fluid "
            "flushed through it and carried waste away faster. It was a beautiful result, and it had an "
            "obvious meaning: sleep is when the brain takes out the rubbish. It went into every popular "
            "book on sleep. <bookmark mark='b'/> In 2024 another team measured clearance in mice a "
            "different way, and found the opposite. Clearance was slower during sleep, and slower still "
            "under anaesthesia. <bookmark mark='c'/> The argument now is about what counts as clearance, "
            "and how to measure fluid moving through a living brain without changing how it moves. Both "
            "studies are in mice. In people the evidence is thin. <bookmark mark='d'/> So this one "
            "doesn't go in the Ledger yet. It's a finding and a counter-finding, a decade apart, with no "
            "verdict. A claim can be in every popular book, and still be open."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(a[0]), FadeIn(b[0]), FadeIn(a[1][0]), FadeIn(b[1][0]))
            vo.wait_until("a")
            self.play(FadeIn(a[1][1]))
            self.wait(8.0)
            self.play(FadeIn(a[1][2]))
            vo.wait_until("b")
            self.play(FadeIn(b[1][1]), FadeIn(b[1][2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2], shift=UP * 0.1))
        self.clear_scene()

    def open(self):
        head = heading(r"Open questions")
        g = np.random.default_rng(8)
        A = axes([0, 2], [0, 10], x_length=4.2, y_length=3.6, xticks=[], yticks=[], xlabel=r"", ylabel=r"lapses after a lost "
                 r"night", center=[-4.5, 0.25, 0])
        ax = A.ax
        first = g.gamma(2.2, 1.6, size=14)
        second = np.clip(first + g.normal(0, 0.6, size=14), 0.2, 9.8)
        first = np.clip(first, 0.2, 9.8)
        pairs = VGroup(*[VGroup(Line(ax.c2p(0.45, a_), ax.c2p(1.55, b_), color=GREY_B, stroke_width=2),
                                Dot(ax.c2p(0.45, a_), radius=0.07, color=OPP), Dot(ax.c2p(1.55, b_), radius=0.07, color=OPP))
                         for a_, b_ in zip(first, second)])
        xl = VGroup(label(r"first visit", font_size=24, color=GREY_A).next_to(ax.c2p(0.45, 0), DOWN, buff=0.15),
                    label(r"second visit", font_size=24, color=GREY_A).next_to(ax.c2p(1.55, 0), DOWN, buff=0.15))
        rows = rows_of([
            (r"who is hit hardest? \ Some fall apart after one bad night, \ some barely change, \ and it is the same people "
             r"each time. \ Nobody can yet predict who", OPP),
            (r"what is the pressure made of? \ A variable called S has worked for forty years without anyone knowing what "
             r"S is", SLEEPC),
            (r"is REM sleep for anything? \ Some drugs suppress it for years, \ with no obvious loss", REMC),
            (r"$\star$ \ short sleepers die sooner, \ and so do long sleepers: \ design the study that tells sleep as a cause "
             r"from sleep as a symptom", THRESH),
        ], 7.4, 28, 0.3).move_to([3.0, -0.2, 0])
        keep_in_frame(rows)
        tag = note(r"the picture: a drawing of the reported pattern, \ not data").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Three more open questions to carry out of this part. <bookmark mark='a'/> First: who is hit "
            "hardest? In the sleep-loss experiments, some people fall apart after one bad night, and "
            "some barely change. Bring them back to the laboratory, and it's the same people each time. "
            "The difference is large, it's stable, and nobody can yet predict it from anything simpler. "
            "<bookmark mark='b'/> Second: what is the pressure made of? Adenosine is part of it. "
            "Synapses may be part of it. A model with one variable called S has worked for forty years, "
            "without anyone knowing what S is. <bookmark mark='c'/> Third: is REM sleep for anything? "
            "Some drugs suppress it for years, and the people who take them don't obviously lose "
            "anything. <bookmark mark='d'/> And the starred problem is the Ledger's fourth row. Short "
            "sleepers die sooner. So do long sleepers. Design the study that could tell sleep as a cause "
            "from sleep as a symptom."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(xl))
            vo.wait_until("a")
            self.play(FadeIn(pairs, lag_ratio=0.1), FadeIn(rows[0]), run_time=2.5)
            for mark_, r in zip("bcd", rows[1:]):
                vo.wait_until(mark_)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
