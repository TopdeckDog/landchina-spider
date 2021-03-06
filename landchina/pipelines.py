# coding: utf-8

import os
import re

import xlwt

XLS_FILE_DIR = 'results'


class SaveExcelPipeline(object):

    def __init__(self):
        # {filename: index in handlers}
        self.file_mapper = {}
        self.handlers = []

    def gc_old_xls(self):
        free_list = []
        if len(self.file_mapper) > 10:
            for filename, index in self.file_mapper.iteritems():
                i = index - 1
                if i < 0:
                    del self.handlers[index]
                    free_list.append(filename)
                else:
                    self.file_mapper[filename] = i

        for i in free_list:
            self.file_mapper.pop(i)

    def save_to_file(self, filename, item):
        if filename not in self.file_mapper:
            self.init_new_excel(filename)
            self.gc_old_xls()

        self.text_to_excel(filename, item)

    def init_new_excel(self, filename):
        xls = xlwt.Workbook()
        sheet = xls.add_sheet('sheet1', cell_overwrite_ok=True)
        sheet.write(0, 0, u'所在地')
        sheet.write(0, 1, u'所在地区划码')
        sheet.write(0, 2, u'上级所在地')
        sheet.write(0, 3, u'上级区划码')
        sheet.write(0, 4, u'行政区')
        sheet.write(0, 5, u'项目名称')
        sheet.write(0, 6, u'项目位置')
        sheet.write(0, 7, u'面积(公顷)')
        sheet.write(0, 8, u'土地来源')
        sheet.write(0, 9, u'土地用途')
        sheet.write(0, 10, u'供地方式')
        sheet.write(0, 11, u'土地使用年限')
        sheet.write(0, 12, u'行业分类')
        sheet.write(0, 13, u'土地级别')
        sheet.write(0, 14, u'成交价格(万元)')
        sheet.write(0, 15, u'土地使用权人')
        sheet.write(0, 16, u'下限')
        sheet.write(0, 17, u'上限')
        sheet.write(0, 18, u'约定交地时间')
        sheet.write(0, 19, u'约定开工时间')
        sheet.write(0, 20, u'约定竣工时间')
        sheet.write(0, 21, u'合同签订日期')
        xls.save(os.path.join(XLS_FILE_DIR, filename + '.xls'))
        self.handlers.append(xls)
        self.file_mapper[filename] = len(self.handlers) - 1

    def process_item(self, item, spider):
        date = item['qy_time']
        r = re.compile(u'[0-9]\d*年[0-9]\d*月')
        date = re.search(r, date).group(0)
        filename = '-'.join([spider.prvn.name, date])
        self.save_to_file(filename, item)
        return item

    def text_to_excel(self, filename, item):
        index = self.file_mapper[filename]
        xls = self.handlers[index]
        sheet = xls.get_sheet('sheet1')
        row = sheet.last_used_row + 1
        sheet.write(row, 0, item['where'])
        sheet.write(row, 1, item['where_code'])
        sheet.write(row, 2, item['parent_where'])
        sheet.write(row, 3, item['parent_code'])
        sheet.write(row, 4, item['domain'])
        sheet.write(row, 5, item['name'])
        sheet.write(row, 6, item['addr'])
        sheet.write(row, 7, item['size'])
        sheet.write(row, 8, item['src'])
        sheet.write(row, 9, item['use'])
        sheet.write(row, 10, item['method'])
        sheet.write(row, 11, item['util'])
        sheet.write(row, 12, item['catalog'])
        sheet.write(row, 13, item['lv'])
        sheet.write(row, 14, item['price'])
        sheet.write(row, 15, item['user'])
        sheet.write(row, 16, item['cap_b'])
        sheet.write(row, 17, item['cap_h'])
        sheet.write(row, 18, item['jd_time'])
        sheet.write(row, 19, item['kg_time'])
        sheet.write(row, 20, item['jg_time'])
        sheet.write(row, 21, item['qy_time'])
        xls.save(os.path.join(XLS_FILE_DIR, filename + '.xls'))
