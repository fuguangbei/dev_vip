API 详情

# API1901
获取城市列表

## METHOD: GET

## URL
/api/v1/cities/

## REQUEST
### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|

### EXAMPLE
~~~curl
curl -X GET -H "Cache-Control: no-cache" "http://120.76.126.214:8000/api/v1/cities"
~~~

## RESPONSE
### STATUS
| value | description |
| ----- | ----------- |
|  200  | 请求成功     |

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
|  id  |Integer|true|城市id|
| name |String | true     | 城市名称     |
|code  | String|   true   | 城市英文名称  |

### EXAMPLE
~~~javascript
[
  {
    "code": "shanghai",
    "name": "上海",
    "id": 1
  },
  {
    "code": "beijing",
    "name": "北京",
    "id": 2
  },
  {
    "code": "guangzhou",
    "name": "广州",
    "id": 3
  },
  {
    "code": "chengdu",
    "name": "成都",
    "id": 4
  }
]
~~~

# API1902
获取"猜你喜欢"列表, 包含3项商品和2项发现内容

## METHOD: GET

## URL
/api/v1/features/

## REQUEST
### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|


### EXAMPLE
~~~curl
curl -X GET "http://localhost:8000/api/v1/features"
~~~

## RESPONSE

### STATUS
| value | description |
| ----- | ----------- |
|200|成功获取列表|
|4xx|请求方式不为get或未登录|

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
|type|String|true|对象类型, 分别为disney, concert, aerospace, explore|
|id|Integer|true|对象id|
|title|String|true|标题|
|content|String|true|描述文字|
|cover|URLString|true|图片URL|
|price|Number|false|商品价格, 发现内容无此字段|

### EXAMPLE
~~~javascript
[
  {
    "title": "未来宇航员套餐 FUTURE PACKAGE",
    "price": 2000000,
    "cover": "/assets/tickets/12/listingcover.jpg",
    "content": "\n体检\n重力飞行: 花式训练\n培训任务和飞行过程拍摄和制作视频\n两人当地豪华酒店住宿3晚\n带徽章的飞行服\n\n\n\n",
    "type": "aerospace",
    "id": 12
  },
  {
    "title": "冰雪奇缘迪斯尼VIP专属通道",
    "price": 3000,
    "cover": "",
    "content": "",
    "type": "disney",
    "id": 8
  },
  {
    "title": "狮子王套餐",
    "price": 1888,
    "cover": "/assets/tickets/9/listingcover.jpg",
    "content": "",
    "type": "disney",
    "id": 9
  },
  {
    "content": "对于多数人，玩转香港迪斯尼乐园只能在一天之内了，因为，香港迪斯尼的特点就是园内没酒店。香港迪斯尼乐园占地有120公顷，中有四个园区，虽然面积也不算太大，但是园中游乐项目众多",
    "cover": "/assets/explore/posts/1/banner.jpg",
    "type": "explore",
    "id": 1,
    "title": "迪士尼乐园一日游详尽攻略"
  },
  {
    "content": "「THE GREAT YOGA」世界巡迴演唱會正式開跑！這是林宥嘉退伍後回歸歌壇的正式個人大型表演，首場將於 6/11於高雄小巨 蛋登場，也是今年全台唯一一場演出！售票時間為3/19(六)中午12點，KKTIX Famiport同步開賣！此次巡迴城市包含北京、深圳、上海、廣 州、成都等地區，預計20場。\n",
    "cover": "/assets/explore/posts/7/banner_WM7zRIJ.png",
    "type": "explore",
    "id": 7,
    "title": "The great YOGA 巡回演唱会预计连开20场"
  }
]
~~~


# API1903
点赞、收藏类消息标为已读

## METHOD: POST

## URL
/feedback/submit/

## REQUEST
### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|
|content|string|true|反馈意见内容|form-data||

### EXAMPLE
~~~curl
curl -X GET -H "Cache-Control: no-cache" "http://120.76.126.214:8000/api/v1/feedback/submit/"
~~~

## RESPONSE
### STATUS
| value | description |
| ----- | ----------- |
|  400  | 参数错误     |
|  200  | 请求成功     |

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |

### EXAMPLE



# API{versionappapi}
## METHOD: GET
## URL
## REQUEST
### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|
### EXAMPLE
## RESPONSE
### STATUS
| value | description |
| ----- | ----------- |
### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
### EXAMPLE
