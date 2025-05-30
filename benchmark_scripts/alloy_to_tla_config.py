import os
import sys
import jpype
import jpype.imports
import time
import re
import traceback
import shutil


def change_block_scope(text, name, scope):
    match = re.search(rf'check\s+{name}\s*{{', text)
    if not match:
        return text

    start = match.end() - 1
    stack = ['{']
    end = start + 1

    while stack and end < len(text):
        if text[end] == '{':
            stack.append('{')
        elif text[end] == '}':
            stack.pop()
        end += 1

    if len(stack):
        print("SYNTAX ERROR: Incorrect number of { and }")
        return text

    post_block = text[end:]
    scope_match = re.match(r'.*[^\n]+', post_block)

    if scope_match:
        after_scope = post_block[scope_match.end():]
        return text[:end] + f' {scope}' + after_scope
    else:
        return text[:end] + f' {scope}' + text[end:]


def create_config_subdirectory(base_name, index, copy_list):
    """Create a directory for the current config and copy files to it."""
    # Create subdirectory name
    dir_name = f"{base_name}_{index:02d}"
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


def list_to_unquoted_string(string_list):
    return ", ".join(f'{item}' for item in string_list)


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


def dict_values_to_string(labels, d):
    # d = {0: [1], 1: [1,0]}
    # out: {a1}, {a1, a0}
    result = []
    for key in sorted(d.keys()):
        values = d[key]
        # Convert each value to its corresponding label
        label_set = {labels[val] for val in values}
        # Format as a set string
        result.append("{" + ", ".join(sorted(label_set)) + "}")
    return ", ".join(result)


def get_object_index(t):
    return int(re.search(r'.*?(\d+)$', str(t)).group(1))


def run(alloy_run_template, create_alloy_config, create_tla_config):
    if len(sys.argv) < 3:
        print("Usage: ./config_gen.py <alloy_file_path> <N>", file=sys.stderr)
        sys.exit(1)

    n = int(sys.argv[2])
    alloy_file_path = sys.argv[1]

    alloy_file_name = os.path.splitext(os.path.basename(alloy_file_path))[0]
    config_dir_prefix = f"config_{alloy_file_name}_n{n:02d}"

    # Create base directory if it doesn't exist
    if not os.path.exists(config_dir_prefix):
        os.makedirs(config_dir_prefix)

    # -------- Create Alloy file --------
    create_alloy_config(config_dir_prefix, alloy_file_path, alloy_file_name, n)
    # -----------------------------------

    # -------- Create Alloy config generator file --------
    with open(alloy_file_path, "r") as src:
        with open("temp.als", "w") as dst:
            dst.write(src.read())
            dst.write("\n")
            dst.write(alloy_run_template(n))

    alloy_jar_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "org.alloytools.alloy.dist.jar")

    if not jpype.isJVMStarted():
        jpype.startJVM(classpath=[alloy_jar_path])

    from edu.mit.csail.sdg.parser import CompUtil, CompModule
    from edu.mit.csail.sdg.ast import Sig, Command
    from edu.mit.csail.sdg.alloy4 import A4Reporter
    from edu.mit.csail.sdg.translator import TranslateAlloyToKodkod, A4Options, A4Solution, A4TupleSet, A4Tuple

    try:
        rep = A4Reporter()
        options = A4Options()
        world = CompUtil.parseEverything_fromFile(rep, None, "temp.als")

        # Run the last command in the model
        commands = world.getAllCommands()
        command = commands.get(commands.size() - 1)
        print(f"Executing command: {command.label}")
        solution = TranslateAlloyToKodkod.execute_command(
            rep, world.getAllReachableSigs(), command, options)

        create_tla_config(config_dir_prefix, world,
                                    solution, n)
    except Exception as e:
        traceback.print_exc()

    os.remove("temp.als")
    # ----------------------------------------------------
