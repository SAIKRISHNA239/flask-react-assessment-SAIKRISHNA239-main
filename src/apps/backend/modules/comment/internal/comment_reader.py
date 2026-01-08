from modules.application.common.base_model import BaseModel
from modules.application.common.types import PaginationResult
from modules.comment.internal.store.comment_repository import CommentRepository
from modules.comment.internal.comment_util import CommentUtil
from modules.comment.types import GetCommentsParams, Comment

class CommentReader:
    @staticmethod
    def get_comments(*, params: GetCommentsParams) -> PaginationResult[Comment]:
        filter_query = {"account_id": params.account_id, "task_id": params.task_id, "active": True}
        total_count = CommentRepository.collection().count_documents(filter_query)
        
        pagination_params, skip, total_pages = BaseModel.calculate_pagination_values(
            params.pagination_params, total_count
        )
        cursor = CommentRepository.collection().find(filter_query)

        if params.sort_params:
            cursor = BaseModel.apply_sort_params(cursor, params.sort_params)
        else:
            # Default sort by created_at descending (newest first)
            cursor = cursor.sort([("created_at", -1)])

        comments_bson = list(cursor.skip(skip).limit(pagination_params.size))
        comments = [CommentUtil.convert_comment_bson_to_comment(doc) for doc in comments_bson]
        
        return PaginationResult(
            items=comments,
            pagination_params=pagination_params,
            total_count=total_count,
            total_pages=total_pages
        )