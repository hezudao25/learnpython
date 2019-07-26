#所有名片记录的列表
card_list=[]

def show_menu():
    """显示菜单"""
    print("*" * 50)
    print("欢迎使用【名片管理系统】 v1.0")
    print("")
    print("1.新增名片")
    print("2.显示全部")
    print("3.查找名片")
    print("")
    print("0.退出系统")
    print("*" * 50)

def new_card():
    """新增名片"""
    print("*" * 50)
    print("新增名片")

    #1. 提示用户输入名片的详细信息
    name_str = input("请输入姓名：")
    phone_str = input("请输入电话：")
    qq_str = input("请输入QQ：")
    email_str = input("请输入Email:")

    #2.使用用户输入的信息建立一个名片
    card_dict = {"name":name_str,"phone":phone_str,"qq":qq_str,"email":email_str}

    #3.将名片字典添加到list
    card_list.append(card_dict)
    print(card_list)

    #4 提示成功
    print("添加 %s 的名片成功！" % name_str)

def show_all():
    """显示所有名片"""
    print("*" * 50)
    print("显示所有名片")

    if len(card_list)==0:
        print("目前没有名片，请使用新增功能添加名片")
        return

    for name in ["姓名","电话","QQ","Email"]:
        print(name,end="\t\t")

    print("")
    print("=" * 50)

    for ky in card_list:

        print("%s\t\t%s\t\t%s\t\t%s" % (ky["name"],ky["phone"],ky["qq"],ky["email"]))


def search_card():
    """查找名片"""
    print("*" * 50)
    print("查找名片")
    #1 提示输入姓名
    search_str = input("关键词：")

    #2 遍历名片列表
    for ky in card_list:

        if ky["name"] == search_str:
            print("姓名\t\t电话\t\tQQ\t\tEmail")
            print("=" * 50)
            print("%s\t\t%s\t\t%s\t\t%s" % (ky["name"], ky["phone"], ky["qq"], ky["email"]))

            #
            deal_card(ky)
            break
    else:
        print("没有找到 %s" % search_str)



def deal_card(find_dict):
    print(find_dict)
    action_str = input("请选择要执行的操作"
                       " 1 修改 2 删除 0 返回：")


    if action_str=="1":
        find_dict["name"]=input_card_info(find_dict["name"],"姓名")
        find_dict["phone"] = input_card_info(find_dict["phome"],"电话")
        find_dict["qq"]=input_card_info(find_dict["qq"],"qq")
        find_dict["email"]=input_card_info(find_dict["email"],"email")
        print("修改名片")
    elif action_str=="2":
        card_list.remove(find_dict)
        print("删除名片")


def input_card_info(dict_value,tip_message):
    """

    :param dict_value:
    :param tip_message:
    :return:
    """
    action_str = input(tip_message+"[回车不修改]：")
    if action_str !="":
        return action_str
    else:
        return dict_value