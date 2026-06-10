"""
数据迁移脚本：将JSON数据导入MySQL数据库
使用方法：python migrate_data.py
"""
import json
import os
from app import app, db
from models import Character, Event, EventChild

def migrate_characters():
    """迁移角色数据"""
    characters_file = os.path.join(os.path.dirname(__file__), 'database', 'characters.json')

    if not os.path.exists(characters_file):
        print("characters.json 文件不存在")
        return

    with open(characters_file, 'r', encoding='utf-8') as f:
        characters = json.load(f)

    for char_data in characters:
        # 检查是否已存在
        existing = Character.query.get(char_data['id'])
        if existing:
            print(f"角色 {char_data['name']} 已存在，跳过")
            continue

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
        print(f"添加角色: {char_data['name']}")

    db.session.commit()
    print(f"角色数据迁移完成，共 {len(characters)} 条")


def migrate_events():
    """迁移剧情事件数据"""
    events_file = os.path.join(os.path.dirname(__file__), 'database', 'events.json')

    if not os.path.exists(events_file):
        print("events.json 文件不存在")
        return

    with open(events_file, 'r', encoding='utf-8') as f:
        events = json.load(f)

    for event_data in events:
        # 检查是否已存在
        existing = Event.query.get(event_data['id'])
        if existing:
            print(f"事件 {event_data['title']} 已存在，跳过")
            continue

        event = Event(
            id=event_data['id'],
            title=event_data['title'],
            period=event_data.get('period', ''),
            summary=event_data.get('summary', '')
        )
        db.session.add(event)

        # 添加子事件
        for child_data in event_data.get('children', []):
            child = EventChild(
                id=child_data['id'],
                event_id=event_data['id'],
                title=child_data['title'],
                detail=child_data.get('detail', '')
            )
            db.session.add(child)

        print(f"添加事件: {event_data['title']}")

    db.session.commit()
    print(f"剧情事件数据迁移完成，共 {len(events)} 条")


if __name__ == '__main__':
    with app.app_context():
        # 创建所有表
        print("创建数据库表...")
        db.create_all()
        print("数据库表创建完成")

        # 迁移数据
        print("\n开始迁移角色数据...")
        migrate_characters()

        print("\n开始迁移剧情事件数据...")
        migrate_events()

        print("\n数据迁移完成！")
