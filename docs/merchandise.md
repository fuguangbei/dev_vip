API 详情

# API1101
分页获取门票的简单数据, 用于列表页的显示

## METHOD: GET

## URL
/api/v1/tickets/{ticket_type}

## REQUEST

### PARAMS
| name | type | required | description | in | example |
|----- | -----| ----- | ----- | -----| ---- |
|ticket_type|String|true|门票种类, 如迪士尼| URL | disney/concert/aerospace/scenery |
|p     |Integer|false|页码数, 缺省时则不分页返回结果| query | 

### EXAMPLE
/api/v1/tickets/disney?p=1

## RESPONSE

### STATUS
| value | description |
| ----- | -----|
| 200 | OK |

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
|has_next|Boolean|true|是否有下一页|
|listing_cover|String|true|门票列表页封面图|
|id|Integer|true|门票id|
|time|Date|false|门票时间|
|title|String|true|门票名称|
|type|String|true|门票种类|
|remaining|Integer|false|门票剩余数|

### EXAMPLE
~~~javascript
{
  "has_next": false,
  "list": [
    {
      "listing_cover": "/assets/tickets/1/listingcover.jpg",
      "type": "disney",
      "id": 1,
      "title": "狮子王套餐"
    },
    {
      "listing_cover": "/assets/tickets/2/listingcover.jpg",
      "type": "disney",
      "id": 2,
      "title": "VVIP专属通道"
    },
    {
      "listing_cover": "/assets/tickets/6/listingcover.jpg",
      "type": "disney",
      "id": 6,
      "title": "团队套餐"
    }
  ]
}
~~~

# API1102
获取门票的详细信息, 用于详情页的显示

## METHOD: GET

## URL
/api/v1/tickets/{ticket_type}/{id}

## REQUEST

### PARAMS
| name | type | required | description | example |
|----- | -----| ----- | ----- | -----|
|ticket_type|String|true|指定待获取的门票种类| disney/concert/aerospace/scenery|
|id|Integer|true|指定门票id|3|

### EXAMPLE
/api/v1/tickets/concert/8

## RESPONSE

### STATUS
| value | description |
| ----- | -----|
| 200 | OK |
| 404 | 找不到对应id的迪士尼门票|

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
|id|Integer|true|门票id|
|listing_cover|String|true|门票列表页封面图|
|detail_cover|String|true|门票详情页封面图|
|title|String|true|门票名称|
|price|Integer|true|门票价格|
|remaining|Integer|true|剩余门票张数|
|vip_channel|RichText|true|"VIP通道"说明|
|purchase_notes|RichText|true|"购买须知"说明|
|package_introduction|RichText|true|"套餐介绍"说明|
|vip_seating|RichText|true|"VIP专座"说明|
|entry_notes|String|false|迪士尼或演唱会票的入场须知说明|
|location|String|true|演唱会地点|
|time|Date|true|演唱会时间|
|performance_introduction|RichText|true|"演出介绍"说明|
|seat|string|true|观演位置|
|schedule|list|false|迪士尼每日余票量的列表|
|schedule.date|Date|true|该余票所代表的日期|
|schedule.id|integer|true|该余票在后台的id|
|schedule.count|integer|true|余票量|

### EXAMPLE

迪士尼门票:
~~~javascript
{
  "purchase_notes": "",
  "title": "冰雪奇缘迪斯尼VIP专属通道",
  "price": 3000,
  "listing_cover": "/assets/tickets/8/cover.jpg",
  "detail_cover": "/assets/tickets/8/cover.jpg",
  "package_introduction": "",
  "vip_channel": "<p style=\"text-align:center\"><span style=\"font-size:22px\">标题</span></p>\r\n\r\n<p style=\"text-align:center\"><input alt=\"\" src=\"/assets/richtext_media/2016/05/20/disney-cover-012x.jpg?size=tiny\" style=\"height:78px; width:100px\" type=\"image\" /></p>\r\n\r\n<p>正文正文<span style=\"color:#FF0000\">带颜色的正文</span></p>",
  "entry_notes": "听工作人员安排",
  "id": 8,
  "remaining": 0
}
~~~

