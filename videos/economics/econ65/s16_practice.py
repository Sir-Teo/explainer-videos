from __future__ import annotations

from videos.economics.econ65.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ workforce, \ policy, \ measurement", r"Where is this economics used, \ and "
             r"what goes wrong?", "Chapter fourteen. In practice: workforce, policy, measurement.",
             scale=("firm", "nation"), horizon=("a year",))
        self.jobs()
        self.cautions()

    def jobs(self):
        cards = point_cards([
            (r"workforce strategy", r"break each job into tasks, \ ask which an assistant speeds up and which it "
             r"cannot do, \ and redesign the job around the second kind", WORK),
            (r"test before rolling out", r"give the tool to a random half, \ measure output, \ quality and "
             r"learning: \ Part 61's experiments, \ on a firm's own staff", TEXT),
            (r"AI policy", r"rules for risky uses, \ competition in the chain of chapter ten, \ insurance for "
             r"displaced workers", MACH),
            (r"productivity measurement", r"free and cheap services GDP undercounts \ (Part 3), \ intangible "
             r"investment it misses \ (the J-curve), \ adoption surveys that lag", GDP),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"where the economics of AI is used", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Where is this used? <bookmark mark='a'/> In workforce strategy: break each job into its tasks, ask "
            "which an assistant speeds up and which it cannot do, and redesign the job around the second kind. "
            "That is the task model, applied inside one firm. <bookmark mark='b'/> Before rolling a tool out to "
            "everyone, give it to a random half and measure output, quality and what people learn, with the "
            "experiments of Part sixty-one. <bookmark mark='c'/> In policy: rules for risky uses, competition along "
            "the chain of chapter ten, and insurance for the workers who are displaced. <bookmark mark='d'/> And "
            "in measurement: GDP undercounts free and cheap services, misses intangible investment, and the "
            "surveys of adoption lag, so statistical agencies are rebuilding how they count."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def cautions(self):
        head = label(r"three cautions from this part", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        rows = VGroup(
            VGroup(label(r"1. \ Exposed is not automated", font_size=26, color=MACH),
                   label(r"a task a model could speed up is a possibility: \ adoption, \ cost and new tasks decide",
                         font_size=19, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"2. \ A task is not a job, \ and a job is not the economy", font_size=26, color=GDP),
                   label(r"time saved on a set task must pass through adoption, \ prices and Hulten's weights "
                         r"before it is growth", font_size=19, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.1),
            VGroup(label(r"3. \ Watch the tasks left to people", font_size=26, color=WORK),
                   label(r"with complements, \ the work machines cannot do sets the pace, \ and its pay",
                         font_size=19, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(head, DOWN, buff=0.7)
        with self.voiceover(
            "Three cautions from this part. <bookmark mark='a'/> Exposed is not automated. A task a model could "
            "speed up is a possibility; adoption, cost and new tasks decide what happens. <bookmark mark='b'/> A "
            "task is not a job, and a job is not the economy. Time saved on a set task has to pass through "
            "adoption, prices and Hulten's weights before it becomes growth. <bookmark mark='c'/> And watch the "
            "tasks left to people. When tasks are complements, the work machines cannot do sets the pace of "
            "growth, and what it pays."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.15))
        self.clear_scene()
