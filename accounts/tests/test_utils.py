import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

def generate_test_image(name="test.jpg", size=(100, 100), color=(255, 0, 0), fmt="JPEG"):
    """
    Generates an in-memory image file — no disk I/O needed.
    """
    buffer = io.BytesIO()
    img = Image.new("RGB", size, color=color)
    img.save(buffer, format=fmt)
    buffer.seek(0)
    return SimpleUploadedFile(
        name=name,
        content=buffer.read(),
        content_type="image/jpeg"
    )