演唱会门票
~~~javascript
{
  "performance_introduction": "<h3 style=\"text-align: center;\"><input alt=\"\" src=\"/assets/richtext_media/2016/05/25/concert-07-detail-012x.jpg\" type=\"image\" /></h3>\r\n\r\n<h3 style=\"text-align: center;\">关于演出</h3>\r\n\r\n<p>郑伊健、陈小春、谢天华、林晓峰、钱嘉乐经典不可复制的兄弟情<br />\r\n岁月友情香港演唱会场场爆满，现在他们来到内地<br />\r\n他们影响了整整一代青年，在电影中学习那种男人应该有的热血，冲劲，尊师重道的原则，为朋友两肋插刀的仗义，那份兄弟情义。<br />\r\n若干年后，心中总还有一个回忆，有这么一个叫陈浩南的年轻人，无比威严的说出&ldquo;整个铜锣湾就只有我一个浩南，陈浩南！&rdquo;。<br />\r\n当他们再次聚在一起，我们那肆无忌惮的青春记忆也跟着一起回来了。</p>",
  "title": "一起兄弟 歲月友情演唱會",
  "price": 4250,
  "listing_cover": "/assets/tickets/None/cover.png",
  "detail_cover": "/assets/tickets/None/cover.png",
  "id": 3,
  "vip_seating": "<p style=\"text-align: center;\"><input alt=\"\" src=\"/assets/richtext_media/2016/05/25/concert-seat.jpg\" style=\"width: 1029px; height: 636px;\" type=\"image\" /></p>\r\n\r\n<p>VIP专座为奔驰中心最佳观看位置，共12座。</p>\r\n\r\n<p>在本平台购买演出门票的用户，演唱会当日可根据手机购票信息，走本平台专用通道进入VIP专座区。</p>\r\n\r\n<p>在工作人员安排下就坐观看演出。</p>",
  "location": "梅德赛斯奔驰中心东区 (上海市浦东新区世博大道1200号区)",
  "entry_notes": "听工作人员安排",
  "time": "2016-06-18",
  "type": "concert",
  "remaining": 42,
  "purchase_notes": "<h3 style=\"text-align: center;\">注意事项</h3>\r\n\r\n<p>为避免快递配送不能及时送达，演出距开场时间少于3天时不提供【快递配送】服务，请您谅解！您可以选择在线支付后上门自取纸质票。客服会第一时间电话联系您，请保持电话畅通。</p>\r\n\r\n<p>凡演出票类商品，开票时间一般为演出前二到四周，正式开票后如有特殊情况客服会第一时间电话联系您，请保持电话畅通。</p>"
}
~~~

景区门票:
~~~javascript
{
  "entry_notes": "",
  "liked": false,
  "purchase_notes": "",
  "title": "布达拉宫",
  "caption_description": "erere",
  "schedule": [],
  "package_introduction": "",
  "price": 1,
  "listing_cover": "/assets/tickets/None/listingcover_XvgS1pZ.jpg",
  "caption_title": "efef",
  "detail_cover": "/assets/tickets/None/detailcover.jpg",
  "type": "scenery",
  "id": 17,
  "remaining": 0
}
~~~
# API1103
收藏或取消收藏门票

## METHOD: GET

## URL
/api/v1/tickets/{ticket_type}/{id}/like

## REQUEST

### PARAMS
| name | type | required | description | example |
|----- | -----| ----- | ----- | -----|
|ticket_type|String|true|门票种类|disney/concert/aerospace/scenery|
|id|Integer|true|门票id|3|

### EXAMPLE
/api/v1/tickets/disney/8/like

## RESPONSE

### STATUS
| value | description |
| ----- | -----|
| 200 | OK |
| 404 | 找不到对应id的门票|

### BODY
"收藏门票: XXX"

或

"取消收藏门票: XXX"

### EXAMPLE

# API1104
获取已收藏门票

## METHOD: GET

## URL
/api/v1/likes/tickets/{ticket_type}

## REQUEST

### PARAMS
| name | type | required | description | example |
|----- | -----| ----- | ----- | -----|
|ticket_type|String|false|指定门票种类, 为空则获取所有已收藏门票| disney/concert/aerospace/scenery

### EXAMPLE
/api/v1/likes/tickets/

or 

/api/v1/lies/tickets/disney

## RESPONSE

### STATUS
| value | description |
| ----- | -----|
| 200 | OK |
| 404 | 找不到对应id的门票|

### BODY
"收藏门票: XXX"

或

"取消收藏门票: XXX"

### EXAMPLE
~~~javascript
[
  {
    "cover": "/assets/tickets/8/cover.jpg",
    "type": "disney",
    "id": 8,
    "validity": "2016-09-30",
    "title": "冰雪奇缘迪斯尼VIP专属通道"
  },
  {
    "cover": "/assets/tickets/9/cover.jpg",
    "type": "disney",
    "id": 9,
    "validity": "2016-09-30",
    "title": "狮子王套餐"
  }
]
~~~

# API1105
获取门票广告, 用于首页显示

## METHOD: GET

