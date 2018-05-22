import os
import re
import sys
import time
import datetime
import platform
import fileinput
import subprocess
from os.path import join
import cStringIO as Buffer


# #####################################################
""" FUNCTION PARAMETERS """
# #####################################################

OPE_SYS = platform.system().lower()
_format = "%a %b %d %H:%M:%S %Y"
date = datetime.datetime.today()
begining = time.time()
highlight = "---------------------------------------------------"
_line = "------------------------------------------------------------------------------------------------------"
print "\n{}\n{:>90}\n{}\n".format(_line, date.strftime(_format), _line)
commands = {

    "versions": """
    git --version
    pip --version
    python --version
    virtualenv --version
    """,

    "pip": "call easy_install pip",

    "venv": "call pip install virtualenv",

    "git_clone": """
    echo "CLONING THE LENTICULAR LENS SOFTWARE"
    git clone https://github.com/veruskacz/alignments.git {0}
    """,

    "git_pull": """
    cd {0}
    git pull
    """,

    "windows": """
    cls
    echo "    >>> UPGRADING PIP"
    python -m pip install --upgrade pip

    echo "   >>> CLONING THE LENTICULAR LENS SOFTWARE"
    echo git clone https://github.com/alkoudouss/alignments.git {0}

    echo "   >>> CREATING A VIRTUAL ENVIRONMENT"
    virtualenv  --python={2}{1}python.exe {0}

    echo "   >>> ACTIVATING THE VIRTUAL ENVIRONMENT"
    call {0}{1}Scripts{1}activate.bat

    echo "   >>> INSTALLING THE LENTICULAR LENS REQUIREMENTS"
    pip install -r  {0}{1}requirements.txt

    echo "   >>> INSTALLATION DONE..."
    echo "   >>> RUNNING THE LENTICULAR LENS"
    cd {0}{1}src
    echo "   >>> mac: LL_STARDOG_PATH="{3}" LL_STARDOG_DATA="{4}" python run.py"
    echo "python -c "import webbrowser as web; web.open_new_tab('http://localhost:5077/')""
    python run.py
    """,

    "mac": """
    cls
    echo "    >>> UPGRADING PIP"
    python -m pip install --upgrade pip

    echo "   >>> CLONING THE LENTICULAR LENS SOFTWARE"
    echo git clone https://github.com/alkoudouss/alignments.git {0}

    echo "   >>> CREATING A VIRTUAL ENVIRONMENT"
    virtualenv  --python={2}{1}python.exe {0}

    echo "   >>> ACTIVATING THE VIRTUAL ENVIRONMENT"
    call {0}{1}Scripts{1}activate.bat

    echo "   >>> INSTALLING THE LENTICULAR LENS REQUIREMENTS"
    pip install -r  {0}{1}requirements.txt

    echo "   >>> INSTALLATION DONE..."
    echo "   >>> RUNNING THE LENTICULAR LENS"
    cd {0}{1}src
    echo "   >>> mac: LL_STARDOG_PATH="{3}" LL_STARDOG_DATA="{4}" python run.py"
    echo "python -c "import webbrowser as web; web.open_new_tab('http://localhost:5077/')""
    python run.py
    """
}


# #####################################################
""" FINSTALLATION FUNCTIONS """
# #####################################################


def execute_cmd(cmd, file_path, output=True, run=True):

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # CREATE THE BATCH FILE FOR CHECKING PIP PYTHON AND VIRTUALENV
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    with open(name=file_path, mode="wb") as writer:
        writer.write(cmd)

    # MAC PERMISSION ISSUES
    if OPE_SYS != 'windows':
        os.chmod(file_path, 0o777)

    # EXECUTE THE COMMAND
    if run is True:

        if output is True:
            output = subprocess.check_output(file_path, shell=True)
            return str(output)
        else:
            # RUNS IN A NEW SHELL
            subprocess.call(file_path, shell=True)


