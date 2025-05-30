#!/usr/bin/env nix-shell
#!nix-shell -i python -p "python3.withPackages(ps: with ps; [ jpype1 ])"

import sys
import os
import re

sys.path.append(os.path.abspath("../../benchmark_scripts"))
from alloy_to_tla_config import edges_to_string, list_to_unquoted_string, create_config_subdirectory, change_block_scope, run


def alloy_run_template(n):
    return f"run {{}} for exactly {n} RM"


def alloy_template(src, n):
    return change_block_scope(src, "TCConsistent",
                              f"for exactly {n} RM, 1..steps")


def tla_template(R):
    return rf'''
CONSTANT RM = {{{list_to_unquoted_string(R)}}}
INVARIANTS TCTypeOK TCConsistent
SPECIFICATION TCSpec
CHECK_DEADLOCK FALSE
'''


def create_alloy_config(config_dir_prefix, alloy_file_path, alloy_file_name,
                        n):
    dst_path = os.path.join(config_dir_prefix, f"{alloy_file_name}.als")
    with open(alloy_file_path, "r") as src:
        with open(dst_path, "w") as dst:
            dst.write(alloy_template(src.read(), n))


def create_tla_config(config_dir_prefix, world, solution, n):
    tla_config_file = "TCommit.cfg"
    copy_list = ["TCommit.tla"]

    R = ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15", "r16", "r17", "r18", "r19", "r20"][:n]

    config_dir = create_config_subdirectory(config_dir_prefix, 1,
                                            copy_list)
    print(f"Created config directory: {config_dir}")

    output_filename = os.path.join(config_dir, f"{tla_config_file}")
    with open(output_filename, 'w') as f:
        f.write(tla_template(R))


run(alloy_run_template, create_alloy_config, create_tla_config)
