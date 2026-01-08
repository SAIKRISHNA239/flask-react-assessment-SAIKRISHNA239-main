from dataclasses import asdict
from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.application.common.constants import DEFAULT_PAGINATION_PARAMS
from modules.application.common.types import PaginationParams
from modules.authentication.rest_api.access_auth_middleware import access_auth_middleware
from modules.comment.errors import CommentBadRequestError
from modules.comment.comment_service import CommentService
from modules.comment.types import (
    CreateCommentParams, UpdateCommentParams, DeleteCommentParams, GetCommentsParams
)

class CommentView(MethodView):
    @access_auth_middleware
    def post(self, account_id: str, task_id: str) -> ResponseReturnValue:
        request_data = request.get_json()
        if not request_data or not request_data.get("content"):
            raise CommentBadRequestError("Content is required")

        params = CreateCommentParams(
            account_id=account_id,
            task_id=task_id,
            content=request_data["content"]
        )
        created_comment = CommentService.create_comment(params=params)
        return jsonify(asdict(created_comment)), 201

    @access_auth_middleware
    def get(self, account_id: str, task_id: str) -> ResponseReturnValue:
        page = request.args.get("page", type=int, default=DEFAULT_PAGINATION_PARAMS.page)
        size = request.args.get("size", type=int, default=DEFAULT_PAGINATION_PARAMS.size)
        
        pagination_params = PaginationParams(page=page, size=size, offset=0)
        params = GetCommentsParams(
            account_id=account_id,
            task_id=task_id,
            pagination_params=pagination_params
        )
        
        result = CommentService.get_comments(params=params)
        return jsonify(asdict(result)), 200

    @access_auth_middleware
    def patch(self, account_id: str, task_id: str, comment_id: str) -> ResponseReturnValue:
        request_data = request.get_json()
        if not request_data or not request_data.get("content"):
            raise CommentBadRequestError("Content is required")

        params = UpdateCommentParams(
            account_id=account_id,
            task_id=task_id,
            comment_id=comment_id,
            content=request_data["content"]
        )
        updated_comment = CommentService.update_comment(params=params)
        return jsonify(asdict(updated_comment)), 200

    @access_auth_middleware
    def delete(self, account_id: str, task_id: str, comment_id: str) -> ResponseReturnValue:
        params = DeleteCommentParams(account_id=account_id, task_id=task_id, comment_id=comment_id)
        CommentService.delete_comment(params=params)
        return "", 204