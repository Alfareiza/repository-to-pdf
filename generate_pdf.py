from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List

import pdfkit
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


class RepoToPDF:
    """
    This class convert repository to pdf where this must be already cloned
    """

    def __init__(self, directory, style="colorful"):
        self.directory = Path(str(directory))
        self.style = style
        self.name_repository = str(directory).strip("/").split("/")[-1]
        self.ignored_files = self.ignored_files()
        self.files_to_convert = self.select_files(self.directory)
        self.tree = self.create_tree(self.directory)

    def ignored_files(self) -> List[str]:
        """
        Scrap the gitignore file it it exists and prepare all the stuffs that must be ignored.
        :return: List of strings, that depicts the files/folders scrapped from .gitignore file.
        """
        # Standard Stuffs
        gitignore_stuff = [
            ".pdf",
            "__init__.py",
            "__pycache__",
            ".gitignore",
            ".git",
            "LICENSE",
            ".github",
            "README.md",
            "requirements.txt",
            "pyproject.toml",
            "poetry.lock",
            ".idea",
            "env-sample",
            "merged.html",
        ]
        # Django Stuffs
        gitignore_stuff += [
            "manage.py",
            "migrations/",
            "static/",
            "test_files/",
            "test/",
            "testes/",
            "test.py",
            "tests.py",
            "wsgi.py",
            "asgi.py",
            "settings.py",
        ]
        gitignore_content = []
        if self.directory.joinpath(".gitignore").exists():
            with self.directory.joinpath(".gitignore").open() as fp:
                content = fp.readlines()
                for i in content:
                    line = i.strip()
                    if len(line) > 0 and not "#" in line:
                        gitignore_content.append(line.strip("*"))
        else:
            print(
                "Since the .gitignore file doesn't exists, all the files will be considered"
            )
        return gitignore_content + gitignore_stuff

    def select_files(self, directory: Path, files_selected=[]) -> List[Path]:
        """
        Discover which files are allowed, then return a list with them.
        :param directory: Path
        :param files_selected: List
        :return: List of paths of selected/filtered files
        """
        for i in sorted(directory.iterdir()):
            if not self.must_ignore(i) and i.is_dir():
                self.select_files(i)
            elif not self.must_ignore(i) and i.is_file():
                # print(f'Valid file -> {i}')
                files_selected.append(i)
        return files_selected

    def must_ignore(self, filename: Path) -> bool:
        """
        Validates if a file must be ignored or not from certain logic.
        :param filename: Path
                Ex.: PosixPath('/home/alfonso/PycharmProjects/xml-to-json/manage.py')
        :return: True or False
        """
        if filename.is_dir() and f"{filename.name}/" in self.ignored_files:
            return True
        elif (
            filename.is_file()
            and filename.suffix in self.ignored_files
            or filename.name in self.ignored_files
        ):
            return True

    def create_tree(self, startpath: Path) -> str:
        """
        Create a tree of the folder
        :param startpath:  Path of the folder
        :return: string that depicts the tree of the folder
        """

        # With a criteria (skip hidden files)
        def is_not_hidden(path):
            # filtered_path = False
            ignore = ("__pycache__/", "__init__.py")
            if (
                path.name.startswith(".")
                or path.name.startswith("__")
                or path.name in ignore
            ):
                return False
            return True

        paths = DisplayablePath.make_tree(
            Path(startpath), criteria=is_not_hidden
        )
        tree = ""
        for path in paths:
            tree += path.displayable() + "\n"
        return tree

    def generate_html(self, file: Path, header_path=False) -> str:
        """
        Generate a html file according to a file received in a directory
        :param file: Path. File from the directory input
        :param header_path: boolean. Determines if the file will
                                    have the directory in the first line
        :return: str. A string that depicts the html file
        """
        path_file = ""
        if header_path:
            for i, parent in enumerate(file.parts):
                if parent == self.name_repository:
                    path_file = "/".join(file.parts[i:])
                    break

        with open(file) as fp:
            content = fp.read()

        content = (
            f"{str(path_file)} \n{content}"
            if content
            else f"{str(file)} \nEmpty File"
        )

        lexer = get_lexer_by_name("python", stripall=True)
        formatter = HtmlFormatter(
            full=True,
            style=self.style,
            filename=file.name,
            linenos=True,
            linenostart=0,
        )
        return highlight(content, lexer, formatter)

    def multiple_html_to_pdf(self, temp_folder: Path) -> None:
        """
        converts multiple html files to a single pdf
        args: path to directory containing html files
        :param temp_folder: Path . Temp folder where the html are.
        :return: Nothing. This function create a pdf in the self.directory path
        """
        empty_html = "<html><head></head><body></body></html>"
        for file in sorted(temp_folder.iterdir(), key=lambda d: len(d.stem)):
            if file.suffix == ".html":
                # append html files
                with open(file, "r") as f:
                    html = f.read()
                    empty_html = empty_html.replace(
                        "</body></html>", html + "</body></html>"
                    )

        # save merged html
        with TemporaryDirectory() as temp:
            merged_file = Path(temp) / "00.html"

            with merged_file.open(mode="w+") as merged:
                merged.write(empty_html)

                # Creates pdf
                pdfkit.from_file(
                    str(merged_file),
                    output_path=f"{str(self.directory)}/{self.name_repository}.pdf",
                    options={
                        "encoding": "UTF-8",
                        "margin-top": "0.15in",
                        "margin-right": "0.45in",
                        "margin-bottom": "0.15in",
                        "margin-left": "0.45in",
                    },
                )

        print(
            f"File {str(self.directory)}/{self.name_repository}.pdf generated with success!"
        )

    def generate_pdf(self):
        # Creates temp folder
        with TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)

            for file in self.files_to_convert:
                html_content = self.generate_html(file, header_path=True)
                name_html_file = "_".join(
                    file.parts[file.parts.index(self.name_repository) :]
                ).replace(file.name, f"{file.stem}.html")
                html_file = temp_dir / name_html_file

                # Creates html temp files
                with html_file.open(mode="w+") as file:
                    file.write(html_content)

            tree_file = temp_dir / "tree.txt"
            with tree_file.open(mode="w+") as tree:
                tree.write(self.tree)

            html_content = self.generate_html(tree_file)
            html_file = temp_dir / "00_tree.html"
            with html_file.open(mode="w+") as html:
                html.write(html_content)

            # Create pdf from html temp files in temp_dir
            self.multiple_html_to_pdf(temp_dir)


