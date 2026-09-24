"""Multimodal helpers"""

import re
import os
from pathlib import Path

# You may need to customize these based on your target model's capabilities:
ALLOWED_IMAGE_EXTENSIONS = ["png", "jpg", "jpeg", "gif", "webp"]
ALLOWED_DOCUMENT_EXTENSIONS = ["pdf", "doc", "docx", "html", "txt", "md"]


class MultimodalHelper:
    """Helper functions for multimodal prompts and tools"""

    def __init__(self, allowed_directory: str):
        self.allowed_path = Path(allowed_directory).resolve()

    def local_open(self, file_name, mode="r"):
        """Open a file only if it is within the allowed directory."""
        requested_path = (self.allowed_path / file_name).resolve()

        try:
            requested_path.relative_to(self.allowed_path)
        except ValueError:
            raise ValueError(f"Access denied: {file_name} is outside allowed directory")

        return open(requested_path, mode)

    def get_bytes_from_file(self, file_name) -> bytes:
        """Get the bytes from a local file"""
        with self.local_open(file_name, "rb") as f:
            file_bytes = f.read()
        return file_bytes

    def get_cleaned_document_name(self, file_stem: str) -> str:
        """Returns a cleaned document name with only alphanumeric and hyphens"""
        # See https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_DocumentBlock.html
        return re.sub(r'[^a-zA-Z0-9-]', '-', file_stem)

    def get_document_content_dict(self, file_name: str) -> dict:
        """Returns a DocumentContent dict containing the data from file"""

        base_name = os.path.basename(file_name)
        split_name = os.path.splitext(base_name)

        doc_name = self.get_cleaned_document_name(split_name[0])
        file_format = split_name[1][1:].lower()

        if file_format not in ALLOWED_DOCUMENT_EXTENSIONS:
            raise ValueError(f"Invalid document file format: {file_format}")

        file_bytes = self.get_bytes_from_file(file_name)

        return {"format": file_format, "name": doc_name, "source": {"bytes": file_bytes}}

    def get_image_content_dict(self, file_name: str) -> dict:
        """Returns an ImageContent dict containing the data from file"""

        file_format = os.path.splitext(file_name)[1][1:].lower()

        if file_format == "jpg":
            file_format = "jpeg"

        if file_format not in ALLOWED_IMAGE_EXTENSIONS:
            raise ValueError(f"Invalid image file format: {file_format}")

        file_bytes = self.get_bytes_from_file(file_name)

        return {"format": file_format, "source": {"bytes": file_bytes}}
