import os

_dir = os.path.dirname(__file__)
with open(os.path.join(_dir, 'scorm-hook.js'), 'r') as f:
    scorm_hook_js = f.read()
