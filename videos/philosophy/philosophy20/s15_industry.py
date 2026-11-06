from __future__ import annotations

from videos.philosophy.philosophy20.common import *  # noqa: F403


class Industry(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"Ontologies in practice", r"What happens when ontology is someone's job?",
                            lit=(2001, 2009), part=PART)
        with self.voiceover("Chapter fourteen. Ontologies in practice."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.landscape()
        self.bfo()
        self.ontoclean()

    def landscape(self):
        head = label(r"Ontologies that run the world", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the semantic web", r"Berners-Lee, \ Hendler and Lassila \ (2001): \ machine-readable meaning on the "
                                  r"web; \ OWL, \ a W3C standard \ (2004; \ OWL 2, \ 2009)", UNIV),
            (r"Gene Ontology \ (2000)", r"tens of thousands of terms for gene functions, \ processes and cell "
                                        r"components, \ used to annotate millions of genes", PARTC),
            (r"SNOMED CT", r"hundreds of thousands of clinical concepts, \ defined in a description logic, \ behind "
                           r"electronic health records", WHOLE),
            (r"Wikidata; \ schema.org", r"the structured data behind search engines and assistants", NOM),
            (r"the work", r"deciding what the categories are, \ how they relate, \ and what counts as the same thing",
             GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.6, x_text=-2.4, label_size=21)
        with self.voiceover(
            "Formal ontology is now an industry. <bookmark mark='a'/>In 2001 Tim Berners-Lee, James Hendler and Ora "
            "Lassila proposed a semantic web of machine-readable meaning; its ontology language, OWL, became a web "
            "standard. <bookmark mark='b'/>The Gene Ontology, founded in 2000, provides tens of thousands of terms for "
            "what genes do, and is used to annotate millions of genes across species. <bookmark mark='c'/>SNOMED CT "
            "defines hundreds of thousands of clinical concepts in a description logic, and sits behind electronic "
            "health records. <bookmark mark='d'/>Wikidata and schema.org structure the data that search engines and "
            "assistants use. <bookmark mark='e'/>The daily work of these projects is ontology in the philosopher's "
            "sense: what the categories are, how they relate, and what counts as the same thing."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def bfo(self):
        head = label(r"Basic Formal Ontology: \ Aristotle as an ISO standard", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        tree = {
            "entity": (0.0, 2.0, GOAL),
            "continuant": (-3.6, 0.9, UNIV), "occurrent": (3.6, 0.9, WHOLE),
            "independent continuant": (-5.4, -0.3, UNIV), "dependent continuant": (-1.8, -0.3, UNIV),
            "process": (2.4, -0.3, WHOLE), "temporal region": (5.0, -0.3, WHOLE),
            "material object": (-5.4, -1.5, PARTC), "quality": (-2.8, -1.5, NOM), "function": (-0.8, -1.5, NOM),
        }
        edges = [("entity", "continuant"), ("entity", "occurrent"), ("continuant", "independent continuant"),
                 ("continuant", "dependent continuant"), ("occurrent", "process"), ("occurrent", "temporal region"),
                 ("independent continuant", "material object"), ("dependent continuant", "quality"),
                 ("dependent continuant", "function")]
        nodes = {}
        for n, (x, y, c) in tree.items():
            t = label(n, font_size=16, color=c)
            b = SurroundingRectangle(t, buff=0.08, corner_radius=0.06, color=c, stroke_width=1.5)
            nodes[n] = VGroup(b, t).move_to([x, y, 0])
        lines = VGroup(*[Line(nodes[a].get_bottom(), nodes[b].get_top(), color=GREY_B, stroke_width=2)
                         for a, b in edges])
        rows = stack([(r"continuants persist through time, \ wholly present at each moment: \ a heart", UNIV),
                      (r"occurrents unfold in time, \ with temporal parts: \ a heartbeat", WHOLE),
                      (r"dependent continuants inhere in others: \ the heart's function, \ its colour \ (chapter 3)",
                       NOM),
                      (r"ISO/IEC 21838-2 \ (2021): \ the top level of hundreds of ontologies", GOAL)], font_size=19,
                     aligned_edge=LEFT, width=12.4).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Many biomedical ontologies share a top level, Basic Formal Ontology, which reads like a page of "
            "Aristotle. <bookmark mark='a'/>Its first division is between continuants, which persist through time and "
            "are wholly present at each moment, like a heart, <bookmark mark='b'/>and occurrents, which unfold in time "
            "and have temporal parts, like a heartbeat. <bookmark mark='c'/>Some continuants depend on others: the "
            "heart's function, from Part 19, and its colour, the qualities of chapter three. "
            "<bookmark mark='d'/>It became an international standard in 2021, and hundreds of ontologies are built "
            "on it. Whether things persist by being wholly present or by having temporal parts is the question of "
            "Part 21."
        ) as vo:
            self.play(FadeIn(head), FadeIn(nodes["entity"]))
            vo.wait_until("a")
            self.play(FadeIn(nodes["continuant"]), FadeIn(nodes["independent continuant"]),
                      FadeIn(nodes["material object"]), Create(VGroup(lines[0], lines[2], lines[6])), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(nodes["occurrent"]), FadeIn(nodes["process"]), FadeIn(nodes["temporal region"]),
                      Create(VGroup(lines[1], lines[4], lines[5])), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(nodes["dependent continuant"]), FadeIn(nodes["quality"]), FadeIn(nodes["function"]),
                      Create(VGroup(lines[3], lines[7], lines[8])), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def ontoclean(self):
        d = load("ontoclean")
        head = label(r"OntoClean: \ philosophy as a debugger \ (Guarino and Welty, \ 2002)", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        tax = d["taxonomy"]
        hd = [r"\text{subclass}", r"\text{superclass}", r"\text{verdict}"]
        rows = []
        for r in d["report"]:
            sub = r["sub"] + " (" + tax[r["sub"]][0] + ")"
            sup = r["sup"] + " (" + tax[r["sup"]][0] + ")"
            rows.append([MathTex(r"\text{" + sub.replace("~", r"$\sim$") + "}", font_size=20),
                         MathTex(r"\text{" + sup.replace("~", r"$\sim$") + "}", font_size=20),
                         MathTex(r"\checkmark" if r["ok"] else r"\times", font_size=26, color=OK if r["ok"] else BAD)])
        grid = ValueGrid(hd, rows, col_w=[3.6, 3.8, 1.3], cell_h=0.44, font_size=19).move_to([-2.2, 0.0, 0])
        key = label(r"+R: \ rigid \ (essential to its instances); \ \ $\sim$R: \ anti-rigid \ (a role or phase)",
                    font_size=16, color=GREY_A).next_to(grid, UP, buff=0.15)
        bad = [r for r in d["report"] if not r["ok"]]
        expl = stack([(r"`" + r["sub"] + (r" is an " if r["sup"][0] in "AEIOU" else r" is a ") + r["sup"] + r"': \ " +
                       r["why"], BAD) for r in bad] +
                     [(r"fixes: \ make \textit{Legal agent} and \textit{Food} roles; \ say objects are "
                       r"\textit{constituted by} matter", OK)], font_size=17, aligned_edge=LEFT, width=4.6).move_to(
            [4.5, -0.3, 0])
        with self.voiceover(
            "Philosophy turns out to debug ontologies. <bookmark mark='a'/>Nicola Guarino and Christopher Welty's "
            "OntoClean marks each class with metaproperties. A class is rigid if it is essential to its instances: a "
            "person cannot stop being a person. It is anti-rigid if every instance could stop belonging to it: a "
            "student can graduate. <bookmark mark='b'/>The Reasoner checks a small taxonomy against two constraints. "
            "<bookmark mark='c'/>It flags three links. Person is a legal agent: but being a legal agent is a role, "
            "anti-rigid, and a rigid class cannot sit under an anti-rigid one. Apple is a food: the same mistake, "
            "since being food is a role an apple plays. And physical object is an amount of matter: a countable thing "
            "under a mass, with incompatible criteria of identity. <bookmark mark='d'/>The fixes come from the "
            "philosophy of this part: treat roles as roles, and say that objects are constituted by matter, not "
            "identical to it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(key))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule),
                      LaggedStart(*[FadeIn(VGroup(*grid.cell[i][:2])) for i in range(len(rows))], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(grid.cell[i][2]) for i in range(len(rows))], lag_ratio=0.15),
                      *[FadeIn(e) for e in expl[:-1]])
            vo.wait_until("d")
            self.play(FadeIn(expl[-1]))
        self.clear_scene()
