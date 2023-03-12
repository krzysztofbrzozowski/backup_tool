"""
@author:    Krzysztof Brzozowski
@file:      display_manager
@time:      04/03/2023
@desc:      
"""
import logging


class DisplayManager:
    @classmethod
    def progress(cls, filename, size, sent):
        progress = float(sent) / float(size) * 100
        try:
            logging.info(f'file: {filename if isinstance(filename, str) else filename.decode()} progress: {progress:.2f}%')
        except Exception as e:
            logging.error(e)