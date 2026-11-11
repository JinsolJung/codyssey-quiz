# Python 퀴즈 게임을 한 단계씩 만들기

터미널은 `codyssey`에 둔 채 편집기에서 `quiz-game` 안의 파일을 편집합니다. 코드 블록마다 지정한 위치에 코드를 넣고 저장하세요. 실행 결과가 예상과 같으면 그 단계의 커밋 명령을 실행합니다.

## 1. 현재 저장소 확인

```bash
cd /Users/hanseokjin/Desktop/project/codyssey
pwd
git rev-parse --show-toplevel
git status --short --branch
git remote -v
python3 --version
```

두 경로 모두 `/Users/hanseokjin/Desktop/project/codyssey`여야 합니다. 현재 저장소의 `main` 브랜치와 `origin`을 그대로 사용합니다. `quiz-game`은 이 저장소 안의 프로젝트 폴더입니다. Python 3.10 이상이 필요합니다.

`README.md`가 새 파일로 준비되어 있다면 내용과 필수 소제목 6개를 확인한 뒤 먼저 커밋합니다. README가 이미 커밋되어 있으면 이 명령은 건너뜁니다.

```bash
git diff --cached -- quiz-game/README.md
git add -- quiz-game/README.md
git commit --only -m "Docs: 퀴즈 프로젝트 README 추가" -- quiz-game/README.md
git push origin main
```

이후의 `git commit --only ... -- 파일`도 표시된 경로의 변경만 커밋합니다. 브랜치를 병합할 6단계 전에는 다른 작업에서 스테이징한 변경이 있는지 `git status --short`로 확인하세요.

## 2. main.py 만들기 · 메뉴와 입력 처리

**새 파일 `quiz-game/main.py`**에 아래 세 블록을 순서대로 씁니다.

먼저 숫자 입력 함수입니다. `strip()`은 앞뒤 공백을 없애고, 숫자로 바꿀 수 없거나 범위를 벗어나면 `while`이 다시 입력을 받습니다.

```python
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
```

빈 줄 두 개를 두고 메뉴를 출력하는 함수를 추가합니다.

```python
def show_menu() -> None:
    print("\n=== Python 기초 퀴즈 ===")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
```

그 아래에 메뉴 반복과 실행 진입점을 추가합니다.

```python
def run() -> None:
    try:
        while True:
            show_menu()
            selected = read_number("선택: ", 1, 5)
            if selected == 5:
                break
            print("준비 중인 기능입니다.")
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 종료되었습니다.")
    print("퀴즈 게임을 종료합니다.")


if __name__ == "__main__":
    run()
```

**실행** `python3 quiz-game/main.py`를 실행합니다. `abc`, `9`, 빈 Enter는 각각 안내 후 다시 입력을 받습니다. ` 5 `는 종료됩니다. 다시 실행한 뒤 `Ctrl+C`를 눌러 종료 안내도 확인합니다.

```bash
git add -- quiz-game/main.py
git commit --only -m "Feat: 콘솔 메뉴와 숫자 입력 구현" -- quiz-game/main.py
```

## 3. quiz.py 만들기 · 문제 하나 표현하기

**새 파일 `quiz-game/quiz.py`**에 `Quiz` 클래스를 씁니다. `self`에 저장한 질문, 선택지, 정답 번호는 문제마다 따로 유지됩니다. `enumerate(..., start=1)`로 화면의 선택지 번호와 정답 번호를 맞춥니다.

```python
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
```

**실행** 아래에서 질문과 선택지 4개가 출력되고, 마지막 줄에 `True False`가 나와야 합니다. `PYTHONPATH=quiz-game`은 이 한 명령에서 Python이 해당 폴더의 `quiz.py`를 찾게 합니다.

```bash
PYTHONPATH=quiz-game python3 -c 'from quiz import Quiz; q = Quiz("빈 리스트는?", ["[]", "{}", "()", "0"], 1); q.display(); print(q.is_correct(1), q.is_correct(2))'
git add -- quiz-game/quiz.py
git commit --only -m "Feat: 문제를 표현하고 채점하는 Quiz 클래스 작성" -- quiz-game/quiz.py
```

