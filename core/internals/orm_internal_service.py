from db import Base
from .base_import_service import BaseImportService


class OrmInternalService(BaseImportService):
    # This class imports models
    # thus it adds them to Base.metadata

    TARGET_FOLDER = "apps"
    TARGET_SUBFOLDERS = "models"
    METADATA_NOT_CHECKED_MESSAGE = "is not checked for metadata (migrations)"
    MODELS_NOT_CHECKED_MESSAGE = "is not checked for models (admin panel)"

    @classmethod
    def get_models_metadata(cls):
        # get all metadata in the project
        # to make auto migrations work
        metadata = cls.get_items(
            target_subfolders=cls.TARGET_SUBFOLDERS,
            not_checked_message=cls.METADATA_NOT_CHECKED_MESSAGE
        )

        metadata = [item['value'].metadata for item in metadata if hasattr(item['value'], 'metadata')]  # Added ->
        # -> (if hasattr(item['value'], 'metadata')) for Enum

        return Base.metadata

    @classmethod
    def get_models(cls):
        # Get all models in the project
        # for Flask Admin
        models = cls.get_items(
            target_subfolders=cls.TARGET_SUBFOLDERS,
            not_checked_message=cls.MODELS_NOT_CHECKED_MESSAGE,
        )

        return [model['value'] for model in models]  # Added ->
        # -> isinstance(model['value'], Base)  if isinstance(model['value'], Base)
