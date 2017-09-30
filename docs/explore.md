API 详情

# API1201
获取发现列表页顶部推荐列表

## METHOD: GET

## URL
/explore/highlights/

## REQUEST

### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|


### EXAMPLE
~~~curl
curl --request GET \
  --url http://localhost:8000/api/v1/explore/highlights \
  --header 'cache-control: no-cache' \
~~~

## RESPONSE

### STATUS
| value | description |
| ----- | ----------- |
|  200  | 成功返回列表  |

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
|link|Integer|true|该条推荐所对应发现的id|
|cover|URLString|true|封面图URL|

### EXAMPLE
~~~javascript
[
  {
    "link": 1,
    "cover": "/assets/explore/highlight/None/cover.jpg"
  }
]
~~~

# API1202
分页获取发现列表

## METHOD: GET

## URL
/explore/posts/

|   |
|---|
|   |

## REQUEST
### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|
|  p  |Integer| false | 页码数, 缺省默认为1 | query string |1|

### EXAMPLE
~~~curl
curl --request GET \
  --url 'http://localhost:8000/api/v1/explore/posts/?p=1' \
  --header 'cache-control: no-cache' \
~~~

## RESPONSE
### STATUS
| value | description |
| ----- | ----------- |
|  200  | 成功获取分页列表|
|  400  | 参数p有误    |
|  404  | p超出范围    |


### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
|has_next|Boolean|true|是否有下一页|
|id|Integer|true|该条发现记录id|
|title|String|true|发现标题|
|cover|URLString|true|发现顶部横幅图URL|
|date|String|true|发布时间|
|raw_content|RichText|true|发现内容|

### EXAMPLE
~~~javascript
{
  "has_next": false,
  "list": [
    {
      "raw_content": "<p>对于多数人，玩转香港迪斯尼乐园只能在一天之内了，因为，香港迪斯尼的特点就是园内没酒店。香港迪斯尼乐园占地有120公顷，中有四个园 区，虽然面积也不算太大，但是园中游乐项目众多，游客更是众多，要在一天的时间内把所有的项目都玩遍，您就必须提前制订一个小小的游园 ",
      "date": "2016-06-13",
      "cover": "/assets/explore/posts/1/banner.jpg",
      "id": 1,
      "title": "迪士尼乐园一日游详尽攻略"
    },
    {
      "raw_content": "<p>「THE GREAT YOGA」世界巡迴演唱會正式開跑！這是林宥嘉退伍後回歸歌壇的正式個人大型表演，首場將於 6/11於高雄小巨 蛋登場，也是今年全台唯一一場演出！售票時間為3/19(六)中午12點，KKTIX Famiport同步開賣！此次巡迴城市包含北京、深圳、上海、廣 州、成都等地區，預計20場。</p>\r\n\r\n<p><input alt=\"\" src=\"/assets/richtext_media/2016/06/13/find-detail6-03.png\" style=\"width: 702px; height: 430px;\" type=\"image\" /></p>",
      "date": "2016-06-13",
      "cover": "/assets/explore/posts/7/banner_WM7zRIJ.png",
      "id": 7,
      "title": "The great YOGA 巡回演唱会预计连开20场"
    }
  ]
}
~~~

# API1203
获取具体某条发现记录

## METHOD: GET
## URL
/explore/posts/{id}

## REQUEST
### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|
|id|Integer|true|发现id|URL|

### EXAMPLE
~~~curl
curl --request GET \
  --url http://120.76.126.214:8000/api/v1/explore/posts/7 \
  --header 'cache-control: no-cache' \
~~~


## RESPONSE
### STATUS
| value | description |
| ----- | ----------- |
|200|成功获取指定发现|
|404|找不到对应id发现|

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
|id|Integer|true|该条发现记录id|
|title|String|true|发现标题|
|cover|URLString|true|发现顶部横幅图URL|
|video|HTMLString|true|通用视频链接HTML代码|
|has_video|boolean|true|该条发现是否包含视频|
|date|Date|true|发布时间|
|raw_content|RichText|true|发现内容|

### EXAMPLE
~~~javascript
{
  "raw_content": "<p>「THE GREAT YOGA」世界巡迴演唱會正式開跑！這是林宥嘉退伍後回歸歌壇的正式個人大型表演，首場將於 6/11於高雄小巨 蛋登場，也是今年全台唯一一場演出！售票時間為3/19(六)中午12點，KKTIX Famiport同步開賣！此次巡迴城市包含北京、深圳、上海、廣 州、成都等地區，預計20場。</p>\r\n\r\n<p><input alt=\"\" src=\"/assets/richtext_media/2016/06/13/find-detail6-03.png\" style=\"width: 702px; height: 430px;\" type=\"image\" /></p>",
  "date": "2016-06-13",
  "cover": "/assets/explore/posts/7/banner_WM7zRIJ.png",
  "id": 7,
  "title": "The great YOGA 巡回演唱会预计连开20场"
}
~~~

