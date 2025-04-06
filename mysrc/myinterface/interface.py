import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QSizePolicy, QFrame, QMessageBox
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer
import json
from apirequest import api_request

class ImageViewerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置应用图标
        self.setup_app_icon()
        # 参数设置
        self.window_width = 800  # 窗口宽度
        self.window_height = 700  # 窗口高度
        self.left_panel_ratio = 0.3  # 左侧区域宽度比例
        self.button_height = 40  # 按钮高度
        self.button_width = 120  # 按钮宽度
        self.label_font_size = 14  # 标签字体大小
        self.result_font_size = 18  # 识别结果字体大小
        self.line_width = 1  # 分隔线宽度
        self.line_style = "solid"  # 分隔线样式（solid 或 dashed）
        self.line_color = "#e0e0e0"  # 分隔线颜色
        self.image_files = []  # 存储图片文件路径
        self.current_image_index = 0  # 当前显示的图片索引
        self.timer = QTimer()  # 定时器用于轮播图片
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle("营业执照识别")
        self.setGeometry(100, 100, self.window_width, self.window_height)

        # 主窗口布局
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        # 全局颜色
        self.setStyleSheet("""
                    QWidget {
                        background-color: #f0f8ff;  /* 淡蓝色背景 */
                        color: #333333;  /* 深灰色文字 */
                        font-size: 14px;
                    }
                    QPushButton {
                        background-color: #87ceeb;  /* 浅蓝色按钮 */
                        border: 1px solid #4682b4;  /* 深蓝色边框 */
                        border-radius: 5px;  /* 圆角 */
                        padding: 5px;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #add8e6;  /* 悬停时更浅的蓝色 */
                    }
                    QLabel {
                        color: #333333;  /* 深灰色文字 */
                    }
                    QFrame {
                        border: 1px solid #4682b4;  /* 深蓝色边框 */
                    }
                """)
        # 左侧布局（控制区域）
        self.left_widget = QWidget()
        self.left_layout = QVBoxLayout()
        self.left_widget.setLayout(self.left_layout)
        self.left_widget.setMaximumWidth(int(self.window_width * self.left_panel_ratio))

        # 设置左侧背景颜色和样式
        self.left_widget.setStyleSheet("""
                    QWidget {
                        background-color: #e6f7ff;  /* 更浅的蓝色背景 */
                        border-right: 1px solid #4682b4;  /* 深蓝色右侧边框 */
                    }
        """)

        # 添加一个占位符，使按钮居中
        self.left_layout.addStretch()

        # 添加选择图片按钮
        self.select_button = QPushButton("选择图片")
        self.select_button.setFixedSize(self.button_width, self.button_height)
        self.select_button.clicked.connect(self.select_image)
        # self.select_button.setStyleSheet("""
        #     QPushButton {
        #         background-color: #ffffff;  /* 白色背景 */
        #         border: 1px solid #e0e0e0;  /* 边框 */
        #         border-radius: 5px;  /* 圆角 */
        #         padding: 5px;
        #         font-size: 14px;
        #     }
        #     QPushButton:hover {
        #         background-color: #f0f0f0;  /* 悬停效果 */
        #     }
        # """)
        self.left_layout.addWidget(self.select_button, alignment=Qt.AlignCenter)

        # 添加选择文件夹按钮
        self.select_folder_button = QPushButton("选择文件夹")
        self.select_folder_button.setFixedSize(self.button_width, self.button_height)
        self.select_folder_button.clicked.connect(self.select_folder)
        # self.select_folder_button.setStyleSheet("""
        #     QPushButton {
        #         background-color: #ffffff;
        #         border: 1px solid #e0e0e0;
        #         border-radius: 5px;
        #         padding: 5px;
        #         font-size: 14px;
        #     }
        #     QPushButton:hover {
        #         background-color: #f0f0f0;
        #     }
        # """)
        self.left_layout.addWidget(self.select_folder_button, alignment=Qt.AlignCenter)

        # 添加去除图片按钮
        self.remove_button = QPushButton("去除图片")
        self.remove_button.setFixedSize(self.button_width, self.button_height)
        self.remove_button.clicked.connect(self.remove_image)
        # self.remove_button.setStyleSheet("""
        #     QPushButton {
        #         background-color: #ffffff;
        #         border: 1px solid #e0e0e0;
        #         border-radius: 5px;
        #         padding: 5px;
        #         font-size: 14px;
        #     }
        #     QPushButton:hover {
        #         background-color: #f0f0f0;
        #     }
        # """)
        self.left_layout.addWidget(self.remove_button, alignment=Qt.AlignCenter)

        # 添加开始识别按钮
        self.start_recognition_button = QPushButton("开始识别")
        self.start_recognition_button.setFixedSize(self.button_width, self.button_height)
        self.start_recognition_button.clicked.connect(self.start_recognition)
        # self.start_recognition_button.setStyleSheet("""
        #     QPushButton {
        #         background-color: #ffffff;
        #         border: 1px solid #e0e0e0;
        #         border-radius: 5px;
        #         padding: 5px;
        #         font-size: 14px;
        #     }
        #     QPushButton:hover {
        #         background-color: #f0f0f0;
        #     }
        # """)
        self.left_layout.addWidget(self.start_recognition_button, alignment=Qt.AlignCenter)

        # 添加一个占位符，使按钮居中
        self.left_layout.addStretch()

        # 添加图片路径显示标签
        self.path_label = QLabel("未选择图片")
        self.path_label.setAlignment(Qt.AlignCenter)
        self.path_label.setWordWrap(True)
        self.path_label.setStyleSheet(f"font-size: {self.label_font_size}px; color: #333333;")
        self.left_layout.addWidget(self.path_label)

        # 添加垂直分隔线
        self.vertical_line = QFrame()
        self.vertical_line.setFrameShape(QFrame.VLine)  # 设置为垂直线
        self.vertical_line.setFrameShadow(QFrame.Plain)  # 设置无阴影
        self.vertical_line.setLineWidth(self.line_width)
        self.vertical_line.setStyleSheet(f"""
            QFrame {{
                border: {self.line_width}px {self.line_style} {self.line_color};
            }}
        """)

        # 右侧布局（图片显示区域和识别结果区域）
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)

        # 上半部分：图片显示区域
        self.image_display_widget = QWidget()
        self.image_display_layout = QVBoxLayout()
        self.image_display_widget.setLayout(self.image_display_layout)
        self.image_display_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 设置上半部分背景颜色和样式
        self.image_display_widget.setStyleSheet("""
                    QWidget {
                        background-color: #ffffff;  /* 白色背景 */
                        border-bottom: 1px solid #4682b4;  /* 深蓝色底部边框 */
                    }
        """)

        # 添加图片显示标签（支持拖拽）
        self.image_label = QLabel("拖拽图片到这里或点击选择图片")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet(f"font-size: {self.label_font_size}px; color: #333333;")
        self.image_label.setAcceptDrops(True)  # 允许拖拽
        self.image_label.dragEnterEvent = self.dragEnterEvent
        self.image_label.dropEvent = self.dropEvent
        self.image_display_layout.addWidget(self.image_label)

        # 设置上半部分高度占比为 70%
        right_layout.addWidget(self.image_display_widget, stretch=6)

        # 添加水平分隔线
        self.horizontal_line = QFrame()
        self.horizontal_line.setFrameShape(QFrame.HLine)  # 设置为水平线
        self.horizontal_line.setFrameShadow(QFrame.Plain)  # 设置无阴影
        self.horizontal_line.setLineWidth(self.line_width)
        self.horizontal_line.setStyleSheet(f"""
            QFrame {{
                border: {self.line_width}px {self.line_style} {self.line_color};
            }}
        """)
        right_layout.addWidget(self.horizontal_line)

        # 下半部分：识别结果区域
        self.result_widget = QWidget()
        self.result_layout = QVBoxLayout()
        self.result_widget.setLayout(self.result_layout)
        self.result_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 设置下半部分背景颜色和样式
        self.result_widget.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;  /* 浅灰色背景 */
            }
        """)

        # 添加识别结果标签
        self.result_label = QLabel("识别结果将显示在这里")
        self.result_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # 左下角对齐
        self.result_label.setStyleSheet(f"font-size: {self.result_font_size}px; color: #333333; padding: 10px;")
        self.result_layout.addWidget(self.result_label)

        # 设置下半部分高度占比为 30%
        right_layout.addWidget(self.result_widget, stretch=4)

        # 将左右两部分和分隔线添加到主布局
        main_layout.addWidget(self.left_widget)
        main_layout.addWidget(self.vertical_line)  # 添加垂直分隔线
        main_layout.addWidget(right_widget)

    def setup_app_icon(self):
        """设置应用图标，支持多种格式和路径"""
        icon_paths = [
            "logo.ico",
            "logo.png",
            "icons/logo.ico",
            "icons/logo.png",
            os.path.join(os.path.dirname(__file__), "logo.ico"),
            os.path.join(os.path.dirname(__file__), "logo.png"),
            os.path.join(os.path.dirname(__file__), "icons", "logo.ico"),
            os.path.join(os.path.dirname(__file__), "icons", "logo.png")
        ]
        
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                try:
                    self.setWindowIcon(QIcon(icon_path))
                    print(f"成功加载图标：{icon_path}")
                    return
                except Exception as e:
                    print(f"加载图标 {icon_path} 失败：{str(e)}")
        
        print("警告：未找到有效的图标文件")
        # 设置一个默认图标（可选）
        self.setWindowIcon(QIcon())

    def select_image(self):
        # 打开文件对话框选择图片
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图片", "", "图片文件 (*.png *.jpg *.bmp *.jfif)"
        )
        if file_path:
            self.image_files = [file_path]  # 只选择一张图片
            self.current_image_index = 0
            self.path_label.setText(file_path)
            self.show_image()  # 选择图片后立即显示

    def select_folder(self):
        # 打开文件夹对话框选择文件夹
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder_path:
            self.folder_path = folder_path
            self.path_label.setText(f"已选择文件夹: {folder_path}")
            # 读取文件夹中的所有图片文件
            self.image_files = [
                os.path.join(folder_path, f)
                for f in os.listdir(folder_path)
                if f.lower().endswith(('.png', '.jpg', '.bmp', '.jfif'))
            ]
            if self.image_files:
                self.current_image_index = 0
                self.show_image()  # 显示第一张图片

    def show_image(self):
        # 显示当前图片
        if self.image_files:
            image_path = self.image_files[self.current_image_index]
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                # 缩放图片以适应窗口大小
                scaled_pixmap = pixmap.scaled(
                    self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_pixmap)
                self.image_label.setText("")  # 清空提示文字
            else:
                self.image_label.setText("无法加载图片")

        else:
            self.image_label.setText("未选择图片")

    def remove_image(self):
        # 去除右侧显示的图片
        self.image_label.clear()
        self.image_label.setText("拖拽图片到这里或点击选择图片")

    def start_recognition(self):
        if self.image_files:
            # 如果是单张图片，直接显示识别结果
            if len(self.image_files) == 1:
                self.result_label.setText("图片正在识别，请稍等...")
                self.process_image(self.image_files[0])
            else:
                # 启动定时器，每隔 2 秒切换一张图片
                self.result_label.setText("图片正在识别，请稍等...")
                self.timer.timeout.connect(self.next_image)
                self.timer.start(2000)  # 2 秒间隔

    def process_image(self, image_path):
        try:
            # 显示正在处理的提示
            self.result_label.setText("图片正在识别，请稍等...")
            # 调用 API 进行识别
            result = api_request(image_path)
            
            # 检查是否有错误
            if "error" in result:
                self.result_label.setText(f"识别失败：{result['error']}")
                return
                
            if result:
                result_text = ""
                # 确保 result 是字典类型
                if isinstance(result, dict):
                    for field, content in result.items():
                        result_text += f"{field}: {content}\n"
                    self.result_label.setText(result_text)
                else:
                    self.result_label.setText(f"识别失败：返回数据格式不正确\n{str(result)}")
            else:
                self.result_label.setText("识别失败：未获取到结果")
        except Exception as e:
            self.result_label.setText(f"识别出错：{str(e)}")
            print(f"识别错误：{str(e)}")
            import traceback
            traceback.print_exc()

    def next_image(self):
        # 切换到下一张图片
        if self.image_files:
            self.current_image_index += 1
            if self.current_image_index < len(self.image_files):
                self.show_image()
                # 显示识别结果（示例中为固定值）
                # self.result_label.setText(f"识别结果: 111111 (图片 {self.current_image_index + 1}/{len(self.image_files)})")
                self.process_image(self.image_files[self.current_image_index])
            else:
                # 所有图片轮播完成
                self.timer.stop()
                QMessageBox.information(self, "提示", "识别完成！")
                self.image_label.clear()
                self.image_label.setText("拖拽图片到这里或点击选择图片")
                self.result_label.setText("识别结果将显示在这里")
                self.current_image_index = 0  # 重置索引

    def dragEnterEvent(self, event):
        # 拖拽文件进入时的事件处理
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        # 拖拽文件释放时的事件处理
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(('.png', '.jpg', '.bmp', '.jfif')):
                self.image_files = [file_path]  # 只选择一张图片
                self.current_image_index = 0
                self.path_label.setText(file_path)
                self.show_image()  # 显示拖拽的图片
                break


def main():
    app = QApplication(sys.argv)
    window = ImageViewerApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        # 确保错误信息被显示
        import traceback
        traceback.print_exc()
        # 给系统一些时间来显示错误信息
        import time
        time.sleep(2)