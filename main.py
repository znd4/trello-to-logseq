from plumbum.cmd import trello, jq, parallel
import sys
from plumbum import FG

boards = trello["board:list", "--format=json"] | jq["-r", "map({id, name})"]
lists = (
    boards
    | jq["-r", ".[] | .name"]
    | parallel[trello["list:list", "--format=json", "--board"]]
    | jq["-c", "."]
    | parallel[
        "-a",
        "-",
        "-a",
        boards,
        jq[
            "--argjson",  #
            "list",
            "{}",
            "--argjson",
            "board",
            "{}",
            "-r",
            "",
        ],
    ]
)
(lists | jq["-c", "."]) & FG
sys.exit(0)
cards = lists | jq["-r", "map({id, name, board, list})})"] | parallel[trello["card:list", "--format=json", "--list"]]
