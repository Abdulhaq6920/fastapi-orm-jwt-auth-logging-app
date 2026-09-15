import json
import logging
import sys
from logging.handlers import RotatingFileHandler
from datetime import datetime, timezone
from pathlib import Path


class StructuredFormatter(logging.Formatter):

    STANDARD_FIELDS = {
        "name",
        "msg",
        "args",
        "levelname",
        "levelno",
        "pathname",
        "filename",
        "module",
        "exc_info",
        "exc_text",
        "stack_info",
        "lineno",
        "funcName",
        "created",
        "msecs",
        "relativeCreated",
        "thread",
        "threadName",
        "processName",
        "process",
        "message",
        "asctime",
    }

    def format(self, record: logging.LogRecord) -> str:

        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "line":record.lineno,
        }

        for key, value in record.__dict__.items():
            if key not in self.STANDARD_FIELDS:
                log_data[key] = value

        if record.exc_info:
            log_data["exception"] = self.formatException(
                record.exc_info
            )

        return json.dumps(
            log_data,
            default=str
        )


def setup_logging():

    log_directory = Path("logs")
    log_directory.mkdir(exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)


    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(
        StructuredFormatter()
    )


    file_handler = RotatingFileHandler(
        filename=log_directory / "app.log",
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding="utf-8"
    )

    file_handler.setFormatter(
        StructuredFormatter()
    )

    root_logger.handlers.clear()

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)