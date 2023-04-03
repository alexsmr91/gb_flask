from combojsonapi.permission.permission_system import (
    PermissionMixin,
    PermissionUser,
    PermissionForGet,
    PermissionForPatch,
)
from flask_combo_jsonapi.exceptions import AccessDenied
from flask_login import current_user
from blog.models.user import User
from blog.models.author import Author
from blog.models.article import Article


class ArticlePermission(PermissionMixin):
    ALL_AVAILABLE_FIELDS = [
        "id",
        "author_id",
        "title",
        "body",
        "dt_created",
        "dt_updated",
        "tags",
    ]
    PATCH_AVAILABLE_FIELDS = [
        "title",
        "body",
        "tags",
    ]

    def get(self, *args, many=True, user_permission: PermissionUser = None, **kwargs) -> PermissionForGet:
        """
        Set available columns
        :param args:
        :param many:
        :param user_permission:
        :param kwargs:
        :return:
        """
        self.permission_for_get.allow_columns = (self.ALL_AVAILABLE_FIELDS, 10)
        return self.permission_for_get

    def patch_permission(self, *args, user_permission: PermissionUser = None, **kwargs) -> PermissionForPatch:
        self.permission_for_patch.allow_columns = (self.PATCH_AVAILABLE_FIELDS, 10)
        return self.permission_for_patch

    def patch_data(self, *args, data: dict = None, obj: User = None, user_permission: PermissionUser = None, **kwargs) -> dict:
        if not current_user.is_authenticated:
            raise AccessDenied("no access")
        user_author_id = Author.query.filter_by(user_id=current_user.id).one_or_none()
        if user_author_id:
            user_author_id = user_author_id.id
        article_author_id = Article.query.filter_by(id=kwargs['id'], ).one_or_none()
        if article_author_id:
            article_author_id = article_author_id.author_id
        else:
            article_author_id = -1
        if not (current_user.is_staff or article_author_id == user_author_id):
            raise AccessDenied("no access")
        permission_for_patch = user_permission.permission_for_patch_permission(model=Article)
        return {
            i_key: i_val
            for i_key, i_val in data.items()
            if i_key in permission_for_patch.columns
        }
