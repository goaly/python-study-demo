import datetime
import re
import uuid

import xlrd
import pymysql

conn = pymysql.connect(host='localhost', user='root', passwd='Al4g56', db='dailylog', port=3306, charset='utf8')


def list_dic(list1, list2):
    '''
    two lists merge a dict,a list as key,other list as value
    :param list1:key
    :param list2:value
    :return:dict
    '''
    dic = dict(map(lambda x, y: [x, y], list1, list2))
    return dic


def merge_cell(sheet_info):
    '''
    #横向合并单元格和垂直合并单元格的处理, 对于合并的单元格，xlrd只有第一个格子有值，此方法把第一个格子中的值复制到合并单元格所有的行列范围
    :param rlow:row, include row exclusive of row_range
    :param rhigh:row_range
    :param clow:col, include col exclusive of col_range
    :param chigh:col_range
    :param sheet_info:object of sheet
    :return:用行列元组当作key存储单元格值的字典
    '''
    merge = {}
    merge_cells = sheet_info.merged_cells
    for (rlow, rhigh, clow, chigh) in merge_cells:
        value_mg_cell = sheet_info.cell_value(rlow, clow)
        if rhigh - rlow == 1:
            # Merge transverse cells横向合并单元格
            for n in range(chigh - clow - 1):
                merge[(rlow, clow + n + 1)] = value_mg_cell
        elif chigh - clow == 1:
            # Merge Vertical Cells垂直合并单元格
            for n in range(rhigh - rlow - 1):
                merge[(rlow + n + 1, clow)] = value_mg_cell
    return merge


# 工作日志工具
class WorkLogTool:

    def get_excel(self, filepath):
        apply_dic = []
        if filepath:
            filename = filepath.split('\\')[-1]
            handler = filename.split('_')[0]
            workbook = xlrd.open_workbook(filepath)
            sheet_info = workbook.sheet_by_index(0)
            # first_line = sheet_info.row_values(0)  # 获取首行，这里的首行是表头，用表头作为字典的key，每一行数据对应表头的value，每一行组成一个字典
            first_line = ['workDate', 'workWeek', 'tasksToday', 'taskNo', 'hours', 'progress', 'nextDayArrange', 'handler', 'filename']

            values_merge_cell = merge_cell(sheet_info)  # 调用处理合并单元格的函数
            for i in range(1, sheet_info.nrows):  # 遍历表格行数据，从第二行开始
                other_line = sheet_info.row_values(i)
                for key in values_merge_cell.keys():
                    if key[0] == i:
                        other_line[key[1]] = values_merge_cell[key]
                # print(other_line)
                dic = list_dic(first_line, other_line)  # 调用组合字典的函数，传入key和value，字典生成
                dic['handler'] = handler
                dic['filename'] = filename
                apply_dic.append(dic)
        return apply_dic

    def format_data(self, excel_data):
        fmt_data = []
        for row_data in excel_data:
            if row_data['tasksToday'].strip() != '':
                work_date = str(row_data['workDate']).strip()
                if work_date != '':
                    endIdx = work_date.find('.')
                    endIdx = (endIdx if (endIdx > -1) else len(work_date))
                    work_date = work_date[0:endIdx]
                    if re.fullmatch('\d{8}', work_date) is None:
                        raise ValueError('日期必须是8位数字')
                    row_data['workDate'] = work_date[0:4] + '-' + work_date[4:6] + '-' + work_date[6:8]
                print(row_data)
                fmt_data.append(row_data)
        return fmt_data

    def save_to_db(self, log_datas):
        if len(log_datas) > 0:
            cursor = conn.cursor()
            cur_userid = 1
            curtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for log_data in log_datas:
                uid = str(uuid.uuid4())
                suid = ''.join(uid.split('-'))
                cursor.execute(
                    "INSERT INTO worklog(createdBy, createdOn, modifiedBy, modifiedOn, workDate, workWeek, tasksToday, "
                    + "taskNo, hours, progress, nextDayArrange, handler, fileName, uuid) "
                    + "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    # 数据元组
                    (cur_userid, curtime, cur_userid, curtime, log_data['workDate'], log_data['workWeek'],
                     log_data['tasksToday'], log_data['taskNo'], log_data['hours'], log_data['progress'],
                     log_data['nextDayArrange'], log_data['handler'], log_data['filename'], suid))
            conn.commit()
