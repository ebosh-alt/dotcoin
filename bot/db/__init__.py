from .Configuration import Configuration
from .Users import User, Users

db_file_name = "D:/telegram_bots/dotcoin/bot/db/database"
users = Users(db_file_name=db_file_name, table_name="users")
configuration = Configuration("D:/telegram_bots/dotcoin/bot/db/configuration.json")
__all__ = ("User", "Users", "users", "configuration")
