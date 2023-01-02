
<h1 align="center" >
    <img src=https://user-images.githubusercontent.com/63620799/167208066-3d935a78-e203-4f8c-be27-fd3ff210828b.gif>
</h1>
<h2 align="center" >
    Python Script that convert your repository to PDF<br>
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/Alfareiza/repository-to-pdf?style=social">
    <img alt="GitHub followers" src="https://img.shields.io/github/followers/Alfareiza?label=Follow%20me%20%3A%29&style=social">
</h2>

<h2>⚈ About This</h2>

I decided to make this program because in cases where I work with projects in django, there are a lot of boring files and structures to follow. This is why I usually print the code to have it closer to me, but for this to happen, they have to go through a lot of copying and pasting. This is why I decided to convert my repositories to pdf.

<h2>⚈ Prerequisites</h2>

Git, Pip, Python (^3.8) installed and configured as environment variables.

### 1. Clone the Project

Execute the next command on your terminal

`git clone https://github.com/Alfareiza/repository-to-pdf.git`

### 2. Isolate the environment

Once the repository has been cloned, a folder is created with the name of the project `repository-to-pdf`. 

Go toward this folder using the terminal :

`cd repository-to-pdf`

And execute:

`python -m venv .venv`

Then to activate the isolated environment execute the next command according to your O.S

|          Windows       |              Linux          |
|------------------------|:---------------------------:|
| .venv\Scripts\activate |  source .venv/bin/activate  |

Finally, execute:

`pip install -r requirements.txt`

All the dependencies and sub-dependencies will be installed on the local project.


<h2>⚈ How to use it</h2>

Once the environment has been isolated, you can execute the program through the terminal.

So, for the magic to happen, execute the next command:

`python -m generate_pdf.py {path_of_the_directory}`

Examples:

```python
    python generate_pdf.py --style tango /home/alfonso/PycharmProjects/blog/

    python generate_pdf.py /home/alfonso/PycharmProjects/colombian_newspapers

    python -m generate_pdf /home/alfonso/PycharmProjects/xml-to-json
    
    python generate_pdf.py C:\Users\Alfonso\PycharmProjects\ScrappingColombianNewspapers
```

In case you want to change the **theme**, you can choose it from the next list:

- bw
- sas
- xcode
- autumn
- borland
- arduino
- igor
- lovelace
- pastie
- rainbow_dash
- emacs
- tango
- colorful
- rrt
- algol
- abap
