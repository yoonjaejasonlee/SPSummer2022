import glob
import re
import pandas as pd
import lizard
import os
import ast
import astor
import complexity_calc


def parse_imports(text):
    temp = []
    p = re.compile(r'^.*import.+$')
    text = text.split("\n")
    for i in text:
        if re.match(r'^.*import.+$', i):
            temp.append(i.strip().split(" ")[1].split('.')[0])
    return temp


def find_local_import(obj, df):
    for key, value in obj.items():
        count = 0
        for i in value:
            if i in df['file_name'].to_list():
                count += 1
        obj[key] = count
    return obj


indentIncreaseNodes = (ast.FunctionDef, ast.ClassDef, ast.If, ast.For, ast.While, ast.With)


def ast_visit(node, indentlevel=0, maxes=0, call_cnt=0, param=0):
    if maxes < indentlevel:
        maxes = indentlevel
    for field, value in ast.iter_fields(node):
        if isinstance(value, list):
            for item in value:
                if isinstance(item, ast.AST):
                    if isinstance(item, indentIncreaseNodes):
                        if isinstance(item, ast.FunctionDef):
                            param += len(item.args.args)
                        maxes, call_cnt, param = ast_visit(item, indentlevel=indentlevel + 1, maxes=maxes, call_cnt=call_cnt,
                                                           param=param)
                    elif isinstance(item, ast.Call):
                        maxes, call_cnt, param = ast_visit(item, indentlevel=indentlevel, maxes=maxes, call_cnt=call_cnt + 1,
                                                           param=param)
                    else:
                        maxes, call_cnt, param = ast_visit(item, indentlevel=indentlevel, maxes=maxes, call_cnt=call_cnt,
                                                           param=param)
        elif isinstance(value, ast.AST):
            maxes, call_cnt, param = ast_visit(value, indentlevel=indentlevel, maxes=maxes, call_cnt=call_cnt, param=param)
    return maxes, call_cnt, param


def calc_complexity(path):
    path = path + "**/*.py"
    files = glob.glob(path, recursive=True)
    name = ""
    code = ""
    name_n_code = {}
    df = pd.DataFrame(
        columns=["file_name", "file_dir", "m_mutual_cnt", "nloc", "loc", "CCN", "func_token", "max_indent",
                 "func_param", "call_cnt"])
    for i in files:
        code_name = i.split("\\")
        name = code_name[len(code_name) - 1]
        if name != "__init__.py":
            name = name.replace(".py", "")
            f = open(i, "r", encoding="UTF-8")
            mlb = lizard.analyze_file(i)
            p = f.read()
            dir_name = i.replace(os.getcwd(), '')
            nloc = mlb.nloc
            loc = len(p.split('\n'))
            CCN = mlb.CCN
            func_token = mlb.token_count
            max_indent, func_call, param = ast_visit(astor.parse_file(i))
            df.loc[len(df)] = [name, dir_name, 0, nloc, loc, CCN, func_token, max_indent, param, func_call]
            name_n_code[dir_name] = parse_imports(p)
            f.close()
    name_n_code = find_local_import(name_n_code, df)
    df['m_mutual_cnt'] = name_n_code.values()
    return df


if __name__ == "__main__":
    df2 = complexity_calc.calc_complexity(path=r"C:/Users/yoonj/Desktop/project-3-s22-yoonjaejasonlee-main/testing/django/")
    print(df2)

