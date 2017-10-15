#!/usr/bin/python3

import sys
import os
import glob
import subprocess
sys.path.append(".")
sys.path.append("core")
from AtCoder import AtCoder

try:
    import AccountInformation
except ImportError:
    class AccountInformation:
        username = None
        password = None

import FormatPredictor
from multiprocessing import Pool, Process, cpu_count
from time import sleep

def prepare_procedure(argv):
    atcoder, pid, url, extension = argv
    samples = []

    # データ取得
    try:
        information, samples = atcoder.get_all(url)
    except Exception:
        print("Problem %s: failed to get the input format/samples" % pid)

    if len(samples) == 0:
        print("Problem %s: no samples" % pid)

    # 入力形式を解析
    try:
        result = FormatPredictor.format_predictor(information, samples)
        if result is None:
            raise Exception
    except Exception:
        result = None
        print("Problem %s: failed to analyze input format." % pid)


    dirname = "workspace/%s/%s" % (contestid, pid)
    os.makedirs(dirname, exist_ok=True)
    solution_name = "%s/%s." % (dirname, pid) + extension

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
        if extension == "py":
            from templates.py.py_code_generator import code_generator
        elif extension == 'cpp':
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

    print("prepared %s!" % pid)


def prepare_workspace(contestid, extension='cpp'):
    atcoder = AtCoder(AccountInformation.username, AccountInformation.password)

    while True:
        plist = atcoder.get_problem_list(contestid)
        if plist:
            break
        sleep(1.5)
        print("retrying to get task list.")

    p = Pool(processes=cpu_count())
    p.map(prepare_procedure, [(atcoder, pid, url, extension) for pid, url in plist.items()])


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        contestid = sys.argv[1]
        prepare_workspace(contestid)
    elif len(sys.argv) == 3:
        contestid = sys.argv[1]
        extension = sys.argv[2]
        prepare_workspace(contestid, extension)
    else:
        print("%s [contest_id]" % sys.argv[0])
