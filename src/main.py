from rope.base.project import Project
from rope.refactor.rename import Rename
from rope.base.libutils import path_to_resource
import re

def main():
    old_name = "my_func"
    new_name = "util_func"

    root_path = "./dummy_code/src/"

    file_names = [root_path+"main.py", root_path+"utils/utils.py"]

    for file_name in file_names:
        file_contents = ""
        with open(file_name) as file:
            file_contents = file.read()
        offsets = [m.start() for m in re.finditer(old_name, file_contents)]
        project = Project("./dummy_code", ropefolder=None)
        resource = path_to_resource(project, file_name)
        for offset in offsets:
            rename_refactor = Rename(project=project, resource=resource, offset=offset).get_changes(new_name)
            rename_refactor.do()

if __name__ == "__main__":
    main()