def normalise_path(file_path):

    """""""""""""""""""""""""""
    # NORMALISES WINDOWS PATH
    """""""""""""""""""""""""""
    file_path = re.sub('[\1]', "\\\\1", file_path)
    file_path = re.sub('[\2]', "\\\\2", file_path)
    file_path = re.sub('[\3]', "\\\\3", file_path)
    file_path = re.sub('[\4]', "\\\\4", file_path)
    file_path = re.sub('[\5]', "\\\\5", file_path)
    file_path = re.sub('[\6]', "\\\\6", file_path)
    file_path = re.sub('[\7]', "\\\\7", file_path)
    file_path = re.sub('[\0]', "\\\\0", file_path)
    file_path = re.sub('[\a]', "\\\\a", file_path)
    file_path = re.sub('[\b]', "\\\\b", file_path)
    file_path = re.sub('[\f]', "\\\\f", file_path)
    file_path = re.sub('[\n]', "\\\\n", file_path)
    file_path = re.sub('[\r]', "\\\\r", file_path)
    file_path = re.sub('[\t]', "\\\\t", file_path)
    file_path = re.sub('[\v]', "\\\\v", file_path)
    return file_path


def replace_all(file_path, search_exp, replace_exp):

    """""""""""""""""""""""""""""""""""""""""""""""
    # REPLACES AN EXPRESSION IN THE SPECIFIED FILE
    """""""""""""""""""""""""""""""""""""""""""""""

    wr = Buffer.StringIO()
    if os.path.isfile(file_path) is False:
        print "THE PROVIDED FILE BELOW DOES NOT EXIST" \
              "\n\t>>> {}\nFOR THAT YOUR ACTION HAS BEEN TERMINATED\n".format(file_path)
        exit(0)

    with open(name=file_path, mode="r") as reader:
        for line in reader:
            found = re.findall(search_exp, line)
            if len(found) > 0:
                print "\t{:50} <-- {}".format(found[0], replace_exp)
                replaced = line.replace(found[0], replace_exp)
                wr.write(replaced)
            else:
                wr.write(line)

    with open(name=file_path, mode="w+") as writer:
        writer.write(wr.getvalue())


def update_settings(directory, stardog_home, stardog_bin, database_name):

    """""""""""""""""""""""""""""""""""""""""""""""""""""
    # UPDATING THE SETTINGS IN THE SERVER SETTING FILE
    """""""""""""""""""""""""""""""""""""""""""""""""""""

    svr_settings = join(directory, "alignments{0}src{0}Alignments{0}Server_Settings.py".format(os.path.sep))

    # STARDOG BIN
    s_bin = """\"LL_STARDOG_PATH",[ ]*"(.*)\""""
    replace_all(svr_settings, s_bin, """{0}""".format(stardog_bin, os.path.sep))

    # STARDOG DATA OF HOME
    s_data = """"LL_STARDOG_DATA",[ ]*"(.*)\""""
    replace_all(svr_settings, s_data, """{}""".format(stardog_home))

    # LENTICULAR LENS DATABASE NAME
    d_data = """"LL_STARDOG_DATABASE",[ ]*"(.*)\""""
    replace_all(svr_settings, d_data, """{}""".format(database_name))


