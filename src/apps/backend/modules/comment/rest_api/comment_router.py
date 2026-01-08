from flask import Blueprint
from modules.comment.rest_api.comment_view import CommentView

class CommentRouter:
    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        view = CommentView.as_view("comment_view")
        
        # List and Create Comments
        blueprint.add_url_rule(
            "/accounts/<account_id>/tasks/<task_id>/comments",
            view_func=view,
            methods=["GET", "POST"]
        )
        
        # Update and Delete Comments
        blueprint.add_url_rule(
            "/accounts/<account_id>/tasks/<task_id>/comments/<comment_id>",
            view_func=view,
            methods=["PATCH", "DELETE"]
        )
        return blueprint