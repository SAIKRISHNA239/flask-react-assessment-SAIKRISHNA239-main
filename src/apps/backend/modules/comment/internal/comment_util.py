from typing import Any
from modules.comment.internal.store.comment_model import CommentModel
from modules.comment.types import Comment

class CommentUtil:
    @staticmethod
    def convert_comment_bson_to_comment(comment_bson: dict[str, Any]) -> Comment:
        comment_model = CommentModel.from_bson(comment_bson)
        return Comment(
            id=str(comment_model.id),
            account_id=comment_model.account_id,
            task_id=comment_model.task_id,
            content=comment_model.content,
            created_at=comment_model.created_at,
        )