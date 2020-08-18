import logging

LOGGER = logging.getLogger(__name__)

DEFAULT_SETTINGS = [
    "CHOICES_SEPARATOR",
    "USER_DID_NOT_ANSWER",
    "TEX_CONFIGURATION_FILE",
    "SURVEY_DEFAULT_PIE_COLOR",
    "EXCEL_COMPATIBLE_CSV",
    "DEFAULT_SURVEY_PUBLISHING_DURATION",
]


def set_default_settings():
    try:
        from . import settings

        for setting in dir(settings):
            if setting in DEFAULT_SETTINGS:
                if not hasattr(settings, setting):
                    setattr(settings, setting, getattr(settings, setting))
                LOGGER.info("Settings '%s' as the default ('%s')", setting, getattr(settings, setting))
    except ImportError:
        pass


set_default_settings()
