from modules.application.common.types import PaginationResult
from modules.comment.internal.comment_reader import CommentReader
from modules.comment.internal.comment_writer import CommentWriter
from modules.comment.types import (
    CreateCommentParams, UpdateCommentParams, DeleteCommentParams, GetCommentsParams, Comment
)

class CommentService:
    @staticmethod
    def create_comment(*, params: CreateCommentParams) -> Comment:
        return CommentWriter.create_comment(params=params)

    @staticmethod
    def update_comment(*, params: UpdateCommentParams) -> Comment:
        return CommentWriter.update_comment(params=params)

    @staticmethod
    def delete_comment(*, params: DeleteCommentParams) -> bool:
        return CommentWriter.delete_comment(params=params)

    @staticmethod
    def get_comments(*, params: GetCommentsParams) -> PaginationResult[Comment]:
        return CommentReader.get_comments(params=params)