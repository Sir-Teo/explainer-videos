from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai29.common import AGENT, CLAIM, HIST, MODEL, OBS, PART, REWARD, TOOL, WORLD, node_box

MEM = C.MEMORY


class Memory(VoiceoverScene):
    def construct(self):
        self.card()
        self.context()
        self.stores()
        self.many()

    def card(self):
        card = chapter_card(4, r"Memory, and many agents", r"What does an agent remember?", part=PART)
        with self.voiceover("Chapter four. Memory, and many agents."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def context(self):
        W, H0 = 12.0, 1.1
        frame = Rectangle(width=W, height=H0, stroke_color=GREY_B, stroke_width=2).move_to([0, 1.2, 0])
        fl = label(r"the context window: \ a fixed number of tokens", font_size=30, color=GREY_A).next_to(frame, UP, buff=0.2)
        g = np.random.default_rng(3)
        kinds = [(WORLD, 0.5)] + [((GREY_A, AGENT, TOOL)[k % 3], w) for k, w in enumerate(g.uniform(0.25, 0.8, 30))]
        blocks, x = VGroup(), frame.get_left()[0]
        for col, w in kinds:
            if x + w > frame.get_right()[0]:
                break
            blocks.add(Rectangle(width=w - 0.03, height=H0 - 0.12, stroke_width=0, fill_color=col, fill_opacity=0.6)
                       .move_to([x + w / 2, frame.get_y(), 0]))
            x += w
        full = label(r"full: \ the oldest steps must go", font_size=28, color=C.PENALTY).next_to(frame, DOWN, buff=0.25)
        summ = Rectangle(width=1.6, height=H0 - 0.12, stroke_width=0, fill_color=MEM, fill_opacity=0.8)
        summ.move_to(frame.get_left() + RIGHT * 0.83)
        sl = label(r"a summary of everything so far: \ what was done, \ what matters next", font_size=26, color=MEM)
        sl.next_to(summ, DOWN, buff=0.25).align_to(summ, LEFT)
        cards = VGroup(
            history_card(r"Oct 2023", r"MemGPT \ (Packer et al.)", r"memory managed like an operating system's: \ the "
                         r"model pages facts in and out of its context", width=4.3, color=HIST, font_size=21),
            history_card(r"2025", r"compaction \ (coding agents)", r"when the window fills, \ the agent summarizes "
                         r"its own work and carries on from the summary", width=4.3, color=HIST, font_size=21),
            history_card(r"2023", r"lost in the middle \ (Liu et al.)", r"even in long windows \ (Part 15), \ models "
                         r"use the middle of a long context less well than its ends", width=4.3, color=HIST,
                         font_size=21),
        ).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "An agent's working memory is its context window, and it fills up. <bookmark mark='a'/> Every thought, "
            "action and observation of the loop adds tokens. A long task produces far more than any window holds. "
            "<bookmark mark='b'/> When it is full, something has to go. <bookmark mark='c'/> The simplest fix is to "
            "summarize: the agent writes down what it has done and what matters, empties the window, and starts "
            "again from the summary. Coding agents do this many times in a long session. <bookmark mark='d'/> "
            "Earlier, MemGPT treated memory like an operating system, paging facts in and out of the context; and "
            "even windows of a million tokens, from Part 15, have a weakness: models use what sits in the middle of "
            "a long context less well than what sits at its ends."
        ) as vo:
            self.play(Create(frame), FadeIn(fl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.1) for b_ in blocks], lag_ratio=0.15), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(full), frame.animate.set_stroke(C.PENALTY))
            vo.wait_until("c")
            self.play(FadeOut(blocks, shift=LEFT * 0.3), FadeIn(summ), FadeIn(sl), FadeOut(full),
                      frame.animate.set_stroke(GREY_B))
            self.play(FadeIn(cards[1], shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(cards[0], shift=UP * 0.15), FadeIn(cards[2], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stores(self):
        agent = node_box(r"agent", AGENT, 30, height=0.9).move_to([-5.3, 0.4, 0])
        store = VGroup(*[RoundedRectangle(width=3.6, height=0.5, corner_radius=0.06, stroke_color=MEM, stroke_width=1.5,
                                          fill_color=MEM, fill_opacity=0.12) for _ in range(6)]).arrange(DOWN, buff=0.1)
        store.move_to([-1.3, 0.2, 0])
        texts = [r"saw a locked door, room 3", r"the user prefers tabs", r"test suite takes 4 min",
                 r"skill: craft a pickaxe", r"lesson: check units first", r"the API key is in .env"]
        for b_, t_ in zip(store, texts):
            b_.add(label(t_, font_size=22, color=GREY_A).move_to(b_))
        sl = label(r"memories, \ stored as embeddings \\ (Part 24)", font_size=24, color=MEM).next_to(store, UP, buff=0.2)
        q = label(r"query: \\ ``how do I \\ run the tests?''", font_size=22, color=AGENT).next_to(agent, DOWN, buff=0.3)
        a1 = Arrow(agent.get_right(), store.get_left() + UP * 0.6, buff=0.1, color=AGENT, stroke_width=2.5)
        a2 = Arrow(store[2].get_left(), agent.get_right() + DOWN * 0.2, buff=0.1, color=MEM, stroke_width=2.5)
        cards = VGroup(
            history_card(r"Apr 2023", r"Generative Agents \ (Park et al.)", r"$25$ characters in a simulated town: \ "
                         r"a stream of memories, \ retrieved by recency, \ importance and relevance; \ reflections "
                         r"written on top", width=4.6, color=HIST, font_size=19),
            history_card(r"Mar 2023", r"Reflexion \ (Shinn et al.)", r"after a failure, \ write a lesson in words \ "
                         r"and read it before the next try", width=4.6, color=HIST, font_size=19),
            history_card(r"May 2023", r"Voyager \ (Wang et al.)", r"in Minecraft, \ a growing library of skills as code: "
                         r"\ $3.3\times$ more unique items, \ tech-tree milestones up to $15.3\times$ faster", width=4.6,
                         color=HIST, font_size=19),
        ).arrange(DOWN, buff=0.2).to_edge(RIGHT, buff=0.25)
        if cards.height > 7.0:
            cards.height = 7.0
            cards.to_edge(RIGHT, buff=0.25)
        with self.voiceover(
            "For memory that outlives the window, agents keep notes outside it. <bookmark mark='a'/> A memory is a "
            "short text stored with its embedding, the vectors of Part 24. <bookmark mark='b'/> To recall, the agent "
            "embeds a question and fetches the nearest notes back into its context. <bookmark mark='c'/> In 2023 "
            "Joon Sung Park and colleagues filled a simulated town with twenty-five such characters, each retrieving "
            "memories by how recent, how important and how relevant they were. <bookmark mark='d'/> Reflexion "
            "stored lessons from failures in words, and read them before trying again. <bookmark mark='e'/> And "
            "Voyager, in Minecraft, saved every skill it mastered as a program to call later, and collected three "
            "point three times as many unique items as earlier agents. Notes, lessons and skills: three kinds of "
            "memory."
        ) as vo:
            self.play(FadeIn(agent))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in store], lag_ratio=0.15), FadeIn(sl))
            vo.wait_until("b")
            self.play(FadeIn(q), GrowArrow(a1))
            self.play(Indicate(store[2], color=MEM), GrowArrow(a2))
            for k, mk in enumerate("cde"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=LEFT * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def many(self):
        lead = node_box(r"lead agent: \ plans, \ splits the task", AGENT, 26, height=0.8).move_to([-3.4, 2.3, 0])
        subs = VGroup(*[node_box(rf"subagent {k}", MODEL, 24, height=0.7) for k in (1, 2, 3)])
        subs.arrange(RIGHT, buff=0.45).move_to([-3.4, 0.4, 0])
        down = VGroup(*[Arrow(lead.get_bottom(), s_.get_top(), buff=0.08, color=GREY_B, stroke_width=2) for s_ in subs])
        up = VGroup(*[Arrow(s_.get_top() + RIGHT * 0.25, lead.get_bottom() + RIGHT * 0.25, buff=0.08, color=MEM,
                            stroke_width=2) for s_ in subs])
        ul = label(r"each with a fresh context of its own; \\ each returns a short summary", font_size=24, color=MEM)
        ul.next_to(subs, DOWN, buff=0.25)
        claim = history_card(r"Jun 2025", r"Anthropic's research system \ (a company report)",
                             r"a lead model with subagents beat a single agent by $90.2\%$ on an internal research "
                             r"evaluation, \ using about $15\times$ the tokens of a chat; \ on BrowseComp, \ token "
                             r"usage alone explained $80\%$ of the variance in performance", width=5.4, color=CLAIM,
                             font_size=21).to_edge(RIGHT, buff=0.3).shift(UP * 1.0)
        good = VGroup(label(r"parallel, \ broad tasks: \ research, \ search", font_size=26, color=REWARD),
                      label(r"tightly coupled tasks: \ one codebase", font_size=26, color=C.PENALTY))
        good.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-2.6, -2.3, 0])
        gl = VGroup(label(r"helps:", font_size=26, color=GREY_A).next_to(good[0], LEFT, buff=0.2),
                    label(r"helps less:", font_size=26, color=GREY_A).next_to(good[1], LEFT, buff=0.2))
        tail = label(r"more agents, \ more tokens: \\ much of the gain is more thinking, \ spread out", font_size=24,
                     color=GREY_A).next_to(claim, DOWN, buff=0.4)
        if tail.width > 5.6:
            tail.width = 5.6
        with self.voiceover(
            "When one context is not enough, use several. <bookmark mark='a'/> A lead agent plans and hands pieces "
            "of the task to subagents, each with a fresh context of its own, <bookmark mark='b'/> and each returns "
            "only a short summary, so the lead's window stays clear. <bookmark mark='c'/> Anthropic reported in "
            "2025 that such a team beat a single agent by ninety percent on its own research evaluation. That is "
            "the company's measurement, on its own test. It also used about fifteen times the tokens of a chat, and "
            "on one public benchmark, the number of tokens spent explained eighty percent of the differences in "
            "performance. <bookmark mark='d'/> So much of the gain is simply more computation, spread out. It helps "
            "most on broad tasks that split cleanly, like research, <bookmark mark='e'/> and less on tightly "
            "coupled ones, like changing one codebase, where every agent needs to know everything."
        ) as vo:
            self.play(FadeIn(lead))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in down], lag_ratio=0.2), FadeIn(subs))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in up], lag_ratio=0.2), FadeIn(ul))
            vo.wait_until("c")
            self.play(FadeIn(claim, shift=LEFT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(tail), FadeIn(good[0]), FadeIn(gl[0]))
            vo.wait_until("e")
            self.play(FadeIn(good[1]), FadeIn(gl[1]))
        self.wait(0.3)
        self.clear_scene()