class DisplayablePath(object):
    display_filename_prefix_middle = "├──"
    display_filename_prefix_last = "└──"
    display_parent_prefix_middle = "    "
    display_parent_prefix_last = "│   "

    def __init__(self, path, parent_path, is_last):
        self.path = Path(str(path))
        self.parent = parent_path
        self.is_last = is_last
        if self.parent:
            self.depth = self.parent.depth + 1
        else:
            self.depth = 0

    @property
    def displayname(self):
        if self.path.is_dir():
            return self.path.name + "/"
        return self.path.name

    @classmethod
    def make_tree(cls, root, parent=None, is_last=False, criteria=None):
        root = Path(str(root))
        criteria = criteria or cls._default_criteria

        displayable_root = cls(root, parent, is_last)
        yield displayable_root

        children = sorted(
            list(path for path in root.iterdir() if criteria(path)),
            key=lambda s: str(s).lower(),
        )
        count = 1
        for path in children:
            is_last = count == len(children)
            if path.is_dir():
                yield from cls.make_tree(
                    path,
                    parent=displayable_root,
                    is_last=is_last,
                    criteria=criteria,
                )
            else:
                yield cls(path, displayable_root, is_last)
            count += 1

    @classmethod
    def _default_criteria(cls, path):
        return True

    @property
    def displayname(self):
        if self.path.is_dir():
            return self.path.name + "/"
        return self.path.name

    def displayable(self):
        if self.parent is None:
            return self.displayname

        _filename_prefix = (
            self.display_filename_prefix_last
            if self.is_last
            else self.display_filename_prefix_middle
        )

        parts = ["{!s} {!s}".format(_filename_prefix, self.displayname)]

        parent = self.parent
        while parent and parent.parent is not None:
            parts.append(
                self.display_parent_prefix_middle
                if parent.is_last
                else self.display_parent_prefix_last
            )
            parent = parent.parent

        return "".join(reversed(parts))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        prog="Repository to PDF",
        description="This program convert a repository to PDF",
        epilog="Enjoy the program! :)",
    )
    parser.add_argument("dir", type=Path, help="Path of the repository.")
    parser.add_argument(
        "--style",
        default="colorful",
        type=str,
        help="Style for the PDF. Choose a style -> https://pygments.org/styles/",
    )

    # Creating a Namespace object
    args = parser.parse_args()
    try:
        if args.style:
            choices = [
                "default",
                "bw",
                "sas",
                "xcode",
                "autumn",
                "borland",
                "arduino",
                "igor",
                "lovelace",
                "pastie",
                "rainbow_dash",
                "emacs",
                "tango",
                "colorful",
                "rrt",
                "algol",
                "abap",
            ]
            if not args.style in choices:
                raise NameError
        if Path(args.dir).exists():
            repo = RepoToPDF(args.dir, style=args.style)
            repo.generate_pdf()
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        print("Invalid Folder !")
    except NameError:
        print(
            f"Invalid Style, please choose one of nexts :\n{', '.join(choices)}"
        )
