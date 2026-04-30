import asyncio
from core.database import AsyncSessionLocal
from models import User, Room, Equipment, RoomEquipment, Slot, Booking, Ticket, AILog
from faker import Faker
from sqlalchemy import select, func
from shared.utils import hash_password
import random
from unidecode import unidecode
from datetime import timedelta, date, time, datetime
import json

fake = Faker("vi_VN")

async def seed_users(session):
    count = (await session.execute(select(func.count(User.id)))).scalar()
    if count and count > 0:
        return
    users_to_add = []
    users_group = [
        {"quantity": 2, "prefix": "ADM", "role": "admin", "password_hash": "adm@123", "email_domain": "@adm.scb.edu.vn"},
        {"quantity": 20, "prefix": "LEC", "role": "lecturer", "password_hash": "lec@123", "email_domain": "@lec.scb.edu.vn"},
        {"quantity": 200, "prefix": "STU", "role": "student", "password_hash": "stu@123", "email_domain": "@stu.scb.edu.vn"}
    ]
    for group in users_group:
        for i in range(group["quantity"]):
            external_id = f"{group['prefix']}2026{str(i).zfill(4)}"
            gender = random.choice(["male", "female"])
            if gender == "male":
                first_name = fake.first_name_male()
                middle_name = random.choice(["Văn", "Hữu", "Đình", "Quang", "Minh"])
                last_name = fake.last_name_male()
            else:
                first_name = fake.first_name_female()
                middle_name = random.choice(["Lan", "Nhã", "Như", "Khánh", "Diệu"])
                last_name = fake.last_name_female()
            full_name = f"{last_name} {middle_name} {first_name}"
            if(group["role"] == "student"): min_age, max_age = 18, 22
            elif(group["role"] == "admin"): min_age, max_age = 25, 40
            else: min_age, max_age = 30, 60
            date_of_birth = fake.date_of_birth(minimum_age=min_age, maximum_age=max_age)
            phone = fake.numerify(text="0#########")
            email_name = unidecode(full_name).replace(" ", "").lower()
            email = f"{email_name}{i}{group['email_domain']}"
            graduation_date = None
            if group["role"] == "student":
                is_graduated = random.random() < 0.3
                if is_graduated:
                    graduation_date = date_of_birth + timedelta(days=(22 * 365) + random.randint(0, 180))
                    if graduation_date > date.today():
                        graduation_date = date.today()
            last_login_at = None
            new_user = User(
                external_id = external_id,
                full_name = full_name,
                gender = gender,
                date_of_birth = date_of_birth,
                phone = phone,
                email = email,
                graduation_date = graduation_date,
                last_login_at = last_login_at,
                password_hash = hash_password(group["password_hash"]),
                role = group["role"]
            )
            users_to_add.append(new_user)
    session.add_all(users_to_add)
    await session.commit()
async def seed_rooms(session):
    count = (await session.execute(select(func.count(Room.id)))).scalar()
    if count and count > 0:
        return
    rooms_to_add = []
    rooms_group = [
        {"quantity": 200, "prefix": "CLA", "type": "class", "base_capacity": 40, "buildings": ["A", "B", "C"]},
        {"quantity": 50, "prefix": "LAB", "type": "lab", "base_capacity": 50, "buildings": ["D", "E"]},
        {"quantity": 3, "prefix": "SPO", "type": "sport", "base_capacity": 500, "buildings": ["E"]}
    ]
    building_floors = {"A": 7, "B": 5, "C": 5, "D": 5, "E": 5}
    for group in rooms_group:
        for i in range(group["quantity"]):
            type = group["type"]
            capacity = group["base_capacity"] + random.choice([0, 10, 20, 30, 40, 50])
            room_number = f"{i + 1:04d}"
            building = random.choice(group["buildings"])
            floor = str(random.randint(1, building_floors[building]))
            name = f"{group['prefix']}-{building}-{room_number}"
            deleted_at = None
            new_room = Room(
                name = name,
                type = type,
                capacity = capacity,
                room_number = room_number,
                floor = floor,
                building = building,
                deleted_at = deleted_at
            )
            rooms_to_add.append(new_room)
    session.add_all(rooms_to_add)
    await session.commit()
