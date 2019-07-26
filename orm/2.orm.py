class ModeMetaclass(type):
    """元类"""
    def __new__(cls, name, bases, attrs):
        mappings = dict()
        # 判断是否需要保存
        for k, v in attrs.items():
            # 判断是否指定的StringField或者InteinterFIELD的实例对象
            if isinstance(v, tuple):
                mappings[k] = v

        # 删除这些已经在字典里的存储属性
        for k in mappings.keys():
            attrs.pop(k)

        # 将之前的 属性 已经对象引用·类名字
        attrs['__mappings__'] = mappings # 保存属性和列的映射关系
        attrs['__table__'] = name # 假设表名和类名一致
        return type.__new__(cls, name, bases, attrs)


class Model(metaclass=ModeMetaclass):
    """把类的属性 传输给元类，并把执行结果返回"""
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

    def save(self):
        fields = []
        args = []
        for k, v in self.__mappings__.items():
            fields.append(v[0])
            args.append(getattr(self, k, None))

        args_temp = list()
        for temp in args:
            # 判断是否是数字类型
            if isinstance(temp, int):
                args_temp.append(str(temp))
            elif isinstance(temp,str):
                args_temp.append("""'%s'""" % temp)

        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(args_temp))
        print('SQL:%s' % sql)


class User(Model):
    uid = ('uid', "int unsigned")
    name = ('username', "varchar(30)")
    email = ('email', "varchar(30)")
    password = ('password', "varchar(30)")


u = User(uid=12345, name="Michacel", email="test@orm.gor", password="123456")
u.save()



