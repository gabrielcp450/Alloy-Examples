#!/usr/bin/env nix-shell
#!nix-shell -i python -p "python3.withPackages(ps: with ps; [ jpype1 ])"

import sys
import os
import re

sys.path.append(os.path.abspath("../../benchmark_scripts"))
from alloy_to_tla_config import edges_to_string, dict_values_to_string, list_to_unquoted_string, create_config_subdirectory, change_block_scope, get_object_index, run


def alloy_run_template(n):
    return f"run {{}} for exactly {n} Acceptor, exactly {n} Quorum, exactly 2 Value, 2 Ballot"


def alloy_template(src, n):
    return change_block_scope(src, "Inv",
                              f"for exactly {n} Acceptor, exactly {n} Quorum, exactly 2 Value, 2 Ballot, 1..steps")


def tla_template(acceptors, quorum):
    return rf'''------------------------------ MODULE MCVoting ------------------------------
EXTENDS Voting, TLC

CONSTANTS a1, a2, a3, a4  \* acceptors
CONSTANTS v1, v2      \* Values

MCAcceptor == {{{list_to_unquoted_string(acceptors)}}}
MCValue == {{v1, v2}}
MCQuorum == {{{dict_values_to_string(acceptors, quorum)}}}
MCBallot == 0..1
MCSymmetry == Permutations(MCAcceptor) \cup Permutations(MCValue)
=============================================================================
'''


def create_alloy_config(config_dir_prefix, alloy_file_path, alloy_file_name,
                        n):
    dst_path = os.path.join(config_dir_prefix, f"{alloy_file_name}.als")
    with open(alloy_file_path, "r") as src:
        with open(dst_path, "w") as dst:
            dst.write(alloy_template(src.read(), n))


def create_tla_config(config_dir_prefix, world, solution, n):
    tla_config_file = "MCVoting.tla"
    copy_list = ["Voting.tla", "TLAPS.tla", "MCVoting.cfg"]

    acceptor_labels = ["a1", "a2", "a3", "a4"][:n]

    index = 1
    if solution.satisfiable():
        while True:
            quorum = {}
            print(f"Instance {index} found. Predicate is consistent.")

            for sig in world.getAllReachableSigs():
                if str(sig) == "this/Quorum":
                    fields = sig.getFields()
                    for field in fields:
                        if str(field.sig
                               ) == "this/Quorum" and field.label == "nodes":
                            ts = solution.eval(field)
                            for t in ts:
                                quorum_index = int(
                                    re.search(r'.*?(\d+)$',
                                              str(t.atom(0))).group(1))
                                acceptor_index = int(
                                    re.search(r'.*?(\d+)$',
                                              str(t.atom(1))).group(1))

                                if quorum_index not in quorum:
                                    quorum[quorum_index] = []
                                quorum[quorum_index].append(acceptor_index)

            config_dir = create_config_subdirectory(config_dir_prefix, index, copy_list)
            print(f"Created config directory: {config_dir}")

            output_filename = os.path.join(config_dir,
                                            f"{tla_config_file}")
            with open(output_filename, 'w') as f:
                f.write(tla_template(acceptor_labels, quorum))
            index += 1

            solution = solution.fork(-1)
            if not solution.satisfiable():
                print("No more satisfying instances.")
                break
    else:
        print("No counterexample found. Assertion may be valid.")


run(alloy_run_template, create_alloy_config, create_tla_config)
