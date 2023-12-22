#!/usr/bin/env bash
set -euo pipefail
boards=$(trello board:list --format json \
    | jq -r 'map({id, name})' \
)
echo $boards | jq
lists=$(\
echo "$boards" | jq -r '.[] | .name' \
    | parallel trello list:list --format json --board \
    | jq -r 'map({id, name})' \
)
echo $lists | jq
jq -n --argjson boards "$boards" --argjson lists "$lists" \
    '$boards '
    # | jq -r 'flatten' \


exit 0
