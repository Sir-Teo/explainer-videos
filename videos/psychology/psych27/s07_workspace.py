from __future__ import annotations

from videos.psychology.psych27.common import *  # noqa: F403


class Workspace(VoiceoverScene):
    def construct(self):
        self.card()
        self.theatre()
        self.ignition_curve()
        self.bimodal()
        self.signatures()

    def card(self):
        card = chapter_card(6, r"The global workspace", r"Is consciousness a broadcast?",
                            lit={1988: r"Baars", 1998: r"Dehaene, \ Kerszberg \& Changeux", 2005: r"Sergent et al.",
                                 2011: r"Dehaene \& Changeux"},
                            part=PART, scale=("mind", "brain"), marr=("how",))
        with self.voiceover("Chapter six. The global workspace."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def theatre(self):
        head = heading(r"A broadcast to the whole brain")
        hub = Circle(radius=1.0, color=GNW, fill_opacity=0.15).move_to([-3.2, 0.4, 0])
        hub_l = label(r"workspace", font_size=22, color=GNW).move_to(hub)
        mods = VGroup()
        names = [r"vision", r"memory", r"language", r"action", r"evaluation", r"attention"]
        for k, n in enumerate(names):
            a = 2 * PI * k / len(names) + PI / 2
            pos = hub.get_center() + 2.4 * np.array([np.cos(a), np.sin(a), 0])
            c = Circle(radius=0.5, color=UNSEEN, fill_opacity=0.1).move_to(pos)
            mods.add(VGroup(c, label(n, font_size=16, color=UNSEEN).move_to(c)))
        links = VGroup(*[Line(hub.get_center(), m_.get_center(), color=GNW, stroke_width=2,
                              stroke_opacity=0.6).set_length(1.4).move_to((hub.get_center() + m_.get_center()) / 2)
                         for m_ in mods])
        rows = rows_of([
            (r"Baars, \ 1988: \ many specialist processors work unconsciously; \ what is conscious is what wins "
             r"a limited stage and is broadcast to all of them", WHITE),
            (r"Dehaene, \ Changeux and colleagues: \ the stage is a network of long-range neurons, \ dense in "
             r"prefrontal and parietal cortex", GNW),
            (r"the prediction: \ access is all or none; \ a stimulus either ignites the network, \ or fades", MODEL),
        ], 5.6, 22, 0.32).move_to([3.4, 0.2, 0])
        tag = historical_tag(r"Baars (1988); \ Dehaene, \ Kerszberg \& Changeux (1998)")
        with self.voiceover(
            "The first of the leading theories is the global workspace. <bookmark mark='a'/> Bernard Baars proposed "
            "it in 1988: the brain has many specialist processors working in parallel and unconsciously, and a "
            "limited stage. Whatever wins the stage is broadcast to all the specialists at once, and that broadcast "
            "is what it is to be conscious of something. <bookmark mark='b'/> Stanislas Dehaene and Jean-Pierre "
            "Changeux made it neural: the stage is a network of neurons with long-range connections, dense in "
            "prefrontal and parietal cortex, that can lock into a self-sustaining state. <bookmark mark='c'/> Its "
            "central prediction is that access is all or none. A stimulus either ignites the network, or fades away."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(hub), FadeIn(hub_l))
            vo.wait_until("a")
            self.play(FadeIn(mods), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(links), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(hub.animate.set_fill(GNW, opacity=0.5), FadeIn(rows[2]))
        self.clear_scene()

    def ignition_curve(self):
        d = load("ignition")
        head = heading(r"Ignition, \ computed")
        A = axes([0, 1.5], [0, 1.05], x_length=6.0, y_length=4.0, xticks=[0, 0.5, 1.0, 1.5], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:g}", xlabel=r"stimulus strength",
                 ylabel=r"activity", center=[-3.2, -0.3, 0], font_size=16)
        s = d["strength"]
        early = d["early_mean"] / max(d["early_mean"].max(), 1e-9)
        ce = curve(A.ax, s, early, SEEN, 4)
        cl = curve(A.ax, s, d["late_mean"], GNW, 4)
        cp = scatter(A.ax, s, d["p_ignite"], GNW, 0.05, 1)
        key = legend([(SEEN, r"sensory stage, \ 60 ms \ (scaled)"), (GNW, r"workspace, \ 600 ms")],
                     font_size=17).move_to(A.ax.c2p(0.42, 0.85))
        rows = rows_of([
            (r"Psyche: \ a sensory stage follows the input linearly; \ a recurrent workspace with strong "
             r"self-excitation receives it", MODEL),
            (r"early, \ sensory activity grows smoothly with strength", SEEN),
            (rf"late, \ the workspace is either off or fully on: \ ignition near strength {d['threshold']:.2f}", GNW),
            (r"a bifurcation: \ below it every input fades, \ above it the network sustains itself after the "
             r"stimulus is gone", WHITE),
        ], 5.6, 22, 0.3).move_to([3.5, -0.1, 0])
        tag = psyche_tag(r"\texttt{workspace.ignition}: \ 400 trials per strength")
        with self.voiceover(
            "Psyche can show what all or none means. <bookmark mark='a'/> A sensory population follows its input "
            "linearly, and feeds a workspace population with strong self-excitation. A brief stimulus, fifty "
            "milliseconds long, arrives at many strengths, four hundred trials each. <bookmark mark='b'/> Sixty "
            "milliseconds in, the sensory activity grows smoothly with the strength of the stimulus. "
            "<bookmark mark='c'/> Six hundred milliseconds in, long after the stimulus is gone, the workspace is "
            f"either silent or fully active, and the switch happens near strength {d['threshold']:.2f}. "
            "<bookmark mark='d'/> That's a bifurcation. Below the threshold every input fades; above it, the network "
            "sustains itself. Graded early, all or none late: the workspace's signature."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ce), FadeIn(key[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(cl), FadeIn(cp), FadeIn(key[1]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def bimodal(self):
        d = load("ignition")
        head = heading(r"At the threshold, \ two kinds of trial")
        A = axes([0, 1.1], [0, max(d["late_hist"]) * 1.15], x_length=5.6, y_length=2.8, xticks=[0, 0.5, 1.0],
                 yticks=None, xfmt=lambda v: f"{v:g}", xlabel=r"workspace activity at 600 ms",
                 ylabel=r"trials", center=[-3.4, 1.0, 0], font_size=16)
        e = d["edges"]
        hb = bars(A.ax, (e[:-1] + e[1:]) / 2, d["late_hist"], GNW, width=float(e[1] - e[0]) * 0.9)
        B = axes([0, 0.8], [0, 1.05], x_length=5.6, y_length=1.3, xticks=[0, 0.2, 0.4, 0.6, 0.8], yticks=[0, 1],
                 xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:g}", xlabel=r"time, \ s",
                 ylabel=r"mean workspace activity", center=[-3.4, -2.55, 0], font_size=15)
        tr = VGroup(*[curve(B.ax, d["t"], d["traces_r"][k], c, 3)
                      for k, c in enumerate((UNSEEN, GNW, SEEN))])
        tags = VGroup(*[label(t, font_size=14, color=c).next_to(B.ax.c2p(float(d["t"][-1]), float(d["traces_r"][k][-1])),
                                                                  RIGHT, buff=0.1)
                        for k, (t, c) in enumerate(((r"weak", UNSEEN), (r"threshold", GNW), (r"strong", SEEN)))])
        tr.add(tags)
        rows = rows_of([
            (rf"at strength {d['threshold']:.2f}, \ {100 * d['p_at_threshold']:.0f}\% of trials ignite", WHITE),
            (r"the same stimulus, \ two outcomes: \ the late activity is bimodal, \ never halfway", GNW),
            (r"averaged over trials, \ the mean looks graded; \ trial by trial, \ it is all or none", MODEL),
            (r"Sergent, \ Baillet and Dehaene, \ 2005: \ in the attentional blink, \ the same word, \ seen or "
             r"missed, \ gives a late brain response that is present or absent", SEEN),
        ], 5.6, 22, 0.3).move_to([3.5, -0.1, 0])
        tag = psyche_tag(r"\texttt{workspace.ignition}; \ Sergent, \ Baillet \& Dehaene (2005)")
        with self.voiceover(
            "Look closely at the threshold. <bookmark mark='a'/> At strength "
            f"{d['threshold']:.2f}, {100 * d['p_at_threshold']:.0f} percent of trials ignite. <bookmark mark='b'/> "
            "The same stimulus produces two outcomes, and the late activity is bimodal: off or on, almost never in "
            "between. <bookmark mark='c'/> Averaged over trials, the mean activity looks graded, rising smoothly "
            "with strength. Only trial by trial is it all or none, which is why averaging can hide the very thing "
            "a theory predicts. <bookmark mark='d'/> In people, Claire Sergent, Sylvain Baillet and Dehaene showed "
            "in 2005 that during the attentional blink, the same word, seen on some trials and missed on others, "
            "produced a late brain response that was either there or not."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(hb))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(B), Create(tr), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def signatures(self):
        head = heading(r"Four signatures of conscious access")
        items = [
            (r"a late, \ large wave over the scalp, \ the P3b, \ from about 300 ms", GNW),
            (r"a sudden rise in prefrontal and parietal activity: \ ignition", GNW),
            (r"long-distance synchrony between distant areas", SEEN),
            (r"information about the stimulus decodable across the whole cortex", SEEN),
        ]
        rows = rows_of(items, 11.6, 26, 0.4).move_to([0, 0.6, 0])
        foot = wrapped_label(r"Dehaene and Changeux, \ 2011; \ each signature has been challenged: \ the P3b tracks "
                             r"the report and the task as well as the experience, \ and disappears in some no-report "
                             r"designs", 12.0, 23, LOST).to_edge(DOWN, buff=0.8)
        tag = published_tag(r"Dehaene \& Changeux (2011)")
        with self.voiceover(
            "From such experiments, Dehaene and Changeux listed four signatures of conscious access in 2011. "
            "<bookmark mark='a'/> A late, large wave over the scalp, called the P3b, from about three hundred "
            "milliseconds. <bookmark mark='b'/> A sudden rise in prefrontal and parietal activity: ignition. "
            "<bookmark mark='c'/> Synchrony between distant areas. <bookmark mark='d'/> And information about the "
            "stimulus that can be decoded across much of the cortex. <bookmark mark='e'/> Each has been challenged. "
            "The P3b in particular tracks the task and the report as much as the experience, and shrinks or vanishes "
            "in some no-report designs, which is exactly where the rival theory pushes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
