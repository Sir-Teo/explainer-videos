from __future__ import annotations

import numpy as np

from videos.psychology.psych7.common import *  # noqa: F403


class Memory(VoiceoverScene):
    def construct(self):
        self.card()
        self.operation()
        self.spared()
        self.skill()
        self.caution()

    def card(self):
        card = chapter_card(7, r"The man who could not make new memories", r"Is memory one thing?",
                            lit={1953: r"H.M.'s operation"}, part=PART, scale=("brain", "mind"),
                            marr=("how", "tissue"))
        with self.voiceover(
            "Chapter seven. The man who could not make new memories."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def operation(self):
        d = archive.SCOVILLE_MILNER_1957.data
        head = heading(rf"Hartford, {d['year']}: \ an operation for epilepsy")
        b = brain_medial(6.0, [-3.8, 0.1, 0])
        cut = lesion_mark(b.at(0.08, -0.22), 0.62)
        cut.set_fill(opacity=0.55)
        cut_l = label(r"removed, on both sides", font_size=24, color=LESION).next_to(b.shell, DOWN, buff=0.12)
        rows = VGroup(
            wrapped_label(r"Henry Molaison, 27, \ with seizures that no drug controlled", 5.6, 28, WHITE),
            wrapped_label(r"the surgeon removes the inner part of both temporal lobes, \ with most of the "
                          r"hippocampus", 5.6, 28, LESION),
            wrapped_label(r"the seizures ease", 5.6, 28, SPARED),
            wrapped_label(r"and from that day he cannot lay down a new memory of anything that happens to "
                          r"him, \ for the next 55 years", 5.6, 28, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([3.5, -0.2, 0])
        keep_in_frame(rows)
        src = historical_tag(archive.SCOVILLE_MILNER_1957.cite)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            f"In {d['year']}, in Hartford, Connecticut, a young man called Henry Molaison had an operation. "
            "<bookmark mark='a'/> He was twenty-seven, and he had epileptic seizures so frequent that he "
            "couldn't work, and no drug controlled them. <bookmark mark='b'/> His surgeon, William Scoville, "
            "tried something that had never been done to a patient of sound mind. He removed the inner part "
            "of the temporal lobe on both sides of the brain, and with it most of the hippocampus. "
            "<bookmark mark='c'/> The seizures eased. <bookmark mark='d'/> And from that day, Henry Molaison "
            "could not lay down a new memory of anything that happened to him. He would meet someone, talk "
            "to them, and a few minutes after they left the room he had no idea he'd ever seen them. He read "
            "the same magazine again and again as if it were new. He lived like that for fifty-five more "
            "years. To science he was known, until he died in 2008, by his initials: H.M."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(b.shell), FadeIn(b.hippocampus),
                      FadeIn(b.callosum))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(cut, scale=0.4), FadeIn(cut_l), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def spared(self):
        m = load("memory")
        head = heading(r"What was lost, \ and what was not")
        names = {"recall today tomorrow": r"remember today, tomorrow",
                 "recall childhood": r"remember his childhood",
                 "repeat seven digits": r"hold seven digits for a few seconds",
                 "learn mirror tracing": r"learn a new skill of the hands"}
        rows = VGroup()
        heads = VGroup(label(r"before", font_size=28, color=GREY_A), label(r"after", font_size=28, color=GREY_A))
        for t, a, h in zip(m["tasks"], m["intact"], m["hm"]):
            name = label(names[t], font_size=34, color=WHITE)
            rows.add(VGroup(name, score_bar(a, SPARED, 2.6, 0.44), score_bar(h, SPARED if h > 0.5 else LESION, 2.6,
                                                                             0.44)))
        y = 1.35
        for r in rows:
            r[0].move_to([-0.6, y, 0], aligned_edge=RIGHT)
            r[1].move_to([1.3, y, 0])
            r[2].move_to([4.5, y, 0])
            y -= 0.95
        heads[0].move_to([1.3, 2.15, 0])
        heads[1].move_to([4.5, 2.15, 0])
        gone = label(r"gone", font_size=30, color=LESION).move_to(rows[0][2])
        table = VGroup(rows, heads, gone)
        keep_in_frame(table)
        end = wrapped_label(r"One operation removed one kind of remembering and left three others. \ Memory is "
                            r"not one thing.", 12.6, 30, P.ACCENT).to_edge(DOWN, buff=0.75)
        tag = psyche_tag(r"computed: Psyche, a memory architecture with one part removed")
        with self.voiceover(
            "What makes H.M. the most important patient in the history of this subject is what he didn't "
            "lose. <bookmark mark='a'/> He could no longer remember today, tomorrow. <bookmark mark='b'/> "
            "But his memories of childhood were there. He knew who he was, and where he grew up. "
            "<bookmark mark='c'/> He could hold a string of digits in mind for as long as he kept attending "
            "to them, as well as you can. His intelligence and his language were untouched. A conversation "
            "with him was perfectly normal, until something distracted him. <bookmark mark='d'/> And he "
            "could learn new skills, which is the next shot. <bookmark mark='e'/> Until 1953 most people who "
            "thought about it took memory to be one faculty, spread through the brain, as Lashley had "
            "concluded. One operation removed one kind of remembering and left three others standing. In "
            "the model on screen that's one box out of four. Memory is not one thing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(heads))
            for k, mark_ in enumerate("abcd"):
                vo.wait_until(mark_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15), *([FadeIn(gone)] if k == 0 else []))
            vo.wait_until("e")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def skill(self):
        m = load("memory")
        head = heading(r"1962: \ he learns, and does not know that he has learned")
        # the task, drawn: a star seen in a mirror
        c0 = np.array([-5.3, 0.9, 0])
        star = VGroup(*[Star(n=5, outer_radius=r, color=VOLT, stroke_width=3).move_to(c0) for r in (1.35, 1.0)])
        star_l = wrapped_label(r"trace between the two lines, \ seeing your hand only in a mirror", 3.2, 25,
                               GREY_A).next_to(star, DOWN, buff=0.2)
        A = axes([0, 31], [0, 40], x_length=5.4, y_length=3.6, xticks=[1, 10, 20, 30], yticks=[0, 20, 40],
                 xlabel=r"attempt (ten a day, for three days)", ylabel=r"errors", center=[-0.45, -0.75, 0])
        ax = A.ax
        t = m["trials"]
        days = VGroup(*[DashedLine(ax.c2p(x, 0), ax.c2p(x, 40), color=GREY_D, stroke_width=2) for x in (10.5, 20.5)])
        c_hm = curve(ax, t, m["errors_hm"], LESION, stroke_width=4)
        c_in = curve(ax, t, m["errors_intact"], GREY_B, stroke_width=2.5)
        lg = legend([(LESION, r"without the hippocampal system"), (GREY_B, r"with it")], font_size=22)
        lg.next_to(ax.c2p(31, 40), DL, buff=0.1)
        side = VGroup(
            wrapped_label(r"his errors fall, \ day after day, \ like anyone's", 3.8, 30, WHITE),
            wrapped_label(r"each day he says he has never seen the task before", 3.8, 30, LESION),
            wrapped_label(r"skill and recollection come apart", 3.8, 31, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([5.0, -0.4, 0])
        keep_in_frame(side)
        src = historical_tag(archive.SCOVILLE_MILNER_1957.cite)
        tag = psyche_tag(r"computed: the shape of the result, not Milner's figures")
        with self.voiceover(
            "The psychologist who studied him for decades was Brenda Milner. In 1962 she gave him a task "
            "that's maddening for anyone. <bookmark mark='a'/> Trace a star, keeping your pencil between two "
            "lines, while you can see your hand only in a mirror. Everyone is terrible at first. "
            "<bookmark mark='b'/> H.M. practised for three days, and his errors fell, day after day, the "
            "way anyone's would. By the third day he was good at it. <bookmark mark='c'/> And every day, "
            "when the apparatus was brought out, he said he'd never seen it before. He had the skill. He had "
            "no memory of acquiring it. <bookmark mark='d'/> So knowing how and remembering that come "
            "apart. That's one half of a double dissociation. The other half came later, from patients with "
            "damage elsewhere, who remember their practice sessions perfectly well and can't improve. Part "
            "20 is built on this."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag))
            self.play(Create(star), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(star_l))
            vo.wait_until("b")
            self.play(FadeIn(A), Create(days))
            self.play(Create(c_in), Create(c_hm), FadeIn(lg), FadeIn(side[0]), run_time=5.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2], shift=UP * 0.1))
        self.clear_scene()

    def caution(self):
        head = heading(r"What one patient can and cannot carry")
        rows = VGroup(
            VGroup(label(r"what the case shows", font_size=36, color=SPARED),
                   wrapped_label(r"laying down new memories of events needs tissue that holding digits, "
                                 r"remembering childhood and learning a skill do not", 12.4, 31, WHITE)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"what it does not show", font_size=36, color=LESION),
                   wrapped_label(r"that memories are kept in the hippocampus: \ his old ones survived its "
                                 r"removal", 12.4, 31, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"and the lesion was larger than its name", font_size=36, color=DATA),
                   wrapped_label(r"the surgeon took the amygdala and the cortex around the hippocampus too. \ "
                                 r"Which piece mattered was settled later, in animals and other patients.", 12.4,
                                 31, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, -0.3, 0])
        with self.voiceover(
            "Apply the rules from chapter four. <bookmark mark='a'/> What the case shows: laying down new "
            "memories of events needs tissue that the other three kinds of remembering don't. That's a "
            "statement about necessity, from a lesion and a loss. <bookmark mark='b'/> What it doesn't "
            "show: that memories are kept in the hippocampus. His old memories survived its removal. "
            "Whatever the hippocampus does, it isn't the warehouse. <bookmark mark='c'/> And, as with Broca, "
            "the lesion was larger than its name. The surgeon took the amygdala, and the cortex around the "
            "hippocampus, as well. Which of those pieces mattered for memory had to be worked out later, "
            "with careful lesions in animals and with other patients. One patient opens a question. It takes "
            "many to close it."
        ) as vo:
            self.play(FadeIn(head))
            for k, mark_ in enumerate("abc"):
                vo.wait_until(mark_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
        self.clear_scene()