## 4. quiz.py에 기본 문제 5개 추가

**`quiz.py` 맨 아래**, 클래스 바깥에 다음 함수를 추가합니다. 새로 게임을 시작할 때마다 이 함수로 `Quiz` 객체 목록을 만듭니다. 다른 주제로 바꾸면 각 질문의 정답 번호도 따로 메모해 두세요.

```python
def default_quizzes() -> list[Quiz]:
    return [
        Quiz("len([10, 20, 30])의 결과는?", ["2", "3", "4", "30"], 2),
        Quiz("input()이 반환하는 자료형은?", ["int", "bool", "str", "list"], 3),
        Quiz("빈 리스트를 만드는 표현은?", ["[]", "{}", "()", '""'], 1),
        Quiz("7 // 2의 결과는?", ["3.5", "4", "1", "3"], 4),
        Quiz("함수에서 값을 돌려줄 때 쓰는 키워드는?", ["break", "return", "print", "import"], 2),
    ]
```

**실행** 기본 문제 수로 `5`가 나와야 합니다. 아래 단계의 정답 순서는 `2 → 3 → 1 → 4 → 2`입니다.

```bash
PYTHONPATH=quiz-game python3 -c 'from quiz import default_quizzes; print(len(default_quizzes()))'
git add -- quiz-game/quiz.py
git commit --only -m "Feat: Python 기초 퀴즈 5문제 추가" -- quiz-game/quiz.py
```

## 5. main.py에 QuizGame 추가 · 게임 상태를 한곳에 두기

**`main.py` 맨 위**에 다음 줄을 추가합니다. 그 아래에 빈 줄 두 개를 둡니다.

```python
from quiz import default_quizzes
```

**`read_number()` 아래의 `def show_menu()`부터 파일 끝까지**를 아래 블록으로 교체합니다. `read_number()`는 그대로 두세요. `QuizGame.__init__()`에서 문제 목록을 준비하고, 메뉴는 번호에 따라 메서드를 호출합니다. 네 개의 준비 중 메서드는 다음 단계에서 하나씩 채웁니다.

```python
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
        print("퀴즈 풀기 준비 중입니다.")

    def add_quiz(self) -> None:
        print("퀴즈 추가 준비 중입니다.")

    def list_quizzes(self) -> None:
        print("퀴즈 목록 준비 중입니다.")

    def show_score(self) -> None:
        print("점수 확인 준비 중입니다.")


if __name__ == "__main__":
    QuizGame().run()
```

**실행** `python3 quiz-game/main.py`에서 1~4번을 누르면 각각의 준비 중 메시지가 나오고, 5번에서 종료됩니다.

```bash
git add -- quiz-game/main.py
git commit --only -m "Refactor: QuizGame에 메뉴와 문제 목록 모으기" -- quiz-game/main.py
```

## 6. 브랜치에서 퀴즈 풀기 추가

```bash
git status --short
git checkout -b feature/quiz-play
```

**`main.py`의 `QuizGame.play()` 전체**를 아래 블록으로 교체합니다. 메서드 시작 줄은 클래스 안에서 공백 4칸으로 들여씁니다. `for`는 문제 목록을 한 번 순회하고, `correct`는 맞힌 문제 수를 셉니다.

```python
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
```

**실행** `python3 quiz-game/main.py`에서 1번을 선택합니다. 첫 문제에 `0`, `abc`, 빈 Enter를 넣으면 같은 문제에서 다시 입력을 받습니다. 이어 `2 → 3 → 1 → 4 → 2`를 넣으면 `5문제 중 5문제 정답`이 표시됩니다.

```bash
git add -- quiz-game/main.py
git commit --only -m "Feat: 퀴즈 출제와 채점 구현" -- quiz-game/main.py
git checkout main
git merge --no-ff feature/quiz-play -m "Merge: 퀴즈 풀기 기능 병합"
git log --oneline --graph --all -10
```

그래프에서 퀴즈 출제 커밋이 `main`에 병합된 것을 확인합니다.

## 7. 퀴즈 추가 연결

**`main.py` 첫 줄**의 가져오기를 다음으로 교체합니다.

