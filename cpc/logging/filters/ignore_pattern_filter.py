import logging
import re


class IgnorePatternFilter(logging.Filter):
    def __init__(self, pattern):
        super().__init__()
        self.pattern = re.compile(pattern)

    def filter(self, record):
        return not self.pattern.search(record.getMessage())