# API1204
收藏/取消收藏发现

## METHOD: GET
## URL
/explore/posts/{id}/like

## REQUEST
### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|
|id|Integer|true|发现id|URL|

### EXAMPLE
~~~curl
curl --request GET \
  --url http://120.76.126.214:8000/api/v1/explore/posts/1/like \
  --header 'cache-control: no-cache' \
~~~


## RESPONSE
### STATUS
| value | description |
| ----- | ----------- |
|200|成功获取指定发现
|404|找不到对应id发现

### BODY
"收藏发现: XXX"

或

"取消收藏发现: XXX"

### EXAMPLE

# API1205
获取已收藏发现

## METHOD: GET

## URL
/likes/explore/

## REQUEST
### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|

### EXAMPLE
~~~curl
curl --request GET \
  --url http://120.76.126.214:8000/api/v1/likes/explore \
  --header 'cache-control: no-cache' \
~~~

## RESPONSE
### STATUS
| value | description |
| ----- | ----------- |

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
|id|Integer|true|该条发现记录id|
|title|String|true|发现标题|
|cover|URLString|true|发现顶部横幅图URL|
|date|Date|true|发布时间|
|raw_content|RichText|true|发现内容|

### EXAMPLE
~~~javascript
{
  "has_next": false,
  "list": [
    {
      "raw_content": "<p>对于多数人，玩转香港迪斯尼乐园只能在一天之内了，因为，香港迪斯尼的特点就是园内没酒店。香港迪斯尼乐园占地有120公顷，中有四个园 区，虽然面积也不算太大，但是园中游乐项目众多，游客更是众多，要在一天的时间内把所有的项目都玩遍，您就必须提前制订一个小小的游园 ",
      "date": "2016-06-13",
      "cover": "/assets/explore/posts/1/banner.jpg",
      "id": 1,
      "title": "迪士尼乐园一日游详尽攻略"
    },
    {
      "raw_content": "<p>「THE GREAT YOGA」世界巡迴演唱會正式開跑！這是林宥嘉退伍後回歸歌壇的正式個人大型表演，首場將於 6/11於高雄小巨 蛋登場，也是今年全台唯一一場演出！售票時間為3/19(六)中午12點，KKTIX Famiport同步開賣！此次巡迴城市包含北京、深圳、上海、廣 州、成都等地區，預計20場。</p>\r\n\r\n<p><input alt=\"\" src=\"/assets/richtext_media/2016/06/13/find-detail6-03.png\" style=\"width: 702px; height: 430px;\" type=\"image\" /></p>",
      "date": "2016-06-13",
      "cover": "/assets/explore/posts/7/banner_WM7zRIJ.png",
      "id": 7,
      "title": "The great YOGA 巡回演唱会预计连开20场"
    }
  ]
}
~~~

# API1206
评论发现

## METHOD: POST
## URL
/explore/posts/{id}/comment/

## REQUEST
### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|
|id|Integer|true|发现id|URL|
|text|CharField|true|评论内容|form-data|

### EXAMPLE
~~~curl
curl --request GET \
  --url http://120.76.126.214:8000/api/v1/explore/posts/7/comment/ \
  --header 'cache-control: no-cache' \
~~~

## RESPONSE
### STATUS
| value | description |
| ----- | ----------- |
|200|成功获取指定发现|
|404|找不到对应id发现|

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
"添加评论成功"

### EXAMPLE

# API1207
获取发现评论列表

## METHOD: GET

## URL
/explore/posts/{id}/comments/

## REQUEST

### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|
|id|Integer|true|发现id|URL|

### EXAMPLE
~~~curl
curl --request GET \
  --url http://120.76.126.214:8000/api/v1/explore/posts/7/comments/ \
  --header 'cache-control: no-cache' \
~~~

## RESPONSE
### STATUS
| value | description |
| ----- | ----------- |
|200|成功获取指定发现|
|404|找不到对应id发现|

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
|name|String|true|该条发现评论作者昵称|
|avatar|URLString|true|发现评论用户头像图片URL|
|date|Date|true|发布时间|
|text|String|true|发现评论内容|
|count|Integer|false|评论条数|

### EXAMPLE
~~~javascript
{
  "text": "好帅!",
  "date": "2016-06-13",
  "avatar": "/assets/explore/posts/7/banner_WM7zRIJ.png",
  "count": 2,
  "name": "Anne"
}
~~~


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