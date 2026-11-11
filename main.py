from quiz import default_quizzes
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
        print("퀴즈 추가 준비 중입니다.")

    def list_quizzes(self) -> None:
        print("퀴즈 목록 준비 중입니다.")

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