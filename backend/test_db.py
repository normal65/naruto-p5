"""
数据库连接测试脚本
"""
from app import app, db
from models import Character, Event, EventChild

def test_connection():
    """测试数据库连接"""
    try:
        with app.app_context():
            # 尝试查询
            characters = Character.query.all()
            events = Event.query.all()
            print(f"数据库连接成功！")
            print(f"角色数量: {len(characters)}")
            print(f"事件数量: {len(events)}")
            return True
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return False

if __name__ == '__main__':
    test_connection()
