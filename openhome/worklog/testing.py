import re
from openhome.worklog import WorkLogTool

if __name__ == '__main__':  # 为程序的主入口

    filepath = 'E:\MyDocuments\工作日志\刘勇顺_工作日志_200224~200228.xlsx'
    log_tool = WorkLogTool()

    filename = log_tool.get_filename(filepath)
    excel_data = log_tool.get_excel(filepath)
    fmt_data = log_tool.format_data(excel_data)
    log_tool.clear_old_record(filename)
    log_tool.save_to_db(fmt_data)

    log_tool.conn.close()
