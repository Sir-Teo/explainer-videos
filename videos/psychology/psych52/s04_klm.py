from __future__ import annotations

from videos.psychology.psych52.common import *  # noqa: F403


class Klm(VoiceoverScene):
    def construct(self):
        card_section(self, 3, r"GOMS and the keystroke-level model", r"How long will this task take?", marr=("how",))
        self.goms()
        self.operators()
        self.methods()
        self.cpm()

    def goms(self):
        chips_section(self, r"GOMS", [
            (r"goals", r"what the user wants: \ ``delete this word''", PERSON),
            (r"operators", r"the elementary acts: \ a keystroke, \ a point, \ a look, \ a moment of thought", MODEL),
            (r"methods", r"sequences of operators that achieve a goal: \ the shortcut, \ or the menu", SYMP),
            (r"selection rules", r"how a user picks a method: \ ``if my hands are on the keys, \ use the shortcut''",
             GOOD),
        ], "Card, Moran and Newell's next step was GOMS. <bookmark mark='a'/> Goals: what the user wants, like "
           "deleting a word. <bookmark mark='b'/> Operators: the elementary acts, a keystroke, a point, a look, a "
           "moment of thought. <bookmark mark='c'/> Methods: sequences of operators that achieve a goal, like the "
           "shortcut or the menu. <bookmark mark='d'/> And selection rules: how a user picks a method. If my hands "
           "are on the keys, use the shortcut.", tag=published_tag(r"Card, \ Moran \& Newell (1983)"))

    def operators(self):
        head = heading(r"The keystroke-level model")
        ops = [(r"K", r"a keystroke", r"0.28 s", r"0.12 s for a fast typist, \ 1.2 s for a novice", PERSON),
               (r"P", r"point with the mouse", r"1.1 s", r"Fitts's law, \ averaged", MODEL),
               (r"B", r"press or release a button", r"0.1 s", r"a click is BB", SYMP),
               (r"H", r"home the hand to keyboard or mouse", r"0.4 s", r"each move between the two", CROWD),
               (r"M", r"prepare mentally", r"1.35 s", r"placed by rules: \ before each new chunk of action", AUTH)]
        rows = VGroup()
        for o, what, t, note_, col in ops:
            rows.add(VGroup(label(o, font_size=34, color=col), wrapped_label(what, 4.2, 21, WHITE),
                            label(t, font_size=24, color=col), wrapped_label(note_, 4.6, 17, GREY_A))
                     .arrange(RIGHT, buff=0.45))
        rows.arrange(DOWN, buff=0.36).move_to([0, -0.2, 0])
        for r in rows:
            r[0].set_x(-5.8)
            r[1].set_x(-5.3 + r[1].width / 2)
            r[2].set_x(-0.4)
            r[3].set_x(0.7 + r[3].width / 2)
        foot = wrapped_label(r"a task's time is the sum of its operators, \ plus the system's response time R",
                             12.0, 21, YOU).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The keystroke-level model is GOMS at its simplest. <bookmark mark='a'/> K, a keystroke: about a quarter "
            "of a second for an average typist. <bookmark mark='b'/> P, pointing with the mouse: about a second, "
            "Fitts's law averaged. <bookmark mark='c'/> B, a button press or release; a click is two. "
            "<bookmark mark='d'/> H, homing the hand between keyboard and mouse: four tenths of a second. "
            "<bookmark mark='e'/> And M, mental preparation: one point three five seconds, placed by rules before each "
            "new chunk of action. <bookmark mark='f'/> A task's time is the sum of its operators, plus the system's "
            "response time."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()

    def methods(self):
        d = load("klm")
        head = heading(r"Three ways to delete a word")
        A = axes([0.3, 3.7], [0, 9], x_length=5.4, y_length=3.0, xticks=None, yticks=[0, 3, 6, 9],
                 yfmt=lambda v: f"{v:.0f} s", ylabel=r"predicted time", center=[-3.3, 0.3, 0], font_size=12)
        cols = [GOOD, MODEL, AUTH]
        b = bars(A.ax, [1, 2, 3], d["times"], cols, width=0.55)
        names = VGroup(*[VGroup(label(s, font_size=14, color=c), label(o, font_size=12, color=GREY_A))
                         .arrange(DOWN, buff=0.05).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.12)
                         for i, (s, o, c) in enumerate(zip([r"shortcut", r"double-click", r"menu"],
                                                           [r"\texttt{MKKKKK}", r"\texttt{HMPBBBBHMK}",
                                                            r"\texttt{HMPBB MPBB MPBB}"], cols))])
        vals = VGroup(*[label(rf"{t:.1f} s", font_size=14, color=c).next_to(A.ax.c2p(i + 1, t), UP, buff=0.08)
                        for i, (t, c) in enumerate(zip(d["times"], cols))])
        rows = rows_of([
            (r"write each method as operators, \ place the M's, \ and add", WHITE),
            (rf"the shortcut (ctrl, \ shift, \ arrow, \ arrow, \ delete): \ {d['times'][0]:.1f} s", GOOD),
            (rf"the menu route: \ {d['times'][2]:.1f} s, \ three times as long, \ mostly in pointing and thinking", AUTH),
            (r"validated against users within about 20\% (Card, \ Moran and Newell); \ it predicts skilled, \ "
             r"error-free work, \ and nothing about learning or errors", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.klm\_time}")
        with self.voiceover(
            "Here are three ways to delete a word. <bookmark mark='a'/> Write each method as operators, place the "
            "mental operators, and add. <bookmark mark='b'/> The keyboard shortcut takes under three seconds. "
            "<bookmark mark='c'/> The menu route takes more than eight, three times as long, mostly in pointing and "
            "thinking. <bookmark mark='d'/> In Card, Moran and Newell's tests, predictions like these came within "
            "about twenty percent of users' times. But the model predicts skilled, error-free work, and nothing about "
            "learning or errors."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[0]), FadeIn(vals[0]), FadeIn(b[1]), FadeIn(vals[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[2]), FadeIn(vals[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def cpm(self):
        rows_section(self, r"When operators overlap: \ CPM-GOMS", [
            (r"the keystroke-level model adds operators one after another; \ skilled people overlap them", WHITE),
            (r"Bonnie John's CPM-GOMS draws each operator on its resource (eyes, \ hands, \ cognition) and finds the "
             r"critical path", MODEL),
            (r"in Project Ernestine it predicted each call type's time, \ and the new workstation's loss, \ before a "
             r"single call was taken", PERSON),
            (r"the lesson for design: \ shortening a task means shortening its critical path, \ not counting "
             r"keystrokes", YOU),
        ], "Skilled people don't do one thing at a time. <bookmark mark='a'/> The keystroke-level model adds "
           "operators one after another, but skilled people overlap them. <bookmark mark='b'/> Bonnie John's "
           "CPM-GOMS draws each operator on its resource, eyes, hands or cognition, and finds the critical path, the "
           "chain that sets the time. <bookmark mark='c'/> In Project Ernestine it predicted each type of call's "
           "time, and the new workstation's loss, before a single call was taken on it. <bookmark mark='d'/> The "
           "lesson for design: shortening a task means shortening its critical path, not counting its keystrokes.")
