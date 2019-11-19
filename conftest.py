import pytest
import time
import os
import shutil


@pytest.fixture(scope="session")
def fix(request):
    os.system('taskkill /f /im securos_svc.exe')
    shutil.rmtree(r'C:\ProgramData\ISS\logs', ignore_errors=True)
    time.sleep(5)

    def fin():
        print('\nSome resource fin')

    request.addfinalizer(fin)
