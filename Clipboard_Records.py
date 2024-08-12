import pyperclip
import time
from datetime import datetime
import sys, os
import configparser
import win32clipboard

# 定义配置文件路径
config_file = 'pyperclipconfig.conf'
# 创建配置解析器对象
config = configparser.ConfigParser()

def read_directory_from_config(config_file):
    # 检查配置文件是否存在
    if not os.path.exists(config_file):
        print('配置文件不存在！，正在新建...')
        time.sleep(3)
        # 配置文件不存在，创建并写入内容
        config['dir_info'] = {'directory': r'D:\pyperclip'}
        # 写入配置文件
        with open(config_file, 'w') as file:
            config.write(file)
        # 退出程序
        print('配置文件新建完成，正在退出...')
        print('请根据配置文件修改内容！')
        time.sleep(4)
        sys.exit()
    
    # 配置文件存在，读取内容
    config.read(config_file)
    
    # 获取directory和directory2的值
    directory = config['dir_info']['directory']
    return directory
pyperclip_dir =read_directory_from_config(config_file)

def write_to_log(data, pyperclip_dir):
    if not os.path.exists(pyperclip_dir):
            os.makedirs(pyperclip_dir)
    dateinfo =datetime.now().strftime("%Y-%m-%d")
    with open(os.path.join(pyperclip_dir,f"Dlog{dateinfo}.txt"), "a", encoding="utf-8") as file:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"[{current_time}]\n{data}\n")

def get_clipboard_data():
    try:
        win32clipboard.OpenClipboard()
        try:
            # 检查剪贴板是否包含文件路径
            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_HDROP):
                file_paths = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
                return "\n".join(file_paths)
        finally:
            win32clipboard.CloseClipboard()
    except Exception as e:
        return str(e)

def main():
    last_data = ""
    last_data2 = ""
    while True:
        try:
            current_data = pyperclip.paste()
            current_data2 = get_clipboard_data()
            if current_data != last_data or current_data2 != last_data2:
                if current_data !="":
                    write_to_log(current_data, pyperclip_dir)
                if current_data2 !=None:
                    write_to_log(current_data2, pyperclip_dir)
                last_data = current_data
                last_data2 = current_data2
            time.sleep(1)  # 等待1秒，避免频繁检测消耗过多资源
        except KeyboardInterrupt:
            print("程序已终止")
            break

if __name__ == "__main__":
    main()
