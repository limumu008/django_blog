1. 准备
    1. 配置初始开发环境
    2. 配置 settings.py 文件
    3. 替换默认 User 模型
    4. 创建网站布局
2. 博客结构
    1. startapp blog
    2. model:article
    3. admin:添加 article
    4. views:添加索引视图
    5. map url
    6. 构建模板及 css
    7. 整理
3. 添加功能
    1. 页码
    2. 邮件分享文章
    3. 用户功能
    4. 使用邮件激活账号
    5. 单级评论
    6. 文章标签,提示消息
    7. 账号激活后自动登录
    8. 添加我的文章索引，添加更新文章
    9. markdown 编辑器(一些文件可能未被 git)
    10. 归档
    11. 草稿
    12. 统计字数、评论数、阅读数
4. 部署
    1. 安全设置
    2. 部署准备
    3. 添加日志
    4. 修复
5. 优化
    1. 添加用户信息
    2. 头像
    3. 添加功能：粉丝与关注的人
    4. 文章推荐
    5. 添加动作流
    6. fix
        1. 关注重定向到登录页
        2. 评论重定向到登录页
    7. 添加对文章点赞功能
    8. 添加回复评论功能
    9. 添加多级回复功能
    10. 添加 haystack 搜索引擎
6. 商城
    1. app:shop
    2. app:cart--使用 session
    3. 使用 context_processor
    4. app:order,使用 购物车创建订单。
    5. 商品搜索
    6. 使用 celery 在结算订单时发送邮件
    7. 使用 celery 在分享文章时发送邮件
    8. 添加 PayPal 支付
    9. app:coupon
    10. 推荐系统
7. 在线学习平台
    1. app:courses
    2. 自定义字段：order
    3. Profile 添加 is_teacher field
    4. template and static