```python
from quiz import Quiz, default_quizzes
```

**`read_number()`와 `class QuizGame` 사이**에 입력 함수 `read_text()`를 넣습니다. 함수는 클래스 바깥에 둡니다.

```python
def read_text(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("입력을 비워 둘 수 없습니다.")
```

**`QuizGame.add_quiz()` 전체**를 교체합니다. 문제와 네 개의 선택지, 정답 번호를 모두 받은 뒤에 목록에 한 번 추가합니다.

```python
    def add_quiz(self) -> None:
        question = read_text("문제: ")
        choices = [read_text(f"선택지 {number}: ") for number in range(1, 5)]
        answer = read_number("정답 번호 (1~4): ", 1, 4)

        self.quizzes.append(Quiz(question, choices, answer))
        print("퀴즈를 추가했습니다.")
```

**실행** `python3 quiz-game/main.py`에서 2번을 선택하고 아래 데이터를 한 줄씩 입력합니다. 문제에 공백만 입력하거나 정답으로 `0`을 입력하면 다시 물어봅니다.

| 입력 | 값 |
| --- | --- |
| 문제 | 딕셔너리에서 값을 찾는 데 쓰는 것은? |
| 선택지 1 | 인덱스 |
| 선택지 2 | 키 |
| 선택지 3 | 줄 번호 |
| 선택지 4 | 파일명 |
| 정답 | 2 |

같은 실행에서 1번을 누르면 추가한 문제가 6번째로 나옵니다. 파일 저장은 10단계에서 연결합니다.

```bash
git add -- quiz-game/main.py
git commit --only -m "Feat: 문제와 선택지를 입력받아 퀴즈 추가" -- quiz-game/main.py
```

## 8. 퀴즈 목록 연결

**`main.py`의 `QuizGame.list_quizzes()` 전체**를 교체합니다.

```python
    def list_quizzes(self) -> None:
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"{number}. {quiz.question}")
```

**실행** `python3 quiz-game/main.py`에서 3번을 누르면 기본 5문제가 나옵니다. 7단계의 문제를 추가한 뒤 다시 3번을 누르면 `총 6개`와 추가한 질문이 나옵니다.

```bash
git add -- quiz-game/main.py
git commit --only -m "Feat: 퀴즈 목록과 문제 수 출력" -- quiz-game/main.py
```

## 9. 최고 기록 연결

**`main.py`의 `QuizGame.__init__()` 안**, `self.quizzes = default_quizzes()` 바로 아래에 한 줄을 추가합니다. `None`은 아직 한 판을 마친 적이 없음을 나타냅니다.

```python
        self.best_score: int | None = None
```

**`QuizGame.play()` 끝**, 결과를 출력하는 `print(...)` 바로 다음 줄에 추가합니다. 첫 기록이거나 더 많이 맞혔을 때만 값을 바꿉니다.

```python
        if self.best_score is None or correct > self.best_score:
            self.best_score = correct
            print("새 최고 기록입니다!")
```

**`QuizGame.show_score()` 전체**를 교체합니다.

```python
    def show_score(self) -> None:
        if self.best_score is None:
            print("아직 퀴즈를 풀지 않았습니다.")
        else:
            print(f"최고 기록: {self.best_score}개 정답")
```

**실행** `python3 quiz-game/main.py`에서 처음 4번을 누르면 기록이 없다고 나옵니다. 1번을 골라 5문제를 모두 맞히고 4번을 누르면 최고 기록이 5개입니다. 한 판 더 풀어 더 적게 맞혀도 5개가 유지되어야 합니다.

```bash
git add -- quiz-game/main.py
git commit --only -m "Feat: 최고 정답 수 갱신과 조회 구현" -- quiz-game/main.py
```

## 10. state.json 저장과 불러오기

### 10-1. Quiz를 JSON으로 저장할 형태로 바꾸기

**`quiz.py`의 `Quiz.is_correct()` 아래, `default_quizzes()` 위**에 아래 메서드를 추가합니다. `to_dict()`의 첫 줄은 `is_correct()`와 같은 깊이로 들여씁니다.

```python
    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }
```

### 10-2. 경로와 저장 메서드 만들기

