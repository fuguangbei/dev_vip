API 详情

# API1301
用户发布新的圈子

## METHOD: POST

## URL
/moments/post/

## REQUEST

### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|
|text|CharField|true|圈子内容|form-data|
|banner|File|false|圈子封面图|form-data|

### EXAMPLE
~~~curl
curl -X POST -H "Cache-Control: no-cache" -H "Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW" -F "text=test20160623112332" "http://120.76.126.214:8000/api/v1/moments/post/"
~~~

## RESPONSE

### STATUS
| value | description |
| ----- | ----------- |
|  200  | 发表圈子成功  |
|  400  |传参不正确/文件格式不为图片|

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |


### EXAMPLE


# API1302
分页获取圈子列表

## METHOD: GET

## URL
/moments/posts/

## REQUEST
### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|
|  p  |Integer| false | 页码数, 缺省默认为1 | query string |1|
|self|随意|false|当该值为false或不传该值时表示获取所有通过审核的圈子, 其余为返回当前登录用户发表的圈子|query string|

### EXAMPLE
~~~curl
curl -X GET -H "Cache-Control: no-cache" -H "Postman-Token: 1fb0e213-5ee1-88e0-2a5a-f454ffbe1adb" "http://localhost:8000/api/v1/moments/posts?p=1&self"
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
|id|Integer|true|该条圈子记录id|
|liked|Boolean|true|该条圈子是否被当前登录用户点赞|
|image|URLString|true|圈子内容图URL|
|date|Date|true|发布时间|
|text|String|true|圈子内容|
|publisher|Object|true|发布人信息|
|name|String|true|发布作者昵称|
|avatar|URLString|true|发布人头像URL|
|userid|Integer|true|发布人id|
|author|String|false|当该条圈子为转发内容时返回原作者昵称|
|caption|String|false|当该条圈子为转发内容时返回转发者留言|
|is_original|Boolean|false|某条圈子是否是当前登录用户原创|
|belong_to_current_user|Boolean|false|某条圈子是否是当前登录用户发布的|


### EXAMPLE
~~~javascript
{
  "has_next": false,
  "list": [
    {
      "publisher": {
        "userid":98,
        "name": "333****3333",
        "avatar": "/static/assets/i/app-icon72x72%402x.png"
      },
      "liked": false,
      "publish_time": "2016-07-19T02:44:56.895Z",
      "verified": false,
      "text": "《大鱼·海棠》",
      "image": "/assets/moments/posts/11/image.jpg",
      "is_original": true,
      "belong_to_current_user": true,
      "date": "1天前",
      "id": 11
    }
  ]
}
~~~

# API1303
获取具体某条圈子记录

## METHOD: GET
## URL
/moments/posts/{id}/

## REQUEST
### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|
|id|Integer|true|圈子id|URL|

### EXAMPLE
~~~curl
curl -X GET -H "Cache-Control: no-cache" -H "Postman-Token: 62348df0-b824-1e84-6761-fa13c29afef8" "http://localhost:8000/api/v1/moments/posts/16/"
~~~


## RESPONSE
### STATUS
| value | description |
| ----- | ----------- |
|200|成功获取指定圈子|
|404|找不到对应id圈子|

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
|id|Integer|true|该条圈子记录id|
|liked|Boolean|true|该条圈子是否被当前登录用户点赞|
|liked_count|Integer|true|该条圈子被点赞数|
|image|URLString|true|圈子内容图URL|
|date|Date|true|发布时间|
|text|String|true|圈子内容|
|publisher|Object|true|发布人信息|
|name|String|true|发布作者昵称|
|userid|Integer|true|发布人id|
|avatar|URLString|true|发布人头像URL|
|author|String|false|当该条圈子为转发内容时返回原作者昵称|
|caption|String|false|当该条圈子为转发内容时返回转发者留言|
|is_original|Boolean|false|某条圈子是否是当前登录用户原创|
|belong_current_user|Boolean|true|是否是当前登录用户的圈子|

### EXAMPLE
~~~javascript
{
  "publisher": {
    "userid":1
    "name": "Ethan",
    "avatar": "/static/assets/i/app-icon72x72%402x.png"
  },
  "liked": false,
  "publish_time": "2016-06-24T08:05:45.060Z",
  "verified": true,
  "text": "This is a great moment 2",
  "image": "/assets/moments/posts/10/image.png",
  "is_original": false,
  "belong_to_current_user": false,
  "liked_count": 0,
  "date": "2016-6-24",
  "id": 10
}
~~~

# API1304
点赞/取消点赞圈子

## METHOD: GET
## URL
/moments/posts/{id}/like/

## REQUEST
### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|
|id|Integer|true|圈子id|URL|

### EXAMPLE
~~~curl
curl -X GET -H "Cache-Control: no-cache" -H "Postman-Token: cab72839-1643-eddb-1c39-f7eea407a937" "http://localhost:8000/api/v1/moments/posts/17/like"
~~~


## RESPONSE
### STATUS
| value | description |
| ----- | ----------- |
|200|成功获取指定圈子
|404|找不到对应id圈子

### BODY
"点赞圈子: XXX"

或

"取消点赞圈子: XXX"

### EXAMPLE

