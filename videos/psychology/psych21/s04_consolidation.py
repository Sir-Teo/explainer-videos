from __future__ import annotations

from videos.psychology.psych21.common import *  # noqa: F403

HIPPO = "#FFB86B"


class Consolidation(VoiceoverScene):
    def construct(self):
        self.card()
        self.ribot()
        self.model()
        self.sleep()
        self.reconsolidation()

    def card(self):
        card = chapter_card(3, r"Consolidation", r"How does a new memory become a lasting one?",
                            lit={1882: r"Ribot", 1900: r"M\"uller \& Pilzecker", 1994: r"Alvarez \& Squire",
                                 2000: r"Nader et al."},
                            part=PART, scale=("circuit", "brain"), marr=("how",))
        with self.voiceover("Chapter three. Consolidation."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def ribot(self):
        head = heading(r"A memory is fragile at first")
        rows = rows_of([
            (r"M\"uller and Pilzecker, \ 1900: \ a second list learnt soon after the first harms it more than one "
             r"learnt later; \ the trace needs time to \emph{consolidate}", WHITE),
            (r"Ribot, \ 1882: \ after a brain injury, \ the newest memories are lost first and the oldest last", LOST),
            (r"H.M. \ (Part 20): \ besides losing new learning, \ he lost some years before his operation, \ and "
             r"kept his childhood", TRACE),
            (r"electroconvulsive therapy, \ head injuries, \ the early stages of Alzheimer's disease: \ the same "
             r"slope, \ recent lost, \ remote kept", CUE),
            (r"so a memory changes where it lives: \ it starts out needing the hippocampus and comes to need it less",
             CTX),
        ], 12.4, 26, 0.36).move_to([0, -0.3, 0])
        tag = historical_tag(r"M\"uller \& Pilzecker (1900); \ Ribot (1882)")
        with self.voiceover(
            "Jenkins and Dallenbach's sleepers point to an older idea. <bookmark mark='a'/> In 1900, in "
            "Göttingen, Georg Müller and Alfons Pilzecker found that a second list learnt soon after the first "
            "harmed it more than one learnt later. They concluded that a trace is fragile at first and takes time "
            "to set, and gave the process its name: consolidation. <bookmark mark='b'/> Twenty years earlier, "
            "Théodule Ribot had described what happens to memory after injury to the brain: the newest memories "
            "go first, and the oldest last. <bookmark mark='c'/> Henry Molaison, H.M., showed it too. Besides "
            "losing the ability to learn, he lost memories of some years before his operation, and kept his "
            "childhood. <bookmark mark='d'/> The same gradient appears after electroconvulsive therapy, head "
            "injury, and in early Alzheimer's disease. <bookmark mark='e'/> The natural reading is that a memory "
            "changes where it lives: at first it needs the hippocampus, and with time it comes to depend on the "
            "cortex instead. Let's build that as a model."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def model(self):
        d = load("consolidate")
        head = heading(r"Derivation: \ two stores and Ribot's gradient")
        eqs = VGroup(
            MathTex(r"\frac{dh}{dt} = -a\,h", font_size=34, color=HIPPO),
            MathTex(r"\frac{dc}{dt} = k\,h - b\,c", font_size=34, color=CTX),
            MathTex(r"c(t) = \frac{k}{a - b}\big(e^{-bt} - e^{-at}\big)", font_size=32, color=CTX),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-4.3, 1.0, 0])
        notes = rows_of([
            (r"$h$: \ the hippocampal trace, \ fast to form, \ fast to fade", HIPPO),
            (r"$c$: \ the cortical trace, \ taught by $h$ while it lasts, \ slow to fade", CTX),
            (r"retrieval strength $h + c$; \ after a hippocampal lesion, \ only $c$", LOST),
        ], 5.2, 21, 0.2).move_to([-4.2, -1.55, 0])
        A = axes([0, 120], [0, 1], x_length=6.2, y_length=3.6, xticks=[0, 30, 60, 90, 120], yticks=[0, 0.5, 1],
                 xlabel=r"age of the memory when the lesion happens \ (days, \ schematic)", ylabel=r"retrieval strength",
                 center=[3.0, 0.3, 0], font_size=18)
        age = d["age"]
        cs = VGroup(curve_in(A.ax, age, d["intact"], TRACE, 4), curve_in(A.ax, age, d["hippo"], HIPPO, 2),
                    curve_in(A.ax, age, d["lesion"], LOST, 4))
        key = legend([(TRACE, r"intact: \ $h + c$"), (HIPPO, r"the hippocampal part, \ $h$"),
                      (LOST, r"after the lesion: \ $c$ alone")], font_size=20).move_to([4.5, 1.3, 0])
        rows = rows_of([
            (rf"after the lesion the best-kept memories are about {d['peak_age']:.0f} days old: \ newer ones had "
             r"not yet reached the cortex, \ older ones had faded anyway", WHITE),
        ], 6.4, 21, 0.2).next_to(A, DOWN, buff=0.3)
        ptag = psyche_tag(r"\texttt{memory.two\_store}: \ after Alvarez and Squire \ (1994)")
        with self.voiceover(
            "Two stores, three lines. <bookmark mark='a'/> A memory is laid down in the hippocampus with "
            "strength h, which fades fast, at rate a. While it lasts, it teaches the cortex: the cortical trace c "
            "grows in proportion to h, and fades slowly, at rate b. <bookmark mark='b'/> The equations solve in "
            "closed form. c rises, peaks, and then declines slowly, long after h has gone. "
            "<bookmark mark='c'/> Retrieval strength is the sum, h plus c, and it falls the way a forgetting "
            "curve does: fast, then slow. <bookmark mark='d'/> Now remove the hippocampus. Only c is left. The "
            "newest memories, which had not yet taught the cortex, are lost entirely. Old memories, which by now "
            "live almost wholly in the cortex, are barely touched. That's Ribot's gradient, from a model of the "
            "same shape as Pablo Alvarez and Larry Squire's network of 1994. <bookmark mark='e'/> The numbers here "
            "are schematic. The real gradient in people can stretch over years, and one rival, multiple trace "
            "theory, holds that vivid episodic detail never stops needing the hippocampus at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ptag))
            vo.wait_until("a")
            self.play(Write(eqs[0]), Write(eqs[1]), FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(Write(eqs[2]))
            vo.wait_until("c")
            self.play(FadeIn(A), Create(cs[0]), Create(cs[1]), FadeIn(key[0]), FadeIn(key[1]), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(Create(cs[2]), FadeIn(key[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows))
        self.clear_scene()

    def sleep(self):
        head = heading(r"What sleep does")
        rows = rows_of([
            (r"Wilson and McNaughton, \ 1994: \ place cells that fired together as a rat ran a track fire together "
             r"again in its sleep afterwards: \ \emph{replay}", HIPPO),
            (r"replay in sleep is fast, \ many times the speed of the run, \ and coordinated with the cortex", CTX),
            (r"Rasch and colleagues, \ 2007: \ an odour present while people learnt, \ presented again in deep "
             r"sleep, \ improved their memory of the locations next day", TRACE),
            (r"the same odour while awake, \ or during dreaming sleep, \ did not: \ \emph{targeted memory "
             r"reactivation}", CUE),
            (r"so sleep is not only time without interference: \ it is when the hippocampus rehearses the day to "
             r"the cortex", MODEL),
        ], 12.4, 25, 0.34).move_to([0, -0.3, 0])
        tag = historical_tag(r"Wilson \& McNaughton (1994); \ Rasch et al.\ (2007)")
        with self.voiceover(
            "How does the hippocampus teach the cortex? One answer came from recording rats. "
            "<bookmark mark='a'/> In 1994 Matthew Wilson and Bruce McNaughton recorded place cells, the "
            "hippocampal cells that fire at particular spots, as a rat ran a track. In its sleep afterwards, the "
            "cells that had fired together on the track fired together again. The day was being replayed. "
            "<bookmark mark='b'/> Replay in sleep runs many times faster than the original run, and is coordinated "
            "with activity in the cortex. <bookmark mark='c'/> In people it can be steered. In 2007 Björn Rasch and "
            "colleagues had people learn the locations of card pairs while a smell of roses was in the air. When the "
            "same smell was given again during deep, slow-wave sleep, memory for the locations was better the next "
            "day. <bookmark mark='d'/> The smell while awake, or in dreaming sleep, did nothing. "
            "<bookmark mark='e'/> So Jenkins and Dallenbach were half right. Sleep is time without interference, and "
            "it's also when the hippocampus rehearses the day to the rest of the brain."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def reconsolidation(self):
        r = archive.HARDWICKE_2016.data
        head = heading(r"Reconsolidation: \ a memory recalled is fragile again")
        strip = trial_strip([
            (r"day 1: \ tone, \ then shock", label(r"learn", font_size=28, color=TRACE), r"rat learns fear"),
            (r"day 2: \ tone alone", label(r"recall", font_size=28, color=CUE), r"the memory is reactivated"),
            (r"then: \ block protein synthesis", label(r"anisomycin", font_size=26, color=LOST), r"in the amygdala"),
            (r"day 3: \ tone", label(r"no fear", font_size=28, color=LOST), r"the memory is gone"),
        ], frame_w=2.8, frame_h=1.1, font_size=18).move_to([0, 1.5, 0])
        rows = rows_of([
            (r"Nader, \ Schafe and LeDoux, \ 2000: \ without the reminder on day 2, \ the same drug did nothing; \ "
             r"given six hours later, \ nothing", WHITE),
            (r"retrieval makes a consolidated memory labile again, \ and it must be stored anew", CUE),
            (r"in rats this is robust; \ in people, \ updating a memory by new learning after a reminder has been "
             rf"harder: \ Hardwicke, \ Taqi and Shanks, \ 2016, \ {r['experiments']} experiments, \ no effect", LOST),
            (r"and it raises a hope: \ could a bad memory be weakened by reactivating it? \ (chapter 14)", FALSE),
        ], 12.4, 24, 0.3).to_edge(DOWN, buff=0.65)
        tag = historical_tag(r"Nader, \ Schafe \& LeDoux (2000); \ " + archive.HARDWICKE_2016.cite)
        with self.voiceover(
            "If consolidation is a process that ends, then an old memory should be safe. In 2000, Karim Nader, Glenn "
            "Schafe and Joseph LeDoux showed it isn't. <bookmark mark='a'/> Rats learnt that a tone meant a shock. "
            "A day later the tone was played once, alone, to reactivate the memory, and straight afterwards a drug "
            "that blocks protein synthesis was injected into the amygdala. The next day, the rats no longer feared "
            "the tone. <bookmark mark='b'/> Without the reminder, the same drug did nothing, and given six hours "
            "after the reminder, nothing either. Recalling the memory had made it fragile again, and it had to be "
            "stored anew: reconsolidation. <bookmark mark='c'/> In animals the finding is robust. In people, the "
            "behavioural version, changing a memory by new learning soon after a reminder, has been harder to pin "
            f"down: Tom Hardwicke, Mona Taqi and David Shanks ran {r['experiments']} experiments in 2016 modelled on an "
            "influential study of motor skills, and found no reconsolidation effect. <bookmark mark='d'/> Still, the "
            "idea that a memory is rewritten every time it's used is the bridge to the second half of this part."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(strip))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
