from .replenishment import replenishment_rt
from .withdrawal import withdrawal_rt
from .menu import menu_admin_rt
from .change_requisites import change_requisites_rt
from .change_commission import change_commission_rt
from .ban_unban import ban_unban_rt
from .change_balance import change_balance_rt
from .new_income import new_income_rt
from .mailing import mailing_rt
from .new_requisites import new_requisites_rt
from .info_project import info_project_rt
from .change_info import change_info_rt

admins_router = (replenishment_rt, withdrawal_rt, menu_admin_rt, change_requisites_rt, change_commission_rt,
                 ban_unban_rt, change_balance_rt, new_income_rt, mailing_rt, new_requisites_rt, info_project_rt,
                 change_info_rt)

