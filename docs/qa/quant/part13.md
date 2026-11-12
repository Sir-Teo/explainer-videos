# Quant, Built, Part 13: review log

Moved here from `videos/quant/quant13/README.md` on 12 November 2026, unchanged, so that the README holds
course material only. It records what earlier QA passes inspected and at which source revision; evidence
files it names were never committed (`docs/qa/evidence/` is git-ignored).

## Validation in this polish pass

All 21 English and 21 Mandarin narration-beat checks and 21 English silent
motion checks pass against the current source. One simulation motion scan flags
a 1.5-second sparse formula transition, manually inspected and retained; the other
62 receipts have zero automated warnings. Their sheets were visually reviewed.
Chinese source coverage is 140/140;
the narration estimate is 61.5 minutes. Eleven sampled speech reports cover
67 lines, and the actual 161.0-second narrated English opening has a reviewed
contact sheet, dead-air scan and verified audio stream. Full continuous
production-voice listening and synchronization remain pending.

The local silent preview is `renders/quant13_polished_silent.mp4` (69:51,
21 embedded chapters and English subtitles). The actual opening is
`media/quant13/narrated_qa/videos/s01_hook/480p15/Hook.mp4`.
See [the evidence record](../../../docs/qa/quant13-polish-evidence.json) and
[the sequential QA log](../../../docs/qa/quantitative-finance-polish.md).

本轮通过21个英文与21个中文叙述节点检查，以及21个英文静音动画检查，其中模拟章节保留一处1.5秒稀疏转场警告，已逐半秒人工检查；其余62份无自动警告，联系表已人工审阅。
中文覆盖140/140，约61.5分钟。十一份实际语音报告检查67句的信号与时间标记，实际英文开场也已审阅。
完整连续生产语音聆听和同步仍待单独完成；这些检查不证明发音正确。
