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

        # # TODO Estimate transfer speed during download not after
        # print(f'MB total size = {size}')
        # print(f'GB total size = {size / (1024 * 1024 * 1024)}')
        #
        # print(f'MB total sent = {sent / (1024 * 1024)}')
        # print(f'GB total sent = {sent / (1024 * 1024 * 1024)}')
        #
        # chunk_diff = sent - cls.chunk
        # chunk_diff = chunk_diff / (1024 * 1024)             # MB size
        # print(f'chunk diff MB = {chunk_diff}')
        #
        # time_diff = time.time() - cls.start
        # print(f'time diff = {time_diff}')
        #
        # # try:
        # #     if time_diff < 1:
        # #         time_diff = 1 / time_diff
        # #
        # # except ZeroDivisionError as e:
        # #     print(e)
        #
        # # try:
        # #     if chunk_diff < 1:
        # #         chunk_diff = 1 / chunk_diff
        # # except ZeroDivisionError as e:
        # #     print(e)
        #
        # print(f'speed {chunk_diff * (1 / time_diff)} MB/s')
        #
        # cls.start = time.time()
        # cls.chunk = sent