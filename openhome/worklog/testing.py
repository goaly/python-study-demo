from openhome.worklog import WorkLogTool

if __name__ == '__main__':  # 为程序的主入口
    log_tool = WorkLogTool()
    excel_data = log_tool.get_excel('E:\MyDocuments\工作日志\刘勇顺_工作日志_200224~200228.xlsx')
    fmt_data = log_tool.format_data(excel_data)
