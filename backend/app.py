import os
import json
import uuid
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from models import db, Character, Event, EventChild

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')
CORS(app)

# 数据库配置（Render用环境变量DATABASE_URL，本地用MySQL）
database_url = os.environ.get('DATABASE_URL', 'mysql+pymysql://normal:4152630@localhost:3306/game')
# Render提供的URL以postgres://开头，需要改成postgresql://
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db.init_app(app)

# 路径配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, '..', 'frontend', 'dist')
IMAGES_DIR = os.path.join(BASE_DIR, '..', 'frontend', 'dist', 'images')
UPLOAD_DIR = os.path.join(BASE_DIR, '..', 'frontend', 'dist', 'images', 'uploads')

# 确保上传目录存在
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 允许的图片格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==================== API ====================

@app.route('/api/events')
def get_events():
    events = Event.query.all()
    return jsonify([event.to_dict() for event in events])

@app.route('/api/characters')
def get_characters():
    characters = Character.query.all()
    return jsonify([char.to_dict() for char in characters])

@app.route('/api/characters', methods=['POST'])
def add_character():
    """添加新人物（支持图片上传）"""
    try:
        # 获取表单数据
        name = request.form.get('name', '')
        name_en = request.form.get('nameEn', '')
        role = request.form.get('role', '')
        summary = request.form.get('summary', '')
        quotes = request.form.get('quotes', '')
        tags = request.form.get('tags', '')

        # 处理图片上传
        image_filename = ''
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                # 生成唯一文件名
                ext = file.filename.rsplit('.', 1)[1].lower()
                image_filename = f"upload_{uuid.uuid4().hex[:8]}.{ext}"
                file.save(os.path.join(UPLOAD_DIR, image_filename))
                image_filename = f"uploads/{image_filename}"

        # 生成新ID
        last_char = Character.query.order_by(Character.id.desc()).first()
        if last_char:
            max_id = int(last_char.id.split('_')[1])
            new_id = f"char_{max_id + 1}"
        else:
            new_id = "char_1"

        # 创建新角色
        new_char = Character(
            id=new_id,
            name=name,
            name_en=name_en,
            role=role,
            image=image_filename,
            summary=summary,
            tags=[t.strip() for t in tags.split(',') if t.strip()],
            quotes=quotes
        )

        db.session.add(new_char)
        db.session.commit()

        return jsonify({"success": True, "character": new_char.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/api/characters/<char_id>', methods=['DELETE'])
def delete_character(char_id):
    character = Character.query.get(char_id)
    if character:
        db.session.delete(character)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"error": "Not found"}), 404

# ==================== 静态文件 ====================

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGES_DIR, filename)

@app.route('/')
def index():
    return send_from_directory(DIST_DIR, 'index.html')

@app.route('/<path:path>')
def serve_frontend(path):
    file_path = os.path.join(DIST_DIR, path)
    if os.path.exists(file_path):
        return send_from_directory(DIST_DIR, path)
    return send_from_directory(DIST_DIR, 'index.html')

if __name__ == '__main__':
    with app.app_context():
        # 创建数据库表
        db.create_all()
        print("数据库表已创建/更新")

    print("=" * 50)
    print("  火影忍者P5风格图鉴")
    print("  访问地址: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
else:
    # gunicorn启动时也创建表，并自动导入初始数据
    with app.app_context():
        db.create_all()
        # 如果数据库为空，自动从JSON导入数据
        if Character.query.count() == 0:
            # 导入角色
            chars_file = os.path.join(BASE_DIR, 'database', 'characters.json')
            if os.path.exists(chars_file):
                with open(chars_file, 'r', encoding='utf-8') as f:
                    characters = json.load(f)
                for char_data in characters:
                    character = Character(
                        id=char_data['id'],
                        name=char_data['name'],
                        name_en=char_data.get('nameEn', ''),
                        role=char_data.get('role', ''),
                        image=char_data.get('image', ''),
                        summary=char_data.get('summary', ''),
                        tags=char_data.get('tags', []),
                        quotes=char_data.get('quotes', '')
                    )
                    db.session.add(character)
                db.session.commit()
                print(f"自动导入 {len(characters)} 个角色")

            # 导入事件
            events_file = os.path.join(BASE_DIR, 'database', 'events.json')
            if os.path.exists(events_file):
                with open(events_file, 'r', encoding='utf-8') as f:
                    events = json.load(f)
                for event_data in events:
                    event = Event(
                        id=event_data['id'],
                        title=event_data['title'],
                        period=event_data.get('period', ''),
                        summary=event_data.get('summary', '')
                    )
                    db.session.add(event)
                    for child_data in event_data.get('children', []):
                        child = EventChild(
                            id=child_data['id'],
                            event_id=event_data['id'],
                            title=child_data['title'],
                            detail=child_data.get('detail', '')
                        )
                        db.session.add(child)
                db.session.commit()
                print(f"自动导入 {len(events)} 个事件")
