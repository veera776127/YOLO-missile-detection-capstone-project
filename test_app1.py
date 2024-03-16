import os
import tempfile
import pytest
from flask import template_rendered
from contextlib import contextmanager
from app import app

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

@contextmanager
def captured_templates(app):
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

def test_home_page(client):
    """Test that the home page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    with captured_templates(app) as templates:
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'index.html'

def test_results_page_without_session(client):
    """Test accessing the results page directly without session data redirects to home."""
    response = client.get('/results', follow_redirects=True)
    assert response.status_code == 200
    with captured_templates(app) as templates:
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'index.html'

# Mocking the perform_object_detection function
from unittest.mock import patch
from werkzeug.datastructures import FileStorage
from io import BytesIO

def test_file_upload(client):
    """Test file upload and object detection workflow."""
    with patch('app.perform_object_detection') as mock_perform:
        mock_perform.return_value = 'path/to/result_image.jpg'
        
        data = {
            'file': (BytesIO(b'my file contents'), 'test.jpg')
        }
        response = client.post('/', data=data, content_type='multipart/form-data', follow_redirects=True)
        
        assert response.status_code == 200
        mock_perform.assert_called_once()
        with captured_templates(app) as templates:
            assert len(templates) == 1
            template, context = templates[0]
            assert template.name == 'index.html'
            assert 'result_image_url' in context