def input_prep(parameter_inputs):

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # PREPARING THE INPUT PARAMETRS AS IT IS GEVEN AS A STRING
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    # INPUT EXTRACTIOIN STEP 1
    inputs_0 = re.findall("run[ ]*=[ ]*([^\"\'\n]+)", parameter_inputs)
    inputs_1 = re.findall("directory[ ]*=[ \"\']*([^\"\'\n]+)", parameter_inputs)
    inputs_2 = re.findall("python_path[ ]*=[ \"\']*([^\"\'\n]+)", parameter_inputs)
    inputs_3 = re.findall("stardog_bin[ ]*=[ \"\']*([^\"\'\n]*)", parameter_inputs)
    inputs_4 = re.findall("stardog_home[ ]*=[ \"\']*([^\"\'\n]*)", parameter_inputs)
    inputs_5 = re.findall("database_name[ ]*=[ \"\']*([^\"\'\n]*)", parameter_inputs)

    #  INPUT EXTRACTIOIN STEP 2
    run = bool(str(inputs_0[0]).strip()) if len(inputs_0) > 0 else None
    directory = normalise_path(str(inputs_1[0]).strip()) if len(inputs_1) > 0 else None
    python_path = normalise_path(str(inputs_2[0]).strip()) if len(inputs_2) > 0 else None
    stardog_bin = normalise_path(str(inputs_3[0]).strip()) if len(inputs_3) > 0 else None
    stardog_home = normalise_path(str(inputs_4[0]).strip()) if len(inputs_4) > 0 else None
    database_name = str(inputs_5[0]).strip() if len(inputs_5) > 0 else None

    # PRINTING THE EXTRACTED INPUTS
    print "{:23}: {}".format("INSTALLATION DIRECTORY", directory)
    print "{:23}: {}".format("INSTALLED PYTHON PATH", python_path)
    print "{:23}: {}".format("STARDOG DATA PATH", stardog_home)
    print "{:23}: {}".format("STARDOG HOME PATH", stardog_bin)
    print "{:23}: {}".format("DATABASE NAME", database_name)

    # CHECKING IF ALL INPUTS HAVE BEEN PROVIDED
    if run is None or directory is None or python_path is None or stardog_bin is None or \
                    stardog_home is None or database_name is None:
        print "THERE IS A MISSING INPUT"
        exit(0)

    # MAC INPUT ARE NOT WITH BACKSLASH
    if OPE_SYS != "windows":
        if directory.__contains__("\\") or python_path.__contains__("\\") or stardog_bin.__contains__("\\") or \
                        stardog_home.__contains__("\\") is None:
            print "\nCHECK YOUR INPUT PATHS AGAIN AS IT LOOKS LIKE A WINDOWS PATH :-)\n"
            exit(0)

    # ENV VARIABLE OR PROPER VARIABLE ARE ALLOWED
    directory = os.getenv("LL_DIRECTORY", directory)
    python_path = os.getenv("LL_PYTHON_PATH", python_path)
    stardog_bin = os.getenv("LL_STARDOG_PATH", stardog_bin)
    stardog_home = os.getenv("LL_STARDOG_DATA", stardog_home)
    database_name = os.getenv("LL_STARDOG_DATABASE", database_name)

    # MAKING SURE THAT THE PATHS END PROPERLY
    if OPE_SYS != "windows":
        stardog_bin = "{}/".format(stardog_bin) if stardog_bin.endswith("/") is False else stardog_bin
        stardog_home = "{}/".format(stardog_home) if stardog_home.endswith("/") is False else stardog_home
    else:
        stardog_bin = "{}\\".format(stardog_bin) if stardog_bin.endswith("\\") is False else stardog_bin
        stardog_home = "{}\\".format(stardog_home) if stardog_home.endswith("\\") is False else stardog_home
        directory = directory.replace("\\", "\\\\")
        python_path = python_path.replace("\\", "\\\\")
        stardog_bin = stardog_bin.replace("\\", "\\\\")
        stardog_home = stardog_home.replace("\\", "\\\\")

    return [directory, python_path, stardog_bin, stardog_home, database_name, run]


def install(parameter_inputs):

    """""""""""""""""""""""""""
    # INSTALLATION MAIN ENTRY
    """""""""""""""""""""""""""

    parameters = input_prep(parameter_inputs)
    directory = parameters[0]
    python_path = parameters[1]
    stardog_bin = parameters[2]
    stardog_home = parameters[3]
    database_name = parameters[4]
    run = parameters[5]

    # RUNNING THE GENERIC INSTALLATION
    generic_install(directory, python_path, stardog_home, stardog_bin, database_name, run=run)

    # RUNNING WINDOWS SPECIFIC INSTALLATION
    if OPE_SYS == "windows":
        win_install(directory, python_path, stardog_home=stardog_home, stardog_bin=stardog_bin, run=run)

    # RUNNING MAC OR LINUX SPECIFIC INSTALLATION
    else:
        mac_install(directory, python_path, stardog_home=stardog_home, stardog_bin=stardog_bin, run=run)


