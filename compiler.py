import os
import sys
import shutil
import subprocess
import tempfile
import time


# =========================================================
# SUPPORTED LANGUAGES
# =========================================================

SUPPORTED_LANGUAGES = {

    "python": {
        "name": "Python",
        "extension": ".py"
    },

    "cpp": {
        "name": "C++",
        "extension": ".cpp"
    },

    "c": {
        "name": "C",
        "extension": ".c"
    },

    "java": {
        "name": "Java",
        "extension": ".java"
    },

    "javascript": {
        "name": "JavaScript",
        "extension": ".js"
    }
}


# =========================================================
# TIMEOUT SETTINGS
# =========================================================

COMPILE_TIMEOUT = 10

RUN_TIMEOUT = 5


# =========================================================
# CHECK COMMAND AVAILABILITY
# =========================================================

def command_exists(command):

    return shutil.which(command) is not None


# =========================================================
# BUILD COMMAND
# =========================================================

def build_command(language, source_file, work_dir):

    if language == "python":

        return [
            sys.executable,
            source_file
        ]

    elif language == "javascript":

        return [
            "node",
            source_file
        ]

    elif language == "cpp":

        executable = os.path.join(
            work_dir,
            "program.exe"
        )

        return {

            "compile": [
                "g++",
                source_file,
                "-std=c++17",
                "-O2",
                "-o",
                executable
            ],

            "run": [
                executable
            ]
        }

    elif language == "c":

        executable = os.path.join(
            work_dir,
            "program.exe"
        )

        return {

            "compile": [
                "gcc",
                source_file,
                "-O2",
                "-o",
                executable
            ],

            "run": [
                executable
            ]
        }

    elif language == "java":

        return {

            "compile": [
                "javac",
                source_file
            ],

            "run": [
                "java",
                "Main"
            ]
        }

    return None


# =========================================================
# RUN PROCESS
# =========================================================

def execute_process(
    command,
    user_input="",
    cwd=None,
    timeout=RUN_TIMEOUT
):

    start_time = time.perf_counter()

    try:

        result = subprocess.run(

            command,

            input=user_input,

            capture_output=True,

            text=True,

            cwd=cwd,

            timeout=timeout,

            shell=False
        )

        elapsed_time = (
            time.perf_counter()
            - start_time
        )

        return {

            "success":
                result.returncode == 0,

            "returncode":
                result.returncode,

            "stdout":
                result.stdout,

            "stderr":
                result.stderr,

            "time":
                f"{elapsed_time:.4f} sec"
        }

    except subprocess.TimeoutExpired:

        return {

            "success": False,

            "returncode": -1,

            "stdout": "",

            "stderr":
                "Execution timed out. "
                f"Maximum execution time is {timeout} seconds.",

            "time":
                f">{timeout} sec"
        }

    except FileNotFoundError as error:

        return {

            "success": False,

            "returncode": -1,

            "stdout": "",

            "stderr":
                f"Required compiler/interpreter not found: {error}",

            "time": ""
        }

    except Exception as error:

        return {

            "success": False,

            "returncode": -1,

            "stdout": "",

            "stderr":
                str(error),

            "time": ""
        }


# =========================================================
# RUN CODE
# =========================================================