## URL
/api/v1/commercials

## REQUEST

### PARAMS
| name | type | required | description | example |
|----- | -----| ----- | ----- | -----|

### EXAMPLE
/api/v1/commercials

## RESPONSE

### STATUS
| value | description |
| ----- | -----|
| 200 | OK |

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
|type|String|true|广告所指向商品种类, 可能为disney, concert, space, scenery|
|id|Integer|true|广告所指向商品id|
|cover|String|true|广告封面图URL|

### EXAMPLE
~~~javascript
[
  {
    "cover": "/assets/tickets/9/cover.jpg",
    "type": "disney",
    "id": 9
  },
  {
    "cover": "/assets/tickets/8/cover.jpg",
    "type": "disney",
    "id": 8
  },
  {
    "cover": "/assets/tickets/None/cover.png",
    "type": "concert",
    "id": 11
  }
]
~~~

# API1106 
下订单准备购买迪士尼或演唱会门票商品

## METHOD: GET

## URL
/api/v1/tickets/{ticket_type}/{id}/purchase

## REQUEST

### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|
|payment|String|true|付款方式, alipay、wechatpay、unionpay| URL| alipay/wechatpay/unionpay|
|ticket_type|String|true|需要购买的票的种类, disney、concert、scenery| URL| disney/concert/scenery|
|id|Integer|true|待购买票的id|URL|2|
|identification|String|depends|身份证号, 购买迪士尼票和景区门票时必传|formdata| 510104199001011234|
|count|Integer|true|购票数量, 购买迪士尼票时最大为5, 购买演唱会票时最大为该票种剩余张数|formdata|12|
|pickup|Boolean|false|是否需要接送, 购买迪士尼票时选填, 其他票时不填|formdata|true/false|
|shipping_address|String|false|收票地址, 购买演唱会票时选填, 其他票不填|formdata|下南大街2号|
|contact|String|true|联系电话|formdata|13822200001|
|schedule|Integer|true|所选日期id, 取值为API1102返回的schedule列表中的schedule.id|


### EXAMPLE
~~~curl
curl --request POST \
  --url http://120.76.126.214:8000/api/v1/tickets/disney/11/purchase \
  --header 'cache-control: no-cache' \
  --header 'content-type: multipart/form-data; boundary=---011000010111000001101001' \
  --form identification=510104199006039999 \
  --form count=6 \
  --form pickup=true \
  --form contact=13822200001
  --form payment=wechatpay
~~~

## RESPONSE

### STATUS
| value | description |
| ----- | ----------- |
| 200   | 创建订单成功 |
| 400   | post参数错误或创建银联订单失败 |
| 403   | 余票不足, 或超过限购数量|
| 404   | 找不到type和id所对应的票|

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
|tn|String|true|银联受理订单号|
|order_number|String|true|商品订单号|

### EXAMPLE
200:
~~~javascript
unionpay
{
  "tn": "201606071559030468488",
  "order_number": "11160607003"
}
wechatpay
{
  "order_number": "16160831055",
  "result": {
    "package": "Sign=WXPay",
    "timestamp": "1472627883",
    "sign": "5D7C69560D5C4171A437DFCF40CADE13",
    "partnerid": "1384731102",
    "appid": "wx6c05f90910b55d08",
    "prepayid": "wx20160831151803f0ee0b3dd40523618990",
    "noncestr": "JkDTzAOsYYuccniJ758gr7NaccscOaA6"
  }
alipay
{
  "seller_email": "dglfmg7945@sandbox.com",
  "body": "套餐",
  "out_trade_no": "07160907004",
  "service": "mobile.securitypay.pay",
  "_input_charset": "utf-8",
  "it_b_pay": "30m",
  "notify_url": "http:120.76.126.214:8000/alipay_notify_url/",
  "payment_type": "1",
  "total_fee": "6888.00",
  "sign_type": "RSA",
  "partner": "2088102168670384",
  "sign": "RbqYPLwdxSwKfGYVOQj1Orbah8/Q4l9HxQYv8c5NY%2BevcNlB34DmncjmrUHqsvZuW02Q0/dcsPIskNP/Kj01xoADGBVyZUVfILtpjyx7bLhH96ENn62mrL%2BXs%2BLc7h0DXReug52Dzq10PWFdgTStcJkusqfZ9SxjrIkCVZRvD0A%3D",
  "subject": "订单商品"
}
}
~~~

400: "订票参数传值有错, 提交订单失败"

403: "一次性购票不能超过5张" "该商品剩余数量为0, 余票不足, 提交订单失败"

404: "演唱会票101不存在, 提交订单失败"


