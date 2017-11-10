import os

from core.TemplateEngine import render


mydir = os.path.dirname(__file__)


def prepare_submitScript(contestid, pid, lang):
    with open("{dir}/template_submitScript.py".format(dir=mydir), "r") as f:
        template = f.read()

    code = render(template,
                  contestid=contestid,
                  pid=pid,
                  lang=lang,
                  fileName=pid + '.py')

    return code


def prepare_testScript():
    with open("{dir}/template_testScript.py".format(dir=mydir), "r") as f:
        code = f.read()
    return code
