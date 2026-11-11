import json
from pathlib import Path
from tempfile import NamedTemporaryFile

from quiz import Quiz, default_quizzes
STATE_PATH = Path(__file__).resolve().parent / "state.json"

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
        self.best_score: int | None = None
        self.needs_save = False

    def show_menu(self) -> None:
        print("\n=== Python 기초 퀴즈 ===")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")

    def run(self) -> None:
        try:
            self.load_state()
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
        finally:
            if self.needs_save:
                self.save_state()
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
        if self.best_score is None or correct > self.best_score:
            self.needs_save = True
            self.best_score = correct
            print("새 최고 기록입니다!")
            self.save_state()
        self.best_score = correct
        print("새 최고 기록입니다!")

    def add_quiz(self) -> None:
        question = read_text("문제: ")
        choices = [read_text(f"선택지 {number}: ") for number in range(1, 5)]
        answer = read_number("정답 번호 (1~4): ", 1, 4)

        self.needs_save = True
        self.quizzes.append(Quiz(question, choices, answer))
        if self.save_state():
            print("퀴즈를 추가하고 저장했습니다.")
        else:
            print("이번 실행에서는 추가한 퀴즈를 사용할 수 있습니다.")

    def list_quizzes(self) -> None:
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"{number}. {quiz.question}")

    def show_score(self) -> None:
        if self.best_score is None:
            print("아직 퀴즈를 풀지 않았습니다.")
        else:
            print(f"최고 기록: {self.best_score}개 정답")

        
    def load_state(self) -> None:
        try:
            state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
            if not isinstance(state, dict) or not isinstance(state.get("quizzes"), list):
                raise ValueError("quizzes 목록이 필요합니다.")
            best_score = state["best_score"]
            if best_score is not None and (type(best_score) is not int or best_score < 0):
                raise ValueError("best_score는 null 또는 0 이상의 정수여야 합니다.")
            quizzes = [
                Quiz(item["question"], item["choices"], item["answer"])
                for item in state["quizzes"]
            ]
        except FileNotFoundError:
            self.needs_save = True
        except OSError as error:
            print(f"state.json을 읽을 수 없습니다. 기본 퀴즈를 사용합니다. ({error})")
        except (ValueError, KeyError, TypeError, RecursionError):
            print("state.json이 손상되었습니다. 기본 퀴즈로 복구합니다.")
            self.needs_save = True
        else:
            self.quizzes = quizzes
            self.best_score = best_score

    def save_state(self) -> bool:
        state = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        temporary_path = None
        try:
            # 쓰기가 끝난 파일로 교체해 도중에 기존 JSON이 잘리는 일을 막는다.
            with NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=STATE_PATH.parent,
                prefix=".state-", suffix=".tmp", delete=False,
            ) as file:
                temporary_path = Path(file.name)
                json.dump(state, file, ensure_ascii=False, indent=2)
                file.write("\n")
            temporary_path.replace(STATE_PATH)
        except (OSError, UnicodeError) as error:
            print(f"state.json에 저장할 수 없습니다. ({error})")
            return False
        finally:
            if temporary_path is not None:
                try:
                    temporary_path.unlink(missing_ok=True)
                except OSError as error:
                    print(f"임시 파일을 정리할 수 없습니다. ({error})")

        self.needs_save = False
        return True

def show_menu() -> None:
    print("\n=== Python 기초 퀴즈 ===")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")

if __name__ == "__main__":
    QuizGame().run()