# API1107
取消商品交易, 关闭订单, 并释放预留票

## METHOD: POST

## URL
/api/v1/orders/{order_number}/cancel

## REQUEST

### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|
|order_number|String|true|需要取消的订单号, 该订单号为下订单时返回的order_number字段| URL| 01160610999 |



### EXAMPLE
~~~curl
curl --request POST \
  --url http://120.76.126.214:8000/api/v1/orders/09160607001/cancel \
  --header 'cache-control: no-cache' \
~~~

## RESPONSE

### STATUS
| value | description |
| ----- | ----------- |
| 200   | 成功取消订单 |
| 400   | 重复取消订单 |
| 403   | 订单不由当前用户创建 |
| 404   | 找不到对应订单 |

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |

### EXAMPLE
200: "订单09160607001已取消"

400: "重复取消订单 09160607001, 操作失败"

403: "订单09160607001不属于用户王小明, 取消失败"

404: "订单不存在, 取消失败"


# API1108
搜索所有商品, 匹配标题中包含给出关键字的商品

## METHOD: GET

## URL
/api/v1/search/

## REQUEST
### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|
|  q  |String|true  |URL encode之后的搜索关键字, 原字符串以空格隔开| query| 

### EXAMPLE
~~~curl
curl -X GET -H "Cache-Control: no-cache" -H "http://localhost:8000/api/v1/search?q=狮子王+宇航+友情"
~~~

## RESPONSE
### STATUS
| value | description |
| ----- | ----------- |
|  200  |返回搜索结果列表|
|  400  | 参数上传有问题|

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
|  id  |Integer|true|搜索结果对象id|
|category|String|true|该条搜索结果的种类(门票或发现)|
|type|String|false|若该条搜索结果为门票, 则返回该字段, 指出门票类型 (迪士尼, 演唱会,  景区等)|
|title|String|true|搜索结果名称|

### EXAMPLE
~~~javascript
[
  {
    "category": "ticket",
    "type": "disney",
    "id": 9,
    "title": "狮子王套餐"
  }
]
~~~

# API1109
获取个人订单列表

## METHOD: GET

## URL
/api/v1/orders/?p=X&filter=Y

## REQUEST
### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|
|p|Integer|false|页码数, 不传该值则为获取整个列表, 不启动分页功能|query|/orders/?p=1
|filter|String|false|增加结果过滤, 控制获取未使用和已使用的订单, 不传该值则为返回所有结果|query|/orders/?filter=past (prospective)|

### EXAMPLE
~~~curl
curl -X GET \
    -H "Cache-Control: no-cache"\
    "http://120.76.126.214:8000/api/v1/orders/?p=1&filter=prospective"
~~~

## RESPONSE
### STATUS
| value | description |
| ----- | ----------- |
|200|成功返回列表|
|400|参数p或filter有错|
|404|页码数不合法|

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
|has_next|boolean|false|是否有下一页, 只在分页模式下显示|
|list|List|false|分页模式下显示, 包含结果列表|
|count|integer|true|订单购买量|
|ticket|Object|true|该订单对应商品(票)基础信息|
|order_number|String|true|订单号|

### EXAMPLE
~~~javascript
{
  "has_next": false,
  "list": [
    {
      "count": 1,
      "ticket": {
        "type": "disney",
        "id": 9,
        "validity": "2016-09-30",
        "title": "狮子王套餐"
      },
      "order_number": "09160607000"
    },
    {
      "count": 1,
      "ticket": {
        "time": "2016-06-16T11:15:49Z",
        "type": "concert",
        "id": 11,
        "title": "一起兄弟 歲月友情演唱會"
      },
      "order_number": "11160607000"
    }
  ]
}
~~~

# API1110
获取订单详情

## METHOD: GET

## URL
/api/v1/orders/{order_number}/

## REQUEST
### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|
|order_number|string|true|11位订单号|URL|/orders/11160607364|

### EXAMPLE
~~~curl
curl -X GET -H "Cache-Control: no-cache" "http://120.76.126.214:8000/api/v1/orders/11160607000"
~~~

## RESPONSE
### STATUS
| value | description |
| ----- | ----------- |
| 200 |成功获取详情|
|404|找不到订单|

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
|order_number|string|true|订单号|
|shipping_status|string|true|订单寄送状态|
|shipping_code|string|false|当订单寄出后显示快递单号|
|ticket|object|true|订单对应票商品基础信息|

### EXAMPLE
~~~javascript
{
  "shipping_status": "正在寄送",
  "ticket": {
    "type": "concert",
    "id": 11
  },
  "order_number": "11160607000"
}
~~~