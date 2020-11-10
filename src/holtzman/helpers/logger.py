import logging
import pathlib
import sys


class HumanReadableFormatter(logging.Formatter):
    def __init__(self):
        super(HumanReadableFormatter, self).__init__()

    def format(self, record: logging.LogRecord) -> str:
        record_extra = getattr(record, "with", None)
        more = ""
        if record_extra is not None:
            more = f": {record_extra}"

        return f"({self.formatTime(record, self.datefmt)}) [{record.levelname}] => {record.getMessage()}{more}"


class LogHandler:
    def __init__(
        self, process_name: str, file_path: pathlib.Path = None, level: str = "DEBUG"
    ):
        self._log_path = file_path
        self._logger = self._create_logger(level)
        self._handlers = dict()

        self.set_handler(process_name, handler_dest=sys.stdout)
        if file_path is not None:
            self.set_handler(f"{process_name}_file", handler_dest=file_path)

    @property
    def log_path(self) -> pathlib.Path:
        return self._log_path

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @staticmethod
    def _create_logger(level: str) -> logging.Logger:
        logger = logging.getLogger("HOLTZMAN")
        logger.setLevel(level)
        return logger

    def set_handler(self, handler_name: str, handler_dest: (pathlib.Path, sys.stdout)) -> None:
        if isinstance(handler_dest, pathlib.Path):
            handler = logging.FileHandler(handler_dest)
        else:
            handler = logging.StreamHandler(handler_dest)
        handler.setFormatter(HumanReadableFormatter())

        self._logger.addHandler(handler)
        self._handlers[handler_name] = handler

    def debug(self, message: str, *args, **kwargs) -> None:
        self._logger.debug(message, *args, extra={"with": kwargs})

    def info(self, message: str, *args, **kwargs) -> None:
        self._logger.info(message, *args, extra={"with": kwargs})

    def warn(self, message: str, *args, **kwargs) -> None:
        self._logger.warning(message, *args, extra={"with": kwargs})

    def error(self, message: str, *args, **kwargs) -> None:
        self._logger.error(message, *args, extra={"with": kwargs})
