import os

from core.TemplateEngine import render


mydir = os.path.dirname(__file__)


def formatInfo(info, ignore):
    """ Add variables into "info" if the variable is not in "ignore".
        When a variable is added into "info", it's also added  into "ignore"
        to avoid duplication.
    """
    lst = info.split(' ')
    for i, l in enumerate(lst):
        idx = l.find('_')
        if idx != -1:
            lst[i] = lst[i][:idx]
    lst = [i for i in lst if i not in ignore]
    ignore += lst
    return lst, ignore


def generate_input_part(information, samples):
    input_part_lines = ""
    ignore = ['...', ':']
    splittedInfo = information.split('\n')[:-1]
    splittedSamples = samples[0][0].split('\n')[:-1]

    for idx, (info, sample) in enumerate(zip(splittedInfo, splittedSamples)):
        formattedInfo = info.split(' ')
        formattedSample = sample.split(' ')
        isInt = formattedSample[0].isdigit()

        line = ""
        if 1 == len(formattedInfo) and formattedInfo[0] not in ignore:
            """ In case one variable is in one line.
                e.g.
                  A
            """
            line += formattedInfo[0] + " = "
            line += "int(input())\n" if isInt else "list(input())\n"
        else:
            formattedInfo, ignore = formatInfo(info, ignore)
            if len(formattedInfo) == 0:
                """ In case no variable is in one line (e.g. ":")
                    or the variables have already be processed.
                """
                pass
            elif formattedInfo == [formattedInfo[0]] * len(formattedInfo):
                """ In case 1 or 2 dimensional variable is in one line.
                    e.g.
                      A_1, ..., A_N
                        or
                      A_11, ..., A_1N
                      :
                      A_M1, ..., A_MN
                """
                if (idx != len(splittedInfo) - 1) and \
                        splittedInfo[idx + 1][0] == ':':
                    """ In case 2 dimensional variable is in several lines.
                        e.g.
                          A_11, ..., A_1N
                          :
                          A_M1, ..., A_MN
                    """
                    if isInt:
                        line += formattedInfo[0] + \
                            " = [list(map(int, input().split())) " + \
                            "for i in range(" + 'N' + ")]\n"
                    else:
                        line += formattedInfo[0] + " = [list(input()) " + \
                            "for i in range(" + 'N' + ")]\n"
                else:
                    """ In case 1 dimensional variable is in one line.
                        e.g.
                          A_1, ..., A_N
                    """
                    if isInt:
                        line += formattedInfo[0] + \
                            " = list(map(int, input().split()))\n"
                    else:
                        line += formattedInfo[0] + " = list(input())\n"
            elif (idx != len(splittedInfo) - 1) and \
                    splittedInfo[idx + 1][0] == ':':
                """ In case 1 dimensional variables are in several lines.
                    e.g.
                      A_1, B_1, ...
                      :
                      A_N, B_N, ...
                """
                for i in formattedInfo:
                    line += i + " = []\n"
                line += "for i in range(" + 'N' + "):\n"
                line += "    "
                for i in range(len(formattedInfo)):
                    line += "temp" + str(i)
                    if i != len(formattedInfo) - 1:
                        line += ", "
                if isInt:
                    line += " = list(map(int, input().split()))\n"
                else:
                    line += " = list(input())\n"
                for i, f in enumerate(formattedInfo):
                    line += "    "
                    line += f + ".append(temp" + str(i) + ")\n"
            else:
                """ In case several numbers are in one line.
                    e.g.
                      A, B, ...
                """
                for i, info in enumerate(formattedInfo):
                    line += info
                    if i != len(formattedInfo) - 1:
                        line += ", "
                line += " = list(map(int, input().split()))\n"

        input_part_lines += line

    return input_part_lines


def code_generator(information=None, samples=None):
    with open("{dir}/template_success.py".format(dir=mydir), "r") as f:
        template_success = f.read()
    with open("{dir}/template_failure.py".format(dir=mydir), "r") as f:
        template_failure = f.read()

    if information is not None:
        input_part_lines = generate_input_part(information, samples)
        code = render(template_success,
                      input_part=input_part_lines)
    else:
        code = render(template_failure)
    return code
