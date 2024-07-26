"""
# 保存名称
name = '样品5'
# 数据名称
data_name = "样条"

# 设定气压，单位 MPa
pressure = 0.15

# 打印速度，单位 mm/s
print_speed = 13

# 设置层高， 单位 mm
layerz = 0.3

# 设置层数
layern = 3

# 设置第一层层高，单位 mm
firstz = 0.1650

# 设置断丝抬高，单位 mm
broken_wire_h = 10

# 设置提前出丝时间，单位 ms
advanced_on = 100

# 设置提前关丝距离，单位 mm
advanced_off = 0.3

generator = GcodeGenerator(data_name, pressure, print_speed, layerz, layern, firstz, broken_wire_h, advanced_on, advanced_off)
generator.write_gcode_file("E:\\JupyterNotebook\\DIW\\Gcode\\%s.txt" % name)
print(generator)
"""


import pandas as pd

class GcodeGenerator:
    def __init__(self, data_name, pressure, print_speed, layerz, layern, firstz, broken_wire_h, advanced_on, advanced_off):
        self.data_name = data_name
        self.pressure = pressure
        self.print_speed = print_speed
        self.layerz = layerz
        self.layern = layern
        self.df = pd.read_csv(r"E:\JupyterNotebook\DIW\CSV\%s.csv" % self.data_name, encoding='ANSI')
        self.firstz = firstz
        self.broken_wire_h = broken_wire_h
        self.advanced_on = advanced_on
        self.advanced_off = advanced_off

    def gen_gcode_file(self):
        code = f"G1 X0.0 Y0.0 Z50 F10\nM100\nM99 D{self.layern} L1\nM108 I{self.pressure}\nM102 H{self.broken_wire_h}\nM171 T{self.advanced_on}\nM172 L{self.advanced_off}\n(<fill>)\n"
        for j in range(1, self.layern+1):
            if j == 1:
                self.df['起点 Z'] = self.firstz
                self.df['端点 Z'] = self.firstz
            else:
                self.df['起点 Z'] = round(self.df['起点 Z'] + self.layerz, 3)
                self.df['端点 Z'] = round(self.df['端点 Z'] + self.layerz, 3)
            for i in range(0, self.df.shape[0]):
                code += f"M103\nG1 Z{self.broken_wire_h}\n"
                code += "G1 X" + str(self.df.loc[i, '起点 X']) + ' '
                code += "Y" + str(self.df.loc[i, '起点 Y']) + ' '
                code += f"Z{self.broken_wire_h}" + ' '
                code += "F16" + '\n'
                code += "G1 Z" + str(self.df.loc[i, '起点 Z']) + ' '
                code += "F16" + '\n'
                code += "M101\n"
                code += "G1 X" + str(self.df.loc[i, '端点 X']) + ' '
                code += "Y" + str(self.df.loc[i, '端点 Y']) + ' '
                code += "Z" + str(self.df.loc[i, '端点 Z']) + ' '
                code += "F" + str(self.print_speed) + '\n'
            code += f"\n;第{j}层打印完毕\n\n"
        code += "M103\n"
        code += "(</fill>)\nG28\nM02"
        return code

    def write_gcode_file(self, path):
        f = None
        try:
            code = self.gen_gcode_file()
            f = open(path, 'w', encoding='ANSI')
            f.write(code)
            print('Gcode file 搞定！！！')
        except Exception as ex:
            print("writeSlcFile exception:", ex)
        finally:
            if f:
                f.close()
                
    def __str__(self):
        return self.gen_gcode_file()
