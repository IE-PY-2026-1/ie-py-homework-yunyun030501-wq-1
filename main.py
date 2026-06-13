# 파일이름 : main.py
# 학    번 : 60232285
# 작 성 자 : 박윤아
# 짐봐줘 매칭 시스템 V3.0

# ── 전역 변수 ───────────────────────────────────────────────────────

luggage_menu = ["캐리어", "반려동물", "마트 짐", "캐리어 + 반려동물"]
extra_fees   = [500, 2000, 300, 2500]
luggage_notes = [
    "캐리어 취급 주의비",
    "반려동물 케어비",
    "마트 짐 냉장 보관비",
    "캐리어 + 반려동물 복합 요금",
]

available_houses = [
    ["김민준", "강남구", True,  4.5],
    ["이서연", "마포구", False, 4.8],
    ["박지호", "용산구", True,  4.2],
    ["최하늘", "은평구", False, 4.6],
]

# [요구사항 1] 이중 리스트(2D List) - 한 행 = 한 예약
# 구조: [이름, 여행지, 연락처, 짐종류, 시간, 최종요금, 보관자]
reservations = []

DATA_FILE = "reservations.csv"   # 저장 파일명


# ── 함수 정의 ───────────────────────────────────────────────────────

def load_reservations():
    """[요구사항: 파일 읽기] 시작 시 csv를 읽어 2D List 복원"""
    global reservations
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                # 시간(float), 요금(float)으로 형 변환하여 2D List에 누적
                row = [
                    parts[0], parts[1], parts[2], parts[3],
                    float(parts[4]), float(parts[5]), parts[6],
                ]
                reservations.append(row)
        print(f"  📂 기존 예약 {len(reservations)}건을 불러왔습니다.")
    except FileNotFoundError:
        # [요구사항 4-예외2] 파일이 없을 때
        print("  📂 저장된 예약 파일이 없어 새로 시작합니다.")
    except (ValueError, IndexError):
        print("  ⚠️  파일 형식이 올바르지 않아 일부 데이터를 건너뜁니다.")


