#!/usr/bin/env nix-shell
#!nix-shell -i python -p "python3.withPackages(ps: with ps; [ jpype1 ])"

import sys
import os
import re

sys.path.append(os.path.abspath("../../benchmark_scripts"))
from alloy_to_tla_config import edges_to_string, list_to_quoted_string, create_config_subdirectory, change_block_scope, run


def alloy_run_template(n):
    return f"run {{}} for exactly {n} Node"


def alloy_template(src, n):
    return change_block_scope(src, "AncestorProperties",
                              f"for exactly {n} Node, 1..steps")


def tla_template(N, I, R):
    return rf'''---------- MODULE MCEcho ----------
EXTENDS Echo

N1 == {{{list_to_quoted_string(N)}}}

I1 == {f'"{I}"'}

R1 == (
{edges_to_string(N, R)}
)

\* Print R and initiator to stdout at startup.
TestSpec == PrintT(R) /\ PrintT(initiator) /\ Spec        
===================================
'''


def create_alloy_config(config_dir_prefix, alloy_file_path, alloy_file_name,
                        n):
    dst_path = os.path.join(config_dir_prefix, f"{alloy_file_name}.als")
    with open(alloy_file_path, "r") as src:
        with open(dst_path, "w") as dst:
            dst.write(alloy_template(src.read(), n))


def create_tla_config(config_dir_prefix, world, solution, n):
    tla_config_file = "MCEcho.tla"
    copy_list = ["Echo.tla", "Relation.tla", "MCEcho.cfg"]
    node_labels = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"][:n]

    node_graph = []
    # initiator = None

    index = 1
    if solution.satisfiable():
        while True:
            print(f"Instance {index} found. Predicate is consistent.")

            for sig in world.getAllReachableSigs():
                # if str(sig) == "this/Initiator":
                #     ts = solution.eval(sig)
                #     for t in ts:
                #         initiator = int(re.search(r'.*?(\d+)$', str(t)).group(1))
                if str(sig) == "this/Node":
                    fields = sig.getFields()
                    for field in fields:
                        if str(field.sig
                               ) == "this/Node" and field.label == "neighbors":
                            ts = solution.eval(field)
                            for t in ts:
                                from_index = int(
                                    re.search(r'.*?(\d+)$',
                                              str(t.atom(0))).group(1))
                                to_index = int(
                                    re.search(r'.*?(\d+)$',
                                              str(t.atom(1))).group(1))
                                node_graph.append((from_index, to_index))

            for initiator in node_labels:
                config_dir = create_config_subdirectory(
                    config_dir_prefix, index, copy_list)
                print(f"Created config directory: {config_dir}")

                output_filename = os.path.join(config_dir,
                                               f"{tla_config_file}")
                with open(output_filename, 'w') as f:
                    f.write(tla_template(node_labels, initiator, node_graph))
                index += 1

            solution = solution.fork(-1)
            if not solution.satisfiable():
                print("No more satisfying instances.")
                break
    else:
        print("No counterexample found. Assertion may be valid.")


run(alloy_run_template, create_alloy_config, create_tla_config)
