from __future__ import annotations

from videos.philosophy.philosophy14.common import *  # noqa: F403

ATOMS = ("b", "p", "s", "f")
NAMES = {"b": r"plays for Barcelona", "p": r"plays for Paris", "s": r"lives in Spain", "f": r"lives in France"}


def facts_panel(facts: dict, title: str, x: float, col) -> VGroup:
    rows = VGroup(label(title, font_size=23, color=col))
    for a in ATOMS:
        rows.add(VGroup(mark(facts[a], 24), label(NAMES[a], font_size=20)).arrange(RIGHT, buff=0.2))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([x, -0.6, 0])
    return rows


class Machines(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Machines that change their minds", r"What happens when a program must revise?",
                            lit=(1979,), part=PART)
        with self.voiceover("Chapter thirteen. Machines that change their minds."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.tms()
        self.databases()
        self.editing()
        self.lessons()

    def tms(self):
        hc = history_card(1979, r"Jon Doyle", r"`A Truth Maintenance System'", width=4.8, color=HIST).to_corner(
            UL, buff=0.35)
        nodes = {"bird": [-4.8, 0.2, 0], "penguin?": [-4.8, -1.6, 0], "flies": [-1.8, 0.2, 0],
                 "can migrate": [1.2, 0.2, 0]}
        boxes = {k: VGroup(RoundedRectangle(width=2.2, height=0.6, corner_radius=0.12, color=BEL, stroke_width=2.5),
                           label(k, font_size=21)).move_to(v) for k, v in nodes.items()}
        for b in boxes.values():
            b[1].move_to(b[0])
        edges = VGroup(Arrow(boxes["bird"].get_right(), boxes["flies"].get_left(), buff=0.1, color=GREY_B),
                       DashedLine(boxes["penguin?"].get_right(), boxes["flies"].get_bottom() + DOWN * 0.05,
                                  color=BAD),
                       Arrow(boxes["flies"].get_right(), boxes["can migrate"].get_left(), buff=0.1, color=GREY_B))
        el = label(r"unless", font_size=18, color=BAD).next_to(edges[1], DOWN, buff=0.05)
        rows = stack([
            (r"each belief records its \textit{justifications}", WHITE),
            (r"`flies' holds because `bird' is in \ and `penguin' is out", GREY_A),
            (r"learn `penguin': \ retract `flies', \ and everything resting on it", BAD),
            (r"de Kleer's ATMS \ (1986): \ track every assumption set at once", GREY_A),
        ], font_size=21, aligned_edge=LEFT, width=5.4).move_to([4.0, -1.8, 0])
        with self.voiceover(
            "The first machines to change their minds were truth maintenance systems, introduced by Jon Doyle in 1979. "
            "<bookmark mark='a'/>Each belief records its justifications. <bookmark mark='b'/>Flies is believed because "
            "bird is believed and penguin is not; can migrate rests on flies. <bookmark mark='c'/>When the system "
            "learns that the bird is a penguin, it retracts flies, and everything that rested on it, and nothing else. "
            "<bookmark mark='d'/>Johan de Kleer's assumption-based version tracks every combination of assumptions at "
            "once. These are belief-base revision, in Hansson's sense, implemented."
        ) as vo:
            self.play(FadeIn(hc), *[FadeIn(b) for b in boxes.values()], Create(edges), FadeIn(el))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
                if mk == "c":
                    self.play(boxes["penguin?"][0].animate.set_color(OK),
                              boxes["flies"][0].animate.set_color(BAD).set_opacity(0.5),
                              boxes["can migrate"][0].animate.set_color(BAD).set_opacity(0.5))
        self.clear_scene()

    def databases(self):
        import itertools as it
        rows_db = [("Ann", "50k"), ("Ann", "60k"), ("Bob", "40k")]
        # repairs: maximal subsets with at most one salary per name
        subsets = [S for r in range(len(rows_db) + 1) for S in it.combinations(rows_db, r)
                   if len({n for n, _ in S}) == len(S)]
        repairs = [S for S in subsets if not any(set(S) < set(T) for T in subsets)]
        certain_bob = all(("Bob", "40k") in R_ for R_ in repairs)
        certain_ann50 = all(("Ann", "50k") in R_ for R_ in repairs)
        certain_ann45 = all(any(n == "Ann" and int(v[:-1]) > 45 for n, v in R_) for R_ in repairs)
        head = label(r"Inconsistent databases", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{name}", r"\text{salary}"]
        grid = ValueGrid(hd, [[rf"\text{{{n}}}", rf"\text{{{v}}}"] for n, v in rows_db], col_w=[1.8, 1.8],
                         cell_h=0.5, font_size=26).move_to([-4.4, 0.6, 0])
        key = label(r"rule: \ one salary per person", font_size=20, color=BAD).next_to(grid, DOWN, buff=0.3)
        reps = VGroup(*[label(r"repair: \ " + r", \ ".join(f"{n}~{v}" for n, v in R_), font_size=21, color=BEL)
                        for R_ in repairs]).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([2.4, 1.4, 0])
        qs = stack([
            (r"a \textit{repair}: \ a maximal consistent part \ (a remainder, \ Chapter 3)", GREY_A),
            (r"certain answer: \ true in every repair \ (skeptical, \ Chapter 10)", GREY_A),
            (r"Bob earns 40k?" + (r" \ certain" if certain_bob else r" \ not certain"), OK if certain_bob else BAD),
            (r"Ann earns more than 45k?" + (r" \ certain" if certain_ann45 else r" \ not certain"),
             OK if certain_ann45 else BAD),
            (r"Ann earns 50k?" + (r" \ certain" if certain_ann50 else r" \ not certain"),
             OK if certain_ann50 else BAD),
            (r"consistent query answering \ (Arenas, \ Bertossi \ and Chomicki, \ 1999)", GOAL),
        ], font_size=21, aligned_edge=LEFT, width=7.0).move_to([2.4, -1.3, 0])
        with self.voiceover(
            "Databases face the same problem. <bookmark mark='a'/>A table lists two salaries for Ann, against the rule "
            "of one salary per person. <bookmark mark='b'/>Marcelo Arenas, Leopoldo Bertossi and Jan Chomicki proposed "
            "repairing it in every minimal way at once. A repair is a maximal consistent part of the data: exactly a "
            "remainder, from chapter three. <bookmark mark='c'/>An answer is certain if it holds in every repair, the "
            "skeptical policy of chapter ten. <bookmark mark='d'/>Bob earns forty thousand: certain. Ann earns more "
            "than forty five thousand: certain, since both her salaries do. <bookmark mark='e'/>Ann earns fifty "
            "thousand: not certain. Consistent query answering is AGM's partial meet, running inside a database."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid), FadeIn(key))
            vo.wait_until("a")
            self.play(Indicate(VGroup(grid.cell[0][1], grid.cell[1][1]), color=BAD))
            vo.wait_until("b")
            self.play(FadeIn(reps), FadeIn(qs[0]))
            vo.wait_until("c")
            self.play(FadeIn(qs[1]))
            vo.wait_until("d")
            self.play(FadeIn(qs[2]), FadeIn(qs[3]))
            vo.wait_until("e")
            self.play(FadeIn(qs[4]), FadeIn(qs[5]))
        self.clear_scene()

    def editing(self):
        d = load("editing")
        head = label(r"Editing what a model knows", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rules = label(r"background: \ Barcelona $\to$ Spain, \ Paris $\to$ France, \ one club, \ one country",
                      font_size=21, color=GREY_A).next_to(head, DOWN, buff=0.25)
        before = facts_panel(R.valuation(d["start"], ATOMS), r"believed", -4.6, BEL)
        local = facts_panel(R.valuation(d["local"], ATOMS), r"a local edit", 0.0, BAD)
        agm = facts_panel(d["agm_facts"][0], r"AGM revision", 4.6, OK)
        news = label(r"news: \ he now plays for Paris", font_size=24, color=NEW).next_to(rules, DOWN, buff=0.3)
        lv = label(r"inconsistent with the background" if not d["local_consistent"] else r"consistent", font_size=20,
                   color=BAD).next_to(local, DOWN, buff=0.25)
        av = label(r"the consequences follow the edit", font_size=20, color=OK).next_to(agm, DOWN, buff=0.25)
        foot = label(r"LLM knowledge editing \ (ROME, \ 2022; \ MEMIT, \ 2023) \ often misses these `ripple effects' "
                     r"\ (Cohen et al., \ 2024)", font_size=20, color=GOAL).to_edge(DOWN, buff=0.3)
        if foot.width > 12.8:
            foot.width = 12.8
        with self.voiceover(
            "A modern version of the problem. <bookmark mark='a'/>A knowledge base, or a language model, believes that "
            "a footballer plays for Barcelona and so lives in Spain, against background facts: Barcelona players live "
            "in Spain, Paris players in France, one club, one country. <bookmark mark='b'/>The news: he now plays for "
            "Paris. <bookmark mark='c'/>A local edit flips the club and touches nothing else. The Reasoner finds the "
            "result inconsistent with the background: he lives in Spain while playing for Paris. "
            "<bookmark mark='d'/>AGM revision moves to the closest world consistent with the news and the background: "
            "Paris, and France, and not Spain. The consequences follow the edit. <bookmark mark='e'/>Methods that edit "
            "facts inside large language models, such as ROME and MEMIT, change the target fact well, but Roi Cohen "
            "and colleagues found that they often miss exactly these ripple effects. Closure under consequence, the "
            "first AGM postulate, is what they lack."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rules), FadeIn(before))
            vo.wait_until("b")
            self.play(FadeIn(news))
            vo.wait_until("c")
            self.play(FadeIn(local), FadeIn(lv))
            vo.wait_until("d")
            self.play(FadeIn(agm), FadeIn(av))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def lessons(self):
        head = label(r"What machines need from this part", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = stack([
            (r"an \textit{ordering} of possibilities, \ not just a list of facts", BEL),
            (r"closure: \ consequences must move with the edit", BEL),
            (r"memory: \ iterated revision must keep what the news doesn't touch \ (Darwiche--Pearl)", BEL),
            (r"defaults with exceptions, \ and a policy for conflicts", BEL),
            (r"and humility about `if': \ conditionals are not just more facts \ (the Wall)", GOAL),
        ], font_size=25, buff=0.35, width=12.4).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "What do machines need from this part? <bookmark mark='a'/>An ordering of possibilities, not just a list "
            "of facts, so that they know what to give up. <bookmark mark='b'/>Closure, so that consequences move with "
            "the change. <bookmark mark='c'/>Memory, so that repeated revisions keep what the news doesn't touch. "
            "<bookmark mark='d'/>Defaults with exceptions, and a policy for conflicts between them. "
            "<bookmark mark='e'/>And humility about if: conditionals are not just more facts to be stored."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
