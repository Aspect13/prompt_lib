import pytest
from flask import json

@pytest.mark.parametrize('project_id, prompt_id, expected_status', [ (1, 1, 200), (999, 999, 404) ])
def test_get_prompt(client, project_id, prompt_id, expected_status):
    response = client.get(f'/api/v1/projects/{project_id}/prompts/{prompt_id}')
    assert response.status_code == expected_status

@pytest.mark.parametrize('project_id, prompt_data, expected_status', [ (1, {'name': 'Test Prompt', 'description': 'A test prompt'}, 201), (1, {}, 400) ])
def test_create_prompt(client, project_id, prompt_data, expected_status):
    response = client.put(f'/api/v1/projects/{project_id}/prompts', json=prompt_data)
    assert response.status_code == expected_status

@pytest.mark.parametrize('project_id, prompt_id, update_data, expected_status', [ (1, 1, {'name': 'Updated Test Prompt'}, 201), (1, 999, {'name': 'Nope'}, 404) ])
def test_update_prompt(client, project_id, prompt_id, update_data, expected_status):
    response = client.patch(f'/api/v1/projects/{project_id}/prompts/{prompt_id}', json=update_data)
    assert response.status_code == expected_status

@pytest.mark.parametrize('project_id, prompt_id, expected_status', [ (1, 1, 204), (1, 999, 404) ])
def test_delete_prompt(client, project_id, prompt_id, expected_status):
    response = client.delete(f'/api/v1/projects/{project_id}/prompts/{prompt_id}')
    assert response.status_code == expected_status