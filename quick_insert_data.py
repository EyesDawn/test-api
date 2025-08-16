#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import sys

def insert_training_data(base_url="http://localhost:8080", token=None):
    """
    快速插入培训测试数据
    """
    
    # 设置请求头
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    if token:
        headers.update({
            'Authorization': f'Bearer {token}',
            'Sa-Token': token
        })
    
    # 测试数据
    training_records = [
        {"name": "张三", "team": "一班", "score": 92.5, "remark": "表现优秀", "absent": 0, "trainingType": "笔试"},
        {"name": "李四", "team": "一班", "score": 85.0, "remark": "基础良好", "absent": 0, "trainingType": "笔试"},
        {"name": "王五", "team": "一班", "score": 0, "remark": "因病缺考", "absent": 1, "trainingType": "笔试"},
        {"name": "赵六", "team": "二班", "score": 88.5, "remark": "答题准确", "absent": 0, "trainingType": "笔试"},
        {"name": "钱七", "team": "二班", "score": 76.0, "remark": "需要加强", "absent": 0, "trainingType": "笔试"},
        {"name": "孙八", "team": "二班", "score": 90.0, "remark": "优秀学员", "absent": 0, "trainingType": "笔试"},
        
        {"name": "张三", "team": "一班", "score": 87.5, "remark": "操作熟练", "absent": 0, "trainingType": "仿真机"},
        {"name": "李四", "team": "一班", "score": 89.0, "remark": "实践能力强", "absent": 0, "trainingType": "仿真机"},
        {"name": "王五", "team": "一班", "score": 91.5, "remark": "技能全面", "absent": 0, "trainingType": "仿真机"},
        {"name": "赵六", "team": "二班", "score": 83.0, "remark": "操作规范", "absent": 0, "trainingType": "仿真机"},
        {"name": "钱七", "team": "二班", "score": 0, "remark": "设备故障", "absent": 1, "trainingType": "仿真机"},
        {"name": "孙八", "team": "二班", "score": 86.5, "remark": "动手能力强", "absent": 0, "trainingType": "仿真机"},
        
        {"name": "张三", "team": "一班", "score": 85.0, "remark": "综合素质好", "absent": 0, "trainingType": "其它"},
        {"name": "李四", "team": "一班", "score": 80.0, "remark": "", "absent": 0, "trainingType": "其它"},
        {"name": "王五", "team": "一班", "score": 88.5, "remark": "积极参与", "absent": 0, "trainingType": "其它"},
        {"name": "赵六", "team": "二班", "score": 0, "remark": "临时出差", "absent": 1, "trainingType": "其它"},
        {"name": "钱七", "team": "二班", "score": 75.5, "remark": "基本合格", "absent": 0, "trainingType": "其它"},
        {"name": "孙八", "team": "二班", "score": 89.0, "remark": "表现突出", "absent": 0, "trainingType": "其它"}
    ]
    
    print(f"🚀 开始插入测试数据到: {base_url}")
    print("=" * 50)
    
    success_count = 0
    failed_count = 0
    
    for i, record in enumerate(training_records):
        try:
            response = requests.post(
                f"{base_url}/training/", 
                json=record, 
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 200:
                    success_count += 1
                    record_id = result.get('data')
                    print(f"✅ [{i+1:2d}] {record['name']} - {record['team']} - {record['trainingType']} (ID: {record_id})")
                else:
                    failed_count += 1
                    print(f"❌ [{i+1:2d}] {record['name']} - 失败: {result.get('msg', '未知错误')}")
            else:
                failed_count += 1
                print(f"❌ [{i+1:2d}] {record['name']} - HTTP {response.status_code}")
                
        except Exception as e:
            failed_count += 1
            print(f"❌ [{i+1:2d}] {record['name']} - 异常: {str(e)}")
    
    print("=" * 50)
    print(f"🎉 插入完成! 成功: {success_count}, 失败: {failed_count}")
    
    if success_count > 0:
        print("\n🔍 可以使用以下命令查看数据:")
        print(f"curl '{base_url}/training/page'")
        print(f"curl '{base_url}/training/team-ranking?trainingType=笔试'")


def main():
    # 默认配置
    base_url = "http://localhost:8080"
    token = None
    
    # 从命令行参数获取配置
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    if len(sys.argv) > 2:
        token = sys.argv[2]
    
    if token:
        print(f"🔑 使用认证Token: {token[:20]}...")
    
    try:
        insert_training_data(base_url, token)
    except KeyboardInterrupt:
        print("\n\n⏹️  用户取消操作")
    except Exception as e:
        print(f"\n❌ 执行失败: {e}")


if __name__ == "__main__":
    print("🏋️‍♀️ 培训管理系统 - 快速数据插入工具")
    print("用法: python quick_insert_data.py [服务器地址] [认证Token]")
    print("示例: python quick_insert_data.py http://192.168.1.100:8080 your-token")
    print()
    
    main()

