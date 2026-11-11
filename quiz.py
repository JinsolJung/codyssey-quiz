class Quiz:
    """문제 하나와 선택지, 정답을 관리한다."""

    def __init__(self, question: str, choices: list[str], answer: int):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 비어 있지 않은 문자열이어야 합니다.")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 4개여야 합니다.")
        if any(not isinstance(choice, str) or not choice.strip() for choice in choices):
            raise ValueError("선택지는 비어 있지 않은 문자열이어야 합니다.")
        if type(answer) is not int or not 1 <= answer <= 4:
            raise ValueError("정답은 1~4 사이의 정수여야 합니다.")

        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self) -> None:
        print(self.question)
        for number, choice in enumerate(self.choices, start=1):
            print(f"  {number}. {choice}")

    def is_correct(self, selected: int) -> bool:
        return selected == self.answer

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }


def default_quizzes() -> list[Quiz]:
    return [
        Quiz("len([10, 20, 30])의 결과는?", ["2", "3", "4", "30"], 2),
        Quiz("input()이 반환하는 자료형은?", ["int", "bool", "str", "list"], 3),
        Quiz("빈 리스트를 만드는 표현은?", ["[]", "{}", "()", '""'], 1),
        Quiz("7 // 2의 결과는?", ["3.5", "4", "1", "3"], 4),
        Quiz("함수에서 값을 돌려줄 때 쓰는 키워드는?", ["break", "return", "print", "import"], 2),
    ]