pc_name = "VQA-2_"
keyword = 'SecurOS'
path = r"C:\Program Files (x86)\ISS\SecurOS\tools\SystemInfo.exe"
working_dirrectory = r"C:\Devel\test_issinfo\test\SystemInfo_"  #Как сделать так, чтобы iisinfo запускался из C:\\Program Files (x86)... я пока не понял, но это может сломать проверку в дженкинсе
# возможно, стоит запускать через системную переменную path
dump_to_copy = r"C:\Devel\dumpfortest\video_full1.dmp"
path_to_copy = r"C:\ProgramData\ISS\dumps\video_full1.dmp"
#window_title = r"C:\Devel\issinfo_exe\test"
path_to_7zip = r'C:\Program Files\7-Zip\7z.exe'
path_to_archive = r'C:\workspace\tests-issinfo\archive'
path_to_postgress_logs = r'C:\workspace\tests-issinfo\archive'
#working_dirrectory_jenkins = r"C:\Users\root\.jenkins\workspace\tests-issinfo\ISSInfo.7z"
working_dirrectory_jenkins_as_service = r"C:\Jenkins\workspace\tests-issinfo\SystemInfo_"
title = 'SystemInfo Utility'
title_window = r"C:\Jenkins\workspace\tests-issinfo"
#title_window = r"C:\Devel\test_issinfo\test"
