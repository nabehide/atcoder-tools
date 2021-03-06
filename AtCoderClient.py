#!/usr/bin/python3

from multiprocessing import Pool, cpu_count
import os
from time import sleep

from core.AtCoder import AtCoder
from core.FormatPredictor import format_predictor

try:
    import AccountInformation
except ImportError:
    class AccountInformation:
        username = None
        password = None

atcoder = None


def prepare_procedure(argv):
    pid, url, py = argv
    samples = []

    # データ取得
    try:
        information, samples = atcoder.get_all(url)
    except Exception:
        print("Problem %s: failed to get the input format/samples" % pid)

    if len(samples) == 0:
        print("Problem %s: no samples" % pid)

    # 入力形式を解析
    if py is False:
        try:
            result = format_predictor(information, samples)
            if result is None:
                raise Exception
        except Exception:
            result = None
            print("Problem %s: failed to analyze input format." % pid)

    dirname = "workspace/%s/%s" % (contestid, pid)
    os.makedirs(dirname, exist_ok=True)
    if py is True:
        solution_name = "%s/%s." % (dirname, pid) + 'py'
    else:
        solution_name = "%s/%s." % (dirname, pid) + 'cpp'

    # 既にコードが存在しているなら上書きする前にバックアップを取る
    if os.path.exists(solution_name):
        backup_id = 1
        while True:
            backup_name = "%s.%d" % (solution_name, backup_id)
            if not os.path.exists(backup_name):
                os.system('cp "%s" "%s"' % (solution_name, backup_name))
                break
            backup_id += 1

    # 自動生成済みコードを格納
    with open(solution_name, "w") as f:
        if py is True:
            try:
                from templates.py.py_code_generator import code_generator
                f.write(code_generator(information, samples))
            except UnboundLocalError:
                pass
        else:
            from templates.cpp.cpp_code_generator import code_generator
            f.write(code_generator(result))

    # サンプルを格納
    for num, (in_content, out_content) in enumerate(samples):
        casename = "%s_%d" % (pid, num + 1)
        infile = "%s/in_%s.txt" % (dirname, casename)
        outfile = "%s/out_%s.txt" % (dirname, casename)
        with open(infile, "w") as file:
            file.write(in_content)
        with open(outfile, "w") as file:
            file.write(out_content)

    # prepare scripts of test/submit
    if py is True:
        with open(dirname + "/testScript.py", "w") as f:
            from templates.py.prepare_scripts import prepare_testScript
            f.write(prepare_testScript())
        with open(dirname + "/submitScript.py", "w") as f:
            from templates.py.prepare_scripts import prepare_submitScript
            f.write(prepare_submitScript(contestid, pid, 'Python3'))

    print("prepared %s!" % pid)


def prepare_workspace(contestid, without_login, py):
    global atcoder
    atcoder = AtCoder()
    if not without_login:
        atcoder.login(AccountInformation.username, AccountInformation.password)

    while True:
        plist = atcoder.get_problem_list(contestid)
        if plist:
            break
        sleep(1.5)
        print("retrying to get task list.")

    p = Pool(processes=cpu_count())
    p.map(prepare_procedure, [(pid, url, py) for pid, url in plist.items()])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("contestid",
                        help="contest ID")
    parser.add_argument("--without-login",
                        action="store_true",
                        help="download testdata without login")
    parser.add_argument("--py",
                        action="store_true",
                        help="prepare scripts for Python")
    args = parser.parse_args()
    contestid = args.contestid
    without_login = args.without_login
    py = args.py
    prepare_workspace(args.contestid, without_login, py)
