from rope.base.project import Project
from rope.refactor.rename import Rename
from rope.base.libutils import path_to_resource
import re
import ast_comments as ast

def main():
    old_name = "my_func"
    new_name = "the_func"

    root_path = "./dummy_code/src/"

    file_names = [root_path+"main.py", root_path+"utils/utils.py"]

    for file_name in file_names:
        file_contents = ""
        comments = []
        with open(file_name) as file:
            file_contents = file.read()
        try:
            tree = ast.parse(file_contents)
        except:
            raise Exception("Unable to parse code.")
        for node in ast.walk(tree):
            if isinstance(node, ast.Comment):
                comments.append({"index": file_contents.index(node.value), "length": len(node.value)})

        offsets = [m.start() for m in re.finditer(old_name, file_contents)]
        project = Project("./dummy_code", ropefolder=None)
        resource = path_to_resource(project, file_name)
        for offset in offsets:
            # check if offset is in a comment
            in_comment = False
            for comment in comments:
                if comment["index"] < offset < comment["index"] + comment["length"]:
                    in_comment = True
                    break
            if not in_comment:
                rename_refactor = Rename(project=project, resource=resource, offset=offset).get_changes(new_name, docs=True)
                rename_refactor.do()

if __name__ == "__main__":
    main()