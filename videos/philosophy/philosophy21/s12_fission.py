from __future__ import annotations

from videos.philosophy.philosophy21.common import *  # noqa: F403


class Fission(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Fission", r"What if you split in two?", lit=(1971, 1976), part=PART)
        with self.voiceover("Chapter eleven. Fission."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.case()
        self.splitbrain()
        self.worms()
        self.price()
        self.brick()
        self.only()

    def case(self):
        hc = history_card(1971, r"Derek Parfit", r"`Personal Identity', \ \textit{Philosophical Review}",
                          width=6.6, color=HIST).to_corner(UL, buff=0.3)
        brain = VGroup(Ellipse(width=1.6, height=1.1, color=NOM, fill_opacity=0.3),
                       Line(UP * 0.55, DOWN * 0.55, color=GREY_B)).move_to([-4.6, -0.6, 0])
        left = VGroup(Ellipse(width=0.8, height=1.1, color=WHOLE, fill_opacity=0.3)).move_to([-2.0, 0.4, 0])
        right = VGroup(Ellipse(width=0.8, height=1.1, color=PARTC, fill_opacity=0.3)).move_to([-2.0, -1.6, 0])
        a1 = Arrow(brain.get_right(), left.get_left(), buff=0.1, color=GREY_B)
        a2 = Arrow(brain.get_right(), right.get_left(), buff=0.1, color=GREY_B)
        ll = label(r"Lefty", font_size=16, color=WHOLE).next_to(left, RIGHT, buff=0.15)
        rl = label(r"Righty", font_size=16, color=PARTC).next_to(right, RIGHT, buff=0.15)
        rows = stack([(r"each half of your brain can carry your psychology \ (Wiggins, \ 1967)", WHITE),
                      (r"each half is transplanted into a new body: \ two people wake", NOM),
                      (r"each is psychologically continuous with you, \ equally", UNIV),
                      (r"you cannot be both: \ Lefty and Righty are two", BAD),
                      (r"and no reason to be one rather than the other", GOAL)], font_size=20, aligned_edge=LEFT,
                     width=6.0).move_to([3.6, -0.4, 0])
        with self.voiceover(
            "David Wiggins first posed the case, and Parfit made it famous. <bookmark mark='a'/>Suppose each half of "
            "your brain could sustain your whole psychology, as patients who lose a hemisphere sometimes show. "
            "<bookmark mark='b'/>Each half is transplanted into a new body, and two people wake up. Call them Lefty "
            "and Righty. <bookmark mark='c'/>Each is psychologically continuous with you, equally. "
            "<bookmark mark='d'/>You cannot be both: Lefty and Righty are two people, who will live different lives. "
            "<bookmark mark='e'/>And there is no reason for you to be one rather than the other. So, it seems, you are "
            "neither. Yet each has everything that would have mattered had only one half survived."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(brain))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(left), FadeIn(right), FadeIn(ll), FadeIn(rl),
                      FadeIn(rows[1]))
            for mk, r in zip("cde", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def worms(self):
        d = load("fission")
        head = label(r"Branching worms", font_size=30, color=CONN).to_edge(UP, buff=0.25)
        ax = Axes(x_range=[-2, 2, 1], y_range=[0, 4.4, 1], x_length=4.4, y_length=4.4,
                  axis_config={"color": GREY_D, "include_ticks": False}).move_to([-3.6, -0.5, 0])
        tl = label(r"time", font_size=14, color=GREY_A).next_to(ax.y_axis, UP, buff=0.05)
        t = np.linspace(0, 4, 41)
        trunk = [ax.c2p(0, tt) for tt in t if tt <= 2]
        lb = [ax.c2p(-0.7 * (tt - 2), tt) for tt in t if tt >= 2]
        rb = [ax.c2p(0.7 * (tt - 2), tt) for tt in t if tt >= 2]
        L = VMobject(stroke_color=WHOLE, stroke_width=14, stroke_opacity=0.55).set_points_as_corners(trunk + lb)
        R = VMobject(stroke_color=PARTC, stroke_width=14, stroke_opacity=0.55).set_points_as_corners(trunk + rb)
        split = DashedLine(ax.c2p(-1.8, 2), ax.c2p(1.8, 2), color=BAD, stroke_width=1.5)
        sl = label(r"the operation", font_size=14, color=BAD).next_to(split, RIGHT, buff=0.05)
        rows = stack([(r"continuity graph: \ " + ", \\ ".join(f"{a}--{b}" for a, b in d["links"]), GREY_A),
                      (r"continuous with the original: \ both branches \ (" +
                       (r"yes" if d["t0_L4"] and d["t0_R4"] else r"no") + r")", UNIV),
                      (r"identity is one-one and transitive: \ it cannot relate the original to both", BAD),
                      (r"Lewis \ (1976): \ two worms all along, \ sharing their stages before the split", WHOLE),
                      (r"so before the operation, \ two people were in one place: \ `multiple occupancy'", GOAL)],
                     font_size=19, aligned_edge=LEFT, width=6.4).move_to([3.4, -0.4, 0])
        with self.voiceover(
            "The Reasoner draws the case as a graph of person-stages over time. <bookmark mark='a'/>A single line of "
            "stages, linked by continuity, branches at the operation into two. <bookmark mark='b'/>The original stage "
            "is continuous with both final stages. <bookmark mark='c'/>But identity is one-one and transitive: if the "
            "original were identical to both, Lefty and Righty would be identical to each other. "
            "<bookmark mark='d'/>David Lewis's answer uses worms. There were two worms all along, Lefty's and "
            "Righty's, sharing their stages before the split. <bookmark mark='e'/>Before the operation two persons "
            "occupied one body, and spoke with one voice; identity, between worms, is untouched."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(tl))
            vo.wait_until("a")
            self.play(Create(L), Create(R), Create(split), FadeIn(sl), FadeIn(rows[0]), run_time=2.5)
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def price(self):
        d = load("fissionpl")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert d["mcs"] == [["F1"], ["F2"], ["F3"], ["F4"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.9, width=3.6, font_size=19,
                       center=[0, -0.5, 0], title=r"The Price List: \ fission")
        positions = [(("F1",), r"non-branching views", r"I survive only if there is no rival continuer: \ fission "
                                                        r"is death \ (Shoemaker; \ Nozick)"),
                     (("F2",), r"none", r"identity's logic is not negotiable: \ almost no one gives this up"),
                     (("F3",), r"Lewis \ (1976)", r"before the split, \ the two branches were two persons in one place"),
                     (("F4",), r"arbitrary winners", r"one branch is me, \ though nothing makes it so \ (brute facts)")]
        with self.voiceover(
            "Fission is a Price List. <bookmark mark='a'/>I would survive teleportation, and would survive if only one "
            "half of my brain lived on. Identity is transitive. The two branches are not identical to each other. And "
            "each branch has an equal claim to be me. <bookmark mark='b'/>All four cannot hold. "
            "<bookmark mark='c'/>Deny the first: on non-branching views, Sydney Shoemaker's and Robert Nozick's, I "
            "survive only if there is no rival continuer, so fission is death, though a double success. "
            "<bookmark mark='d'/>Deny the second: almost no one will give up the logic of identity. "
            "<bookmark mark='e'/>Deny the third: Lewis's two worms, two persons in one place before the split. "
            "<bookmark mark='f'/>Or deny the fourth: one branch is me, though no fact makes it so."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cdef", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=3.0)
                self.play(*anims)
        self.clear_scene()

    def brick(self):
        w = wall(upto=21, current=21).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(21, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        rows = card[1][1]
        with self.voiceover(
            "This is the twenty-first brick in the Wall. <bookmark mark='a'/>The dream: that personal identity is what "
            "matters in survival, so that whether I will exist is always a deep, determinate question. "
            "<bookmark mark='b'/>The wall: fission. Continuity, which carries everything we care about, can branch; "
            "identity, being transitive and one-one, cannot. <bookmark mark='c'/>What it forces, on Parfit's reading: "
            "identity is not what matters. What matters is continuity and connectedness, and they can hold to two "
            "future people at once."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(Indicate(w.brick[21], color=P.CONCL, scale_factor=1.08), FadeIn(card[0]), FadeIn(card[1][0]),
                      FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def only(self):
        head = label(r"The only-x-and-y principle", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the principle", r"whether $x$ is $y$ can depend only on facts about $x$, \ $y$ and the relations "
                               r"between them \ (Wiggins; \ Noonan)", UNIV),
            (r"closest continuer", r"Nozick: \ whether Lefty is me depends on whether Righty also survives", BAD),
            (r"the clash", r"Lefty's being me then depends on a fact about someone else: \ identity becomes "
                           r"extrinsic", GOAL),
            (r"Parfit's moral", r"double survival differs from single survival only extrinsically: \ how could that "
                                r"matter so much?", NOM),
            (r"fusion", r"the reverse case: \ two people merge into one \ (Parfit): \ is that death, \ or survival "
                        r"twice?", PARTC),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.8, x_text=-2.4, label_size=21)
        with self.voiceover(
            "A principle sharpens the case against non-branching views. <bookmark mark='a'/>The only-x-and-y "
            "principle, defended by Wiggins and Harold Noonan: whether x is y can depend only on facts about x and y "
            "and the relations between them. <bookmark mark='b'/>Nozick's closest continuer theory denies it: whether "
            "Lefty is me depends on whether Righty also survives. <bookmark mark='c'/>So my identity with Lefty would "
            "depend on a fact about someone else entirely. <bookmark mark='d'/>Parfit drew the moral: double survival "
            "differs from ordinary survival only in a fact external to the relation between me and Lefty, so how "
            "could it make the difference between life and death? <bookmark mark='e'/>And the reverse case, fusion, "
            "in which two people merge into one, raises the same questions run backwards."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def splitbrain(self):
        hc = history_card(1971, r"Thomas Nagel", r"`Brain Bisection and the Unity of Consciousness'", width=7.4,
                          color=HIST).to_corner(UL, buff=0.3)
        lh = Ellipse(width=1.2, height=1.6, color=WHOLE, fill_opacity=0.3).move_to([-4.6, -0.6, 0])
        rh = Ellipse(width=1.2, height=1.6, color=PARTC, fill_opacity=0.3).move_to([-3.2, -0.6, 0])
        cut = DashedLine([-3.9, 0.4, 0], [-3.9, -1.6, 0], color=BAD, stroke_width=3)
        cl = label(r"corpus callosum cut", font_size=15, color=BAD).next_to(cut, DOWN, buff=0.15)
        rows = stack([(r"Sperry and Gazzaniga \ (1960s): \ patients with the hemispheres disconnected", WHITE),
                      (r"an object shown to the left visual field: \ the left hand picks it out, \ the speaking left "
                       r"hemisphere denies seeing it", NOM),
                      (r"one person, \ or two streams of consciousness, \ in one skull?", GOAL),
                      (r"Nagel: \ no whole number of minds fits the facts", BAD),
                      (r"half of fission is already real", UNIV)], font_size=19, aligned_edge=LEFT,
                     width=6.4).move_to([3.4, -0.4, 0])
        with self.voiceover(
            "Fission is not wholly science fiction. <bookmark mark='a'/>In the 1960s, Roger Sperry and Michael "
            "Gazzaniga studied patients whose corpus callosum had been cut to treat epilepsy, disconnecting the two "
            "hemispheres. <bookmark mark='b'/>Show an object only to the left visual field, which goes to the right "
            "hemisphere, and the left hand can pick it out, while the speaking left hemisphere says it saw nothing. "
            "<bookmark mark='c'/>Is there one person here, or two streams of consciousness in one skull? "
            "<bookmark mark='d'/>Thomas Nagel concluded that no whole number of minds fits the facts. "
            "<bookmark mark='e'/>Half of the fission case is already real."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(lh), FadeIn(rh))
            vo.wait_until("a")
            self.play(Create(cut), FadeIn(cl), FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
