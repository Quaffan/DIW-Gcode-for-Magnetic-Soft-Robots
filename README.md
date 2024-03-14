# DIW-Gcode-for-Magnetic-Soft-Robots
DIW: direct ink writing 直写式3D打印

磁性软体机器人在设计的过程中，需要对磁编程单元进行定向的有规律的打印

本代码旨在帮助实验人员设计并生成打印路径代码（Gcode）

使用方式：
* 使用前需要确保Python的版本不低于3.6
* 需要确认已安装第三方库，诸如pyclipper、vtk、pandas，安装方式（pip install _library_name_） 
* 启动Start文件，利用path绘制封闭的磁编程单元
* 设置扫描平行线的各项参数，导出扫描线段的数据
* 设置打印的各项参数，导出能够被DIW打印机识别的Gcode
