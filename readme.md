# 卡曼天连VIP尊享移动应用API说明

# 开发/测试服务器:
http://:8000/

# API根目录: 
/api/v1/

# 首页/通用APIs

| API ID | 功能 | URL | 请求方式 | 登陆 | 备注 |
|--------|----- |-----|------------------|---------|------|------------|-----|--------| 
|[API1901](docs/universal.md#api1901)|获取城市列表|/cities/|get|否|
|[API1902](docs/universal.md#api1902)|获取"猜你喜欢"列表|/features/|get|是|
|[API1903](docs/universal.md#api1903)|提交意见反馈|/feedback/submit/|post|是|

# 注册登录APIs

| API ID | 功能 | URL | 请求方式 | 登陆 | 备注 |
|--------|----- |-----|------------------|---------|------|------------|-----|--------| 
|[API1001](docs/registrar.md#api1001)|获取手机验证码|/pin/{phone_number}|get|否| 11位手机号
|[API1002](docs/registrar.md#api1002)|用户推荐码注册|/signup|post|否|
|[API1003](docs/registrar.md#api1003)|用户登录|/login|post|否|
|[API1004](docs/registrar.md#api1004)|用户退出登录|/logout|get|是|
|[API1005](docs/registrar.md#api1005)|获取用户信息|/profiles|get|是|
|[API1006](docs/registrar.md#api1006)|更新用户信息|/profiles|post|是|
|[API1007](docs/registrar.md#api1007)|获取标签|/labels|get|否|
|[API1008](docs/registrar.md#api1008)|根据id或名字获取标签|/labels/{id or name}|get|否|
|[API1009](docs/registrar.md#api1009)|获取标签种类|/label_categories|get|否|
|[API1010](docs/registrar.md#api1010)|根据id或名字获取标签种类|/label_categories|get|否|
|[API1011](docs/registrar.md#api1011)|申请成为代理|/apply/agent/|get|是|

# 门票/商品APIs

| API ID | 功能 | URL | 请求方式 | 登陆 | 备注 |
|--------|----- |-----|------------------|---------|------|------------|-----|--------| 
|[API1101](docs/merchandise.md#api1101)|获取门票列表|/tickets/{ticket_type}|get|否|
|[API1102](docs/merchandise.md#api1102)|获取门票详情|/tickets/{ticket_type}/{id}|get|否|
|[API1103](docs/merchandise.md#api1103)|收藏/取消收藏门票|/tickets/{ticket_type}/{id}/like|get|是|
|[API1104](docs/merchandise.md#api1104)|获取已收藏门票|/likes/tickets/{ticket_type}|get|是|
|[API1105](docs/merchandise.md#api1105)|获取门票广告列表|/commercials|get|否|
|[API1106](docs/merchandise.md#api1106)|下商品订单(迪士尼/演唱会门票)|/tickets/{ticket_type}/{id}/purchase|post|是|
|[API1107](docs/merchandise.md#api1107)|取消商品订单|/orders/{order_number}/cancel|post|是|
|[API1108](docs/merchandise.md#api1108)|搜索商品|/search/|get|否|
|[API1109](docs/merchandise.md#api1109)|获取个人订单列表|/orders/|get|是|
|[API1110](docs/merchandise.md#api1110)|获取订单详情|/orders/{order_number}|get|是|

# 发现功能APIs
| API ID | 功能 | URL | 请求方式 | 登陆 | 备注 |
|--------|----- |-----|------------------|---------|------|------------|-----|--------| 
|[API1201](docs/explore.md#api1201)|获取发现列表页顶部推荐列表|/explore/highlights/|get|否|
|[API1202](docs/explore.md#api1202)|分页获取发现列表|/explore/posts/|get|否|
|[API1203](docs/explore.md#api1203)|获取具体某条发现记录|/explore/posts/{id}|get|否|
|[API1204](docs/explore.md#api1204)|收藏/取消收藏发现|/explore/posts/{id}/like|get|是|
|[API1205](docs/explore.md#api1205)|获取已收藏发现|/likes/explore|get|是|
|[API1206](docs/explore.md#api1206)|评论发现|/explore/posts/{id}/comment/|post|是|
|[API1207](docs/explore.md#api1207)|获取发现评论列表|/explore/posts/{id}/comments/|get|否|

# 圈子功能APIs
| API ID | 功能 | URL | 请求方式 | 登陆 | 备注 |
|--------|----- |-----|------------------|---------|------|------------|-----|--------|
|[API1301](docs/moments.md#api1301)|用户发布新的圈子|/moments/post/|post|是|
|[API1302](docs/moments.md#api1302)|分页获取圈子列表|/moments/posts/|get|否|
|[API1303](docs/moments.md#api1303)|获取具体某条圈子记录|/moments/posts/{id}/|get|否|
|[API1304](docs/moments.md#api1304)|点赞/取消点赞圈子|/moments/posts/{id}/like/|get|是|
|API1305|分页获取当前登录用户发布的所有圈子|/moments/myposts/|get|是|
|[API1306](docs/moments.md#api1306)|评论圈子|/moments/posts/{id}/comment/|post|是|
|[API1307](docs/moments.md#api1307)|获取圈子评论列表|/moments/posts/{id}/comments/|get|否|
|[API1308](docs/moments.md#api1308)|删除当前用户发表的某条圈子|/moments/posts/{id}/delete/|get|是|
|[API1309](docs/moments.md#api1309)|转发圈子|/moments/posts/{id}/forward/|post|是|

# 消息推送功能APIs
| API ID | 功能 | URL | 请求方式 | 登陆 | 备注 |
|--------|----- |-----|------------------|---------|------|------------|-----|--------|
|[API1401](docs/notifications.md#api1401)|获取当前用户的设备信息(包括channel_id/user_id/device_type)|/notifications/device/|post|是|
|[API1402](docs/notifications.md#api1402)|分页获取消息列表|/notifications/|get|是|
|[API1403](docs/notifications.md#api1403)|具体某条消息记录标为已读|/notifications/notification/{id}/read/|get|是|
|[API1404](docs/notifications.md#api1404)|获取未读消息数|/notifications/unread/|get|是|
|API1405(docs/notifications.md#api1405)|发送分享类消息推送|/notifications/share/|get|是|
|API1406(docs/notifications.md#api1406)|删除当前用户推送设备信息(包括channel_id/user_id/device_type)|/notifications/device/delete/|get|是|
|[API1407](docs/notifications.md#api1407)|点赞、收藏类消息标为已读|/notifications/notification/read/|get|是|
