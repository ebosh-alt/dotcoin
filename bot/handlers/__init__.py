from .greeting import greeting_rt
from .del_notification import del_notification_rt
from .bacs import bacs_rt
from .profile import profile_rt
from .top_up import top_up_rt
from .admin_handler import admins_router
from .withdrawal import withdrawal_rt
from .change_requisites import requisites_rt
from .info import info_rt

routers = (greeting_rt, del_notification_rt, bacs_rt, profile_rt, top_up_rt, withdrawal_rt, requisites_rt, info_rt,
           *admins_router)