async def seed_equipments(session):
    count = (await session.execute(select(func.count(Equipment.id)))).scalar()
    if count and count > 0:
        return
    equipments_to_add = []
    equipments_group = [
        {"quantity": 200, "prefix": "PRO", "base_name": "Máy chiếu", "type": "projector", "description": "Máy chiếu độ phân giải Full HD, hỗ trợ kết nối HDMI/VGA.", "usage_guide": "1. Không đứng lên ghế. 2. Không để vật sắc nhọn làm rách đệm. 3. Xếp gọn lại sau khi sử dụng."},
        {"quantity": 200, "prefix": "AC", "base_name": "Điều hoà", "type": "ac", "description": "Điều hòa công suất 18.000 BTU, chế độ làm lạnh nhanh Inverter.", "usage_guide": "1. Sử dụng điều khiển để bật/tắt. 2. Để nhiệt độ lý tưởng 24-26°C. 3. Đóng kín cửa sổ và cửa ra vào."},
        {"quantity": 200, "prefix": "CHA", "base_name": "Ghế", "type": "chair", "description": "Ghế tựa khung thép, đệm bọc da simili cao cấp.", "usage_guide": "1. Không đứng lên ghế. 2. Không để vật sắc nhọn làm rách đệm. 3. Xếp gọn lại sau khi sử dụng."},
        {"quantity": 200, "prefix": "TAB", "base_name": "Bàn học", "type": "table", "description": "Bàn học gỗ công nghiệp, kích thước tiêu chuẩn cho 2 người.", "usage_guide": "1. Không vẽ bẩn lên mặt bàn. 2. Tránh để nước đọng lâu trên bề mặt gỗ. 3. Không ngồi lên bàn."},
        {"quantity": 200, "prefix": "BOA", "base_name": "Bảng", "type": "board", "description": "Bảng từ trắng chống lóa, dùng cho bút dạ và nam châm.", "usage_guide": "1. Chỉ sử dụng bút dạ chuyên dụng. 2. Dùng khăn mềm để lau bảng. 3. Không dùng vật cứng cào mặt bảng."},
        {"quantity": 100, "prefix": "COM", "base_name": "Máy tính", "type": "computer", "description": "Máy tính để bàn cấu hình Core i5, RAM 16GB dùng cho thực hành.", "usage_guide": "1. Nhấn nút nguồn trên case. 2. Đăng nhập bằng tài khoản sinh viên. 3. Shutdown máy trước khi rời phòng."},
        {"quantity": 200, "prefix": "SPE", "base_name": "Loa", "type": "speaker", "description": "Hệ thống loa gắn tường công suất 30W, âm thanh rõ nét.", "usage_guide": "1. Kết nối qua cổng AUX hoặc Bluetooth tại bảng điều khiển. 2. Điều chỉnh âm lượng vừa đủ nghe. 3. Tắt nguồn sau khi sử dụng."},
    ]
    for group in equipments_group:
        for i in range(group["quantity"]):
            name = f"{group['base_name']} {i + 1:04d}"
            type = group["type"]
            description = group["description"]
            usage_guide = group["usage_guide"]
            code = f"{group['prefix']}2026{i + 1:04d}"
            qr_code = f"https://smartcampus.edu.vn/qr/{code}"
            new_equipment = Equipment(
                name = name,
                type = type,
                description = description,
                usage_guide = usage_guide,
                code = code,
                qr_code = qr_code
            )
            equipments_to_add.append(new_equipment)
    session.add_all(equipments_to_add)
    await session.commit()
async def seed_rooms_equipments(session):
    count = (await session.execute(select(func.count(RoomEquipment.id)))).scalar()
    if count and count > 0:
        return
    rooms_equipments_to_add = []
    rooms_result = await session.execute(select(Room.id))
    room_ids = [r[0] for r in rooms_result.all()]
    equipments_result = await session.execute(select(Equipment.id))
    equipment_ids = [e[0] for e in equipments_result.all()]
    random.shuffle(equipment_ids)
    num_rooms = len(room_ids)
    for i, equipment_id in enumerate(equipment_ids):
        room_id = room_ids[i % num_rooms]
        new_room_equipment = RoomEquipment(
            room_id = room_id,
            equipment_id = equipment_id
        )
        rooms_equipments_to_add.append(new_room_equipment)
    session.add_all(rooms_equipments_to_add)
    await session.commit()
