from __future__ import annotations

from videos.psychology.psych20.common import *  # noqa: F403


class Index(VoiceoverScene):
    def construct(self):
        self.card()
        self.index()
        self.separation()
        self.context_in_brain()

    def card(self):
        card = chapter_card(12, r"The hippocampus as an index", r"What does the hippocampus store, \ and how does it "
                            r"keep memories apart?", lit={1971: r"Marr", 1986: r"Teyler \& DiScenna",
                                                         2007: r"Leutgeb et al.", 2011: r"time cells",
                                                         2012: r"Liu et al."},
                            part=PART, scale=("cell", "brain"), marr=("how", "where"))
        with self.voiceover("Chapter twelve. The hippocampus as an index."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def index(self):
        head = heading(r"An index to the cortex")
        cortex = VGroup(*[Circle(radius=0.42, color=c, stroke_width=3) for c in (CUE, WORD, CTX, LOST, MODEL)])
        cortex.arrange(RIGHT, buff=0.55).move_to([0, 1.9, 0])
        cl = VGroup(*[label(t, font_size=17, color=GREY_A).next_to(c_, UP, buff=0.12) for t, c_ in zip(
            (r"sight", r"sound", r"place", r"smell", r"meaning"), cortex)])
        hip = Dot([0, -0.2, 0], radius=0.22, color=WORD)
        hl = label(r"an index in the hippocampus", font_size=20, color=WORD).next_to(hip, DOWN, buff=0.15)
        links = VGroup(*[Line(hip.get_center(), c_.get_bottom(), color=WORD, stroke_width=2.5) for c_ in cortex])
        rows = rows_of([
            (r"Teyler and DiScenna, \ 1986: \ the episode lives in the cortex, \ spread over many areas", WHITE),
            (r"the hippocampus stores a small, \ sparse pointer that binds the pieces together", WORD),
            (r"a cue reactivates part of the pattern; \ the index completes it, \ and replays the whole", MODEL),
            (r"recurrent connections in CA3, \ like a Hopfield network: \ completion from a fragment", CTX),
        ], 12.4, 25, 0.3).to_edge(DOWN, buff=0.85)
        tag = historical_tag(r"Marr (1971); \ Teyler \& DiScenna (1986)")
        with self.voiceover(
            "How does the hippocampus fit in? An influential answer is that it doesn't store the memory at all, "
            "only an index to it. <bookmark mark='a'/> An episode, the butcher's face, his voice, the shop, the "
            "smell of the place, is represented across many areas of the cortex. <bookmark mark='b'/> On Timothy "
            "Teyler and Pascal DiScenna's indexing theory, the hippocampus stores a small, sparse pattern that "
            "points to all of those pieces at once, binding them into one event. <bookmark mark='c'/> Later, a cue "
            "reactivates a part of the pattern. The index lights up, and drives the rest of the cortex back into "
            "the state it was in. <bookmark mark='d'/> The completion step looks like chapter nine. A region of the "
            "hippocampus called CA3 is full of connections from its own cells back onto each other, the anatomy of "
            "an attractor network, as David Marr proposed in 1971."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cortex), FadeIn(cl), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(hip), FadeIn(hl), *[Create(l_) for l_ in links], FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Indicate(cortex[1], color=WORD), run_time=0.8)
            self.play(LaggedStart(*[c_.animate.set_fill(c_.get_color(), 0.5) for c_ in cortex], lag_ratio=0.15),
                      FadeIn(rows[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def separation(self):
        s = load("separation")
        head = heading(r"Pattern separation: \ keeping similar days apart")
        A = axes([0, 1], [0, 1], x_length=5.0, y_length=4.0, xticks=[0, 0.25, 0.5, 0.75, 1],
                 yticks=[0, 0.25, 0.5, 0.75, 1], xlabel=r"overlap of two inputs", ylabel=r"overlap of their codes",
                 center=[-3.3, -0.2, 0], font_size=17, xfmt=lambda v: f"{v:.2f}".rstrip("0").rstrip("."),
                 yfmt=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
        ax = A.ax
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=GREY_C, stroke_width=2)
        c = curve_in(ax, s["input"], s["output"], MODEL, 4)
        pts = scatter(ax, s["input"], s["output"], MODEL, radius=0.06, opacity=1.0)
        i8 = int(np.argmin(np.abs(s["input"] - 0.8)))
        rows = rows_of([
            (r"today's parking space and yesterday's: \ nearly the same input, \ and they must not merge", WHITE),
            (r"the dentate gyrus: \ several times more cells than its input, \ and very few active at once", WORD),
            (r"expand, \ then keep only the most strongly driven cells: \ similar inputs get much less similar codes",
             MODEL),
            (rf"inputs that share 80\% of their active units: \ codes that share {pct(s['output'][i8])}", MODEL),
            (r"rats: \ small changes to a room change dentate gyrus firing a lot \ (Leutgeb et al., \ 2007)", CTX),
            (r"separation to store, \ completion to recall: \ a trade-off the hippocampus has to strike", CUE),
        ], 6.4, 21, 0.28).move_to([3.4, -0.1, 0])
        ptag = psyche_tag(r"\texttt{memory.pattern\_separation}: \ 200 inputs to 2,000 cells, \ 2\% active")
        with self.voiceover(
            "An index has a problem. <bookmark mark='a'/> Where you parked this morning and where you parked "
            "yesterday are almost the same memory: same car park, same car, same time of day. If their indexes "
            "overlap too much, one will overwrite the other, and you'll walk to yesterday's space. "
            "<bookmark mark='b'/> The dentate gyrus, the entrance to the hippocampus, seems built to prevent this. "
            "It has many more cells than the region that feeds it, and only a few percent are active at a time. "
            "<bookmark mark='c'/> Here's what that architecture does in a small simulation: two hundred input "
            "units projecting to two thousand cells, of which only the most strongly driven two percent fire. Pairs "
            "of inputs that overlap a little get codes that barely overlap at all, and even very similar inputs get "
            f"codes that are much less alike. <bookmark mark='d'/> Inputs sharing eighty percent of their active "
            f"units get codes sharing {spct(s['output'][i8])}. <bookmark mark='e'/> In rats, small changes to a "
            "familiar room change the firing of dentate gyrus cells much more than they change the room. "
            "<bookmark mark='f'/> So the hippocampus needs both: separation, to store similar events apart, and "
            "completion, to recall a whole event from a part. The two pull against each other, and how the circuit "
            "balances them is an active question."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(diag), FadeIn(ptag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(c), FadeIn(pts), FadeIn(rows[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(Indicate(pts[i8], color=WORD, scale_factor=2.0), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
            vo.wait_until("f")
            self.play(FadeIn(rows[5]))
        self.clear_scene()

    def context_in_brain(self):
        e = archive.LIU_2012.data
        head = heading(r"Looking for the context, \ and the trace, \ in the brain")
        rows = rows_of([
            (r"time cells, \ 2011: \ in rats waiting through an empty delay, \ hippocampal cells fire in sequence, \ "
             r"each at its own moment", CTX),
            (r"a slowly changing population code for when: \ the kind of signal a drifting context needs", CTX),
            (r"Manning and colleagues, \ 2011: \ in patients' implanted electrodes, \ the brain state at recall "
             r"resembles the state when the word was studied, \ \emph{and its neighbours}", MODEL),
            (r"context reinstatement, \ seen in the brain: \ the model's central claim", MODEL),
            (rf"engrams, \ 2012: \ in {e['animal']}, \ reactivating the cells active during learning brings back "
             r"the fear memory", WORD),
            (r"what such a cell stores, \ an item or its context, \ is not yet known", GREY_A),
        ], 12.6, 25, 0.33).move_to([0, -0.25, 0])
        tag = historical_tag(r"MacDonald et al.\ (2011); \ Manning et al.\ (2011); \ " + archive.LIU_2012.cite)
        with self.voiceover(
            "If memory search runs on a drifting context, the brain should contain one. "
            "<bookmark mark='a'/> In 2011 Christopher MacDonald, Howard Eichenbaum and their colleagues recorded "
            "from the hippocampus of rats waiting through an empty delay. Cells fired one after another, each at its "
            "own moment, like place cells for time. <bookmark mark='b'/> A population that changes slowly and "
            "steadily is exactly the kind of signal a drifting context needs. <bookmark mark='c'/> The same year, "
            "Jeremy Manning, Kahana and their colleagues recorded from electrodes implanted in patients being "
            "treated for epilepsy, while they did free recall. Just before a word was recalled, the pattern of brain "
            "activity resembled the pattern from when that word was studied, and also the patterns of its "
            "neighbours in the list. <bookmark mark='d'/> That is context reinstatement, the model's central claim, "
            "seen in the brain. <bookmark mark='e'/> And Part 5's engram experiment showed that reactivating the "
            "cells active during learning, by light, brings back a memory in mice. <bookmark mark='f'/> What those "
            "cells hold, the thing remembered or its context, nobody yet knows."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcdef", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
