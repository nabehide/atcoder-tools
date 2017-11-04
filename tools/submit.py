import sys
sys.path.append("../../..")
sys.path.append("../../../core")
from AtCoder import AtCoder

try:
    import AccountInformation
except ImportError:
    class AccountInformation:
        username = None
        password = None


def main(contestid, pid, lang, fileName):
    source = ""
    f = open(fileName, 'r')
    for line in f:
        source += line
    f.close()

    atcoder = AtCoder()
    atcoder.login(AccountInformation.username, AccountInformation.password)
    atcoder.submit_source_code(contestid, pid, lang, source)


if __name__ == '__main__':
    if len(sys.argv) == 5:
        contestid = sys.argv[1]
        pid = sys.argv[2]
        lang = sys.argv[3]
        fileName = sys.argv[4]
        main(contestid, pid, lang, fileName)
    else:
        print("%s [contestid] [pid] [lang] [fileName]" % sys.argv[0])