def save_reservations():
    """[요구사항 3: 파일 저장 Write] 2D List를 csv로 저장"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for row in reservations:
            # 한 행의 각 항목을 문자열로 바꿔 콤마로 연결
            line = ",".join(str(item) for item in row)
            f.write(line + "\n")
    print(f"  💾 예약 {len(reservations)}건을 '{DATA_FILE}'에 저장했습니다.")


def get_traveler_info():
    """1단계: 여행자 정보 입력 후 리스트 반환"""
    print("\n[1단계] 여행자 정보를 입력해주세요")
    name        = input("  이름     : ")
    destination = input("  여행지   : ")
    phone       = input("  연락처   : ")
    return [name, destination, phone]


def select_luggage():
    """2단계: 짐 종류 선택 - 선택 번호(1~4) 반환"""
    print("\n[2단계] 짐 종류를 선택해주세요")
    for i, option in enumerate(luggage_menu, 1):
        print(f"  {i}. {option}  (+{extra_fees[i-1]:,}원)")

    while True:
        choice_str = input("  번호 선택 (1~4): ")
        if choice_str in ["1", "2", "3", "4"]:
            return int(choice_str)
        print("  ⚠️  1~4 중 하나를 입력해주세요.")


def input_hours():
    """3단계: 보관 시간 입력 - [요구사항 4-예외1] ValueError 처리"""
    while True:
        try:
            hours = float(input("\n[3단계] 보관 시간을 입력하세요 (시간 단위, 예: 2.5): "))
            if hours <= 0:
                print("  ⚠️  0보다 큰 숫자를 입력해주세요.")
                continue
            return hours
        except ValueError:
            print("  ⚠️  숫자만 입력해주세요. (예: 2, 3.5)")


def calculate_fee(hours, extra_fee):
    """4단계: 요금 계산 - 요금 정보 딕셔너리 반환"""
    BASE_RATE  = 1500   # 지역 변수
    base_total = BASE_RATE * hours

    if hours >= 8:
        discount_rate = 0.20
        time_note = "8시간 이상 장기 보관 → 20% 할인"
    elif hours >= 4:
        discount_rate = 0.10
        time_note = "4시간 이상 보관 → 10% 할인"
    else:
        discount_rate = 0.0
        time_note = "기본 요금 적용 (할인 없음)"

    discount_amount = (base_total + extra_fee) * discount_rate
    total_fee = (base_total + extra_fee) - discount_amount

    return {
        "base_rate":       BASE_RATE,
        "base_total":      base_total,
        "discount_rate":   discount_rate,
        "discount_amount": discount_amount,
        "total_fee":       total_fee,
        "time_note":       time_note,
    }


def match_house(needs_pet):
    """5단계: 보관자 매칭 - 펫 필요 여부로 매칭"""
    matched = None
    for house in available_houses:
        if needs_pet and house[2]:
            matched = house
            break
        elif (not needs_pet) and (not house[2]):
            matched = house
            break
    if matched is None:
        matched = available_houses[0]
    return matched


def print_receipt(name, dest, phone, luggage_type, hours,
                  matched_house, fee_info, luggage_idx, is_premium):
    """6단계: 예약 확인서 출력"""
    print("\n============================")
    print("   📋 예약 확인서")
    print("============================")
    print(f"  👤 이름     : {name}")
    print(f"  ✈️  여행지   : {dest}")
    print(f"  📱 연락처   : {phone}")
    print(f"  🧳 짐 종류  : {luggage_type}")
    print(f"  ⏱️  보관 시간 : {hours}시간")
    print()
    print("  💰 요금 내역")
    print(f"     기본 요금  : {fee_info['base_rate']:,}원 × {hours}시간 = {fee_info['base_total']:,.0f}원")
    print(f"     짐 추가비  : {luggage_notes[luggage_idx]} {extra_fees[luggage_idx]:,}원")
    print(f"     할인 적용  : {fee_info['time_note']} (-{fee_info['discount_amount']:,.0f}원)")
    print(f"     ──────────────────────────")
    print(f"     최종 금액  : {fee_info['total_fee']:,.0f}원")
    print()
    if is_premium:
        print("  ⭐ 프리미엄 케어 대상! 전담 보관자 배정")
    print(f"  🏠 매칭된 보관자 : {matched_house[0]} ({matched_house[1]})")
    print(f"     펫 가능 여부   : {'✅' if matched_house[2] else '❌'}")
    print(f"     보관자 평점    : ⭐ {matched_house[3]}")
    print("============================")
    print("  예약이 완료되었습니다! 즐거운 여행 되세요 🛫")
    print("============================")


def add_reservation():
    """예약 입력 전체 흐름 - [요구사항 1] 2D List에 append 누적"""
    global reservations

    name, dest, phone = get_traveler_info()
    luggage_choice = select_luggage()

    luggage_idx  = luggage_choice - 1
    luggage_type = luggage_menu[luggage_idx]

    hours = input_hours()

    extra_fee = extra_fees[luggage_idx]
    fee_info  = calculate_fee(hours, extra_fee)

    needs_pet  = (luggage_choice == 2) or (luggage_choice == 4)
    matched    = match_house(needs_pet)
    is_premium = needs_pet and (hours >= 4)

    print_receipt(name, dest, phone, luggage_type, hours,
                  matched, fee_info, luggage_idx, is_premium)

    # 한 행(1차원 리스트)을 2D List에 누적
    row = [name, dest, phone, luggage_type, hours,
           round(fee_info["total_fee"]), matched[0]]
    reservations.append(row)

    # 입력할 때마다 자동 저장
    save_reservations()


def show_reservations():
    """[요구사항 2] 중첩 for + 인덱싱으로 2D List 표 출력"""
    print("\n=====================================================================")
    print("   📋 전체 예약 목록")
    print("=====================================================================")
    if not reservations:
        print("  등록된 예약이 없습니다.")
        print("=====================================================================")
        return

    headers = ["No", "이름", "여행지", "짐종류", "시간", "요금", "보관자"]
    # 헤더 출력
    print(f"  {headers[0]:<3}{headers[1]:<7}{headers[2]:<7}{headers[3]:<16}"
          f"{headers[4]:<6}{headers[5]:<10}{headers[6]:<6}")
    print("  " + "-" * 63)

    # 바깥 for = 행(예약), 안쪽 for = 열(항목) → 중첩 for + 인덱싱
    for i in range(len(reservations)):
        row = reservations[i]
        cells = [
            str(i + 1),
            row[0],            # 이름
            row[1],            # 여행지
            row[3],            # 짐종류
            f"{row[4]}h",      # 시간
            f"{row[5]:,.0f}원",  # 요금
            row[6],            # 보관자
        ]
        line = "  "
        widths = [3, 7, 7, 16, 6, 10, 6]
        for j in range(len(cells)):
            line += f"{cells[j]:<{widths[j]}}"
        print(line)
    print("=====================================================================")


def show_analysis():
    """예약 통계 분석 출력"""
    print("\n============================")
    print("   📊 예약 분석")
    print("============================")
    total = len(reservations)
    print(f"  총 예약 건수 : {total}건")
    if total > 0:
        # 요금은 각 행의 5번 인덱스
        fees = [row[5] for row in reservations]
        avg_fee = sum(fees) / total
        print(f"  평균 요금    : {avg_fee:,.0f}원")
        print(f"  최고 요금    : {max(fees):,.0f}원")
        print(f"  최저 요금    : {min(fees):,.0f}원")

        # 짐 종류별 건수 통계
        print("\n  [짐 종류별 예약 건수]")
        for menu_name in luggage_menu:
            count = sum(1 for row in reservations if row[3] == menu_name)
            bar = "■" * count
            print(f"    {menu_name:<16}: {count}건 {bar}")
    print("============================")


# ── 메인 루프 ───────────────────────────────────────────────────────

print("============================")
print("   🧳 짐봐줘 매칭 시스템 V3.0")
print("============================")

load_reservations()   # 시작 시 기존 예약 불러오기

while True:
    print("\n[메인 메뉴]")
    print("  1. 예약 입력")
    print("  2. 예약 조회")
    print("  3. 분석")
    print("  4. 종료 (저장)")

    menu = input("  번호를 선택하세요: ").strip()

    if menu == "1":
        add_reservation()
    elif menu == "2":
        show_reservations()
    elif menu == "3":
        show_analysis()
    elif menu == "4":
        save_reservations()
        print("\n  👋 프로그램을 종료합니다. 감사합니다!")
        break
    else:
        print("  ⚠️  1~4 중 하나를 입력해주세요.")


