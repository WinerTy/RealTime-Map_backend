from starlette_admin.contrib.sqla import ModelView

from models import UsersBan


class AdminUsersBans(ModelView):
    fields = [
        UsersBan.id,
        UsersBan.user,
        UsersBan.banned_at,
        UsersBan.banned_until,
        UsersBan.is_permanent,
        UsersBan.moderator,
        UsersBan.reason,
        UsersBan.reason_text,
        UsersBan.unbanned_at,
        UsersBan.unbanned_by,
    ]
    exclude_fields_from_list = [UsersBan.reason_text]
