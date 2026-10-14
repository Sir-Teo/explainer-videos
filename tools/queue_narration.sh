#!/bin/zsh
# Narration queue for the series masters: synthesize one "<video> <lang>" line of renders/qa/tts_queue.txt at a time
# with tools/narrate.py (the TTS server must be running: .venv-tts/bin/python tools/tts_server.py --voice qwen3-narrator).
# Append lines to the queue to add work; a line "stop" ends the runner. Each item logs "done <video> <lang> (exit N)"
# to renders/qa/tts_queue.log, which tools/queue_masters.sh waits for.
cd "${0:A:h}/.."
Q=renders/qa/tts_queue.txt
touch $Q
while pgrep -f "tools/narrate.py" >/dev/null; do sleep 15; done  # let a narration already running finish first
while true; do
  item=$(head -1 $Q)
  if [[ -z "$item" ]]; then sleep 30; continue; fi
  sed -i '' 1d $Q
  [[ "$item" == stop ]] && break
  set -- ${=item}
  echo "$(date +%H:%M) start $1 $2" >> renders/qa/tts_queue.log
  EXPLAINER_TTS=server EXPLAINER_VOICE=qwen3-narrator PYTHONWARNINGS=ignore \
    .venv/bin/python tools/narrate.py $1 --lang $2 > renders/qa/narrate_${1}_$2.log 2>&1
  rc=$?
  echo "$(date +%H:%M) done  $1 $2 (exit $rc): $(tail -1 renders/qa/narrate_${1}_$2.log)" >> renders/qa/tts_queue.log
done
