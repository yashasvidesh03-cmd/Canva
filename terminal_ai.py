import sys
import traceback

def run_command(command):
    output = ""
    try:
        old_stdout = sys.stdout
        sys.stdout = mystdout = __import__('io').StringIO()
        exec(command, {})
        output = mystdout.getvalue()
        sys.stdout = old_stdout
    except Exception:
        output = traceback.format_exc()
    return output
      
