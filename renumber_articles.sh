#!/usr/bin/env bash
# Usage: ./renumber_articles.sh [file.md]
# Defaults to README.md if no file is given.

FILE="${1:-README.md}"

if [ ! -f "$FILE" ]; then
  echo "Error: file '$FILE' not found."
  exit 1
fi

perl -i -pe 'BEGIN{$n=0} s/^(Article )\d+/$1 . ++$n/e' "$FILE"
echo "Articles renumbered in '$FILE'."


# chmod +x renumber_articles.sh
# bash renumber_articles.sh