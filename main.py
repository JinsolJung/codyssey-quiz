from quiz import Quiz, default_quizzes
def read_number(prompt: str, minimum: int, maximum: int) -> int:
    while True:
        try:
            number = int(input(prompt).strip())
        except ValueError:
            pass
        else:
            if minimum <= number <= maximum:
                return number
        print(f"{minimum}~{maximum} 사이의 숫자를 입력하세요.")

def read_text(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("입력을 비워 둘 수 없습니다.")

class QuizGame:
    """메뉴와 게임 상태를 관리한다."""

    def __init__(self):
        self.quizzes = default_quizzes()

    def show_menu(self) -> None:
        print("\n=== Python 기초 퀴즈 ===")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")

    def run(self) -> None:
        try:
            while True:
                self.show_menu()
                selected = read_number("선택: ", 1, 5)
                if selected == 1:
                    self.play()
                elif selected == 2:
                    self.add_quiz()
                elif selected == 3:
                    self.list_quizzes()
                elif selected == 4:
                    self.show_score()
                else:
                    break
        except (KeyboardInterrupt, EOFError):
            print("\n입력이 종료되었습니다.")
        print("퀴즈 게임을 종료합니다.")

    def play(self) -> None:
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        correct = 0
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"\n[문제 {number}]")
            quiz.display()
            selected = read_number("정답 번호 (1~4): ", 1, 4)
            if quiz.is_correct(selected):
                correct += 1
                print("정답입니다!")
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

        print(f"\n결과: {len(self.quizzes)}문제 중 {correct}문제 정답")

    def add_quiz(self) -> None:
        question = read_text("문제: ")
        choices = [read_text(f"선택지 {number}: ") for number in range(1, 5)]
        answer = read_number("정답 번호 (1~4): ", 1, 4)

        self.quizzes.append(Quiz(question, choices, answer))
        print("퀴즈를 추가했습니다.")

    def list_quizzes(self) -> None:
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"{number}. {quiz.question}")

    def show_score(self) -> None:
        print("점수 확인 준비 중입니다.")

        
def show_menu() -> None:
    print("\n=== Python 기초 퀴즈 ===")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")


if __name__ == "__main__":
    QuizGame().run()