**`main.py` 맨 위의 가져오기 한 줄**을 아래 블록으로 교체합니다. `__file__`로 경로를 계산하므로 터미널이 `codyssey`에 있어도 데이터는 `quiz-game/state.json`에 저장됩니다.

```python
import json
from pathlib import Path
from tempfile import NamedTemporaryFile

from quiz import Quiz, default_quizzes


STATE_PATH = Path(__file__).resolve().parent / "state.json"
```

**`main.py`의 `QuizGame.show_score()` 아래, 맨 끝의 `if __name__ == "__main__":` 위**에 다음 두 메서드를 추가합니다. 읽을 때 전체 데이터를 확인한 뒤에만 목록과 점수를 바꿉니다. 쓸 때는 같은 폴더의 임시 파일에 모두 쓴 뒤 `state.json`으로 교체합니다.

```python
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
```

### 10-3. 메뉴 시작과 종료에 연결하기

**`QuizGame.__init__()`의 최고 기록 초기화 아래**에 저장 대기 여부를 추가합니다.

```python
        self.needs_save = False
```

**`QuizGame.run()` 전체**를 교체합니다. 메뉴 전에 파일을 읽고, 종료 직전에 아직 저장할 변경이 있으면 저장을 시도합니다. `finally`는 5번으로 나가거나 `Ctrl+C` 또는 EOF로 입력이 끝날 때도 실행됩니다.

```python
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
```

### 10-4. 등록과 최고 기록 갱신 직후 저장하기

**`QuizGame.play()` 마지막의 `if self.best_score is None or correct > self.best_score:` 블록**을 교체합니다.

```python
        if self.best_score is None or correct > self.best_score:
            self.needs_save = True
            self.best_score = correct
            print("새 최고 기록입니다!")
            self.save_state()
```

**`QuizGame.add_quiz()`에서 정답 입력 바로 다음의 두 줄**인 `self.quizzes.append(...)`와 `print("퀴즈를 추가했습니다.")`를 아래 블록으로 교체합니다. 문제와 선택지, 정답을 읽는 앞부분은 그대로 둡니다.

```python
        self.needs_save = True
        self.quizzes.append(Quiz(question, choices, answer))
        if self.save_state():
            print("퀴즈를 추가하고 저장했습니다.")
        else:
            print("이번 실행에서는 추가한 퀴즈를 사용할 수 있습니다.")
```

### 10-5. 저장 결과 확인하고 커밋하기

| 확인 | 해 볼 일 | 예상 결과 |
| --- | --- | --- |
| 재실행 | `python3 quiz-game/main.py`로 실행해 5개를 맞히고 7단계 문제를 추가합니다. 5번으로 종료 후 다시 실행해 3번과 4번을 누릅니다. | 6문제와 최고 기록 5개가 보입니다. |
| JSON | `python3 -m json.tool --no-ensure-ascii quiz-game/state.json` | `quizzes`, `best_score`와 한글이 보입니다. |
| 입력 중 종료 | 2번에서 문제 한 줄만 입력한 뒤 `Ctrl+C`를 누릅니다. 다시 실행해 3번을 확인합니다. | 종료 안내가 보이고 미완성 문제는 목록에 없습니다. |
| EOF | `python3 quiz-game/main.py < /dev/null` | 종료 안내가 표시됩니다. |

기존 기록을 보존한 채 손상된 파일과 빈 목록을 확인하려면 아래에서 앞뒤 두 명령으로 백업과 복원을 합니다. 두 실행에서 차례대로 `3 → 5`, `1 → 3 → 5`를 입력합니다.

```bash
quiz_backup_dir="$(mktemp -d)"
cp quiz-game/state.json "$quiz_backup_dir/state.json"
printf '{' > quiz-game/state.json
python3 quiz-game/main.py
printf '%s\n' '{"quizzes":[],"best_score":null}' > quiz-game/state.json
python3 quiz-game/main.py
cp "$quiz_backup_dir/state.json" quiz-game/state.json
```

첫 실행에서는 손상 안내와 기본 5문제가 표시됩니다. 두 번째 실행에서는 1번과 3번 모두 등록된 퀴즈가 없다고 표시합니다. `git check-ignore`는 데이터 파일이 커밋 대상에서 빠져 있는지 확인합니다.

