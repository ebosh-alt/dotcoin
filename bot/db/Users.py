from collections import namedtuple

from .SQLite import SqliteDatabase


class User:
    def __init__(self, id, **kwargs):
        self.id: int = id
        if len(kwargs):
            self.name: str = kwargs.get("name")
            self.username: str = kwargs.get("username")
            self.ref_link: str = kwargs.get("ref_link")
            self.count: int = kwargs.get("count")
            self.requisites: str = kwargs.get("requisites")
            self.status: bool = kwargs.get("status")
            self.buy: bool = kwargs.get("buy")
        else:
            self.name: str | None = None
            self.username: str | None = None
            self.ref_link: str | None = None
            self.count: int = 0
            self.requisites: str | None = None
            self.status: bool = True
            self.buy: bool = False

    def __iter__(self):
        dict_class = self.__dict__
        Result = namedtuple("Result", ["name", "value"])
        for attr in dict_class:
            if not attr.startswith("__"):
                if attr != "flag":
                    yield Result(attr, dict_class[attr])
                else:
                    yield Result(attr, dict_class[attr].value)

    def data_by_excel(self) -> list:
        status = "Разблокированный" if self.status else "Заблокированный"
        return [self.id, self.username, self.count, status]


class Users(SqliteDatabase):
    def __init__(self, db_file_name, table_name, *args) -> None:
        SqliteDatabase.__init__(self, db_file_name, table_name, *args)
        self.len = len(self.get_keys())

    def add(self, obj: User) -> None:
        self.add_row(obj)
        self.len += 1

    def __len__(self):
        return self.len

    def __delitem__(self, key):
        self.del_instance(key)
        self.len -= 1

    def __iter__(self) -> User | bool:
        keys = self.get_keys()
        for id in keys:
            user = self.get(id)
            yield user

    def get(self, id: int) -> User | bool:
        if id in self:
            obj_tuple = self.get_elem_sqllite3(id)
            obj = User(
                id=obj_tuple[0],
                name=obj_tuple[1],
                username=obj_tuple[2],
                ref_link=obj_tuple[3],
                count=obj_tuple[4],
                requisites=obj_tuple[5],
                buy=obj_tuple[6],
                status=obj_tuple[7],

            )
            return obj
        return False
