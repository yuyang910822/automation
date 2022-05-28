import openpyxl
from openpyxl.worksheet.worksheet import Worksheet


class ExcelClass:

    def __init__(self, filePath: str, sheetName: str):
        """
        创建excel对象
        :param filePath: 文件完整路径
        :param sheetName: sheet名称
        """
        self.workbook = openpyxl.load_workbook(filePath)
        self.sheetName = sheetName

    def close(self):
        """关闭工作薄对象，释放内存"""
        self.workbook.close()

    def readDada(self) -> list:
        """
        读取数据生成测试数据
        :return:
        """
        worksheet: Worksheet = self.workbook[self.sheetName].values
        data = []
        for i in list(worksheet)[1:]:
            if None not in i[0:1]:
                data.append(dict(zip(worksheet[0], i)))
        return data


if __name__ == '__main__':
    e = ExcelClass(r'C:\Users\yuyang\Desktop\1.xlsx', 'She')
    e.readDada()