def generic_install(directory, python_path, stardog_home, stardog_bin, database_name, run=False):

    print "{:23}: {}\n".format("COMPUTER TYPE", platform.system().upper())

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # 1. CHECK WHETHER THE INSTALLATION DIRECTORY EXISTS
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if os.path.isdir(directory) is False:
        try:
            os.mkdir(directory)
            print "\nTHE PROVIDED DIRECTORY DID NOT EXIST BUT WAS CREATED\n"
        except Exception as err:
            print "\nTHE PROVIDED DIRECTORY COULD NOT BE CREATED\n"
            print err
            exit(0)
    # 2. INSTALLATION BATCH FILE PATH
    w_dir = join(directory, "alignments")
    file_path = join(directory, "INSTALLATION.bat" if OPE_SYS == "windows" else "INSTALLATION.sh")

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # 3. CHECKING THE AVAILABLE VESIONS OF THE REQUIRED PAKAGES
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    requirements_out = execute_cmd(commands["versions"], file_path)

    # 4. GIT VERSION IS REQUIRED
    git = re.findall('git version (.+)', str(requirements_out))
    git_version = git[0] if len(git) > 0 else 0
    if int(git_version[0]) == 0:
        print "\nYOU NEED TO INSTALL GIT FROM [https://git-scm.com/downloads]\n"
        exit(0)
    elif int(git_version[0]) <= 1:
        print "\nYOU NEED TO UPGRADE YOUR GIT FROM [https://git-scm.com/downloads]\n"
        exit(0)
    print "\n{:23}: {}".format("GIT VERSION", git_version)

    # 5. PYTHON VERSION IS REQUIRED
    pattern = "([\d*\.]+)"
    python = re.findall('python {}'.format(pattern), str(requirements_out))
    python_version = int(str(python[0]).replace(".", "")) if len(python) > 0 else 0
    if (python_version >= 27) and (python_version < 2713):

        print "{:23}: {}".format("PYTHON VERSION", python[0])

        # MAKE SURE PIP IS INSTALL
        pip = re.findall('pip {}'.format(pattern), str(requirements_out))
        pip_version = pip[0] if len(pip) > 0 else 0
        if pip_version > 0:
            print "{:23}: {}".format("PIP VERSION", pip_version)
        else:
            # INSTALLING PIP
            requirements_out = execute_cmd(cmd=commands["pip"], file_path=file_path)
            print requirements_out

        # MAKE SURE VIRTUAL ENVIRONMENT IS INSTALL
        env = re.findall('{}\n'.format(pattern), requirements_out)
        env_version = env[0] if len(env) > 0 else 0
        if env_version > 0:
            print "{:23}: {}".format("VIRTUALENV VERSION", env_version)
        else:
            # INSTALLING THE VIRTUAL ENV
            requirements_out = execute_cmd(cmd=commands["venv"], file_path=file_path)
            print requirements_out
    else:
        print "PYTHON VERSION 2.7.12 IS REQUIRED TO RUN THE LENTICULAR LENS"
        exit(0)

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # 6. CLONE OR PULTHE LENTICULAR LENS SOFTWARE
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if os.path.isdir(join(directory, "alignments")) is False:
        print "\n{0}\n    >>> LENTICULAR LENS CLONE REQUEST\n{0}\n".format(highlight)
        cloning = commands["git_clone"].format(w_dir)
    else:
        print "\n{0}\n    >>> LENTICULAR LENS PULL REQUEST\n{0}\n".format(highlight)
        pulling = commands["git_pull"].format(join(directory, "alignments"))
    execute_cmd(pulling, file_path, output=False, run=run)

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # 7. UPDAT THE SEVER SETTINGS WITH STARDOG HOME AND BIN PATHS
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    print "\n{0}\n    >>> UPDATING SERVER SETTINGS\n{0}\n".format(highlight)
    update_settings(directory, stardog_home, stardog_bin, database_name)

    # 8. SLEEPING TIME FOR WINDOWS USER FOR CHECKING WHAT HAS BEE DONE SO FAR
    # AS A NEW WINDOW WILL PUP UP AND ERASE ALL PREVIUS OUPUTS
    if OPE_SYS == 'windows':
        print "\n{0}\n    >>> SLEEPING FOR 20 SECONDS FOR USER CHECKS\n{0}\n".format(highlight)
        time.sleep(10)


