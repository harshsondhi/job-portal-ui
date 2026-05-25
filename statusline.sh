#!/usr/bin/env bash
# Claude Code status line script
# Located in: job-portal-ui/statusline.sh

input=$(cat)

model=$(echo "$input" | jq -r '.model.display_name // "Unknown Model"')
used=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
remaining=$(echo "$input" | jq -r '.context_window.remaining_percentage // empty')

# Build context bar (10-char wide)
if [ -n "$used" ]; then
  # Round to nearest integer
  used_int=$(printf '%.0f' "$used")
  filled=$(( used_int * 10 / 100 ))
  empty_blocks=$(( 10 - filled ))

  bar=""
  i=0
  while [ $i -lt $filled ]; do
    bar="${bar}█"
    i=$(( i + 1 ))
  done
  i=0
  while [ $i -lt $empty_blocks ]; do
    bar="${bar}░"
    i=$(( i + 1 ))
  done

  remaining_int=$(printf '%.0f' "$remaining")

  printf "\033[0;36m%s\033[0m  \033[0;33m[%s]\033[0m \033[0;32m%d%%\033[0m used / \033[0;32m%d%%\033[0m left" \
    "$model" "$bar" "$used_int" "$remaining_int"
else
  printf "\033[0;36m%s\033[0m  \033[0;90mContext: N/A\033[0m" "$model"
fi
