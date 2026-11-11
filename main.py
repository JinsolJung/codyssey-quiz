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

        
def show_menu() -> None:
    print("\n=== Python 기초 퀴즈 ===")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")


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