
import sys
from os.path import abspath
from os.path import dirname
import app
import _thread
from tool import check_due_thread


sys.path.insert(0, abspath(dirname(__file__)))
thread = _thread.start_new_thread(check_due_thread, ())
application = app.app