```bash
git check-ignore quiz-game/state.json
git add -- quiz-game/main.py quiz-game/quiz.py
git commit --only -m "Feat: UTF-8 JSON 저장과 복구 구현" -- quiz-game/main.py quiz-game/quiz.py
```

## 11. README 확인하고 main 푸시

**`quiz-game/README.md`**에서 아래 소제목 6개를 순서대로 확인합니다. `실행 방법`에 `codyssey` 루트에서는 `python3 quiz-game/main.py`로 실행한다는 줄을 추가합니다. 현재 `quiz-game` 안에 있을 때는 기존의 `python3 main.py`를 사용합니다.

1. 프로젝트 개요
2. 퀴즈 주제와 선정 이유
3. 실행 방법
4. 기능 목록
5. 파일 구조
6. 데이터 파일 설명

마지막 항목에는 `quiz-game/state.json`의 경로와 역할, UTF-8, `quizzes`와 `best_score`의 구조가 들어가야 합니다.

```bash
git add -- quiz-game/README.md quiz-game/GUIDE.md
git commit --only -m "Docs: codyssey 루트 실행 방법과 단계별 가이드 정리" -- quiz-game/README.md quiz-game/GUIDE.md
git push origin main
git log --oneline --graph --all
git rev-list --count --no-merges main -- quiz-game
```

마지막 숫자는 퀴즈 폴더에 영향을 준 커밋 수입니다. 초기 설정 커밋과 위 단계들을 합쳐 최소 10개인지 확인합니다. `git log` 그래프에서는 별도로 병합 커밋을 확인합니다.

## 12. clone → 수정 → push → pull

`codyssey` 루트에서 시작합니다. 아래 명령은 현재 `origin`을 읽어 `codyssey` 옆의 새 `codyssey-quiz-clone`에 복제합니다. 이미 같은 이름의 폴더가 있으면 다른 새 이름을 사용합니다.

```bash
git clone "$(git remote get-url origin)" ../codyssey-quiz-clone
cd ../codyssey-quiz-clone
python3 quiz-game/main.py
```

5번으로 종료한 뒤, **복제본의 `quiz-game/README.md` 실행 방법 항목**에 `복제본에서도 위 명령으로 실행할 수 있습니다.`를 한 줄 추가합니다. 복제본에서 `git var GIT_AUTHOR_IDENT`가 이름이나 이메일을 요구하면 `git config --local user.name "본인 이름"`과 `git config --local user.email "본인 이메일"`로 설정합니다.

```bash
git add -- quiz-game/README.md
git commit --only -m "Docs: 복제본 실행 확인 기록" -- quiz-game/README.md
git push origin main
cd /Users/hanseokjin/Desktop/project/codyssey
git pull --ff-only origin main
git log -1 --oneline
git grep -n '복제본에서도' -- quiz-game/README.md
```

원래 `codyssey`의 README에서 복제본에 쓴 줄이 검색되면 완료입니다.

## 제출 화면 확인

- [ ] `git remote get-url origin`으로 저장소 주소를 확인합니다. 제출 링크에서 GitHub 저장소와 `quiz-game` 폴더가 열리는지 확인합니다.
- [ ] 편집기와 터미널에서 Python 버전, Git 버전, 현재 브랜치가 보이는 환경 화면을 캡처합니다.
- [ ] 메뉴, 플레이 결과, 퀴즈 추가, 목록, 점수 화면을 캡처합니다. 저장소에 넣는 경우 `quiz-game/docs/screenshots/`에 `menu.png`, `play.png`, `add_quiz.png`, `list.png`, `score.png`로 저장할 수 있습니다.
- [ ] `git log --oneline --graph --all`에서 기능별 커밋과 병합이 보이는 화면을 캡처합니다.
- [ ] `init`을 직접 실행한 적이 없다면 별도 임시 폴더에서 `git init -b main`을 실행해 저장소 생성 흐름을 확인합니다. 실제 제출 저장소에서는 이미 연결된 `codyssey`를 사용합니다.