def win_install(directory, python_path, stardog_home, stardog_bin, run=False):

    # UPGRADE PIP
    # INSTALL THE VIRTUALENV AND ACTIVATE IT
    # INSTALL OR UPDATE THE REQUIREMENTS
    # RUN THE LENTICULAR LENS

    print "\n{0}\n    >>> WINDOWS INSTALLATIONS\n{0}\n".format(highlight)
    file_path = join(directory, "INSTALLATION.bat")
    w_dir = join(directory, "alignments")
    cmds = commands["windows"].format(w_dir, os.path.sep, python_path, stardog_bin, stardog_home)
    execute_cmd(cmds, file_path, output=False, run=run)
    wb.open_new_tab('http://localhost:5077/')


def mac_install(directory, python_path, stardog_home, stardog_bin, run=False):

    # UPGRADE PIP
    # INSTALL THE VIRTUALENV AND ACTIVATE IT
    # INSTALL OR UPDATE THE REQUIREMENTS
    # RUN THE LENTICULAR LENS

    print "\n{0}\n    >>> MAC/LINUX INSTALLATIONS\n{0}\n"
    file_path = join(directory, "INSTALLATION.sh")
    w_dir = join(directory, "alignments")
    cmds = commands["mac"].format(w_dir, os.path.sep, python_path, stardog_bin, stardog_home)
    execute_cmd(cmds, file_path, output=False, run=run)


# ######################################################
"""             INSTALLATION PARAMETERS              """
########################################################
# CHANGE THE FOLLOWING INFORMATIION
#   1. WORKING DIRECTORY PATH
#   2. PYTHON PATH
#   3. STADOG BIN DIRECTORY
#   4. STARDOG DATA BASE DIRECTORY
#   5. STARDOG BATABASE NAME
########################################################
#$######################################################

parameter_input = """

run = True
directory = C:\Productivity\LinkAnalysis\Coverage\InstallTest\Install
python_path = C:\Python27
stardog_bin = C:\Program Files\stardog-5.3.0\bin
stardog_home = C:\Productivity\data\stardog_ISWC
database_name = risis

"""

# #####################################################
""" RUNNING THE LENTICULAR LENS INSTALLATION BASES
    ON THE PARAMETERS VALUES ENTERED ABOVE  """
# #####################################################

install(parameter_input)
# import webbrowser as web
# web.open_new_tab('http://localhost:5077/')
# export_database(Svr.settings[St.stardog_path], "risis", "C:\Productivity\LinkAnalysis\Coverage")
# #####################################################
""" RUNNING THE LENTICULAR LENS INSTALLATION BASES
    ON THE PARAMETERS VALUES ENTERED ABOVE
    MAC OR LINUX EXTRA OPTION USING ENV VARIABLES """
# #####################################################

# DIRECTORY="" PYTHON_PATH="" STARDOG_PATH="" STARDOG_DATA="" python LenticularLensInstallation.py

# https://coderwall.com/p/w78iva/give-your-python-program-a-shell-with-the-cmd-module