def run_code(
    language,
    code,
    user_input=""
):

    language = (
        language or ""
    ).strip().lower()

    code = code or ""

    user_input = user_input or ""

    # =====================================================
    # VALIDATE LANGUAGE
    # =====================================================

    if language not in SUPPORTED_LANGUAGES:

        return {

            "success": False,

            "status": "Error",

            "stdout": "",

            "stderr":
                "Unsupported programming language.",

            "compile_output": "",

            "output": "",

            "time": "",

            "memory": ""
        }

    # =====================================================
    # VALIDATE CODE
    # =====================================================

    if not code.strip():

        return {

            "success": False,

            "status": "Error",

            "stdout": "",

            "stderr":
                "Code cannot be empty.",

            "compile_output": "",

            "output": "",

            "time": "",

            "memory": ""
        }

    # =====================================================
    # CREATE TEMPORARY DIRECTORY
    # =====================================================

    temp_dir = tempfile.mkdtemp(
        prefix="ai_dsa_"
    )

    try:

        extension = SUPPORTED_LANGUAGES[
            language
        ]["extension"]

        # =================================================
        # JAVA FILE MUST BE Main.java
        # =================================================

        if language == "java":

            filename = "Main.java"

        else:

            filename = (
                "main"
                + extension
            )

        source_file = os.path.join(
            temp_dir,
            filename
        )

        # =================================================
        # WRITE SOURCE CODE
        # =================================================

        with open(
            source_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(code)

        # =================================================
        # BUILD EXECUTION COMMAND
        # =================================================

        commands = build_command(
            language,
            source_file,
            temp_dir
        )

        if commands is None:

            return {

                "success": False,

                "status": "Error",

                "stdout": "",

                "stderr":
                    "Unable to build execution command.",

                "compile_output": "",

                "output": "",

                "time": "",

                "memory": ""
            }

        # =================================================
        # PYTHON
        # =================================================

        if language == "python":

            if not command_exists(
                sys.executable
            ):

                return {

                    "success": False,

                    "status": "Error",

                    "stdout": "",

                    "stderr":
                        "Python interpreter was not found.",

                    "compile_output": "",

                    "output": "",

                    "time": "",

                    "memory": ""
                }

            result = execute_process(

                commands,

                user_input,

                cwd=temp_dir,

                timeout=RUN_TIMEOUT
            )

            return {

                "success":
                    result["success"],

                "status":
                    "Accepted"
                    if result["success"]
                    else "Runtime Error",

                "stdout":
                    result["stdout"],

                "stderr":
                    result["stderr"],

                "compile_output": "",

                "output":
                    result["stdout"],

                "time":
                    result["time"],

                "memory": ""
            }

        # =================================================
        # JAVASCRIPT
        # =================================================

        if language == "javascript":

            if not command_exists("node"):

                return {

                    "success": False,

                    "status": "Error",

                    "stdout": "",

                    "stderr":
                        "Node.js was not found. "
                        "Install Node.js and add it to PATH.",

                    "compile_output": "",

                    "output": "",

                    "time": "",

                    "memory": ""
                }

            result = execute_process(

                commands,

                user_input,

                cwd=temp_dir,

                timeout=RUN_TIMEOUT
            )

            return {

                "success":
                    result["success"],

                "status":
                    "Accepted"
                    if result["success"]
                    else "Runtime Error",

                "stdout":
                    result["stdout"],

                "stderr":
                    result["stderr"],

                "compile_output": "",

                "output":
                    result["stdout"],

                "time":
                    result["time"],

                "memory": ""
            }

        # =================================================
        # C++
        # =================================================

        if language == "cpp":

            if not command_exists("g++"):

                return {

                    "success": False,

                    "status": "Error",

                    "stdout": "",

                    "stderr":
                        "g++ compiler was not found. "
                        "Install MinGW/GCC and add it to PATH.",

                    "compile_output": "",

                    "output": "",

                    "time": "",

                    "memory": ""
                }

            # -------------------------------------------------
            # COMPILE C++
            # -------------------------------------------------

            compile_result = execute_process(

                commands["compile"],

                cwd=temp_dir,

                timeout=COMPILE_TIMEOUT
            )

            if not compile_result["success"]:

                return {

                    "success": False,

                    "status": "Compilation Error",

                    "stdout": "",

                    "stderr":
                        compile_result["stderr"],

                    "compile_output":
                        compile_result["stderr"],

                    "output": "",

                    "time":
                        compile_result["time"],

                    "memory": ""
                }

            # -------------------------------------------------
            # RUN C++
            # -------------------------------------------------

            run_result = execute_process(

                commands["run"],

                user_input,

                cwd=temp_dir,

                timeout=RUN_TIMEOUT
            )

            return {

                "success":
                    run_result["success"],

                "status":
                    "Accepted"
                    if run_result["success"]
                    else "Runtime Error",

                "stdout":
                    run_result["stdout"],

                "stderr":
                    run_result["stderr"],

                "compile_output": "",

                "output":
                    run_result["stdout"],

                "time":
                    run_result["time"],

                "memory": ""
            }

        # =================================================
        # C
        # =================================================

        if language == "c":

            if not command_exists("gcc"):

                return {

                    "success": False,

                    "status": "Error",

                    "stdout": "",

                    "stderr":
                        "gcc compiler was not found. "
                        "Install MinGW/GCC and add it to PATH.",

                    "compile_output": "",

                    "output": "",

                    "time": "",

                    "memory": ""
                }

            # -------------------------------------------------
            # COMPILE C
            # -------------------------------------------------

            compile_result = execute_process(

                commands["compile"],

                cwd=temp_dir,

                timeout=COMPILE_TIMEOUT
            )

            if not compile_result["success"]:

                return {

                    "success": False,

                    "status": "Compilation Error",

                    "stdout": "",

                    "stderr":
                        compile_result["stderr"],

                    "compile_output":
                        compile_result["stderr"],

                    "output": "",

                    "time":
                        compile_result["time"],

                    "memory": ""
                }

            # -------------------------------------------------
            # RUN C
            # -------------------------------------------------

            run_result = execute_process(

                commands["run"],

                user_input,

                cwd=temp_dir,

                timeout=RUN_TIMEOUT
            )

            return {

                "success":
                    run_result["success"],

                "status":
                    "Accepted"
                    if run_result["success"]
                    else "Runtime Error",

                "stdout":
                    run_result["stdout"],

                "stderr":
                    run_result["stderr"],

                "compile_output": "",

                "output":
                    run_result["stdout"],

                "time":
                    run_result["time"],

                "memory": ""
            }

        # =================================================
        # JAVA
        # =================================================

        if language == "java":

            if not command_exists("javac"):

                return {

                    "success": False,

                    "status": "Error",

                    "stdout": "",

                    "stderr":
                        "javac was not found. "
                        "Install the JDK and add it to PATH.",

                    "compile_output": "",

                    "output": "",

                    "time": "",

                    "memory": ""
                }

            if not command_exists("java"):

                return {

                    "success": False,

                    "status": "Error",

                    "stdout": "",

                    "stderr":
                        "Java runtime was not found. "
                        "Install the JDK and add it to PATH.",

                    "compile_output": "",

                    "output": "",

                    "time": "",

                    "memory": ""
                }

            # -------------------------------------------------
            # COMPILE JAVA
            # -------------------------------------------------

            compile_result = execute_process(

                commands["compile"],

                cwd=temp_dir,

                timeout=COMPILE_TIMEOUT
            )

            if not compile_result["success"]:

                return {

                    "success": False,

                    "status": "Compilation Error",

                    "stdout": "",

                    "stderr":
                        compile_result["stderr"],

                    "compile_output":
                        compile_result["stderr"],

                    "output": "",

                    "time":
                        compile_result["time"],

                    "memory": ""
                }

            # -------------------------------------------------
            # RUN JAVA
            # -------------------------------------------------

            run_result = execute_process(

                commands["run"],

                user_input,

                cwd=temp_dir,

                timeout=RUN_TIMEOUT
            )

            return {

                "success":
                    run_result["success"],

                "status":
                    "Accepted"
                    if run_result["success"]
                    else "Runtime Error",

                "stdout":
                    run_result["stdout"],

                "stderr":
                    run_result["stderr"],

                "compile_output": "",

                "output":
                    run_result["stdout"],

                "time":
                    run_result["time"],

                "memory": ""
            }

        # =================================================
        # FALLBACK
        # =================================================

        return {

            "success": False,

            "status": "Error",

            "stdout": "",

            "stderr":
                "Unknown execution error.",

            "compile_output": "",

            "output": "",

            "time": "",

            "memory": ""
        }

    # =====================================================
    # GENERAL ERROR
    # =====================================================

    except Exception as error:

        return {

            "success": False,

            "status": "Error",

            "stdout": "",

            "stderr":
                str(error),

            "compile_output": "",

            "output": "",

            "time": "",

            "memory": ""
        }

    # =====================================================
    # CLEAN TEMPORARY FILES
    # =====================================================

    finally:

        try:

            shutil.rmtree(
                temp_dir,
                ignore_errors=True
            )

        except Exception:

            pass