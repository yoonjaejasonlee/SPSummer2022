import glob
import re
import pandas as pd
import lizard
import os
import ast
import astor
import sqlalchemy.engine
import pymysql
import shutil
from git.repo.base import Repo
from datetime import datetime

pymysql.install_as_MySQLdb()

queue_size = 0
asa = 0
py_count = 0
total_count = 0
CC_avg = 0
CC_min = 0
CC_max = 0
total_lines = 0
lines = 0
total_files = 0
j = 1
paths = None


# -------------------CLASS FOR QUEUE---------------------------------------
class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, data):
        self.queue.append(data)

    def dequeue(self):
        dequeue_object = None
        if self.isEmpty():
            print("Queue is Empty\n")
        else:
            dequeue_object = self.queue[0]
            self.queue = self.queue[1:]

        return dequeue_object

    def peek(self):
        peek_object = None
        if self.isEmpty():
            print("Queue is Empty")
        else:
            peek_object = self.queue[0]

        return peek_object

    def isEmpty(self):
        is_empty = False
        if len(self.queue) == 0:
            is_empty = True
        return is_empty


# --------------------------------------------------------------------
queue = Queue()
URL = 'mysql+mysqlconnector://root:a1234567!@sparrow-ml.fasoo.com:30198/Analyzer'
engine = sqlalchemy.create_engine(URL, echo=False)


def queuing(lists):
    for s in lists:
        queue.enqueue(s)

    print("Queue Size: ", len(queue.queue))
    goes_through()
# -----------------Analyze----------------------------------


def parse_imports(text):
    temp = []
    text = text.split("\n")
    for i in text:
        if re.match(r'^.*import .+$', i):
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
                        maxes, call_cnt, param = ast_visit(item, indentlevel=indentlevel + 1, maxes=maxes,
                                                           call_cnt=call_cnt,
                                                           param=param)
                    elif isinstance(item, ast.Call):
                        maxes, call_cnt, param = ast_visit(item, indentlevel=indentlevel, maxes=maxes,
                                                           call_cnt=call_cnt + 1,
                                                           param=param)
                    else:
                        maxes, call_cnt, param = ast_visit(item, indentlevel=indentlevel, maxes=maxes,
                                                           call_cnt=call_cnt,
                                                           param=param)
        elif isinstance(value, ast.AST):
            maxes, call_cnt, param = ast_visit(value, indentlevel=indentlevel, maxes=maxes, call_cnt=call_cnt,
                                               param=param)
    return maxes, call_cnt, param


def goes_through():
    while not queue.isEmpty():
        url = queue.peek()
        queue.dequeue()
        user_name = url.rsplit('/', 2)[1]
        repo_name = url.rsplit('/', 1)[-1]

        temp_location = f"testing/{user_name}/{repo_name}/"
        Repo.clone_from(url, temp_location)
        df = calc_complexity(temp_location)
        get_average(df, url)
        shutil.rmtree(f"testing/{user_name}")


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
            try:
                parsed_file = astor.parse_file(i)
                max_indent, func_call, param = ast_visit(parsed_file)
            except:
                continue
            f = open(i, "r", encoding='ISO-8859-1', errors='ignore')
            mlb = lizard.analyze_file(i)
            p = f.read()
            dir_name = i.replace(os.getcwd(), '')
            nloc = mlb.nloc
            loc = len(p.split('\n'))
            CCN = mlb.CCN
            func_token = mlb.token_count
            parsed_file = ""
            df.update(df, overwrite=True)
            df.loc[len(df)] = [name, dir_name, 0, nloc, loc, CCN, func_token, max_indent, param, func_call]
            name_n_code[dir_name] = parse_imports(p)
            f.close()
    name_n_code = find_local_import(name_n_code, df)
    df['m_mutual_cnt'] = name_n_code.values()

    return df


def get_average(dataframe, path):
    user_name = path.rsplit('/', 2)[1]
    repo_name = path.rsplit('/', 1)[-1]
    df2 = pd.DataFrame(
        columns=["Time", "URL", "User_name", "Repo_name", "Total_File_Num", "Max_Mutual_CNT", "Avg_nloc", "Total_LOC",
                 "Avg_CCN",
                 "Max_CCN",
                 "Avg_func_token", "Max_indent","Avg_indent", "Max_func_param", "Avg_func_param", "Max_call_cnt", "Avg_call_cnt", "Process_Usage", "Process_Time"]
    )
    max_mutual = dataframe['m_mutual_cnt'].max()
    avg_nloc = dataframe['nloc'].mean()
    total_loc = dataframe['loc'].sum()
    avg_ccn = dataframe['CCN'].mean()
    max_ccn = dataframe['CCN'].max()
    max_indent = dataframe['max_indent'].max()
    avg_indent = dataframe['max_indent'].mean()
    max_param = dataframe['func_param'].max()
    avg_param = dataframe['func_param'].mean()
    avg_token = dataframe['func_token'].mean()
    max_call_cnt = dataframe['call_cnt'].max()
    avg_call_cnt = dataframe['call_cnt'].mean()
    row_num = dataframe.shape[0]
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df2.loc[len(df2)] = [timestamp, path, user_name, repo_name, row_num, max_mutual, avg_nloc, total_loc, avg_ccn,
                         max_ccn,
                         avg_token, max_indent, avg_indent, max_param, avg_param, max_call_cnt, avg_call_cnt, None, None]
    if total_loc != 0:
        df2.to_sql(name='test', con=engine, if_exists='append', index=False)
        print(f"{user_name}/{repo_name} has been added to DB...... Updated Queue Size : {len(queue.queue)} ")
    else:
        print(f"Cannot fetch any files from {user_name}/{repo_name}..... Updated Queue Size : {len(queue.queue)}")
