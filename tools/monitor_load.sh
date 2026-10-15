#!/bin/zsh
# Log machine load every 60 s to renders/qa/load.log: CPU use (of 800% on 8 cores), the share of renders (manim)
# and narration (tts_server), free memory, and swap-out rate, to tune render parallelism (renders/qa/master_jobs).
cd "${0:A:h}/.."
prev=$(vm_stat | awk '/Swapouts/ {gsub("\\.","",$2); print $2}')
while true; do
  sleep 60
  now=$(vm_stat | awk '/Swapouts/ {gsub("\\.","",$2); print $2}')
  ps -A -o %cpu=,command= | awk -v t="$(date +%H:%M)" -v jobs="$(cat renders/qa/master_jobs 2>/dev/null)" \
    -v free="$(memory_pressure | tail -1 | grep -o '[0-9]*%')" -v swap="$(( (now - prev) * 16 / 1024 ))" '
    {tot += $1} /manim render|ffmpeg/ {r += $1} /tts_server/ {s += $1}
    END {printf "%s cpu %3.0f%% (renders %3.0f%%, tts %3.0f%%)  mem free %s  swap-out %d MB/min  jobs %s\n", t, tot, r, s, free, swap, jobs}' >> renders/qa/load.log
  prev=$now
done
