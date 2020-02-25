from pywinauto.application import Application
from model.input_data import *
import time
import os
from shutil import copyfile
import pytest
from subprocess import Popen, PIPE
from parse import *
import shutil
import patoolib
import datetime as dt
from datetime import timedelta


def test_only_full_dumps(fix):
    # pycharm должен быть запущен от имени администратора, иначе не может запустить процесс
    m = dt.datetime.now()
    app = Application(backend="uia").start(path)
    file_name, file_name1, file_name2, file_name3 = set_file_name_with_datetime(m)
    time.sleep(10)
    app.connect(title='SystemInfo Utility')
    dlg = app.window(title='SystemInfo Utility')
    dlg1 = dlg.child_window(auto_id="1003")
    value = dlg1.get_value()
    time.sleep(2)
    assert value == file_name or value == file_name1 or value == file_name2 or value == file_name3
    #проверка чек-боксов по дефолту
    dlg2 = dlg.child_window(auto_id="1009")
    value2 = dlg2.get_toggle_state()
    assert value2 == 1
    dlg3 = dlg.child_window(auto_id="1011")
    value3 = dlg3.get_toggle_state()
    assert value3 == 0
    dlg4 = dlg.child_window(auto_id="1010")
    value4 = dlg4.get_toggle_state()
    assert value4 == 0
    time.sleep(3)
    dlg.Пуск.click()
    time.sleep(270)
    new_dlg = app.top_window()
    time.sleep(1)
    new_dlg.Открытьдиректорию.click()
    time.sleep(1)
    # воркспейс для дженкинса, в пайчареме надо заменить на devel\
    app = Application().connect(title=r"C:\workspace\tests-issinfo")
    window = app.window(title=r"C:\workspace\tests-issinfo")
    time.sleep(1)
    window.close()
    delete_issinfo(file_name, file_name1, file_name2, file_name3)
    dlg.close()


def test_delete_dumps():
    m = dt.datetime.now()
    app = Application(backend="uia").start(path).connect(title='SystemInfo Utility')
    file_name, file_name1, file_name2, file_name3 = set_file_name_with_datetime(m)
    dlg = app.window(title='SystemInfo Utility')
    dlg2 = dlg.child_window(auto_id="1011")
    #как именно выделять чек-бокс, не разобрался. Просто кликаю, ставит\снимает.
    dlg2.click()
    copyfile(dump_to_copy, path_to_copy)
    time.sleep(5)
    dlg.Пуск.click()
    time.sleep(380)
    app = Application(backend="uia").connect(path=path)
    close_final_dialogs(app, dlg)
    #внутри удаления идет проверка на существование файла, возможно стоит ее вытащить сюда, но не факт.
    delete_issinfo(file_name, file_name1, file_name2, file_name3)

def test_additional_databases():
    m = dt.datetime.now()
    app = Application(backend="uia").start(path).connect(title='SystemInfo Utility')
    file_name, file_name1, file_name2, file_name3 = set_file_name_with_datetime(m)
    dlg = app.window(title='SystemInfo Utility')
    dlg2 = dlg.child_window(auto_id="1010")
    # как именно выделять чек-бокс, не разобрался. Просто кликаю, ставит\снимает.
    dlg2.click()
    dlg.Пуск.click()
    time.sleep(340)
    close_final_dialogs(app, dlg)
    d = check_if_db_postgres_in_issinfo(file_name, file_name1, file_name2, file_name3)
    #если нет файла БД специально фейлит тест
    if not "protocol.sql" in d:
        pytest.fail("protocol.sql is not in issinfo")
    else:
        print("protocol.sql is in issinfo")
    if not os.path.exists(path_to_archive):
        os.makedirs(path_to_archive)
    time.sleep(2)
    extract_files_from_issinfo(file_name, file_name1, file_name2, file_name3)
    time.sleep(15)
    total_size = 0
    total_size = check_size_of_postgres_logs(file_name, file_name1, file_name2, file_name3, total_size)
    #print("Directory size: " + str(total_size))
    assert total_size < 1000000
    time.sleep(1)
    shutil.rmtree(path_to_archive)
    delete_issinfo(file_name, file_name1, file_name2, file_name3)

"""
#тест сделан для того, чтобы другие тесты не ломались без залогиненного клиента
def test_login_client():
    time.sleep(5)
    # так как фикстура запускает перезапуск процесса (возможно, стоит над этим подумать и как-то изменить), нужен слип, чтобы процесс запустился
    app1 = Application(backend="uia").connect(title="SecurOS Enterprise")
    time.sleep(1)
    app1.window().Edit2.click_input()
    time.sleep(1)
    app1.window().Edit2.type_keys("securos")
    time.sleep(1)
    app1.window().Авторизоваться.click()
"""
def close_final_dialogs(app, dlg):
    new_dlg = app.top_window()
    new_dlg.OK.click()
    dlg.close()

def set_file_name_with_datetime(m):
    m1 = m + timedelta(seconds=1)
    tm = m.strftime("%Y.%m.%d_%H.%M.%S")
    tm1 = m1.strftime("%Y.%m.%d_%H.%M.%S")
    file_name = working_dirrectory_jenkins_as_service + pc_name + tm + ".7z"
    file_name1 = working_dirrectory_jenkins_as_service + pc_name + tm1 + ".7z"
    file_name2 = working_dirrectory + pc_name + tm + ".7z"
    file_name3 = working_dirrectory + pc_name + tm1 + ".7z"
    return file_name, file_name1, file_name2, file_name3

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





"""
    PROCNAME = "ServerControlAgent.exe"
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == PROCNAME:
            proc.kill()
"""
"""
    #pycharm запускает issinfo из одной дирректории, дженкинс из другой. Как объединить пока не знаю, пока решил просто копировать и работать по старому.
    ненужный кусок, который был закомментирован в тесте про дополнительные базы, скорее всего надо удалить.
    if os.path.isfile(file_name):
        copyfile(file_name, working_dirrectory)
    if os.path.isfile(file_name1):
        copyfile(file_name1, working_dirrectory)
    if os.path.isfile(file_name2):
        copyfile(file_name2, working_dirrectory)
    else:
        copyfile(file_name3, working_dirrectory)
"""
"""
    #except pywinauto.findwindows.ElementNotFoundError:
"""

"""
пример удаления файлов 
    if os.path.isfile(r'C:\workspace\tests-issinfo\ISSInfo.7z'):
        os.remove(r'C:\workspace\tests-issinfo\ISSInfo.7z')
"""
"""
    #app1.window().print_control_identifiers()
"""