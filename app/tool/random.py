import random


class RandomGenerator:
    """随机生成器工具类"""

    @staticmethod
    def generate_sms_code(length: int = 4) -> int:
        """
        生成指定长度的随机数字验证码

        Args:
            length: 验证码长度,默认为4位

        Returns:
            int: 生成的数字验证码
        """
        # 生成第一位为1-9的随机数,避免首位为0
        first = str(random.randint(1, 9))

        # 生成剩余位数的随机数字(0-9)
        rest = ''.join(str(random.randint(0, 9)) for _ in range(length - 1))

        # 组合并转换为整数
        return int(first + rest)

    @staticmethod
    def generate_password(length: int = 8) -> str:
        """
        生成指定长度的随机密码

        Args:
            length: 密码长度,默认为8位

        Returns:
            str: 生成的随机密码,包含大小写字母、数字和特殊字符
        """
        # 定义字符集
        lowercase = 'abcdefghijklmnopqrstuvwxyz'
        uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        digits = '0123456789'
        special = '!@#$%^&*'

        # 确保密码包含各类字符
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(special)
        ]

        # 生成剩余字符
        all_chars = lowercase + uppercase + digits + special
        for _ in range(length - 4):
            password.append(random.choice(all_chars))

        # 打乱密码字符顺序
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def generate_username(prefix: str = "user") -> str:
        """
        生成随机用户名

        Args:
            prefix: 用户名前缀,默认为"user"

        Returns:
            str: 生成的随机用户名,格式为 prefix + 随机数字
        """
        # 生成6位随机数字
        random_digits = ''.join(str(random.randint(0, 9)) for _ in range(6))

        # 组合用户名
        return f"{prefix}{random_digits}"
