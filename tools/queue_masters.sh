#!/bin/zsh
# Build queue for the series: run one line of renders/qa/render_queue.txt at a time, either
#   preview <video> [build args]   a 480p QA build, or
#   master <video> <lang>          a 2160p60 CRF 16 upload master, started once tools/queue_narration.sh has logged
#                                  that video's narration in that language as done (exit 0). One scene at a
#                                  time: narration sets the pace, and two 4K scenes beside the TTS server swap.
# Append lines to the queue to add work; a line "stop" ends the runner.
cd "${0:A:h}/.."
source .venv/bin/activate
Q=renders/qa/render_queue.txt
touch $Q
while pgrep -f "tools/build.py" >/dev/null; do sleep 30; done  # let a build already running finish first
while true; do
  item=$(head -1 $Q)
  if [[ -z "$item" ]]; then sleep 60; continue; fi
  set -- ${=item}
  if [[ $1 == master ]] && ! grep -q "done  $2 $3 (exit 0)" renders/qa/tts_queue.log; then
    sleep 60; continue  # its narration isn't ready yet
  fi
  sed -i '' 1d $Q
  [[ "$item" == stop ]] && break
  echo "$(date +%H:%M) start $item" >> renders/qa/render_queue.log
  if [[ $1 == preview ]]; then
    nice -n 10 python -u tools/build.py $2 -q l -j 3 ${@:3} > renders/qa/build_$2.log 2>&1
    rc=$?; log=renders/qa/build_$2.log
  else
    EXPLAINER_TTS=server EXPLAINER_VOICE=qwen3-narrator nice -n 5 \
      python -u tools/build.py $2 -q k --fps 60 --crf 16 -j 1 --lang $3 > renders/qa/master_$2_$3.log 2>&1
    rc=$?; log=renders/qa/master_$2_$3.log
    # verify it and add it to the upload kit (renders/upload/analysis-built)
    [[ $rc == 0 && $2 == analysis* ]] && python tools/package_uploads.py --parts ${2#analysis} >> renders/qa/package.log 2>&1
  fi
  echo "$(date +%H:%M) done  $item (exit $rc): $(grep -E 'Wrote|Failed|Missing' $log | tail -1)" >> renders/qa/render_queue.log
done
