# 导入所需库（需要安装cryptography库：pip install cryptography）
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# 配置常量
KEY_FILE = "secret.key"
ENCRYPTED_FILE = "vault.dat"
SALT = b'secure_salt_'  # 生产环境应使用随机生成值

def generate_key(password: str):
    """生成加密密钥（基于用户密码和密钥派生函数）"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=480000,  # NIST推荐迭代次数
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def save_key(key: bytes):
    """安全存储加密密钥"""
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

def load_key():
    """加载存储的加密密钥"""
    if not os.path.exists(KEY_FILE):
        return None
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

def encrypt_text(text: str, key: bytes):
    """加密文本并返回密文"""
    fernet = Fernet(key)
    return fernet.encrypt(text.encode())

def decrypt_text(token: bytes, key: bytes):
    """解密文本返回明文"""
    fernet = Fernet(key)
    return fernet.decrypt(token).decode()

def clear_screen():
    """清屏函数（跨平台支持）"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    """显示加密系统横幅"""
    print("\n\033[92m" + "="*50)
    print("⚡ 军用级文本加密系统 2.0".center(50))
    print("="*50 + "\033[0m")
    print("安全标准：AES-256 | PBKDF2-HMAC-SHA256 | 128位盐值\n")

def main_menu():
    """主菜单界面"""
    print("\033[94m1. 初始化安全密钥")
    print("2. 加密文本/文件")
    print("3. 解密数据")
    print("4. 安全擦除密钥")
    print("5. 退出系统\033[0m")
    print("\033[91m" + "-"*50 + "\033[0m")

def initialize_system():
    """初始化加密系统（首次使用）"""
    clear_screen()
    display_banner()
    print("\033[93m⚠ 首次使用需要创建主密码\033[0m")
    
    while True:
        password = input("\n设置主密码（至少12字符）：")
        if len(password) >= 12:
            confirm = input("确认主密码：")
            if password == confirm:
                key = generate_key(password)
                save_key(key)
                print("\n\033[92m✓ 加密系统已激活！\033[0m")
                input("按回车返回主菜单...")
                return
            else:
                print("\033[91m密码不匹配！\033[0m")
        else:
            print("\033[91m密码长度不足！\033[0m")

def encrypt_operation():
    """加密操作流程"""
    clear_screen()
    display_banner()
    
    if not os.path.exists(KEY_FILE):
        print("\033[91m请先初始化系统！\033[0m")
        return
    
    print("1. 加密文本内容")
    print("2. 加密文件内容")
    choice = input("请选择模式：")
    
    password = input("\n输入主密码验证：")
    stored_key = load_key()
    if generate_key(password) != stored_key:
        print("\033[91m✗ 密码验证失败！\033[0m")
        return
    
    if choice == '1':
        text = input("\n输入要加密的文本：")
        encrypted = encrypt_text(text, stored_key)
        print(f"\n加密结果：\n{encrypted.decode()}")
    elif choice == '2':
        path = input("输入文件路径：")
        try:
            with open(path, 'r') as f:
                encrypted = encrypt_text(f.read(), stored_key)
            with open(ENCRYPTED_FILE, 'wb') as f:
                f.write(encrypted)
            print(f"\n\033[92m✓ 文件已加密保存至 {ENCRYPTED_FILE}\033[0m")
        except Exception as e:
            print(f"\033[91m错误：{str(e)}\033[0m")
    else:
        print("\033[91m无效选择！\033[0m")
    
    input("\n按回车返回主菜单...")

def decrypt_operation():
    """解密操作流程"""
    clear_screen()
    display_banner()
    
    if not os.path.exists(KEY_FILE):
        print("\033[91m系统未初始化！\033[0m")
        return
    
    password = input("输入主密码：")
    stored_key = load_key()
    if generate_key(password) != stored_key:
        print("\033[91m✗ 密码验证失败！\033[0m")
        return
    
    print("1. 解密文本内容")
    print("2. 解密文件内容")
    choice = input("请选择模式：")
    
    if choice == '1':
        cipher = input("\n输入加密文本：")
        try:
            decrypted = decrypt_text(cipher.encode(), stored_key)
            print(f"\n解密结果：\n{decrypted}")
        except:
            print("\033[91m解密失败！\033[0m")
    elif choice == '2':
        if not os.path.exists(ENCRYPTED_FILE):
            print("\033[91m加密文件不存在！\033[0m")
            return
        try:
            with open(ENCRYPTED_FILE, 'rb') as f:
                decrypted = decrypt_text(f.read(), stored_key)
            print(f"\n解密内容：\n{decrypted}")
        except:
            print("\033[91m文件损坏或密码错误！\033[0m")
    else:
        print("\033[91m无效选择！\033[0m")
    
    input("\n按回车返回主菜单...")

def secure_wipe():
    """安全删除密钥"""
    if os.path.exists(KEY_FILE):
        os.remove(KEY_FILE)
        print("\033[92m✓ 所有密钥已安全擦除\033[0m")
    else:
        print("\033[93m⚠ 系统未初始化\033[0m")
    input("按回车返回主菜单...")

if __name__ == "__main__":
    try:
        while True:
            clear_screen()
            display_banner()
            main_menu()
            
            choice = input("请选择操作（1-5）：")
            
            if choice == '1':
                initialize_system()
            elif choice == '2':
                encrypt_operation()
            elif choice == '3':
                decrypt_operation()
            elif choice == '4':
                secure_wipe()
            elif choice == '5':
                print("\n\033[92m安全退出完成！\033[0m")
                break
            else:
                print("\033[91m无效选择！\033[0m")
                input("按回车重试...")
    except KeyboardInterrupt:
        print("\n\033[93m安全终止操作！\033[0m")