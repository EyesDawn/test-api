#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import os
import sys
from typing import Dict, Any, List

class TrainingAPITester:
    def __init__(self, base_url: str = "http://localhost:8080", token: str = None):
        """
        初始化API测试器
        
        Args:
            base_url: API服务器地址
            token: 认证token（如果需要）
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
        # 设置请求头
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        # 如果有token，设置认证头
        if token:
            self.session.headers.update({
                'Authorization': f'Bearer {token}',
                'Sa-Token': token  # Sa-Token框架的token头
            })

    def load_json_data(self, filename: str) -> Any:
        """从JSON文件加载数据"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ 文件不存在: {filename}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析错误: {e}")
            return None

    def make_request(self, method: str, endpoint: str, data: Any = None, params: Dict = None) -> Dict:
        """发送HTTP请求"""
        url = f"{self.base_url}{endpoint}"
        
        print(f"📡 {method.upper()} {url}")
        if params:
            print(f"   查询参数: {params}")
        if data:
            print(f"   请求体: {json.dumps(data, ensure_ascii=False, indent=2)}")
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, params=params)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, params=params)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, params=params)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")
            
            print(f"   状态码: {response.status_code}")
            
            # 尝试解析JSON响应
            try:
                response_data = response.json()
                print(f"   响应: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                return {
                    'status_code': response.status_code,
                    'data': response_data,
                    'success': response.status_code == 200
                }
            except json.JSONDecodeError:
                print(f"   响应: {response.text}")
                return {
                    'status_code': response.status_code,
                    'data': response.text,
                    'success': response.status_code == 200
                }
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 请求失败: {e}")
            return {
                'status_code': 0,
                'data': str(e),
                'success': False
            }

    def test_add_training_records(self, data_file: str = "training_test_data.json"):
        """测试新增培训记录接口"""
        print("\n🔍 测试新增培训记录接口")
        print("=" * 50)
        
        # 加载测试数据
        test_data = self.load_json_data(data_file)
        if not test_data:
            return
        
        training_records = test_data.get('training_records', [])
        created_ids = []
        
        for i, record in enumerate(training_records):
            print(f"\n📝 添加第 {i+1} 条记录:")
            result = self.make_request('POST', '/training/', data=record)
            
            if result['success']:
                record_id = result['data'].get('data')
                if record_id:
                    created_ids.append(record_id)
                    print(f"✅ 成功创建记录，ID: {record_id}")
                else:
                    print("❌ 创建失败，未返回ID")
            else:
                print("❌ 创建失败")
        
        print(f"\n🎉 成功创建 {len(created_ids)} 条记录")
        return created_ids

    def test_query_training_records(self):
        """测试分页查询接口"""
        print("\n🔍 测试分页查询接口")
        print("=" * 50)
        
        # 测试基本查询
        result = self.make_request('GET', '/training/page')
        
        # 测试带参数查询
        print(f"\n📊 测试关键字搜索:")
        result = self.make_request('GET', '/training/page', params={'keywords': '张'})
        
        print(f"\n📊 测试班组筛选:")
        result = self.make_request('GET', '/training/page', params={'team': '一班'})
        
        print(f"\n📊 测试培训类型筛选:")
        result = self.make_request('GET', '/training/page', params={'trainingType': '笔试'})

    def test_team_ranking(self):
        """测试班组排名接口"""
        print("\n🔍 测试班组排名接口")
        print("=" * 50)
        
        training_types = ['笔试', '仿真机', '其它']
        
        for training_type in training_types:
            print(f"\n🏆 {training_type} 班组排名:")
            result = self.make_request('GET', '/training/team-ranking', 
                                     params={'trainingType': training_type})

    def test_get_training_types(self):
        """测试获取培训类型列表接口"""
        print("\n🔍 测试获取培训类型列表接口")
        print("=" * 50)
        
        result = self.make_request('GET', '/training/types')

    def test_update_ranking(self):
        """测试更新排名接口"""
        print("\n🔍 测试更新排名接口")
        print("=" * 50)
        
        training_types = ['笔试', '仿真机', '其它']
        
        for training_type in training_types:
            print(f"\n🔄 更新 {training_type} 排名:")
            result = self.make_request('PUT', '/training/update-ranking', 
                                     params={'trainingType': training_type})

    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始API测试")
        print("=" * 60)
        
        # 1. 插入测试数据
        created_ids = self.test_add_training_records()
        
        # 2. 测试查询接口
        self.test_query_training_records()
        
        # 3. 测试班组排名
        self.test_team_ranking()
        
        # 4. 测试培训类型列表
        self.test_get_training_types()
        
        # 5. 测试更新排名
        self.test_update_ranking()
        
        print("\n✅ 所有测试完成")
        return created_ids


def main():
    # 配置参数
    BASE_URL = "http://localhost:8080"  # 修改为你的服务器地址
    TOKEN = None  # 如果需要认证，请设置token
    
    # 从命令行参数获取配置
    if len(sys.argv) > 1:
        BASE_URL = sys.argv[1]
    if len(sys.argv) > 2:
        TOKEN = sys.argv[2]
    
    print(f"🌐 测试服务器: {BASE_URL}")
    if TOKEN:
        print(f"🔑 使用Token: {TOKEN[:20]}...")
    
    # 创建测试器
    tester = TrainingAPITester(base_url=BASE_URL, token=TOKEN)
    
    # 运行测试
    tester.run_all_tests()


if __name__ == "__main__":
    main()

