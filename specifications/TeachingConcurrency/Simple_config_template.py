#!/usr/bin/env nix-shell
#!nix-shell -i python -p "python3.withPackages(ps: with ps; [ jpype1 ])"

import sys
import os
import re

sys.path.append(os.path.abspath("../../benchmark_scripts"))
from alloy_to_tla_config import edges_to_string, list_to_quoted_string, create_config_subdirectory, change_block_scope, run


def alloy_run_template(n):
    return f"run {{}} for exactly {n} Process"


def alloy_template(src, n):
    return change_block_scope(src, "Invariants",
                              f"for exactly {n} Process, 1..steps")


def tla_template(N):
    return rf'''
CONSTANT N = {N}
SPECIFICATION Spec
INVARIANTS PCorrect TypeOK Inv
'''


def create_alloy_config(config_dir_prefix, alloy_file_path, alloy_file_name,
                        n):
    dst_path = os.path.join(config_dir_prefix, f"{alloy_file_name}.als")
    with open(alloy_file_path, "r") as src:
        with open(dst_path, "w") as dst:
            dst.write(alloy_template(src.read(), n))


def create_tla_config(config_dir_prefix, world, solution, n):
    tla_config_file = "Simple.cfg"
    copy_list = ["Simple.tla", "TLAPS.tla"]

    config_dir = create_config_subdirectory(config_dir_prefix, 1,
                                            copy_list)
    print(f"Created config directory: {config_dir}")

    output_filename = os.path.join(config_dir, f"{tla_config_file}")
    with open(output_filename, 'w') as f:
        f.write(tla_template(n))


run(alloy_run_template, create_alloy_config, create_tla_config)
