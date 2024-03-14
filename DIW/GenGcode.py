import pandas as pd

class GcodeGenerator:
    def __init__(self, data_name, pressure, print_speed, layerz, layern, firstz, broken_wire_h, advanced_on, advanced_off):
        self.data_name = data_name
        self.pressure = pressure
        self.print_speed = print_speed
        self.layerz = layerz
        self.layern = layern
        self.df = pd.read_csv(r"E:\JupyterNotebook\DIW\CSV\%s.csv" % self.data_name)
        self.firstz = firstz
        self.broken_wire_h = broken_wire_h
        self.advanced_on = advanced_on
        self.advanced_off = advanced_off

    def gen_gcode_file(self):
        code = f"G1 X0.0 Y0.0 Z50 F10\nM100\nM99 D{self.layern} L1\nM108 I{self.pressure}\nM102 H{self.broken_wire_h}\nM171 T{self.advanced_on}\nM172 L{self.advanced_off}\nM175 P0 A1 N4\n(<fill>)\n"
        for j in range(1, self.layern+1):
            if j == 1:
                self.df['起点 Z'] = self.firstz
                self.df['端点 Z'] = self.firstz
            else:
                self.df['起点 Z'] = round(self.df['起点 Z'] + self.layerz, 3)
                self.df['端点 Z'] = round(self.df['端点 Z'] + self.layerz, 3)
            for i in range(0, self.df.shape[0]):
                code += f"M103\nG91\nG1 Z{self.broken_wire_h}\nG90\n"
                code += "G1 X" + str(self.df.loc[i, '起点 X']) + ' '
                code += "Y" + str(self.df.loc[i, '起点 Y']) + ' '
                code += "Z" + str(self.df.loc[i, '起点 Z']) + ' '
                code += "F" + str(self.print_speed) + '\n'
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
            f = open(path, 'w', encoding='utf-8')
            f.write(code)
            print('Gcode file 搞定！！！')
        except Exception as ex:
            print("writeSlcFile exception:", ex)
        finally:
            if f:
                f.close()
                
    def __str__(self):
        return self.gen_gcode_file()
