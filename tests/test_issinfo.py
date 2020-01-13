from pywinauto.application import Application
from model.input_data import *
import time
import os
from shutil import copyfile
import pytest
from subprocess import Popen, PIPE
from parse import *
#from pyunpack import Archive
import shutil
import pywinauto
import patoolib
import ctypes, sys


import subprocess as sp
"""
def test1():
    #sp.check_call(['DoesnotNeedAdminPrivilege.exe'])
    prog = sp.Popen(['runas', '/noprofile', r'/user:Vqa-2\root', r'C:\Program Files (x86)\ISS\SecurOS\tools\issinfo.exe'], stdin=sp.PIPE)
    prog.stdin.write(b'P0stgres')
    prog.communicate()
    #ctypes.windll.shell32.ShellExecuteW(None, "runas", "issinfo.exe", r'C:\Program Files (x86)\ISS\SecurOS\tools', None, 1)
    #ctypes.windll.shell32.ShellExecuteW(None, 'run', 'issinfo.exe', r'C:\\Program Files (x86)\\ISS\\SecurOS\\tools\\', None, 1)
    #subprocess.call(['runas', '/user:Vqa-2/root', r'C:\Program Files (x86)\ISS\SecurOS\tools\issinfo.exe'])
    time.sleep(10)
    #prog = sp.Popen(['runas', '/noprofile', '/user:root', r'C:\Program Files (x86)\ISS\SecurOS\tools\issinfo.exe'], stdin=sp.PIPE)
    #rog.stdin.write('P0stgres')
    #prog.communicate()
"""

def test_only_full_dumps(fix):
    # pycharm должен быть запущен от имени администратора, иначе не может запустить процесс
    app = Application(backend="uia").start(path)
    time.sleep(10)
    app.connect(title='ISSInfo')
    #app = Application().connect(title='Server Control Agent')
    dlg = app.window(title='ISSInfo')
    dlg1 = dlg.child_window(auto_id="1003")
    value = dlg1.get_value()
    time.sleep(2)
    assert value == working_dirrectory or value == working_dirrectory_jenkins
    #print("connected")
    dlg2 = dlg.child_window(auto_id="1009")
    value2 = dlg2.get_toggle_state()
    assert value2 == 1
    dlg3 = dlg.child_window(auto_id="1011")
    value3 = dlg3.get_toggle_state()
    assert value3 == 0
    dlg4 = dlg.child_window(auto_id="1010")
    value4 = dlg4.get_toggle_state()
    assert value4 == 0
    dlg.Пуск.click()
    #dlg.child_window(auto_id="1001").click()
    #dlg5 = dlg.child_window(auto_id="TitleBar")
    time.sleep(280)
    #dlg5.wait('visible', timeout=380)
    #dlg5.child_window(auto_id="1012").click()
    new_dlg = app.top_window()
    time.sleep(1)
    new_dlg.Открытьдиректорию.click()
    time.sleep(1)
    # разные воркспейсы у дженкинса и пайчарма осложняют жизнь
    try:
        app1 = Application().connect(title="C:\\Users\\root\\.jenkins\\workspace\\tests-issinfo")
    except pywinauto.findwindows.ElementNotFoundError:
        app1 = Application().connect(title="C:\\Devel\\test_issinfo\\tests")
        window = app1.window(title="C:\\Devel\\test_issinfo\\tests")
    else:
        window = app1.window(title="C:\\Users\\root\\.jenkins\\workspace\\tests-issinfo")

    time.sleep(1)
    window.close()
    #new_dlg.OK.Click()
    dlg.close()


def test_delete_dumps():
    app = Application(backend="uia").start(path).connect(title='ISSInfo')
    #app = Application(backend="uia").connect(title='ISSInfo')
    dlg = app.window(title='ISSInfo')
    dlg2 = dlg.child_window(auto_id="1011")
    #как именно выделять чек-бокс, не разобрался. Просто кликаю, ставит\снимает.
    dlg2.click()
    copyfile(dump_to_copy, path_to_copy)
    time.sleep(5)
    dlg.Пуск.click()
    time.sleep(430)
    app = Application(backend="uia").connect(path=path)
    new_dlg = app.top_window()
    new_dlg.OK.click()
    dlg.close()
    if os.path.isfile(path_to_copy):
        pytest.fail("File is not deleted")
    os.path.exists(path_to_copy)
    print("File is deleted")


def test_additional_databases():
    if os.path.isfile(r'C:\Users\root\.jenkins\workspace\tests-issinfo\ISSInfo.7z'):
        os.remove(r'C:\Users\root\.jenkins\workspace\tests-issinfo\ISSInfo.7z')
    app = Application(backend="uia").start(path).connect(title='ISSInfo')
    # app = Application(backend="uia").connect(title='ISSInfo')
    dlg = app.window(title='ISSInfo')
    dlg2 = dlg.child_window(auto_id="1010")
    # как именно выделять чек-бокс, не разобрался. Просто кликаю, ставит\снимает.
    dlg2.click()
    dlg.Пуск.click()
    time.sleep(350)
    new_dlg = app.top_window()
    new_dlg.OK.click()
    dlg.close()
    #pycharm запускает issinfo из одной дирректории, дженкинс из другой. Как объединить пока не знаю, пока решил просто копировать и работать по старому.
    #при запуске теста из пайчарма этот пункт зафейлится
    if os.path.isfile(r'C:\Users\root\.jenkins\workspace\tests-issinfo\ISSInfo.7z'):
        copyfile(working_dirrectory_jenkins, working_dirrectory)
    # проверка, есть ли доп. база postgres в issinfo
    p = Popen(path_to_7zip + ' l ' + working_dirrectory, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    rc = p.returncode
    # d - список всех файлов в issinfo
    d = output.decode('utf-8')
    if not "protocol.sql" in d:
        pytest.fail("protocol.sql is not in issinfo")
    else:
        print("protocol.sql is in issinfo")

def test_size_of_postgress_logs():
    if not os.path.exists(path_to_archive):
        os.makedirs(path_to_archive)
    time.sleep(2)
    patoolib.extract_archive(working_dirrectory, outdir=path_to_archive)
    #Archive(working_dirrectory).extractall(path_to_archive)
    time.sleep(15)
    total_size = 0

    for path, dirs, files in os.walk(path_to_postgress_logs):
        for f in files:
            fp = os.path.join(path, f)
            total_size += os.path.getsize(fp)
    print("Directory size: " + str(total_size))
    assert total_size < 1000000
    shutil.rmtree(path_to_archive)

#тест сделан для того, чтобы другие тесты не ломались без залогиненного клиента
def test_login_client():
    time.sleep(5)
    # так как фикстура запускает перезапуск процесса (возможно, стоит над этим подумать и как-то изменить), нужен слип, чтобы процесс запустился
    app1 = Application(backend="uia").connect(title="SecurOS Enterprise")
    time.sleep(1)
    app1.window_().Edit2.type_keys("securos")
    time.sleep(1)
    app1.window_().Авторизоваться.click()
    #app1.window().print_control_identifiers()


"""
    PROCNAME = "ServerControlAgent.exe"
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == PROCNAME:
            proc.kill()
"""