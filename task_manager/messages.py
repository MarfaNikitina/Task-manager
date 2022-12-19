from django.utils.translation import gettext as _

NO_USER_PERMISSION_MESSAGE = _(
    "You do not have permissions to change another user."
)
NO_AUTHORIZATION_MESSAGE = _('You are not authorized! Please sign in.')
PROTECTED_ERROR_MESSAGE = _(
    "Cannot delete user because user is in use"
)
USER_CREATE_MESSAGE = _("User created successfully")
USER_UPDATE_MESSAGE = _("User updated successfully")
USER_DELETE_MESSAGE = _("User deleted successfully")
USER_EXIST_MESSAGE = _("A user with the same name already exists.")

SUCCESS_LOGIN_MESSAGE = _("You are logged in")
SUCCESS_LOGOUT_MESSAGE = _("You are logged out")

NO_PERMISSION_MESSAGE = _('You are not authorized! Please sign in.')
NO_DELETE_TASK_MESSAGE = _("A task can only be deleted by its author.")
TASK_CREATE_MESSAGE = _("Task created successfully")
TASK_UPDATE_MESSAGE = _("Task updated successfully")
TASK_DELETE_MESSAGE = _("Task deleted successfully")

NO_DELETE_STATUS_MESSAGE = _("Can't delete status because it's in use")
STATUS_CREATE_MESSAGE = _("Status created successfully")
STATUS_UPDATE_MESSAGE = _("Status updated successfully")
STATUS_DELETE_MESSAGE = _("Status deleted successfully")

NO_DELETE_LABEL_MESSAGE = _("Can't delete label because it's in use")
LABEL_CREATE_MESSAGE = _("Label created successfully")
LABEL_UPDATE_MESSAGE = _("Label updated successfully")
LABEL_DELETE_MESSAGE = _("Label deleted successfully")
