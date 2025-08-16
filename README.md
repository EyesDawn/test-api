# 培训管理API测试工具

这个Python脚本用于测试培训管理系统的REST API接口。

## 📁 文件说明

- `test_training_api.py` - 主要的测试脚本
- `training_test_data.json` - 测试数据文件
- `requirements.txt` - Python依赖包列表
- `API_TEST_README.md` - 使用说明文档

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置服务器地址

编辑 `test_training_api.py` 中的配置：

```python
BASE_URL = "http://your-server:8080"  # 修改为你的服务器地址
TOKEN = "your-auth-token"              # 如果需要认证，设置token
```

### 3. 运行测试

```bash
# 基本用法
python test_training_api.py

# 指定服务器地址
python test_training_api.py http://192.168.1.100:8080

# 指定服务器地址和token
python test_training_api.py http://192.168.1.100:8080 your-auth-token
```

## 📊 测试数据

测试数据包含27条培训记录，涵盖：

- **3种培训类型**: 笔试、仿真机、其它
- **4个班组**: 一班、二班、三班、四班
- **正常和缺考情况**: 包含缺考记录用于测试排名逻辑
- **多样化分数和备注**: 真实模拟实际使用场景

### 测试数据分布

| 培训类型 | 一班 | 二班 | 三班 | 四班 | 总计 |
|----------|------|------|------|------|------|
| 笔试     | 3    | 3    | 2    | 3    | 11   |
| 仿真机   | 3    | 3    | 2    | 0    | 8    |
| 其它     | 3    | 3    | 2    | 0    | 8    |
| **总计** | **9** | **9** | **6** | **3** | **27** |

## 🧪 测试覆盖范围

### 1. 数据管理接口
- ✅ 新增培训记录 (`POST /training/`)
- ✅ 分页查询 (`GET /training/page`)
- ✅ 获取单条记录 (`GET /training/{id}`)

### 2. 查询和筛选
- ✅ 关键字搜索（姓名、备注）
- ✅ 班组筛选
- ✅ 培训类型筛选
- ✅ 缺考状态筛选

### 3. 统计功能
- ✅ 班组排名 (`GET /training/team-ranking`)
- ✅ 培训类型列表 (`GET /training/types`)

### 4. 系统功能
- ✅ 手动更新排名 (`PUT /training/update-ranking`)

## 🔧 自定义测试

### 修改测试数据

编辑 `training_test_data.json` 文件，添加或修改测试记录：

```json
{
  "name": "新员工",
  "team": "新班组",
  "score": 90.0,
  "remark": "测试备注",
  "absent": 0,
  "trainingType": "笔试"
}
```

### 添加新的测试方法

在 `TrainingAPITester` 类中添加新的测试方法：

```python
def test_custom_function(self):
    """自定义测试函数"""
    print("\n🔍 自定义测试")
    result = self.make_request('GET', '/training/custom-endpoint')
    return result
```

## 📝 输出示例

```
🚀 开始API测试
============================================================

🔍 测试新增培训记录接口
==================================================

📝 添加第 1 条记录:
📡 POST http://localhost:8080/training/
   请求体: {
     "name": "张三",
     "team": "一班",
     "score": 92.5,
     "remark": "表现优秀，理论掌握扎实",
     "absent": 0,
     "trainingType": "笔试"
   }
   状态码: 200
   响应: {
     "code": 200,
     "msg": "插入成功",
     "data": 1
   }
✅ 成功创建记录，ID: 1

...

🎉 成功创建 27 条记录

🔍 测试分页查询接口
==================================================

📡 GET http://localhost:8080/training/page
   状态码: 200
   响应: {
     "code": 200,
     "data": {
       "list": [...],
       "total": 27
     }
   }

...

✅ 所有测试完成
```

## 🚨 注意事项

1. **权限问题**: 如果接口需要认证，请确保设置了正确的token
2. **网络连接**: 确保能够访问目标服务器
3. **数据重复**: 多次运行脚本会重复插入数据
4. **服务器状态**: 确保后端服务正常运行
5. **数据库连接**: 确保数据库服务正常

## 🔍 故障排除

### 连接失败
```
❌ 请求失败: Connection refused
```
**解决方案**: 检查服务器地址和端口是否正确

### 认证失败
```
状态码: 401
响应: {"code": 401, "msg": "未授权"}
```
**解决方案**: 检查token是否正确设置

### 权限不足
```
状态码: 403
响应: {"code": 403, "msg": "权限不足"}
```
**解决方案**: 确保账户有相应的操作权限

## 📞 联系支持

如果遇到问题，请检查：
1. 服务器是否正常运行
2. 网络连接是否正常
3. 认证信息是否正确
4. API接口是否有变更

