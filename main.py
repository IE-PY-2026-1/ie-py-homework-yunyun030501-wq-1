# 파일이름 : yun_03
# 작 성 자 : yoona

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

reservations = []   # 전역: 전체 예약 목록 저장


# ── 함수 정의 ───────────────────────────────────────────────────────

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


def calculate_fee(hours, extra_fee):
    """4단계: 요금 계산 - 시간과 추가요금을 받아 요금 정보 딕셔너리 반환"""
    BASE_RATE  = 1500   # 지역 변수: 함수 안에서만 사용
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
    """5단계: 보관자 매칭 - 펫 필요 여부를 받아 매칭된 집 반환"""
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


def print_receipt(traveler_info, matched_house, fee_info, luggage_idx, is_premium):
    """6단계: 예약 확인서 출력"""
    print("\n============================")
    print("   📋 예약 확인서")
    print("============================")
    print(f"  👤 이름     : {traveler_info[0]}")
    print(f"  ✈️  여행지   : {traveler_info[1]}")
    print(f"  📱 연락처   : {traveler_info[2]}")
    print(f"  🧳 짐 종류  : {traveler_info[3]}")
    print(f"  ⏱️  보관 시간 : {traveler_info[4]}시간")
    print()
    print("  💰 요금 내역")
    print(f"     기본 요금  : {fee_info['base_rate']:,}원 × {traveler_info[4]}시간 = {fee_info['base_total']:,.0f}원")
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
    print()
    print(f"  📌 저장된 여행자 정보 리스트:")
    print(f"     {traveler_info}")
    print("============================")
    print("  예약이 완료되었습니다! 즐거운 여행 되세요 🛫")
    print("============================")


def add_reservation():
    """예약 입력 전체 흐름 - global reservations에 결과 저장"""
    global reservations   # 전역 변수 사용 선언

    traveler_info  = get_traveler_info()
    luggage_choice = select_luggage()

    luggage_idx  = luggage_choice - 1
    luggage_type = luggage_menu[luggage_idx]
    traveler_info.append(luggage_type)

    hours = float(input("\n[3단계] 보관 시간을 입력하세요 (시간 단위, 예: 2.5): "))
    traveler_info.append(hours)

    extra_fee     = extra_fees[luggage_idx]
    fee_info      = calculate_fee(hours, extra_fee)

    needs_pet     = (luggage_choice == 2) or (luggage_choice == 4)
    matched_house = match_house(needs_pet)
    is_premium    = needs_pet and (hours >= 4)

    print_receipt(traveler_info, matched_house, fee_info, luggage_idx, is_premium)

    reservations.append({
        "traveler": traveler_info,
        "house":    matched_house[0],
        "fee":      fee_info["total_fee"],
    })


def show_reservations():
    """전체 예약 목록 조회"""
    print("\n============================")
    print("   📋 전체 예약 목록")
    print("============================")
    if not reservations:
        print("  등록된 예약이 없습니다.")
    else:
        for i, r in enumerate(reservations, 1):
            t = r["traveler"]
            print(f"  [{i}] {t[0]} | {t[1]} | {t[3]} {t[4]}시간 | {r['fee']:,.0f}원 | 보관자: {r['house']}")
    print("============================")


def show_analysis():
    """예약 통계 분석 출력"""
    print("\n============================")
    print("   📊 예약 분석")
    print("============================")
    total = len(reservations)
    print(f"  총 예약 건수 : {total}건")
    if total > 0:
        fees = [r["fee"] for r in reservations]
        avg_fee = sum(fees) / total
        print(f"  평균 요금    : {avg_fee:,.0f}원")
        print(f"  최고 요금    : {max(fees):,.0f}원")
        print(f"  최저 요금    : {min(fees):,.0f}원")
    print("============================")


# ── 메인 루프 ───────────────────────────────────────────────────────

print("============================")
print("   🧳 짐봐줘 매칭 시스템 V3.0")
print("============================")

while True:
    print("\n[메인 메뉴]")
    print("  1. 예약 입력")
    print("  2. 예약 조회")
    print("  3. 분석")
    print("  4. 종료")

    menu = input("  번호를 선택하세요: ").strip()

    if menu == "1":
        add_reservation()
    elif menu == "2":
        show_reservations()
    elif menu == "3":
        show_analysis()
    elif menu == "4":
        print("\n  👋 프로그램을 종료합니다. 감사합니다!")
        break
    else:
        print("  ⚠️  1~4 중 하나를 입력해주세요.")
