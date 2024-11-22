import sys
import os
import webview
from flask_backend.demo import app

# 设置Flask应用运行在本地的端口号
FLASK_PORT = 5000

# 启动Flask应用（在子进程中运行，避免阻塞主线程）
def start_flask_app():
    os.environ['FLASK_APP'] = 'flask_backend.demo'
    os.system(f'flask run --port={FLASK_PORT}')

if __name__ == '__main__':
    # 创建新的线程来启动Flask应用
    import threading
    flask_thread = threading.Thread(target=start_flask_app)
    flask_thread.start()

    # 构建Vue前端页面的本地访问路径
    vue_index_path = os.path.abspath(os.path.join('vue_frontend', 'demo.vue'))

    # 创建一个窗口并加载Vue前端页面（这里假设通过本地文件协议访问Vue页面）
    window = webview.create_window('Vue + Flask + Pywebview Example', f'http://localhost:5173/demo')

    # 启动pywebview的主循环
    webview.start()

    # 当窗口关闭时，尝试停止Flask应用（这里简单地通过发送中断信号到子进程来实现）
    while flask_thread.is_alive():
        try:
            flask_thread.join(timeout=1)
        except KeyboardInterrupt:
            pass

    print("Flask 应用已停止")
