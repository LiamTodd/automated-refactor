from rope.base.project import Project
from rope.refactor.rename import Rename
from rope.base.libutils import path_to_resource
import ast_comments as ast

def do_refactor(file_name, old_name, new_name, project, resource):
    node_found = True
    while node_found:
        with open(file_name) as file:
            file_contents = file.read()
        try:
            tree = ast.parse(file_contents)
        except:
            raise Exception("Unable to parse code.")
        node_found = False
        for node in ast.walk(tree):
            if (isinstance(node, ast.Name) and node.id == old_name) or (isinstance(node, ast.FunctionDef) and node.name == old_name):
                node_found = True
                col_offset = node.col_offset
                line_number = node.lineno
                index = sum(len(line)+1 for i, line in enumerate(file_contents.splitlines()) if i < line_number - 1) + col_offset
                if (isinstance(node, ast.FunctionDef) and node.name == old_name):
                    index += 4 # account for 'def '
                rename_refactor = Rename(project=project, resource=resource, offset=index).get_changes(new_name, docs=True)
                rename_refactor.do()
                # only change on occurrence at a time
                break


def main():
    old_name = "p"
    new_name = "my_param"

    root_path = "./dummy_code/src/"
    file_names = [root_path+"main.py", root_path+"utils/utils.py"]

    for file_name in file_names:
        project = Project("./dummy_code", ropefolder=None)
        resource = path_to_resource(project, file_name)
        do_refactor(file_name, old_name, new_name, project, resource)

if __name__ == "__main__":
    main()