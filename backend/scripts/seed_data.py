import asyncio
from sqlalchemy import select, func
from datetime import date, datetime, timedelta, time
from faker import Faker
import random
import json
from core.database import AsyncSessionLocal
from shared.utils import hash_password
from models import Base, User, Room, Equipment, RoomEquipment, Slot, Booking, Ticket, AILog, RefreshToken

fake = Faker("vi_VN")

async def seed_users(session):
    count = (await session.execute(select(func.count(User.id)))).scalar()
    if count and count > 0:
        print(f"Đã có ({count} users) người dùng")
        return
    users_to_add = []
    user_groups = [
        {"count": 2, "prefix": "ADMIN", "role": "admin", "password": "Admin@123456", "email_suffix": "smartcampus.edu.vn"},
        {"count": 23, "prefix": "LEC", "role": "lecturer", "password": "Lec@123456", "email_suffix": "smartcampus.edu.vn"},
        {"count": 100, "prefix": "SV", "role": "student", "password": "Student@123456", "email_suffix": "student.edu.vn"}
    ]
    for group in user_groups:
        if group["role"] == "student":
            min_age, max_age = 18, 22
        elif group["role"] == "admin":
            min_age, max_age = 25, 40
        else:
            min_age, max_age = 30, 60
        for i in range(1, group["count"] + 1):
            gender = random.choice(["Nam", "Nữ"])
            if gender == "Nam":
                first_name = fake.first_name_male()
                # Faker vi_VN thường dùng prefix cho các từ như 'Văn', 'Hữu', 'Đình'
                middle_name = random.choice(["Văn", "Hữu", "Đình", "Quang", "Minh"]) 
                last_name = fake.last_name_male()
            else:
                first_name = fake.first_name_female()
                middle_name = "Thị" # Hoặc random.choice(["Thị", "Ngọc", "Kiều"])
                last_name = fake.last_name_female()
            full_name = f"{last_name} {middle_name} {first_name}"
            if group["role"] == "student":
                year = 2020 + random.randint(0, 4)
                external_id = f"{group['prefix']}{year}{i:04d}"
            else:
                external_id = f"{group['prefix']}{i:03d}"
            users_to_add.append(User(
                external_id=external_id,
                full_name=full_name,
                gender=gender,
                role=group["role"],
                date_of_birth=fake.date_of_birth(minimum_age=min_age, maximum_age=max_age),
                email=f"{group['role']}{i}_{random.randint(100, 999)}@{group['email_suffix']}",
                phone=f"0{random.randint(300000000, 999999999)}",
                password_hash=hash_password(group["password"]),
                is_active=True,
                created_at=datetime.now(),
                updated_at=datetime.now()
            ))
    session.add_all(users_to_add)
    await session.commit()
