import pytest
import base64
import json
import struct
import os
from io import BytesIO
from PIL import Image
from aiohttp import web
from unittest.mock import patch
from urllib.parse import quote
from app.model_manager import ModelFileManager

pytestmark = (
    pytest.mark.asyncio
)  # This applies the asyncio mark to all test functions in the module

@pytest.fixture
def model_manager():
    return ModelFileManager()

@pytest.fixture
def app(model_manager):
    app = web.Application()
    routes = web.RouteTableDef()
    model_manager.add_routes(routes)
    app.add_routes(routes)
    return app

async def test_get_model_folders_includes_registered_extensions(aiohttp_client, app, tmp_path):
    """Folders expose their registered extension set verbatim; an empty list
    means match-all (filter_files_extensions semantics)."""
    with patch('folder_paths.folder_names_and_paths', {
        'test_checkpoints': ([str(tmp_path)], {'.safetensors', '.ckpt'}),
        'test_configs': ([str(tmp_path)], ['.yaml']),
        'test_match_all': ([str(tmp_path)], set()),
        'configs': ([str(tmp_path)], ['.yaml']),
    }):
        client = await aiohttp_client(app)
        response = await client.get('/experiment/models')

        assert response.status == 200
        folders = {f['name']: f for f in await response.json()}

        assert 'configs' not in folders  # blocklisted
        assert folders['test_checkpoints']['folders'] == [str(tmp_path)]
        assert folders['test_checkpoints']['extensions'] == ['.ckpt', '.safetensors']
        assert folders['test_configs']['extensions'] == ['.yaml']
        # Match-all registrations are exposed honestly, not substituted.
        assert folders['test_match_all']['extensions'] == []

@pytest.mark.parametrize(('folder_name', 'model_name'), [
    ('models', 'test_model'),
    ('models', 'test_model[v1]'),
    ('models[v1]', 'test_model'),
    pytest.param('models', 'test_model?', marks=pytest.mark.skipif(os.name == 'nt', reason='Invalid Windows filename')),
    pytest.param('models', 'test_model*', marks=pytest.mark.skipif(os.name == 'nt', reason='Invalid Windows filename')),
    pytest.param('models?', 'test_model', marks=pytest.mark.skipif(os.name == 'nt', reason='Invalid Windows filename')),
    pytest.param('models*', 'test_model', marks=pytest.mark.skipif(os.name == 'nt', reason='Invalid Windows filename')),
])
async def test_get_model_preview_safetensors(aiohttp_client, app, tmp_path, folder_name, model_name):
    model_dir = tmp_path / folder_name
    model_dir.mkdir()
    img = Image.new('RGB', (100, 100), 'white')
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    img_b64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

    safetensors_file = model_dir / f"{model_name}.safetensors"
    header_bytes = json.dumps({
        "__metadata__": {
            "ssmd_cover_images": json.dumps([img_b64])
        }
    }).encode('utf-8')
    length_bytes = struct.pack('<Q', len(header_bytes))
    # A different model may match the unescaped name.
    if model_name != 'test_model':
        black_img = BytesIO()
        Image.new('RGB', (100, 100), 'black').save(black_img, format='PNG')
        decoy_header = json.dumps({"__metadata__": {
            "ssmd_cover_images": json.dumps([base64.b64encode(black_img.getvalue()).decode('utf-8')])
        }}).encode('utf-8')
        (model_dir / 'test_modelv.safetensors').write_bytes(struct.pack('<Q', len(decoy_header)) + decoy_header)

    with open(safetensors_file, 'wb') as f:
        f.write(length_bytes)
        f.write(header_bytes)

    with patch('folder_paths.folder_names_and_paths', {
        'test_folder': ([str(model_dir)], None)
    }):
        client = await aiohttp_client(app)
        response = await client.get(f'/experiment/models/preview/test_folder/0/{quote(model_name)}.safetensors')

        # Verify response
        assert response.status == 200
        assert response.content_type == 'image/webp'

        # Verify the response contains valid image data
        img_bytes = BytesIO(await response.read())
        img = Image.open(img_bytes)
        assert img.format
        assert img.format.lower() == 'webp'
        assert all(channel > 240 for channel in img.getpixel((50, 50)))

        # Clean up
        img.close()


@pytest.mark.parametrize(('folder_name', 'model_name'), [
    ('models', 'test_model[v1]'),
    ('models[v1]', 'test_model'),
    pytest.param('models', 'test_model?', marks=pytest.mark.skipif(os.name == 'nt', reason='Invalid Windows filename')),
    pytest.param('models', 'test_model*', marks=pytest.mark.skipif(os.name == 'nt', reason='Invalid Windows filename')),
])
@pytest.mark.parametrize('suffix', ['.png', '.preview.png'])
async def test_get_model_preview_literal_path(aiohttp_client, app, tmp_path, folder_name, model_name, suffix):
    model_dir = tmp_path / folder_name
    model_dir.mkdir()
    Image.new('RGB', (10, 10), 'white').save(model_dir / f'{model_name}{suffix}')
    Image.new('RGB', (10, 10), 'black').save(model_dir / 'test_modelv.preview.png')

    with patch('folder_paths.folder_names_and_paths', {'test_folder': ([str(model_dir)], None)}):
        client = await aiohttp_client(app)
        response = await client.get(f'/experiment/models/preview/test_folder/0/{quote(model_name)}.safetensors')

    assert response.status == 200
    assert response.content_type == 'image/webp'
    with Image.open(BytesIO(await response.read())) as img:
        assert all(channel > 240 for channel in img.getpixel((5, 5)))
