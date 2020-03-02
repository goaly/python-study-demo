import re
import os
from openhome.worklog import WorkLogTool

if __name__ == '__main__':  # 为程序的主入口

    dirpath = 'E:\MyDocuments\工作日志'

    log_tool = WorkLogTool()
    log_tool.save_all_excel_to_db(dirpath)

    log_tool.conn.close()