async def seed_rooms(session):
    count = (await session.execute(select(func.count(Room.id)))).scalar()
    if count and count > 0:
        print(f"Dữ liệu phòng đã tồn tại ({count} rooms). Bỏ qua bước seed.")
        return
    rooms_to_add = []
    buildings = {
        "A": {"floors": 5, "rooms_per_floor": 4, "type": "class", "base_capacity": 50},
        "B": {"floors": 3, "rooms_per_floor": 3, "type": "lab", "base_capacity": 30},
        "C": {"floors": 2, "rooms_per_floor": 2, "type": "sport", "base_capacity": 100}
    }
    status_options = ["available", "maintenance", "inactive"]
    for b_name, config in buildings.items():
        building_label = f"Tòa {b_name}"
        for floor in range(1, config["floors"] + 1):
            for r_idx in range(1, config["rooms_per_floor"] + 1):
                room_number = f"{b_name}{floor}{r_idx:02d}"
                capacity = config["base_capacity"] + random.choice([-10, -5, 0, 5, 10, 20])
                status = random.choices(status_options, weights=[80, 15, 5], k=1)[0]
                rooms_to_add.append(
                    Room(
                        room_number=room_number,
                        name=f"Phòng {config['type'].upper()} {room_number}",
                        type=config["type"],
                        status=status,
                        capacity=capacity,
                        floor=floor,
                        building=building_label,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                )
    session.add_all(rooms_to_add)
    await session.commit()
async def seed_equipments(session):
    count = (await session.execute(select(func.count(Equipment.id)))).scalar()
    if count and count > 0:
        print(f"Dữ liệu phòng đã tồn tại ({count} rooms). Bỏ qua bước seed.")
        return
    equipments_to_add = []
    equipment_meta = {
        "projector": {
            "prefix": "PROJ", "name": "Máy chiếu", "count": 20,
            "brands": ["Panasonic", "Sony", "Epson", "ViewSonic"],
            "specs": ["Độ phân giải 4K", "Cổng kết nối HDMI/VGA", "Độ sáng 4000 Lumens"]
        },
        "ac": {
            "prefix": "AC", "name": "Điều hòa", "count": 40,
            "brands": ["Daikin", "Panasonic", "LG", "Samsung"],
            "specs": ["Inverter tiết kiệm điện", "Công suất 18000 BTU", "Khử khuẩn Nano"]
        },
        "computer": {
            "prefix": "COMP", "name": "Máy tính", "count": 100,
            "brands": ["Dell", "HP", "Lenovo", "Asus"],
            "specs": ["CPU Core i7", "RAM 16GB", "SSD 512GB", "Monitor 24 inch"]
        },
        "speaker": {
            "prefix": "SPK", "name": "Loa âm trần", "count": 30,
            "brands": ["Bose", "JBL", "TOA", "Yamaha"],
            "specs": ["Công suất 30W", "Tần số 80Hz-20kHz", "Độ nhạy 90dB"]
        }
    }
    status_options = ["active", "maintenance", "broken"]
    status_weights = [85, 10, 5]
    for e_type, config in equipment_meta.items():
        for i in range(1, config["count"] + 1):
            code = f"{config['prefix']}-{i:03d}"
            status = random.choices(status_options, weights=status_weights, k=1)[0]
            brand = random.choice(config["brands"])
            spec = random.choice(config["specs"])
            usage_steps = [
                f"Bước 1: Kiểm tra nguồn điện và cáp kết nối của {config['name']}.",
                f"Bước 2: Nhấn nút nguồn trên thiết bị hoặc điều khiển từ xa.",
                f"Bước 3: Chọn nguồn tín hiệu đầu vào (Input) phù hợp.",
                f"Bước 4: Điều chỉnh thông số {spec.lower()} để đạt hiệu quả tốt nhất.",
                f"Lưu ý: Nếu có sự cố, hãy báo ngay cho kỹ thuật qua mã {code}."
            ]
            equipments_to_add.append(
                Equipment(
                    name=f"{config['name']} {brand} {i:03d}",
                    code=code,
                    type=e_type,
                    status=status,
                    description=(
                        f"Thiết bị: {config['name']}. Thương hiệu: {brand}. "
                        f"Model: {fake.bothify('??-####').upper()}. "
                        f"Thông số: {spec}. Tình trạng vật lý: {fake.word()}."
                    ),
                    usage_guide="\n".join(usage_steps),
                    qr_code=f"https://smartcampus.edu.vn/qr/{code}",
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
            )
    session.add_all(equipments_to_add)
    await session.commit()
async def seed_room_equipments(session):
    count = (await session.execute(select(func.count(Equipment.id)))).scalar()
    if count and count > 0:
        print(f"Dữ liệu phòng đã tồn tại ({count} rooms). Bỏ qua bước seed.")
        return
    rooms_res = await session.execute(select(Room.id, Room.type))
    rooms = rooms_res.all()
    equips_res = await session.execute(select(Equipment.id, Equipment.type))
    all_equips = equips_res.all()
    equips_by_type = {}
    for e_id, e_type in all_equips:
        if e_type not in equips_by_type:
            equips_by_type[e_type] = []
        equips_by_type[e_type].append(e_id)
    room_equipments_to_add = []
    used_equip_ids = set()
    for r_id, r_type in rooms:
        needed_types = []
        if r_type == "class":
            needed_types = ["projector", "ac", "speaker"]
        elif r_type == "lab":
            needed_types = ["projector", "ac", "computer", "speaker"]
        elif r_type == "sport":
            needed_types = ["ac", "speaker"]
        for t in needed_types:
            if t in equips_by_type:
                available = [eid for eid in equips_by_type[t] if eid not in used_equip_ids]
                if not available:
                    continue
                if t == "computer" and r_type == "lab":
                    num_comp = random.randint(5, 10)
                    to_assign = available[:num_comp]
                    for eid in to_assign:
                        # Nội dung note thật hơn để AI học vị trí và tình trạng
                        note = f"Vị trí bàn {random.randint(1, 10)}, dãy {random.choice(['A', 'B', 'C'])}. Tình trạng: {random.choice(['Tốt', 'Mới', 'Ổn định'])}."
                        room_equipments_to_add.append(RoomEquipment(room_id=r_id, equipment_id=eid, note=note))
                        used_equip_ids.add(eid)
                else:
                    eid = random.choice(available)
                    pos = "Góc tường" if t == "ac" else "Trần nhà" if t in ["projector", "speaker"] else "Bục giảng"
                    note = f"Lắp đặt tại {pos}. Kiểm tra lần cuối: {fake.date_this_year().strftime('%d/%m/%Y')}."
                    room_equipments_to_add.append(RoomEquipment(room_id=r_id, equipment_id=eid, note=note))
                    used_equip_ids.add(eid)
    if room_equipments_to_add:
        session.add_all(room_equipments_to_add)
        await session.commit()
        print(f"Successfully assigned {len(room_equipments_to_add)} equipments to existing rooms")
    else:
        print("No assignments created. Check if Equipment and Room data exist")
async def seed_slots(session):
    count = (await session.execute(select(func.count(Slot.id)))).scalar()
    if count and count > 0:
        print(f"Dữ liệu phòng đã tồn tại ({count} rooms). Bỏ qua bước seed.")
        return
    slot_configs = [
        {"name": "Tiết 1", "start": "07:00", "end": "07:50"},
        {"name": "Tiết 2", "start": "08:00", "end": "08:50"},
        {"name": "Tiết 3", "start": "09:00", "end": "09:50"},
        {"name": "Tiết 4", "start": "10:00", "end": "10:50"},
        {"name": "Tiết 5", "start": "11:00", "end": "11:50"},
        {"name": "Tiết 6", "start": "12:00", "end": "12:50"},
        {"name": "Tiết 7", "start": "13:00", "end": "13:50"},
        {"name": "Tiết 8", "start": "14:00", "end": "14:50"},
        {"name": "Tiết 9", "start": "15:00", "end": "15:50"},
        {"name": "Tiết 10", "start": "16:00", "end": "16:50"},
        {"name": "Tiết 11", "start": "17:00", "end": "17:50"},
        {"name": "Tiết 12", "start": "18:00", "end": "18:50"},
    ]
    slots_to_add = []
    for i, config in enumerate(slot_configs, start=1):
        sh, sm = [int(t) for t in config["start"].split(":")]
        eh, em = [int(t) for t in config["end"].split(":")]
        slots_to_add.append(
            Slot(
                name=config["name"],
                order_index=i, 
                start_time=time(sh, sm),
                end_time=time(eh, em),
                is_active=True
            )
        )
    session.add_all(slots_to_add)
    await session.commit()
async def seed_bookings(session):
    count = (await session.execute(select(func.count(Booking.id)))).scalar()
    if count and count > 0:
        print(f"Dữ liệu phòng đã tồn tại ({count} rooms). Bỏ qua bước seed.")
        return
    users_res = await session.execute(select(User.id, User.role).where(User.role != 'admin'))
    users_data = users_res.all() # Danh sách tuple (id, role)
    user_ids = [u[0] for u in users_data]
    admin_res = await session.execute(select(User.id).where(User.role == 'admin'))
    admin_ids = [r[0] for r in admin_res.all()]
    rooms_res = await session.execute(select(Room.id))
    room_ids = [r[0] for r in rooms_res.all()]
    slots_res = await session.execute(select(Slot.id))
    slot_ids = [r[0] for r in slots_res.all()]
    bookings_to_add = []
    used_slots = set() 
    today = date.today()
    sources = ['manual', 'ai']
    reasons = {
        "student": ["Học nhóm đồ án", "Họp câu lạc bộ", "Tự học buổi tối", "Làm bài tập lớn"],
        "lecturer": ["Giảng dạy bù", "Họp hội đồng bộ môn", "Hướng dẫn sinh viên nghiên cứu", "Tổ chức Seminar"]
    }
    for _ in range(50):
        booking_date = today + timedelta(days=random.randint(-7, 7))
        room_id = random.choice(room_ids)
        slot_id = random.choice(slot_ids)
        unique_key = (room_id, slot_id, booking_date)
        if unique_key in used_slots:
            continue
        used_slots.add(unique_key)
        user_id, user_role = random.choice(users_data)
        source = random.choice(sources)
        if booking_date < today:
            status = random.choice(['completed', 'cancelled', 'rejected'])
        else:
            status = random.choice(['pending', 'approved'])
        approved_by = None
        approved_at = None
        if status in ['approved', 'completed']:
            approved_by = random.choice(admin_ids)
            approved_at = datetime.now() - timedelta(hours=random.randint(1, 24))
        reason_text = random.choice(reasons.get(user_role, ["Sử dụng phòng học"]))
        note_prefix = "AI gợi ý: " if source == "ai" else "Yêu cầu: "
        note = f"{note_prefix}{reason_text}. {fake.sentence(nb_words=4)}"
        bookings_to_add.append(
            Booking(
                user_id=user_id,
                room_id=room_id,
                slot_id=slot_id,
                date=booking_date,
                status=status,
                source=source,
                approved_by=approved_by,
                approved_at=approved_at,
                note=note,
                created_at=datetime.now() - timedelta(days=2)
            )
        )
    session.add_all(bookings_to_add)
    await session.commit()
async def seed_tickets(session):
    count = (await session.execute(select(func.count(Ticket.id)))).scalar()
    if count and count > 0:
        print(f"Dữ liệu phòng đã tồn tại ({count} rooms). Bỏ qua bước seed.")
        return
    users_res = await session.execute(select(User.id).where(User.role != 'admin'))
    user_ids = [r[0] for r in users_res.all()]
    bookings_res = await session.execute(select(Booking.id, Booking.room_id).limit(20))
    bookings = bookings_res.all()
    equips_res = await session.execute(select(Equipment.id, Equipment.name).limit(20))
    equipments = equips_res.all()
    tickets_to_add = []
    scenarios = [
        {
            "type": "equipment", 
            "titles": ["Hỏng thiết bị", "Lỗi vận hành", "Cần bảo trì"],
            "desc_templates": ["Thiết bị {item} có dấu hiệu {issue}. Đã thử khởi động lại nhưng không được.", "Yêu cầu kiểm tra gấp {item}."]
        },
        {
            "type": "booking", 
            "titles": ["Sự cố nhận phòng", "Trùng lịch phòng", "Cửa phòng bị khóa"],
            "desc_templates": ["Mã đặt phòng {id} gặp lỗi. {issue}.", "Tôi đã đến phòng nhưng {issue}."]
        },
        {
            "type": "system", 
            "titles": ["Lỗi phần mềm", "Sự cố đăng nhập", "Lỗi kết nối"],
            "desc_templates": ["Hệ thống báo lỗi {code}. {issue}.", "Ứng dụng bị crash khi tôi thực hiện {action}."]
        },
        {
            "type": "ai_anomaly", 
            "titles": ["Gợi ý AI sai", "Lỗi thuật toán", "AI không phản hồi"],
            "desc_templates": ["AI gợi ý {wrong_thing} là không hợp lý.", "Kết quả phân tích từ AI {issue}."]
        }
    ]
    statuses = ['open', 'in_progress', 'resolved', 'closed']
    for i in range(30):
        scenario = random.choice(scenarios)
        status = random.choice(statuses)
        user_id = random.choice(user_ids)
        if scenario['type'] == 'equipment':
            e_id, e_name = random.choice(equipments)
            title = f"{random.choice(scenario['titles'])}: {e_name}"
            issue = random.choice(["không lên nguồn", "kêu to", "chạy chập chờn", "bị mất tín hiệu"])
            description = random.choice(scenario['desc_templates']).format(item=e_name, issue=issue)
        elif scenario['type'] == 'booking' and bookings:
            b_id, r_id = random.choice(bookings)
            title = random.choice(scenario['titles'])
            issue = random.choice(["thẻ từ không mở được cửa", "phòng đang có người khác sử dụng", "thiếu chìa khóa"])
            description = random.choice(scenario['desc_templates']).format(id=f"BK-{b_id}", issue=issue)
        elif scenario['type'] == 'system':
            title = random.choice(scenario['titles'])
            action = random.choice(["đặt phòng", "xem lịch học", "gửi báo cáo"])
            code = random.choice(["500 Internal Server Error", "403 Forbidden", "Timeout"])
            description = random.choice(scenario['desc_templates']).format(code=code, action=action, issue="không phản hồi")
        else:
            title = random.choice(scenario['titles'])
            wrong_thing = random.choice(["phòng Lab cho tiết Thể dục", "tiết 12 cho sinh viên ở xa", "gợi ý bảo trì thiết bị đang mới"])
            description = random.choice(scenario['desc_templates']).format(wrong_thing=wrong_thing, issue="bị sai lệch thông tin")
        ticket_data = {
            "user_id": user_id,
            "title": f"{title} #{i+1}",
            "description": f"{description} ({fake.sentence(nb_words=5)})",
            "status": status,
            "type": scenario['type'],
            "resolved_at": datetime.now() if status in ['resolved', 'closed'] else None,
            "created_at": datetime.now() - timedelta(days=random.randint(0, 5))
        }
        if scenario['type'] == 'equipment':
            ticket_data["equipment_id"] = e_id
        elif scenario['type'] == 'booking' and bookings:
            ticket_data["booking_id"] = b_id
            ticket_data["room_id"] = r_id
        tickets_to_add.append(Ticket(**ticket_data))
    session.add_all(tickets_to_add)
    await session.commit()
async def seed_ai_logs(session):
    result = await session.execute(select(func.count(AILog.id)))
    if result.scalar() > 0:
        print("AI Logs already exist. Skipping...")
        return
    users_res = await session.execute(select(User.id))
    user_ids = [r[0] for r in users_res.all()]
    bookings_res = await session.execute(select(Booking.id))
    booking_ids = [r[0] for r in bookings_res.all()]
    ai_logs_to_add = []
    for i in range(40):
        log_type = random.choice(["booking_parse", "booking_review", "chatbot", "anomaly_detect", "support"])
        user_id = random.choice(user_ids)
        status = random.choices(["success", "failed", "rejected"], weights=[70, 15, 15], k=1)[0]
        input_text = ""
        output_text = ""
        booking_id = None
        if log_type == "booking_parse":
            room_type = random.choice(["Lab", "Phòng học", "Sân thể thao"])
            day = random.choice(["thứ Hai", "thứ Ba", "mai", "cuối tuần này"])
            input_text = f"Tôi muốn đặt {room_type} vào {day} cho {random.randint(5, 30)} người"
            output_dict = {
                "room_type": room_type.lower(),
                "parsed_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
                "slots": [random.randint(1, 4)],
                "confidence": round(random.uniform(0.8, 0.99), 2)
            }
            output_text = json.dumps(output_dict, ensure_ascii=False)
            booking_id = random.choice(booking_ids) if booking_ids else None
        elif log_type == "booking_review":
            input_text = f"Review booking ID BK-{random.randint(100, 999)} cho phòng {random.choice(['A', 'B', 'C'])}{random.randint(101, 505)}"
            if status == "success":
                output_text = "Approved: Yêu cầu hợp lệ và phù hợp với tiêu chuẩn sử dụng."
            else:
                output_text = f"Rejected: {random.choice(['Trùng lịch bảo trì thiết bị', 'Vượt quá hạn mức đặt phòng trong tuần', 'Phòng không đủ sức chứa'])}."
            booking_id = random.choice(booking_ids) if booking_ids else None
        elif log_type == "chatbot":
            questions = [
                "Làm thế nào để tôi hủy đặt phòng?",
                "Quy định sử dụng máy chiếu là gì?",
                "Phòng Lab B202 có những thiết bị nào?",
                "Admin là ai vậy?"
            ]
            input_text = random.choice(questions)
            output_text = f"{fake.sentence(nb_words=10)} Vui lòng liên hệ {fake.email()} nếu cần hỗ trợ thêm."
        elif log_type == "anomaly_detect":
            input_text = f"Check pattern for User {fake.bothify('???###').upper()}"
            if status == "success":
                output_text = "Không phát hiện dấu hiệu bất thường."
            else:
                output_text = f"Cảnh báo: Phát hiện {random.choice(['đăng nhập từ địa chỉ IP lạ', 'nhiều yêu cầu thất bại liên tiếp', 'truy cập ngoài giờ hành chính'])}."
        else:
            e_code = f"{random.choice(['PROJ', 'AC', 'COMP'])}-{random.randint(1, 50):03d}"
            input_text = f"Thiết bị {e_code} gặp sự cố {random.choice(['không kết nối được', 'bị hỏng nút nguồn', 'chạy quá nóng'])}"
            output_text = f"Đã tự động tạo Ticket #{random.randint(1000, 9999)} cho bộ phận kỹ thuật."
        ai_logs_to_add.append(
            AILog(
                user_id=user_id,
                booking_id=booking_id,
                type=log_type,
                input=input_text,
                output=output_text,
                status=status,
                created_at=datetime.now() - timedelta(hours=random.randint(1, 100))
            )
        )
    session.add_all(ai_logs_to_add)
    await session.commit()
async def main():
    async with AsyncSessionLocal() as session:
        await seed_users(session)
        await seed_rooms(session)
        await seed_equipments(session)
        await seed_room_equipments(session)
        await seed_slots(session)
        await seed_bookings(session)
        await seed_tickets(session)
        await seed_ai_logs(session)
    print("Done seeding!")

if __name__ == "__main__":
    asyncio.run(main())