async def seed_slots(session):
    count = (await session.execute(select(func.count(Slot.id)))).scalar()
    if count and count > 0:
        return
    slots_to_add = []
    slots_group = [
        {"name": "Tiết 01", "order_index": 1, "start_time": time(7, 30), "end_time": time(8, 15)},
        {"name": "Tiết 02", "order_index": 2, "start_time": time(8, 20), "end_time": time(9, 5)},
        {"name": "Tiết 03", "order_index": 3, "start_time": time(9, 15), "end_time": time(10, 0)},
        {"name": "Tiết 04", "order_index": 4, "start_time": time(10, 5), "end_time": time(10, 50)},
        {"name": "Tiết 05", "order_index": 5, "start_time": time(11, 0), "end_time": time(11, 45)},
        {"name": "Tiết 06", "order_index": 6, "start_time": time(11, 50), "end_time": time(12, 35)},
        {"name": "Tiết 07", "order_index": 7, "start_time": time(13, 30), "end_time": time(14, 15)},
        {"name": "Tiết 08", "order_index": 8, "start_time": time(14, 20), "end_time": time(15, 5)},
        {"name": "Tiết 09", "order_index": 9, "start_time": time(15, 15), "end_time": time(16, 0)},
        {"name": "Tiết 10", "order_index": 10, "start_time": time(16, 5), "end_time": time(16, 50)},
        {"name": "Tiết 11", "order_index": 11, "start_time": time(17, 0), "end_time": time(17, 45)},
        {"name": "Tiết 12", "order_index": 12, "start_time": time(17, 50), "end_time": time(18, 35)},
    ]
    for group in slots_group:
        name = group["name"]
        order_index = group["order_index"]
        start_time = group["start_time"]
        end_time = group["end_time"]
        deleted_at = None
        new_slot = Slot(
            name = name,
            order_index = order_index,
            start_time = start_time,
            end_time = end_time,
            deleted_at = deleted_at
        )
        slots_to_add.append(new_slot)
    session.add_all(slots_to_add)
    await session.commit()
async def seed_bookings(session):
    count = (await session.execute(select(func.count(Booking.id)))).scalar()
    if count and count > 0:
        return
    bookings_to_add = []
    users_result = await session.execute(select(User.id).where(User.role.in_(['student', 'lecturer'])))
    user_ids = [u[0] for u in users_result.all()]
    rooms_result = await session.execute(select(Room.id))
    room_ids = [r[0] for r in rooms_result.all()]
    slots_result = await session.execute(select(Slot.id))
    slot_ids = [s[0] for s in slots_result.all()]
    today = date.today()
    booked_slots = set()
    for _ in range(200):
        user_id = random.choice(user_ids)
        room_id = random.choice(room_ids)
        slot_id = random.choice(slot_ids)
        booked_date = today + timedelta(days = random.randint(0, 15))

        # Những phòng được đặt sẽ bị bỏ qua
        overlap_key = (room_id, slot_id, booked_date)
        if overlap_key in booked_slots:
            continue
        booked_slots.add(overlap_key)
        
        source = random.choice(['manual', 'ai'])
        if booked_date < today: status = random.choice(['completed', 'cancelled', 'rejected'])
        else: status = random.choice(['pending', 'approved', 'cancelled'])
        note = "Đặt phòng"
        created_at = datetime.combine(booked_date - timedelta(days=random.randint(1, 3)), time(8, 0))
        approved_at = None
        checked_in_at = None
        cancelled_at = None
        if status in ['approved', 'completed']:
            approved_at = created_at + timedelta(hours=random.randint(1, 5))
            if status == 'completed':
                checked_in_at = datetime.combine(booked_date, time(random.randint(7, 17), 0))
        elif status == 'cancelled':
            cancelled_at = created_at + timedelta(hours=random.randint(1, 24))
        new_booking = Booking(
            user_id = user_id,
            room_id = room_id,
            slot_id = slot_id,
            date = booked_date,
            source = source,
            status = status,
            note = note,
            approved_at = approved_at,
            checked_in_at = checked_in_at,
            cancelled_at = cancelled_at,
            created_at = created_at
        )
        bookings_to_add.append(new_booking)
    session.add_all(bookings_to_add)
    await session.commit()
async def seed_tickets(session):
    count = (await session.execute(select(func.count(Ticket.id)))).scalar()
    if count and count > 0:
        return
    tickets_to_add = []
    ticket_groups = [
        {"quantity": 50, "type": "equipment", "titles": ["Máy chiếu không lên nguồn", "Điều hòa chảy nước", "Bàn bị gãy chân", "Loa rè không nghe rõ", "Máy tính bị màn hình xanh"], "description": "Thiết bị gặp vấn đề trong quá trình sử dụng, cần kỹ thuật kiểm tra.", "status": ["open", "in_progress", "resolved", "closed"], "days_back": (1, 10)},
        {"quantity": 30, "type": "booking", "titles": ["Phòng chưa được dọn dẹp", "Cửa phòng bị khóa không vào được", "Thiếu ghế ngồi so với đăng ký", "Ổ cắm điện không có điện"], "description": "Phản ánh về tình trạng phòng học khi bắt đầu ca mượn.", "status": ["open", "resolved"], "days_back": (0, 5)}
    ]
    users_result = await session.execute(select(User.id).where(User.role.in_(['student', 'lecturer'])))
    user_ids = [u[0] for u in users_result.all()]
    room_equipment_result = await session.execute(select(RoomEquipment.room_id, RoomEquipment.equipment_id))
    room_equipment_ids = room_equipment_result.all()
    bookings_result = await session.execute(select(Booking.id))
    booking_ids = [b[0] for b in bookings_result.all()]
    for group in ticket_groups:
        for _ in range(group["quantity"]):
            user_id = random.choice(user_ids)
            room_id = None
            equipment_id = None
            booking_id = None
            if group["type"] == "equipment" and room_equipment_ids: room_id, equipment_id = random.choice(room_equipment_ids)
            elif group["type"] == "booking" and booking_ids: booking_id = random.choice(booking_ids)
            title = f"{'Sự cố' if group['type'] == 'equipment' else 'Vấn đề'}: {random.choice(group['titles'])}"
            type = group["type"]
            status = random.choice(group["status"])
            description = group["description"]
            resolved_at = None
            created_at = datetime.now() - timedelta(days=random.randint(*group["days_back"]))
            if status in ["resolved", "closed"]: resolved_at = created_at + timedelta(hours=random.randint(2, 48))
            tickets_to_add.append(Ticket(
                user_id = user_id,
                equipment_id = equipment_id,
                room_id = room_id,
                booking_id = booking_id,
                title = title,
                type = type,
                status = status,
                description = description,
                resolved_at = resolved_at,
                created_at = created_at
            ))
    session.add_all(tickets_to_add)
    await session.commit()
