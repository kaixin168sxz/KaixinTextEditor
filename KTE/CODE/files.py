import pickle

# 定义字符串替换规则，将字母和数字进行混淆
English_conversion = str.maketrans("abcdefghijklmnopqrstuvwxyz", "qwertyuiopasdfghjklmnbvczx")
Digital_transformation = str.maketrans("0123456789", "2587413690")
English_Reverse_conversion = str.maketrans("qwertyuiopasdfghjklmnbvczx", "abcdefghijklmnopqrstuvwxyz")
Digital_Reverse_conversion = str.maketrans("2587413690", "0123456789")


# 使用pickle模块将列表对象序列化为二进制数据
def save_file(file_name, file_content):
    global English_conversion, Digital_transformation
    data = str(pickle.dumps(file_content))
    # 对序列化后的二进制数据进行字符串替换操作
    new_data_1 = data.translate(English_conversion)
    new_data_2 = new_data_1.translate(Digital_transformation)

    # 将替换后的二进制数据写入文件
    with open(file_name, 'w') as file_save:
        file_save.write(new_data_2)


def read_file(read_name):
    global Digital_Reverse_conversion, English_Reverse_conversion
    # 从文件中读取替换后的二进制数据
    with open(read_name, 'r') as file_read:
        r = (file_read.read())
    # 对读取的二进制数据进行字符串替换操作，恢复原始数据
    old_data_1 = r.translate(English_Reverse_conversion)
    old_data_2 = pickle.loads(eval(old_data_1.translate(Digital_Reverse_conversion)))
    return old_data_2
