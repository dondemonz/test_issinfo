from pywinauto.application import Application
from fixture.helper import *
import time
import os
from shutil import copyfile
import pytest
from parse import *
import shutil
import datetime as dt


def test_only_full_dumps(fix):
    # pycharm должен быть запущен от имени администратора, иначе не может запустить процесс
    m = dt.datetime.now()
    app = Application(backend="uia").start(path)
    file_name, file_name1, file_name2, file_name3 = set_file_name_with_datetime(m)
    time.sleep(2)
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
    time.sleep(290)
    new_dlg = app.top_window()
    time.sleep(1)
    new_dlg.Открытьдиректорию.click()
    time.sleep(1)
    # воркспейс для дженкинса, в пайчареме надо заменить на devel\
    app = Application().connect(title=r"C:\workspace\tests-issinfo")
    window = app.window(title=r"C:\workspace\tests-issinfo")
    #app = Application().connect(title=r"C:\Devel\test_issinfo\test")
    #window = app.window(title=r"C:\Devel\test_issinfo\test")
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
    time.sleep(390)
    app = Application(backend="uia").connect(path=path)
    close_final_dialogs(app, dlg)
    #внутри удаления идет проверка на существование файла, возможно стоит ее вытащить сюда, но не факт.
    delete_issinfo(file_name, file_name1, file_name2, file_name3)

def test_additional_databases(fix):
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
    time.sleep(1)



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