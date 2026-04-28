# 파일이름 :yun_02
# 작 성 자 :yoona
uggage_menu = [“캐리어”, “반려동물”, “마트 짐”, “캐리어 + 반려동물”]

available_houses = [
[“김민준”, “강남구”, True,  4.5],   # [이름, 지역, 펫가능여부, 평점]
[“이서연”, “마포구”, False, 4.8],
[“박지호”, “용산구”, True,  4.2],
[“최하늘”, “은평구”, False, 4.6],
]

# 짐 종류별 추가 요금 리스트 (인덱스 0~3이 luggage_menu와 대응)

extra_fees    = [500, 2000, 300, 2500]
luggage_notes = [
“캐리어 취급 주의비”,
“반려동물 케어비”,
“마트 짐 냉장 보관비”,
“캐리어 + 반려동물 복합 요금”,
]

# ── 프로그램 시작 ───────────────────────────────────────────────────

print(”============================”)
print(”   🧳 짐봐줘 매칭 시스템 V2.0”)
print(”============================”)

# ── 1단계: 여행자 정보 입력 → 리스트에 저장 ────────────────────────

print(”\n[1단계] 여행자 정보를 입력해주세요”)
name        = input(”  이름     : “)
destination = input(”  여행지   : “)
phone       = input(”  연락처   : “)

traveler_info = [name, destination, phone]   # 리스트에 저장

# ── 2단계: 짐 종류 선택 ────────────────────────────────────────────

print(”\n[2단계] 짐 종류를 선택해주세요”)
for i, option in enumerate(luggage_menu, 1):
print(f”  {i}. {option}  (+{extra_fees[i-1]:,}원)”)

while True:
choice_str = input(”  번호 선택 (1~4): “)
if choice_str in [“1”, “2”, “3”, “4”]:
luggage_choice = int(choice_str)
break
print(”  ⚠️  1~4 중 하나를 입력해주세요.”)

luggage_idx  = luggage_choice - 1            # 0-based 인덱스
luggage_type = luggage_menu[luggage_idx]
extra_fee    = extra_fees[luggage_idx]
traveler_info.append(luggage_type)           # 리스트에 추가

# ── 3단계: 보관 시간 입력 ──────────────────────────────────────────

hours = float(input(”\n[3단계] 보관 시간을 입력하세요 (시간 단위, 예: 2.5): “))
traveler_info.append(hours)                  # 리스트에 추가

# ── 4단계: 요금 계산 (조건문) ──────────────────────────────────────

BASE_RATE = 1500   # 시간당 기본 요금 (원)
base_total = BASE_RATE * hours

# 보관 시간에 따른 할인율

if hours >= 8:
discount_rate = 0.20
time_note = “8시간 이상 장기 보관 → 20% 할인”
elif hours >= 4:
discount_rate = 0.10
time_note = “4시간 이상 보관 → 10% 할인”
else:
discount_rate = 0.0
time_note = “기본 요금 적용 (할인 없음)”

discount_amount = (base_total + extra_fee) * discount_rate
total_fee = (base_total + extra_fee) - discount_amount

# ── 5단계: 보관자 매칭 (조건문 + and/or) ──────────────────────────

needs_pet = (luggage_choice == 2) or (luggage_choice == 4)   # 반려동물 포함 여부

matched_house = None
for house in available_houses:
# 반려동물이 필요하면 펫 가능 집만 / 아니면 아무 집이나 OK
if needs_pet and house[2]:          # and 연산자
matched_house = house
break
elif (not needs_pet) and (not house[2]):   # 일반 짐은 일반 집 우선
matched_house = house
break

# 매칭 실패 시 첫 번째 집으로 대체

if matched_house is None:
matched_house = available_houses[0]

# 프리미엄 케어 조건: 반려동물 포함 AND 4시간 이상

is_premium = needs_pet and (hours >= 4)

# ── 6단계: 예약 확인서 출력 ───────────────────────────────────────

print(”\n============================”)
print(”   📋 예약 확인서”)
print(”============================”)
print(f”  👤 이름     : {traveler_info[0]}”)
print(f”  ✈️  여행지   : {traveler_info[1]}”)
print(f”  📱 연락처   : {traveler_info[2]}”)
print(f”  🧳 짐 종류  : {traveler_info[3]}”)
print(f”  ⏱️  보관 시간 : {traveler_info[4]}시간”)
print()
print(”  💰 요금 내역”)
print(f”     기본 요금  : {BASE_RATE:,}원 × {hours}시간 = {base_total:,.0f}원”)
print(f”     짐 추가비  : {luggage_notes[luggage_idx]} {extra_fee:,}원”)
print(f”     할인 적용  : {time_note} (-{discount_amount:,.0f}원)”)
print(f”     ──────────────────────────”)
print(f”     최종 금액  : {total_fee:,.0f}원”)
print()

if is_premium:
print(”  ⭐ 프리미엄 케어 대상! 전담 보관자 배정”)

print(f”  🏠 매칭된 보관자 : {matched_house[0]} ({matched_house[1]})”)
print(f”     펫 가능 여부   : {‘✅’ if matched_house[2] else ‘❌’}”)
print(f”     보관자 평점    : ⭐ {matched_house[3]}”)
print()
print(f”  📌 저장된 여행자 정보 리스트:”)
print(f”     {traveler_info}”)
print(”============================”)
print(”  예약이 완료되었습니다! 즐거운 여행 되세요 🛫”)
print(”============================”)
