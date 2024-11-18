import os
import subprocess
import sys
from PyQt6.QtCore import QProcess
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel, QTextEdit


def list_processes():
    subfolders = [f for f in os.listdir('process') if os.path.isdir(os.path.join('process', f))]
    return subfolders


def run_stream(process_name):
    stream_path = os.path.join('process', process_name, 'stream.py')
    try:
        # 使用 QProcess 来运行进程，以便更好地控制
        process = QProcess()
        process.start('python', [stream_path])
        return process
    except Exception as e:
        print(f"Error running {stream_path}: {e}")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 顶部文本描述
        title_label = QLabel("可选择以下流程:")
        layout.addWidget(title_label)

        self.processes = list_processes()

        # 流程列表
        self.list_widget = QListWidget()
        for folder in self.processes:
            self.list_widget.addItem(folder)
        layout.addWidget(self.list_widget)

        # 运行按钮
        run_button = QPushButton("运行所选流程")
        run_button.clicked.connect(self.run_selected_process)
        layout.addWidget(run_button)

        self.setLayout(layout)
        
    def run_selected_process(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            selected_folder = selected_items[0].text()
            process = run_stream(selected_folder)
            global current_process_window
            current_process_window = ProcessWindow(selected_folder, process)
            current_process_window.show()

    def read_process_output(self):
        # 读取进程输出并更新到界面标签
        output = self.process.readAllStandardOutput().data().decode()
        # 将新的输出添加到现有的输出文本中
        self.output_label.append(output)
        # 如果输出文本的长度超过限制，删除最旧的部分以保持在限制内
        max_length = 1000  # 这里设置输出框的最大长度，你可以根据需要调整
        if self.output_label.document().characterCount() > max_length:
            self.output_label.textCursor().deletePreviousChar()

class ProcessWindow(QWidget):
    def __init__(self, process_name, process):
        super().__init__()
        self.init_ui(process_name)
        self.process = process
        # 连接进程的 readyReadStandardOutput 信号到槽函数，以便读取输出
        self.process.readyReadStandardOutput.connect(self.read_process_output)
        # 连接进程的 finished 信号到槽函数，以便在进程结束时执行清理操作
        self.process.finished.connect(self.process_finished)

    def init_ui(self, process_name):
        layout = QVBoxLayout()

        # 顶部显示进程名字
        title_label = QLabel(process_name)
        layout.addWidget(title_label)

        self.output_label = QTextEdit()
        self.output_label.setReadOnly(True)
        layout.addWidget(self.output_label)

        # 终止任务按钮
        terminate_button = QPushButton("终止任务")
        terminate_button.clicked.connect(self.terminate_process)
        layout.addWidget(terminate_button)

        # 关闭按钮，初始不可用
        self.close_button = QPushButton("关闭")
        self.close_button.setEnabled(False)
        self.close_button.clicked.connect(self.close_window)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def read_process_output(self):
        # 读取进程输出并更新到界面标签
        output = self.process.readAllStandardOutput().data().decode()
        # 将新的输出添加到现有的输出文本中
        self.output_label.append(self.output_label.toPlainText() + output)
        # 如果输出文本的长度超过限制，删除最旧的部分以保持在限制内
        max_length = 1000  # 这里设置输出框的最大长度，你可以根据需要调整
        if len(self.output_label.toPlainText() + output) > max_length:
            self.output_label.setText(self.output_label.toPlainText()[-max_length:])

    def terminate_process(self):
        # 终止进程
        self.process.terminate()
        self.close_window()

    def process_finished(self):
        # 当进程结束时，启用关闭按钮
        self.close_button.setEnabled(True)

    def close_window(self):
        # 关闭当前窗口并回到主窗口
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    # 全局变量存储当前打开的进程窗口
    current_process_window = None

    sys.exit(app.exec())
