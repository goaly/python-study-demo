import re
import os
from openhome.worklog import WorkLogTool

if __name__ == '__main__':  # 为程序的主入口

    # dirpath = 'E:\MyDocuments\工作日志'
    # for root, dirs, files in os.walk(dirpath, topdown=False):
    #     for name in files:
    #         filepath = os.path.join(root, name)
    #         if os.path.exists(filepath):
    #             print(filepath)


    dirpath = 'E:\MyDocuments\工作日志'
    log_tool = WorkLogTool()
    log_tool.save_all_excel_to_db(dirpath)

    log_tool.conn.close()
