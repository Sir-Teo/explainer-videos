from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs39.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, mono)


class Crdt(VoiceoverScene):
    def construct(self):
        self.card()
        self.lattice()
        self.gcounter()
        self.measured()
        self.sets()
        self.editing()
        self.cost()

    def card(self):
        card = chapter_card(3, r"CRDTs", r"Can replicas accept every write and still agree?", lit=(2011, 2011),
                            extra=((2011, r"Shapiro, Pregui\c{c}a, \\ Baquero and Zawirski"),), part=PART)
        with self.voiceover("Chapter three. Conflict-free replicated data types."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def lattice(self):
        head = label(r"Merge must be a join", font_size=36).to_edge(UP, buff=0.3)
        props = VGroup(
            MathTex(r"a \sqcup b = b \sqcup a", font_size=36, color=DATA),
            MathTex(r"(a \sqcup b) \sqcup c = a \sqcup (b \sqcup c)", font_size=36, color=LAM),
            MathTex(r"a \sqcup a = a", font_size=36, color=KERN),
        ).arrange(DOWN, buff=0.3).move_to([-3.6, 0.6, 0])
        names = VGroup(label(r"commutative", font_size=20, color=DATA), label(r"associative", font_size=20, color=LAM),
                       label(r"idempotent", font_size=20, color=KERN))
        for n, p in zip(names, props):
            n.next_to(p, LEFT, buff=0.3)
        side = VGroup(
            wrapped_label(r"each replica's state lives in a \textbf{join-semilattice}; \ local updates only move "
                          r"\textit{up}; \ merging two states takes their least upper bound", 5.8, font_size=20,
                          color=WHITE),
            wrapped_label(r"\textbf{Theorem.} \ If every update eventually reaches every replica, \ in any order, \ "
                          r"any number of times, \ all replicas reach the same state: \ the join of all updates.", 5.8,
                          font_size=20, color=YES),
            wrapped_label(r"\textit{Proof.} \ A replica's state is the join of the updates it has received, \ "
                          r"because the three laws let us reorder, \ regroup and deduplicate them. \ Replicas that "
                          r"have received the same set are therefore equal.", 5.8, font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, -0.2, 0])
        with self.voiceover(
            "Multi-leader and leaderless systems must merge conflicting copies. In 2011 Marc Shapiro and his "
            "colleagues found a way to make every merge safe: design the data type so that merging is a join. "
            "<bookmark mark='a'/> Merging must be commutative, so the order of messages does not matter; "
            "associative, so the grouping does not matter; and idempotent, so receiving the same state twice does "
            "nothing. <bookmark mark='b'/> Mathematically, the states form a join-semilattice: updates only move "
            "up, and merge takes the least upper bound. <bookmark mark='c'/> Then convergence is a theorem: if "
            "every update eventually reaches every replica, in any order and any number of times, all replicas end "
            "in the same state. <bookmark mark='d'/> The proof is that a replica's state is just the join of the "
            "updates it has seen, and the three laws let us reorder, regroup and deduplicate them freely."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(Write(p), FadeIn(n)) for p, n in zip(props, names)],
                                  lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def gcounter(self):
        c = load("crdt")
        head = label(r"A counter that cannot lose increments", font_size=36).to_edge(UP, buff=0.3)
        rows = [[s[0], mono(str(tuple(s[1])), 18, DATA), mono(str(tuple(s[2])), 18, LAM), mono(str(tuple(s[3])), 18,
                                                                                               KERN)]
                for s in c["gcounter"]]
        tab = VGroup()
        hdr = VGroup(*[label(t, font_size=20, color=GREY_B) for t in (r"step", r"replica A", r"replica B",
                                                                     r"replica C")])
        xs = [-4.2, -0.6, 1.9, 4.4]
        for t, x in zip(hdr, xs):
            t.move_to([x, 1.8, 0])
        tab.add(hdr)
        for i, row in enumerate(rows):
            y = 1.2 - i * 0.6
            items = [label(row[0], font_size=20, color=WHITE)] + row[1:]
            for t, x in zip(items, xs):
                t.move_to([x, y, 0])
            tab.add(VGroup(*items))
        notes = VGroup(
            wrapped_label(r"\textbf{G-counter}: \ one slot per replica; \ a replica increments only its own; \ merge "
                          r"takes the maximum of each slot; \ the value is the sum", 12.4, font_size=21, color=WHITE),
            wrapped_label(rf"after gossip, \ every replica holds (2, 1, 0): \ value {c['value']}, \ though no message "
                          r"was ordered and some were merged twice", 12.4, font_size=21, color=YES),
            wrapped_label(r"\textbf{PN-counter}: \ two G-counters, \ increments minus decrements; \ "
                          r"\textbf{LWW register}: \ keep the value with the highest (timestamp, replica)", 12.4,
                          font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The simplest example is a counter. A naive replicated counter, add the other replica's count when you "
            "merge, double-counts the moment a merge is repeated. <bookmark mark='a'/> A grow-only counter keeps "
            "one slot per replica. Each replica increments only its own slot, merging takes the maximum of each "
            "slot, and the value is the sum. Here replica A adds two and B adds one; C merges A; A merges B; then "
            "they gossip in no particular order. <bookmark mark='b'/> Every replica ends with two, one, zero: a "
            "value of three, though messages crossed and some states were merged twice. "
            "<bookmark mark='c'/> Two of them make a counter that can go down, and a last-writer-wins register "
            "keeps whichever value has the highest timestamp, which is a join too, though it silently discards the "
            "losing write."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            self.play(LaggedStart(*[FadeIn(r) for r in tab[1:]], lag_ratio=0.5), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def measured(self):
        c = load("crdt")
        head = label(r"Tested: \ random gossip, \ random orders", font_size=36).to_edge(UP, buff=0.3)
        names = {"gcounter": r"G-counter", "pncounter": r"PN-counter", "orset": r"observed-remove set",
                 "lww": r"last-writer-wins register", "naive-set": r"naive set \ (replay the other's log)"}
        rows = [[names[r["kind"]], f"{r['converged']} of {r['trials']}"] for r in c["rows"]]
        tab = grid_table([r"data type", r"runs in which all replicas agree"], rows, widths=[5.6, 4.2], row_h=0.5,
                         font_size=22, mono_cols=())
        tab.next_to(head, DOWN, buff=0.6).set_x(0)
        for k, r in enumerate(c["rows"], start=1):
            tab.cells[k][1].set_color(YES if r["converged"] == r["trials"] else NO)
        foot = wrapped_label(r"four replicas, \ 40 random operations each run, \ merges in random directions and "
                             r"orders, \ then anti-entropy until every pair has merged. \ The naive set applies the "
                             r"other replica's adds and removes in its own order: \ add-then-remove on one side and "
                             r"remove-then-add on the other disagree for ever.", 12.4, font_size=20,
                             color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "We tested four CRDTs against a naive alternative, a thousand runs each: four replicas, forty random "
            "operations, merges between random pairs in random directions, and finally gossip until every pair has "
            "merged. <bookmark mark='a'/> Every CRDT converged in every run. The naive set, which merges by replaying "
            "the other replica's log of adds and removes, ended with every replica agreeing in only fifteen runs of "
            "a thousand, because adding and removing the same element do not commute."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(foot))
        self.wait(0.5)
        self.clear_scene()

    def sets(self):
        head = label(r"Sets, \ sequences, \ and shared documents", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"\textbf{OR-set}: \ every add carries a unique tag; \ a remove deletes only the tags it has "
                          r"seen, \ so a concurrent add wins \ (``add-wins'')", 12.4, font_size=22, color=YES),
            wrapped_label(r"\textbf{sequence CRDTs} \ (RGA, \ Logoot, \ Fugue): \ each character gets an identifier "
                          r"between its neighbours', \ so concurrent insertions interleave the same way on every "
                          r"replica: \ collaborative editors", 12.4, font_size=22, color=LAM),
            wrapped_label(r"the alternative, \ \textbf{operational transformation} \ (Google Docs), \ rewrites "
                          r"concurrent edits against each other through a server", 12.4, font_size=22, color=HEAD),
            wrapped_label(r"the catch: \ CRDTs converge, \ but to \textit{a} state, \ not necessarily the one users "
                          r"meant; \ and invariants that span replicas \ (``the balance stays positive'') \ still need "
                          r"coordination", 12.4, font_size=22, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "The same idea scales to richer types. <bookmark mark='a'/> An observed-remove set tags every addition "
            "uniquely, and a removal deletes only the tags it has seen, so an addition concurrent with a removal "
            "survives. <bookmark mark='b'/> Sequence CRDTs give every character an identifier that sorts between its "
            "neighbours', so two people typing at the same spot see their characters interleaved the same way on "
            "every replica: the basis of collaborative editors that work offline. <bookmark mark='c'/> Google Docs "
            "took the other road, operational transformation, rewriting concurrent edits against each other through "
            "a central server. <bookmark mark='d'/> The catch: a CRDT guarantees that replicas agree, not that they "
            "agree on what users intended, and an invariant spanning replicas, like a balance that must not go "
            "negative, still needs coordination."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def editing(self):
        r = load("rga")
        d = r["demo"]
        head = label(r"Two people, \ one sentence", font_size=36).to_edge(UP, buff=0.3)

        def line(who, txt, col):
            return VGroup(label(who, font_size=20, color=GREY_A), mono(txt, size=24, color=col)).arrange(
                RIGHT, buff=0.3)
        start = line(r"both start with", "the cat sat", WHITE)
        local = VGroup(line(r"Alice types ``fat ''", d["rga"]["a_local"], HEAD),
                       line(r"Bob changes ``sat'' to ``ran''", d["rga"]["b_local"], LAM)).arrange(DOWN, buff=0.2,
                                                                                                  aligned_edge=LEFT)
        naive = VGroup(label(r"replaying positions: \ ``insert at 4'', \ ``delete at 8''", font_size=20, color=NO),
                       line(r"Alice now has", d["naive"]["a"], NO), line(r"Bob now has", d["naive"]["b"], NO)).arrange(
            DOWN, buff=0.16, aligned_edge=LEFT)
        rga = VGroup(label(r"RGA: \ ``insert after the character with id (4, A)''", font_size=20, color=YES),
                     line(r"Alice now has", d["rga"]["a"], YES), line(r"Bob now has", d["rga"]["b"], YES)).arrange(
            DOWN, buff=0.16, aligned_edge=LEFT)
        col = VGroup(start, local).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(head, DOWN, buff=0.45).to_edge(
            LEFT, buff=0.8)
        VGroup(naive, rga).arrange(RIGHT, buff=0.8, aligned_edge=UP).next_to(col, DOWN, buff=0.45).set_x(0)
        foot = wrapped_label(rf"random sessions, \ {r['users']} editors, \ {r['ops']} edits, \ any delivery order: \ "
                             rf"RGA converged in {r['sessions']['rga']} of {r['trials']}, \ positional replay in "
                             rf"{r['sessions']['naive']}", 12.4, font_size=21, color=WHITE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Text is the hardest case, because edits name positions, and positions shift. <bookmark mark='a'/> "
            "Alice and Bob share the sentence the cat sat. At the same moment Alice types fat in front of cat, and "
            "Bob changes sat to ran. <bookmark mark='b'/> If each replica simply replays the other's edits by "
            "position, insert at four, delete at eight, Bob ends up right by luck, and Alice's copy deletes the "
            "wrong word: the fat ran sat. The replicas disagree for ever. <bookmark mark='c'/> A sequence CRDT such "
            "as RGA, the replicated growable array, never uses positions. Every character gets a unique identifier, "
            "a counter and the replica's name, and an insertion says which character it follows. Deletions leave "
            "an invisible tombstone, and characters inserted after the same one are ordered by identifier. Both "
            "replicas now read the fat cat ran. <bookmark mark='d'/> In five hundred random sessions of three "
            "editors, RGA converged every time, and positional replay never did. Editors like Automerge and Yjs "
            "are built this way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(start))
            vo.wait_until("a")
            self.play(FadeIn(local))
            vo.wait_until("b")
            self.play(FadeIn(naive))
            vo.wait_until("c")
            self.play(FadeIn(rga))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def cost(self):
        o = load("overhead")
        rows_d = o["rows"]
        head = label(r"What convergence costs", font_size=36).to_edge(UP, buff=0.3)
        top = max(r["visible"] + r["tombstones"] for r in rows_d)
        bars = VGroup()
        x0, w, hmax, y0 = -5.8, 0.9, 3.6, -2.2
        for i, r in enumerate(rows_d):
            x = x0 + i * 1.5
            hv = hmax * r["visible"] / top
            ht = hmax * r["tombstones"] / top
            bv = Rectangle(width=w, height=hv, stroke_width=0, fill_color=YES, fill_opacity=0.85).move_to(
                [x, y0 + hv / 2, 0])
            bt = Rectangle(width=w, height=ht, stroke_width=0, fill_color=GREY_C, fill_opacity=0.7).move_to(
                [x, y0 + hv + ht / 2, 0])
            lb = label(f"{r['edits']:,}", font_size=16, color=GREY_B).move_to([x, y0 - 0.25, 0])
            bars.add(VGroup(bv, bt, lb))
        xl = label(r"edits so far", font_size=17, color=GREY_A).move_to([x0 + 2.25, y0 - 0.65, 0])
        key = VGroup(label(r"visible characters", font_size=17, color=YES),
                     label(r"tombstones", font_size=17, color=GREY_B)).arrange(RIGHT, buff=0.5).move_to(
            [x0 + 2.25, 1.9, 0])
        last = rows_d[-1]
        notes = VGroup(
            wrapped_label(rf"one RGA document, \ {o['p_delete'] * 100:.0f}\% of edits deletions: \ after "
                          rf"{last['edits']:,} edits, \ {last['visible']:,} characters visible and "
                          rf"{last['tombstones']:,} tombstones kept", 5.8, font_size=19, color=WHITE),
            wrapped_label(rf"each element carries its own id and its neighbour's \ ({o['id_bytes']} bytes each): \ "
                          rf"{last['bytes_per_char']:.0f} bytes per visible character, \ against 1 for plain text",
                          5.8, font_size=19, color=NO),
            wrapped_label(r"a tombstone may be discarded only once every replica has seen the delete \ "
                          r"(\textit{causal stability}): \ knowing that is itself coordination", 5.8, font_size=19,
                          color=HEAD),
            wrapped_label(r"compact encodings \ (runs of consecutive ids, \ column compression) \ in Automerge and "
                          r"Yjs cut the overhead by orders of magnitude", 5.8, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.4, -0.2, 0])
        with self.voiceover(
            "Convergence is not free. <bookmark mark='a'/> We edited one RGA document twenty thousand times, three "
            "edits in ten being deletions. Deleted characters cannot simply vanish, because a late insertion might "
            "still refer to them, so they stay as tombstones: after twenty thousand edits, eight thousand visible "
            "characters and almost six thousand tombstones. <bookmark mark='b'/> Every element carries its own "
            "identifier and its neighbour's, so the document costs forty-two bytes for each character you can see, "
            "against one for plain text. <bookmark mark='c'/> A tombstone can be thrown away only when every replica "
            "has seen the deletion, and knowing that requires the replicas to coordinate, the very thing CRDTs "
            "avoid. <bookmark mark='d'/> Practical libraries such as Automerge and Yjs store runs of consecutive "
            "identifiers and compress by column, and cut the overhead by orders of magnitude. Making that "
            "efficient was one of the research problems of the last decade."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in bars], lag_ratio=0.3), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA,)
