from pywinauto.application import Application
from pywinauto import keyboard
from model.input_data import *
import time
import os
from shutil import copyfile
import pytest
from subprocess import Popen, PIPE
from parse import *
import shutil
import pywinauto
import patoolib
import datetime as dt
from datetime import timedelta


def test_only_full_dumps(fix):
    # pycharm должен быть запущен от имени администратора, иначе не может запустить процесс
    m = dt.datetime.now()
    m1 = m + timedelta(seconds=1)
    tm = m.strftime("%Y.%m.%d_%H.%M.%S")
    tm1 = m1.strftime("%Y.%m.%d_%H.%M.%S")
    app = Application(backend="uia").start(path)
    file_name = working_dirrectory_jenkins_as_service+pc_name+tm+".7z"
    file_name1 = working_dirrectory_jenkins_as_service+pc_name+tm1+".7z"
    file_name2 = working_dirrectory+pc_name+tm+".7z"
    file_name3 = working_dirrectory+pc_name+tm1+".7z"
    time.sleep(10)
    app.connect(title='SystemInfo Utility')
    #app = Application().connect(title='Server Control Agent')
    dlg = app.window(title='SystemInfo Utility')
    dlg1 = dlg.child_window(auto_id="1003")
    value = dlg1.get_value()
    time.sleep(2)
    assert value == file_name or value == file_name1 or value == file_name2 or value == file_name3
    #print("connected")
    #проверка чек-боксов
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
    #изменение имени файла с нового с именем компа и датой на старое ISSInfo.7z для удобства, возможно позже надо будет сделать проверку
    #dlg5 = dlg.child_window(auto_id="1003")
    #dlg5.print_ctrl_ids
    dlg.Пуск.click()
    #dlg.child_window(auto_id="1001").click()
    #dlg5 = dlg.child_window(auto_id="TitleBar")
    time.sleep(270)
    #dlg5.wait('visible', timeout=380)
    #dlg5.child_window(auto_id="1012").click()
    new_dlg = app.top_window()
    time.sleep(1)
    new_dlg.Открытьдиректорию.click()
    time.sleep(1)
    # разные воркспейсы у дженкинса и пайчарма осложняют жизнь
    #app1 = Application().connect(title="SystemInfo Utility")
    #except pywinauto.findwindows.ElementNotFoundError:
    app = Application().connect(title=r"C:\workspace\tests-issinfo")
    window = app.window(title=r"C:\workspace\tests-issinfo")
    time.sleep(1)
    window.close()
    #new_dlg.OK.Click()
    delete_issinfo(file_name, file_name1, file_name2, file_name3)
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


def test_delete_dumps():
    m = dt.datetime.now()
    m1 = m + timedelta(seconds=1)
    tm = m.strftime("%Y.%m.%d_%H.%M.%S")
    tm1 = m1.strftime("%Y.%m.%d_%H.%M.%S")
    app = Application(backend="uia").start(path).connect(title='SystemInfo Utility')
    file_name = working_dirrectory_jenkins_as_service+pc_name+tm+".7z"
    file_name1 = working_dirrectory_jenkins_as_service+pc_name+tm1+".7z"
    file_name2 = working_dirrectory+pc_name+tm+".7z"
    file_name3 = working_dirrectory+pc_name+tm1+".7z"
    #app = Application(backend="uia").connect(title='ISSInfo')
    dlg = app.window(title='SystemInfo Utility')
    dlg2 = dlg.child_window(auto_id="1011")
    #как именно выделять чек-бокс, не разобрался. Просто кликаю, ставит\снимает.
    dlg2.click()
    copyfile(dump_to_copy, path_to_copy)
    time.sleep(5)
    dlg.Пуск.click()
    time.sleep(380)
    app = Application(backend="uia").connect(path=path)
    new_dlg = app.top_window()
    new_dlg.OK.click()
    dlg.close()
    delete_issinfo(file_name, file_name1, file_name2, file_name3)

def test_additional_databases():
    #if os.path.isfile(r'C:\workspace\tests-issinfo\ISSInfo.7z'):
    #    os.remove(r'C:\workspace\tests-issinfo\ISSInfo.7z')
    m = dt.datetime.now()
    m1 = m + timedelta(seconds=1)
    tm = m.strftime("%Y.%m.%d_%H.%M.%S")
    tm1 = m1.strftime("%Y.%m.%d_%H.%M.%S")
    app = Application(backend="uia").start(path).connect(title='SystemInfo Utility')
    file_name = working_dirrectory_jenkins_as_service+pc_name+tm+".7z"
    file_name1 = working_dirrectory_jenkins_as_service+pc_name+tm1+".7z"
    file_name2 = working_dirrectory+pc_name+tm+".7z"
    file_name3 = working_dirrectory+pc_name+tm1+".7z"
     # app = Application(backend="uia").connect(title='ISSInfo')
    dlg = app.window(title='SystemInfo Utility')
    dlg2 = dlg.child_window(auto_id="1010")
    # как именно выделять чек-бокс, не разобрался. Просто кликаю, ставит\снимает.
    dlg2.click()
    dlg.Пуск.click()
    time.sleep(320)
    new_dlg = app.top_window()
    new_dlg.OK.click()
    dlg.close()
    #pycharm запускает issinfo из одной дирректории, дженкинс из другой. Как объединить пока не знаю, пока решил просто копировать и работать по старому.
    #при запуске теста из пайчарма этот пункт зафейлится
    """
    if os.path.isfile(file_name4):
        copyfile(file_name4, working_dirrectory)
    else:
        copyfile(file_name5, working_dirrectory)
    """

    d = check_if_db_postgres_in_issinfo(file_name, file_name1, file_name2, file_name3)

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

    print("Directory size: " + str(total_size))
    assert total_size < 1000000
    time.sleep(1)
    shutil.rmtree(path_to_archive)
    delete_issinfo(file_name, file_name1, file_name2, file_name3)

#тест сделан для того, чтобы другие тесты не ломались без залогиненного клиента
def test_login_client():
    time.sleep(5)
    # так как фикстура запускает перезапуск процесса (возможно, стоит над этим подумать и как-то изменить), нужен слип, чтобы процесс запустился
    app1 = Application(backend="uia").connect(title="SecurOS Enterprise")
    time.sleep(1)
    app1.window().Edit2.set_focus()
    app1.window().Edit2.type_keys("securos")
    time.sleep(1)
    app1.window().Авторизоваться.click()
    #app1.window().print_control_identifiers()

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
    if os.path.isfile(file_name1):
        patoolib.extract_archive(file_name1, outdir=path_to_archive)
    if os.path.isfile(file_name2):
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