#!/usr/bin/env nix-shell
#!nix-shell -i python -p "python3.withPackages(ps: with ps; [ jpype1 ])"

import os
import sys
import jpype
import jpype.imports
import time
import re
import traceback
import shutil

def create_config_directory(base_name, index, copy_list):
    """Create a directory for the current config and copy files to it."""
    # Create base directory if it doesn't exist
    if not os.path.exists(base_name):
        os.makedirs(base_name)
    
    # Create subdirectory name
    dir_name = f"{base_name}_{index}"
    subdir_path = os.path.join(base_name, dir_name)
    
    # Create subdirectory if it doesn't exist
    if not os.path.exists(subdir_path):
        os.makedirs(subdir_path)
    
    # Get current directory
    curr_dir = os.getcwd()
    
    # Copy each item to the solution directory
    for item in copy_list:
        src_path = os.path.join(curr_dir, item)
        dst_path = os.path.join(curr_dir, subdir_path, item)
        
        if os.path.isdir(src_path):
            if not os.path.exists(dst_path):
                shutil.copytree(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)
    
    return subdir_path

def list_to_quoted_string(string_list):
    return ", ".join(f'"{item}"' for item in string_list)

def edges_to_string(node_labels, actual_edges):
    node_count = len(node_labels)
    lines = []
    for i in range(node_count):
        for j in range(node_count):
            from_node = node_labels[i]
            to_node = node_labels[j]
            exists = (i, j) in actual_edges

            line = f'<<"{from_node}", "{to_node}">> :> {"TRUE" if exists else "FALSE"}'
            if i + j < node_count + node_count - 2:
                line += " @@"
            lines.append(line)

    return "\n".join(lines)


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

def main():
    if len(sys.argv) < 2:
        print("Usage: ./tla_config_gen.py <alloy_file_path>", file=sys.stderr)
        sys.exit(1)

    # Path to the Alloy JAR file - adjust this to your environment
    alloy_jar_path = "org.alloytools.alloy.dist.jar"

    # Start the JVM if it's not already running
    if not jpype.isJVMStarted():
        jpype.startJVM(classpath=[alloy_jar_path])

    # Import Java classes
    from edu.mit.csail.sdg.parser import CompUtil, CompModule
    from edu.mit.csail.sdg.ast import Sig
    from edu.mit.csail.sdg.alloy4 import A4Reporter
    from edu.mit.csail.sdg.translator import TranslateAlloyToKodkod, A4Options, A4Solution, A4TupleSet, A4Tuple
    from java.io import File

    try:
        # Parse the model
        world = CompUtil.parseEverything_fromFile(None, None, sys.argv[1])

        # Options for the solver
        options = A4Options()

        # Run the last command in the model
        commands = world.getAllCommands()
        command = commands.get(commands.size() - 1)
        print(f"Executing command: {command.label}")

        rep = A4Reporter()
        solution = TranslateAlloyToKodkod.execute_command(rep, world.getAllReachableSigs(), command, options)

        index = 1
        config_name = "MCEcho"
        config_dir_prefix = "echo_n1"
        node_labels = ["a"]
        copy_list = ["Echo.tla", "Relation.tla", "MCEcho.cfg"]

        if solution.satisfiable():
            while True:
                print(f"Instance {index} found. Predicate is consistent.")

                node_graph = []
                # initiator = None

                for sig in world.getAllReachableSigs():
                    # if str(sig) == "this/Initiator":
                    #     ts = solution.eval(sig)
                    #     for t in ts:
                    #         initiator = int(re.search(r'.*?(\d+)$', str(t)).group(1))
                    if str(sig) == "this/Node":
                        fields = sig.getFields()
                        for field in fields:
                            if str(field.sig) == "this/Node" and field.label == "neighbors":
                                ts = solution.eval(field)
                                for t in ts:
                                    from_index = int(re.search(r'.*?(\d+)$', str(t.atom(0))).group(1))
                                    to_index = int(re.search(r'.*?(\d+)$', str(t.atom(1))).group(1))
                                    node_graph.append((from_index, to_index))

                for initiator in node_labels:
                    config_dir = create_config_directory(config_dir_prefix, index, copy_list)
                    print(f"Created config directory: {config_dir}")

                    output_filename = os.path.join(config_dir, f"{config_name}.tla")
                    with open(output_filename, 'w') as f:
                        f.write(tla_template(node_labels, initiator, node_graph))
                    index += 1

                solution = solution.fork(-1)
                if not solution.satisfiable():
                    print("No more satisfying instances.")
                    break
        else:
            print("No counterexample found. Assertion may be valid.")

    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    main()
