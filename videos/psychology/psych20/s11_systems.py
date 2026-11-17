from __future__ import annotations

from videos.psychology.psych20.common import *  # noqa: F403


class Systems(VoiceoverScene):
    def construct(self):
        self.card()
        self.hm()
        self.taxonomy()
        self.priming()

    def card(self):
        card = chapter_card(10, r"One memory or many?", r"What does a damaged brain say about the parts of memory?",
                            lit={1957: r"Scoville \& Milner", 1970: r"Warrington \& Weiskrantz", 1972: r"Tulving",
                                 1984: r"Graf, \ Squire \& Mandler"},
                            part=PART, scale=("brain", "mind"), marr=("where", "what"))
        with self.voiceover("Chapter ten. One memory or many?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def hm(self):
        h = archive.SCOVILLE_MILNER_1957.data
        head = heading(r"H.M.: \ what was lost, \ and what was not")
        rows = rows_of([
            (rf"{h['year']}: \ to stop his seizures, \ {h['removed']}", WHITE),
            (r"lost: \ the ability to lay down new memories of facts and events, \ for the rest of his life", LOST),
            (r"kept: \ his intelligence, \ his language, \ his old memories from long before the operation, \ and a "
             r"span of about seven digits", MODEL),
            (r"and something more: \ over three days of mirror drawing he improved like anyone, \ and each day said "
             r"he had never done it", WORD),
            (r"short-term and long-term memory came apart; \ so did knowing \emph{that} and knowing \emph{how}", CTX),
        ], 12.4, 26, 0.35).move_to([0, -0.2, 0])
        tag = historical_tag(archive.SCOVILLE_MILNER_1957.cite + r"; \ Milner (1962)")
        with self.voiceover(
            "Part 7 introduced Henry Molaison, known for fifty years as the patient H.M. "
            f"<bookmark mark='a'/> In {h['year']}, to stop his seizures, the surgeon William Scoville removed the "
            "inner part of both temporal lobes, including most of the hippocampus. <bookmark mark='b'/> The seizures "
            "eased. But from then on he could not form new memories of facts or events. He met Brenda Milner, who "
            "studied him for decades, as a stranger every time. <bookmark mark='c'/> A great deal was untouched: "
            "his intelligence, his language, memories from long before the operation, and his span, which was "
            "normal. Holding a few digits for a few seconds was fine; it was laying down anything lasting that had "
            "gone. <bookmark mark='d'/> And Milner found something else. Asked to trace a star while watching his "
            "hand in a mirror, he improved over three days like anyone else, while saying each day that he had "
            "never done it before. <bookmark mark='e'/> Two splits at once: short-term from long-term memory, and "
            "knowing that from knowing how."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def taxonomy(self):
        head = heading(r"A map of memory systems")

        def box(t, col, w=3.1):
            tx = label(t, font_size=22, color=col)
            b = RoundedRectangle(corner_radius=0.1, width=max(w, tx.width + 0.35), height=0.7, stroke_color=col,
                                 stroke_width=2.5)
            return VGroup(b, tx.move_to(b))

        top = box(r"long-term memory", WHITE).move_to([0, 2.2, 0])
        decl = box(r"declarative: \ knowing that", MODEL, 3.6).move_to([-3.4, 1.0, 0])
        nond = box(r"non-declarative: \ knowing how", WORD, 3.6).move_to([3.4, 1.0, 0])
        epi = box(r"episodic: \ events", CTX).move_to([-5.0, -0.25, 0])
        sem = box(r"semantic: \ facts", CTX).move_to([-1.8, -0.25, 0])
        skills = box(r"skills", WORD, 1.7).move_to([1.3, -0.25, 0])
        prim = box(r"priming", WORD, 1.7).move_to([3.2, -0.25, 0])
        cond = box(r"conditioning", WORD, 2.2).move_to([5.4, -0.25, 0])
        lines = VGroup(*[Line(a.get_bottom(), b.get_top(), color=GREY_C, stroke_width=2) for a, b in
                         ((top, decl), (top, nond), (decl, epi), (decl, sem), (nond, skills), (nond, prim),
                          (nond, cond))])
        where = VGroup(
            label(r"hippocampus and medial temporal lobe", font_size=18, color=MODEL).next_to(VGroup(epi, sem), DOWN,
                                                                                               buff=0.22),
            label(r"basal ganglia, \ cerebellum, \ cortex, \ amygdala", font_size=18, color=WORD).next_to(
                VGroup(skills, prim, cond), DOWN, buff=0.22),
        )
        rows = rows_of([
            (r"Tulving, \ 1972: \ remembering an event, \ and knowing a fact, \ are different kinds of memory", CTX),
            (r"Squire's taxonomy: \ a hippocampal system for facts and events, \ and several others that need no "
             r"awareness", MODEL),
            (r"a dissociation (Part 7) is evidence for separate systems, \ not proof: \ one system with two kinds of "
             r"test can mimic it", LOST),
        ], 12.6, 23, 0.25).to_edge(DOWN, buff=0.85)
        tag = historical_tag(r"Tulving (1972); \ Squire (1992, \ 2004)")
        with self.voiceover(
            "Patients like H.M. led to a map. <bookmark mark='a'/> In 1972 Endel Tulving separated episodic memory, "
            "for events you were there for, from semantic memory, for facts you know without remembering learning "
            "them. <bookmark mark='b'/> Larry Squire's taxonomy puts both under declarative memory, which depends on "
            "the hippocampus and the medial temporal lobe and can be brought to mind. Under non-declarative memory "
            "go skills, priming and conditioning, which show themselves in performance and live in the basal "
            "ganglia, the cerebellum and the cortex itself. <bookmark mark='c'/> But remember the warning from Part "
            "7. A dissociation, in which a patient fails one test and passes another, is evidence for separate "
            "systems, not proof. One system tested in two different ways can produce the same pattern, if one test "
            "is simply more sensitive than the other. The next example shows how carefully that has to be checked."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lines[0]), FadeIn(decl), Create(lines[2]), Create(lines[3]), FadeIn(epi), FadeIn(sem),
                      FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(lines[1]), FadeIn(nond), *[Create(l_) for l_ in lines[4:]], FadeIn(skills),
                      FadeIn(prim), FadeIn(cond), FadeIn(where), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def priming(self):
        head = heading(r"The same words, \ two instructions")
        stem = label(r"MOT\underline{\ \ \ \ \ \ \ \ }", font_size=56, color=WORD).move_to([0, 2.1, 0])
        ins = VGroup(
            label(r"``complete it with the first word that comes to mind''", font_size=26, color=MODEL),
            label(r"``complete it with a word from the list you studied''", font_size=26, color=LOST),
        ).arrange(DOWN, buff=0.3).next_to(stem, DOWN, buff=0.45)
        rows = rows_of([
            (r"Warrington and Weiskrantz, \ 1970: \ amnesic patients helped by word fragments as much as anyone", WHITE),
            (r"Graf, \ Squire and Mandler, \ 1984: \ the same stems, \ two instructions", WHITE),
            (r"first word that comes to mind: \ amnesic patients complete as many studied words as controls: \ "
             r"priming is intact", MODEL),
            (r"a word from the list: \ the same stems, \ now a memory test, \ and the patients fall far behind", LOST),
            (r"same cue, \ same words, \ only the instruction differs: \ the strongest case for separate systems", CTX),
        ], 12.4, 25, 0.3).move_to([0, -1.5, 0])
        tag = historical_tag(r"Warrington \& Weiskrantz (1970); \ Graf, \ Squire \& Mandler (1984)")
        with self.voiceover(
            "In 1970 Elizabeth Warrington and Lawrence Weiskrantz found that amnesic patients, who could not "
            "recall a list of words, were helped by fragments of those words as much as anyone. "
            "<bookmark mark='a'/> Peter Graf, Larry Squire and George Mandler made the test exact in 1984. After "
            "studying a list including motel, people saw the first three letters of words, M O T. "
            "<bookmark mark='b'/> Told to complete each stem with the first word that came to mind, amnesic patients "
            "produced studied words as often as healthy people did: the list had primed them. "
            "<bookmark mark='c'/> Told to complete the same stems with words from the list, the healthy people "
            "improved and the patients did not. <bookmark mark='d'/> Same words, same cues, same patients; only the "
            "instruction changes, from use to remember. That's about as clean a dissociation as there is, and it's "
            "the strongest case that remembering and being influenced by the past rest on different systems."
        ) as vo:
            self.play(FadeIn(head), FadeIn(stem), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(ins[0]), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(ins[1]), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
