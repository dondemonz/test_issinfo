import pytest
import time
import os
import shutil
from pywinauto.application import Application


@pytest.fixture(scope="session", autouse=True)
def fix(request):
    os.system('taskkill /f /im securos_svc.exe')
    shutil.rmtree(r'C:\ProgramData\ISS\logs', ignore_errors=True)
    shutil.rmtree(r'C:\ProgramData\ISS\dumps', ignore_errors=True)
    time.sleep(5)

    def fin():
        print('\nSome resource fin')
        time.sleep(5)
        # так как фикстура запускает перезапуск процесса (возможно, стоит над этим подумать и как-то изменить), нужен слип, чтобы процесс запустился
        app1 = Application(backend="uia").connect(title="SecurOS Enterprise")
        time.sleep(1)
        app1.window().Edit2.set_focus()
        time.sleep(1)
        app1.window().Edit2.click_input()
        time.sleep(1)
        app1.window().Edit2.type_keys("securos")
        time.sleep(1)
        app1.window().Авторизоваться.click()

    request.addfinalizer(fin)
