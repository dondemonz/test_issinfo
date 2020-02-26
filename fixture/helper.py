from datetime import timedelta
from model.input_data import *
import os
import patoolib
from subprocess import Popen, PIPE

#пока вынес просто методы, когда-нибудь, возможно, оформлю фикстуру
def set_file_name_with_datetime(m):
    m1 = m + timedelta(seconds=1)
    tm = m.strftime("%Y.%m.%d_%H.%M.%S")
    tm1 = m1.strftime("%Y.%m.%d_%H.%M.%S")
    file_name = working_dirrectory_jenkins_as_service + pc_name + tm + ".7z"
    file_name1 = working_dirrectory_jenkins_as_service + pc_name + tm1 + ".7z"
    file_name2 = working_dirrectory + pc_name + tm + ".7z"
    file_name3 = working_dirrectory + pc_name + tm1 + ".7z"
    return file_name, file_name1, file_name2, file_name3

def close_final_dialogs(app, dlg):
    new_dlg = app.top_window()
    new_dlg.OK.click()
    dlg.close()

def delete_issinfo(file_name, file_name1, file_name2, file_name3):
    if os.path.isfile(file_name):
        f = os.path.isfile(file_name)
        assert f == True
        os.remove(file_name)
    elif os.path.isfile(file_name1):
        f = os.path.isfile(file_name1)
        assert f == True
        os.remove(file_name1)
    elif os.path.isfile(file_name2):
        f = os.path.isfile(file_name2)
        assert f == True
        os.remove(file_name2)
    else:
        f = os.path.isfile(file_name3)
        assert f == True
        os.remove(file_name3)

def check_size_of_postgres_logs(file_name, file_name1, file_name2, file_name3, total_size):
    if os.path.isfile(file_name):
        for path1, dirs, files in os.walk(path_to_postgress_logs + file_name + "\PostgresLogs"):
            for f in files:
                fp = os.path.join(path1, f)
                total_size += os.path.getsize(fp)
    elif os.path.isfile(file_name1):
        for path1, dirs, files in os.walk(path_to_postgress_logs + file_name1 + "\PostgresLogs"):
            for f in files:
                fp = os.path.join(path1, f)
                total_size += os.path.getsize(fp)
    elif os.path.isfile(file_name2):
        for path1, dirs, files in os.walk(path_to_postgress_logs + file_name2 + "\PostgresLogs"):
            for f in files:
                fp = os.path.join(path1, f)
                total_size += os.path.getsize(fp)
    else:
        for path1, dirs, files in os.walk(path_to_postgress_logs + file_name3 + "\PostgresLogs"):
            for f in files:
                fp = os.path.join(path1, f)
                total_size += os.path.getsize(fp)
    return total_size


def extract_files_from_issinfo(file_name, file_name1, file_name2, file_name3):
    if os.path.isfile(file_name):
        patoolib.extract_archive(file_name, outdir=path_to_archive)
    elif os.path.isfile(file_name1):
        patoolib.extract_archive(file_name1, outdir=path_to_archive)
    elif os.path.isfile(file_name2):
        patoolib.extract_archive(file_name2, outdir=path_to_archive)
    else:
        patoolib.extract_archive(file_name3, outdir=path_to_archive)



def check_if_db_postgres_in_issinfo(file_name, file_name1, file_name2, file_name3):
    # проверка, есть ли доп. база postgres в issinfo
    if os.path.isfile(file_name):
        p = Popen(path_to_7zip + ' l ' + file_name, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate(b"input data that is passed to subprocess' stdin")
        rc = p.returncode
        # d - список всех файлов в issinfo
        d = output.decode('utf-8')
    elif os.path.isfile(file_name1):
        p = Popen(path_to_7zip + ' l ' + file_name1, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate(b"input data that is passed to subprocess' stdin")
        rc = p.returncode
        # d - список всех файлов в issinfo
        d = output.decode('utf-8')
    elif os.path.isfile(file_name2):
        p = Popen(path_to_7zip + ' l ' + file_name2, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate(b"input data that is passed to subprocess' stdin")
        rc = p.returncode
        # d - список всех файлов в issinfo
        d = output.decode('utf-8')
    else:
        p = Popen(path_to_7zip + ' l ' + file_name3, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate(b"input data that is passed to subprocess' stdin")
        rc = p.returncode
        # d - список всех файлов в issinfo
        d = output.decode('utf-8')
    return d