import pytest
from flask import json

@pytest.mark.parametrize('project_id, prompt_id, expected_status', [ (1, 1, 200), (999, 999, 404) ])
def test_get_prompt(client, project_id, prompt_id, expected_status):
    response = client.get(f'/api/v1/projects/{project_id}/prompts/{prompt_id}')
    assert response.status_code == expected_status

# Additional tests for PUT, PATCH, and DELETE endpoints will follow the same structure