async def seed_ai_logs(session):
    count = (await session.execute(select(func.count(AILog.id)))).scalar()
    if count and count > 0:
        return
    ai_logs_to_add = []
    ai_groups = [
        {"quantity": 40, "type": "natural_language_booking", "inputs": ["Đặt phòng Lab A tiết 1", "Tìm phòng trống sáng mai", "Hủy lịch đặt phòng P.302"], "outputs": ["Đã tìm thấy phòng phù hợp.", "Đặt phòng thành công!", "Lịch đã được hủy."], "status": ["success", "failed"], "days_back": (0, 30)},
        {"quantity": 30, "type": "troubleshooting", "inputs": ["Tại sao máy chiếu không lên?", "Cách bật điều hòa?", "Loa phòng 201 bị rè"], "outputs": ["Kiểm tra dây nguồn máy chiếu.", "Dùng điều khiển treo tường.", "Đã ghi nhận sự cố loa."], "status": ["success", "escalated"], "days_back": (0, 30)},
        {"quantity": 30, "type": "moderation", "inputs": ["Nội dung đặt phòng: 'Học nhóm'", "Báo cáo: 'Cửa bị hỏng'", "Input chứa từ ngữ thô tục"], "outputs": ["Nội dung hợp lệ.", "Duyệt an toàn.", "Cảnh báo: Vi phạm tiêu chuẩn nội dung."], "status": ["success", "flagged", "escalated"], "days_back": (0, 30)}
    ]
    users_result = await session.execute(select(User.id).where(User.role.in_(['student', 'lecturer'])))
    user_ids = [u[0] for u in users_result.all()]
    room_equipment_result = await session.execute(select(RoomEquipment.room_id, RoomEquipment.equipment_id))
    room_equipment_ids = room_equipment_result.all()
    bookings_result = await session.execute(select(Booking.id))
    booking_ids = [b[0] for b in bookings_result.all()]
    for group in ai_groups:
        for _ in range(group["quantity"]):
            user_id = random.choice(user_ids)
            equipment_id = None
            room_id = None
            booking_id = None
            if group["type"] == "troubleshooting" and room_equipment_ids: room_id, equipment_id = random.choice(room_equipment_ids)
            elif group["type"] in ["natural_language_booking", "moderation"] and booking_ids:   booking_id = random.choice(booking_ids)
            type = group["type"]
            status = random.choice(group["status"])
            input_text = random.choice(group["inputs"])
            output_text = random.choice(group["outputs"])
            metadata_json = {"confidence_score": round(random.uniform(0.85, 0.99), 2) if status == "success" else round(random.uniform(0.3, 0.7), 2)}
            created_at = datetime.now() - timedelta(days=random.randint(*group["days_back"]))
            ai_logs_to_add.append(AILog(
                user_id = user_id,
                room_id = room_id,
                equipment_id = equipment_id,
                booking_id = booking_id,
                type = type,
                status = status,
                input_text = input_text,
                output_text = output_text,
                metadata_json = json.dumps(metadata_json),
                created_at = created_at
            ))
    session.add_all(ai_logs_to_add)
    await session.commit()

async def seed_data():
    async with AsyncSessionLocal() as session:
        await seed_users(session)
        await seed_rooms(session)
        await seed_equipments(session)
        await seed_rooms_equipments(session)
        await seed_slots(session)
        await seed_bookings(session)
        await seed_tickets(session)
        await seed_ai_logs(session)

if __name__ == "__main__":
    asyncio.run(seed_data())