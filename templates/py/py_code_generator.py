import os

from core.TemplateEngine import render


mydir = os.path.dirname(__file__)


def formatInformation(information):
    return information.split('\n')[:-1]


def formatSamples(samples):
    # lst = []
    # for s in samples:
    #     lst.append(s[0].split('\n'))
    # return lst
    return samples[0][0].split('\n')[:-1]


def formatInfo(info, ignore):
    lst = info.split(' ')
    for i, l in enumerate(lst):
        idx = l.find('_')
        if idx != -1:
            lst[i] = lst[i][:idx]
    lst = [i for i in lst if i not in ignore]
    ignore += lst
    return lst, ignore


def code_generator(information=None, samples=None):
    with open("{dir}/template_success.cpp".format(dir=mydir), "r") as f:
        template_success = f.read()
    with open("{dir}/template_failure.cpp".format(dir=mydir), "r") as f:
        template_failure = f.read()

    ignore = ['...', ':']

    if information is not None:

        information = formatInformation(information)
        samples = formatSamples(samples)

        input_part_lines = ""
        for idx, (info, sample) in enumerate(zip(information, samples)):
            formattedInfo = info.split(' ')
            formattedSample = sample.split(' ')
            isVariableInt = formattedSample[0].isdigit()

            # if len(formattedInfo) == len(formattedSample):
            line = ""
            if 1 == len(formattedInfo) and formattedInfo[0] not in ignore:
                line += formattedInfo[0] + " = "
                line += "int(input())\n" if isVariableInt else "list(input())\n"
            else:
                formattedInfo, ignore = formatInfo(info, ignore)
                if len(formattedInfo) == 0:
                    pass
                elif formattedInfo == [formattedInfo[0]] * len(formattedInfo):
                    if (idx != len(information) - 1) and information[idx + 1][0] == ':':
                        if isVariableInt:
                            line += formattedInfo[0] + " = [list(map(int, input().split())) for i in range(" + 'N' + ")]\n"
                        else:
                            line += formattedInfo[0] + " = [list(input()) for i in range(" + 'N' + ")]\n"
                    else:
                        if isVariableInt:
                            line += formattedInfo[0] + " = list(map(int, input().split()))\n"
                        else:
                            line += formattedInfo[0] + " = list(input())\n"
                elif (idx != len(information) - 1) and information[idx + 1][0] == ':':
                    for i in formattedInfo:
                        line += i + " = []\n"
                    line += "for i in range(" + 'N' + "):\n"
                    for i in range(len(formattedInfo)):
                        line += "temp" + str(i)
                        if i != len(formattedInfo) - 1:
                            line += ", "
                    if isVariableInt:
                        line += " = list(map(int, input().split()))\n"
                    else:
                        line += " = list(input())\n"
                    for i, f in enumerate(formattedInfo):
                        line += "    "
                        line += f + ".append(temp" + str(i) + ")\n"
                else:
                    for i, info in enumerate(formattedInfo):
                        line += info
                        if i != len(formattedInfo) - 1:
                            line += ", "
                    line += " = list(map(int, input().split()))\n"

            input_part_lines += line
            ignore.append('')

        code = render(template_success,
                      input_part=input_part_lines)
    else:
        code = template_failure
    return code
