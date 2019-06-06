#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys

all_sections_map = {
    "100": {
        "x": 3,
        "y": 4 + 0.5,
        "w": 1.5,
        "h": 4,
        "rooms": [
            101,
            103,
            105,
            107,
            109,
            111,
            113,
            115,
            117,
            119,
            "121G",
            "121M",
            123,
            102,
            "104G",
            "104M",
            106,
            108,
            110,
            "HVV",
            112,
            114,
            "116G",
            "116M",
            118,
            120,
            122,
        ],
    },
    "200": {
        "x": 5.5,
        "y": 4.5 + 0.5,
        "w": 1.5,
        "h": 4,
        "rooms": [
            201,
            203,
            205,
            207,
            209,
            211,
            213,
            215,
            217,
            219,
            "221G",
            "221M",
            223,
            202,
            204,
            "206M",
            "206G",
            208,
            "210M",
            "210G",
            212,
            214,
            "216G",
            "216M",
            218,
            220,
            222,
        ],
    },
    "300": {
        "x": 8,
        "y": 5 + 0.5,
        "w": 1.5,
        "h": 4,
        "rooms": [
            301,
            303,
            305,
            307,
            309,
            311,
            313,
            315,
            317,
            319,
            321,
            323,
            302,
            304,
            306,
            308,
            310,
            312,
            314,
            316,
            318,
            320,
            "322k",
        ],
    },
    "400": {
        "x": -3,
        "y": 4,
        "w": 1.5,
        "h": 4,
        "rooms": [
            402,
            404,
            406,
            408,
            410,
            412,
            414,
            416,
            418,
            420,
            "422G",
            "422M",
            424,
            401,
            "403G",
            "403M",
            405,
            407,
            409,
            "HVØ",
            411,
            413,
            "415G",
            "415M",
            417,
            419,
            421,
        ],
    },
    "500": {
        "x": -5.5,
        "y": 4.5,
        "w": 1.5,
        "h": 4,
        "rooms": [
            502,
            504,
            506,
            508,
            510,
            512,
            514,
            516,
            518,
            520,
            "522G",
            "522M",
            524,
            501,
            "503G",
            "503M",
            505,
            "507M",
            "507G",
            509,
            511,
            513,
            515,
            "517M",
            "517G",
            519,
            521,
        ],
    },
    "600": {
        "x": -8,
        "y": 5,
        "w": 1.5,
        "h": 4,
        "rooms": [
            602,
            604,
            606,
            608,
            610,
            612,
            614,
            616,
            618,
            620,
            622,
            624,
            601,
            603,
            605,
            607,
            609,
            611,
            613,
            615,
            617,
            619,
            "623k",
        ],
    },
    "HB": {
        "x": 0,
        "y": -1,
        "w": 3,
        "h": 2,
        "rooms": [
            2,
            4,
            "6A",
            "6B",
            8,
            10,
            12,
            14,
            16,
            18,
            20,
            "22A",
            "22B",
            24,
            26,
            28,
            30,
            11,
            9,
            7,
            1,
            3,
            5,
        ],
    },
    "700": {
        "x": -4,
        "y": -1.5,
        "w": 1.5,
        "h": 0.8,
        "rooms": [710, 708, 706, 704, 711, 709, 707, 705, 703, 702, 701, 712],
    },
    "Gule": {
        "x": -1,
        "y": -3.5,
        "w": 1.5,
        "h": 0.8,
        "rooms": ["H1", "H2", "H3", "H4", "H5", "H6", "H7"],
    },
    "Porten": {"x": -7, "y": 0.5, "w": 2.5, "h": 0.8, "rooms": ["P1+4", "P2", "P3"]},
    "AX": {"x": -7, "y": -1, "w": 2.5, "h": 0.8, "rooms": ["AX1", "AX2", "AX3"]},
    "Perm": {"x": 0, "y": 1.5, "w": 0.8, "h": 0.8, "rooms": ["Perm"]},
}


class Parsed:
    def __init__(self, file_bytter):
        self.bytter = self.load_bytter(
            file_bytter, get_room_to_section_map(all_sections_map)
        )

    def load_bytter(self, filnavn, room_to_section_map):
        """
        Hent inn bytter fra fil.
        """
        lines = []
        with open(filnavn, "r") as content_file:
            lines = content_file.readlines()

        moves = {}

        recheck = re.compile(r"^(.+) -> ([^ ]+)( \[(.*)\])?$", re.DOTALL)
        for line in lines:
            res = recheck.match(line.strip())
            if res:
                section_from = room_to_section_map[str(res.group(1))]
                section_to = room_to_section_map[str(res.group(2))]

                if section_from not in moves:
                    moves[section_from] = {}

                if section_to not in moves[section_from]:
                    moves[section_from][section_to] = 0

                moves[section_from][section_to] += 1

        result = []
        for section_from, item in moves.items():
            for section_to, count in item.items():
                result.append([section_from, section_to, count])

        return result


def get_room_to_section_map(all_sections_map):
    result = {}

    for groupid in all_sections_map:
        group = all_sections_map[groupid]

        for room in group["rooms"]:
            result[str(room)] = groupid

    return result


# tegn områdene
def draw_nodes(parsed):
    for groupid in all_sections_map:
        group = all_sections_map[groupid]
        x = float(group["x"])
        y = float(group["y"])

        print(
            '\t"%s" [ pos = "%.4f,%.4f!", shape = box, width = %.4f, height = %.4f, fixedsize = true ];'
            % (groupid, x, y, group["w"], group["h"])
        )


# tegn rombyttene
def draw_edges(parsed):
    for section_from, section_to, count in parsed.bytter:
        print(
            '\t"%s" -> "%s" [color="lightblue:dodgerblue;0.5", penwidth=%f, arrowsize=%f, constraint=false]'
            % (section_from, section_to, 1.5 * count, 0.3 + 0.3 * count)
        )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Mangler argumenter!\n")
        sys.exit(1)

    file_bytter = sys.argv[1]

    print(
        """digraph {
    layout=fdp
    overlap = true

    edge[constraint=false]
    splines=true

    outputorder=nodesfirst"""
    )

    parsed = Parsed(file_bytter)

    draw_nodes(parsed)
    draw_edges(parsed)

    print("}")
