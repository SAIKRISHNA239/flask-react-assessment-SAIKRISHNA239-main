from tests.modules.task.base_test_task import BaseTestTask

class TestCommentApi(BaseTestTask):
    
    def test_create_comment_success(self):
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        
        data = {"content": "This is a test comment"}
        url = f"/api/accounts/{account.id}/tasks/{task.id}/comments"
        
        response = self.test_client.post(
            url, 
            headers={"Authorization": f"Bearer {token}"},
            json=data
        )
        
        assert response.status_code == 201
        assert response.json["content"] == "This is a test comment"
        assert response.json["task_id"] == task.id

    def test_get_comments_success(self):
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        
        # Create a comment first
        self.test_client.post(
            f"/api/accounts/{account.id}/tasks/{task.id}/comments",
            headers={"Authorization": f"Bearer {token}"},
            json={"content": "Comment 1"}
        )
        
        response = self.test_client.get(
            f"/api/accounts/{account.id}/tasks/{task.id}/comments",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        assert len(response.json["items"]) == 1
        assert response.json["items"][0]["content"] == "Comment 1"

    def test_delete_comment_success(self):
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        
        # Create comment
        create_res = self.test_client.post(
            f"/api/accounts/{account.id}/tasks/{task.id}/comments",
            headers={"Authorization": f"Bearer {token}"},
            json={"content": "To be deleted"}
        )
        comment_id = create_res.json["id"]
        
        # Delete comment
        del_res = self.test_client.delete(
            f"/api/accounts/{account.id}/tasks/{task.id}/comments/{comment_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert del_res.status_code == 204