# API1305 (已过期, 停止使用)
获取当前登录用户发布的所有圈子

## METHOD: GET

## URL
/moments/myposts/

## REQUEST
### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|
|  p  |Integer| false | 页码数, 缺省默认为1 | query string |1|

### EXAMPLE
~~~curl
curl -X GET -H "Cache-Control: no-cache" -H "Postman-Token: dd7970a2-ee8a-5a48-bc90-7eb66a142f74" "http://localhost:8000/api/v1/moments/myposts"
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
|id|Integer|true|该条圈子记录id|
|liked|Boolean|true|该条圈子是否被当前登录用户点赞|
|image|URLString|true|圈子内容图URL|
|date|Date|true|发布时间|
|text|String|true|圈子内容|
|name|String|true|发布作者昵称|
|avatar|URLString|true|发布作者头像|
|userid|Integer|true|发布人id|
|belong_current_user|Boolean|true|是否是当前登录用户的圈子|

### EXAMPLE
~~~javascript
{
  "has_next": true,
  "belong_current_user": true,
  "list": [
    {
      "liked": true,
      "text": "test20160623112332",
      "image": "",
      "user": {
        "userid":33,
        "name": "John Doe",
        "avatar": "/assets/registrar/user_profile/18283617632/avatar.jpg"
      },
      "date": "2016-06-23T03:23:35.751Z",
      "id": 17
    },
    {
      "liked": false,
      "text": "test20160623111512",
      "image": "",
      "user": {
        "userid":33,
        "name": "John Doe",
        "avatar": "/assets/registrar/user_profile/18283617632/avatar.jpg"
      },
      "date": "2016-06-23T03:15:15.318Z",
      "id": 16
    },
    {
      "liked": false,
      "text": "test20160623",
      "image": "",
      "user": {
        "userid":33,
        "name": "John Doe",
        "avatar": "/assets/registrar/user_profile/18283617632/avatar.jpg"
      },
      "date": "2016-06-23T02:46:41.518Z",
      "id": 15
    }
  ]
}
~~~


# API1306
评论圈子

## METHOD: POST
## URL
/moments/posts/{id}/comment/

## REQUEST
### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|
|id|Integer|true|圈子id|URL|
|text|CharField|true|评论内容|form-data|

### EXAMPLE
~~~curl
curl -X POST -H "Cache-Control: no-cache" -H "Postman-Token: 5525e3ed-d542-ed10-778b-a0f274df5e19" -H "Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW" -F "text=test2" "http://localhost:8000/api/v1/moments/posts/2/comment/"
~~~

## RESPONSE
### STATUS
| value | description |
| ----- | ----------- |
|200|成功获取指定圈子|
|404|找不到对应id圈子|

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
"添加评论成功"

### EXAMPLE

# API1307
获取圈子评论列表

## METHOD: GET

## URL
/moments/posts/{id}/comments/

## REQUEST

### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|
|id|Integer|true|圈子id|URL|

### EXAMPLE
~~~curl
curl -X POST -H "Cache-Control: no-cache" -H "Postman-Token: 5525e3ed-d542-ed10-778b-a0f274df5e19" -H "Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW" -F "text=test2" "http://localhost:8000/api/v1/moments/posts/2/comment/"
~~~

## RESPONSE
### STATUS
| value | description |
| ----- | ----------- |
|200|成功获取指定圈子|
|404|找不到对应id圈子|

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
|user|Object|true|评论人信息|
|name|String|true|该条圈子评论作者昵称|
|avatar|URLString|true|圈子评论用户头像图片URL|
|userid|Integer|true|发布人id|
|date|Date|true|发布时间|
|text|String|true|圈子评论内容|
|count|Integer|false|评论条数|

### EXAMPLE
~~~javascript
{
  "count": 1,
  "data": [
    {
      "date": "2016-06-23T07:47:01.368Z",
      "text": "test2",
      "user": {
        "userid":33,
        "name": "John Doe",
        "avatar": "/assets/registrar/user_profile/18283617632/avatar.jpg"
      }
    }
  ]
}
~~~


# API1308
删除当前用户发表的某条圈子

## METHOD: GET

## URL
/moments/posts/{id}/delete/

## REQUEST

### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|
|id|Integer|true|圈子id|URL|

### EXAMPLE
~~~curl
curl -X GET -H "Cache-Control: no-cache" -H "Postman-Token: 2c71127d-2bf0-8636-7b4a-5ab86cfb8ecf" "http://localhost:8000/api/v1/moments/posts/9/delete/"
~~~

## RESPONSE
### STATUS
| value | description |
| ----- | ----------- |
|200|删除圈子id成功|
|404|找不到对应id圈子|

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |

### EXAMPLE

# API1309
转发圈子

## METHOD: POST

## URL
/moments/posts/{id}/forward

## REQUEST
### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|
|id|Integer|true|圈子id|URL|
|caption|String|false|转发留言内容|form-data|

### EXAMPLE
~~~curl
curl -X POST \
    -H "Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW" \
    -F "caption=This is a great moment" \
    "http://localhost:8000/api/v1/moments/posts/8/forward"
~~~

## RESPONSE
### STATUS
| value | description |
| ----- | ----------- |
|200|转发成功|
|404|找不到id对应圈子|

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