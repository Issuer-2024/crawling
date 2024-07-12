import os
from datetime import datetime
import csv
import logging

logger = logging.getLogger(__name__)
job_logger = logging.getLogger('job_logger')
import traceback

class FileManager:

    def __init__(self):
        self.schema = {
            'ISSUE': ['문서 번호', '상위 플랫폼', '하위 플랫폼', '순위',
                      '제목', 'URL', '조회수', '제목', '내용', '작성자',
                      '추천 수', '비추천 수', '댓글 수', '작성 시간'],
            'ISSUE_COMMENTS': ['문서 번호', '작성자', '내용', '추천 수', '비추천 수', '대댓글 수', '작성 시간']}

    def save(self, data, main_type, sub_type):
        (logger.info
         (f"[COLLECTED DATA] {data}"))
        if not data:
            return

        try:
            current_datetime = datetime.now().strftime("%Y-%m-%d_%H-00-00")
            base_dir = os.getenv('DIR_CRAWLING_DATA')
            if not os.path.exists(f'{base_dir}/{current_datetime}/{main_type}'):
                os.makedirs(f'{base_dir}/{current_datetime}/{main_type}')
            base_dir = f'{base_dir}/{current_datetime}/{main_type}'
            filename = f'{base_dir}/{sub_type}_ISSUE.csv' if main_type != 'ISSUE_COMMENTS' else f'{base_dir}/{sub_type}/' + \
                                                                                                data[0][
                                                                                                    '문서 번호'] + '_COMMENTS.csv'

            file_exists = os.path.exists(filename)

            with open(filename, mode='a', newline='', encoding='utf-8') as file:  # 'a' 모드로 열어 파일에 추가
                writer = csv.writer(file)

                # 파일이 존재 하지 않으면 스키마 작성
                if not file_exists:
                    writer.writerow(
                        self.schema[main_type])

                if isinstance(data, list):

                    for row in data:
                        tmp = []
                        for col in self.schema[main_type]:
                            tmp.append(row[col])
                        writer.writerow(tmp)

                if isinstance(data, dict):
                    row = []
                    for col in self.schema[main_type]:
                        row.append(data[col])
                    writer.writerow(row)
        except Exception as e:
            logger.error(e)
            traceback.print_exc()

    def load(self, path):
        pass

    def delete(self):
        pass
