from abc import ABC


class FileManager(ABC):

    def __init__(self):
        self.schema = {
            'ISSUE': ['문서 번호', '상위 플랫폼', '하위 플랫폼', '순위',
                      '제목', 'URL', '조회수', '제목', '내용', '작성자',
                      '추천 수', '비추천 수', '댓글 수', '작성 시간'],
            'ISSUE_COMMENTS': ['문서 번호', '작성자', '내용', '추천 수', '비추천 수', '대댓글 수', '작성 시간']}