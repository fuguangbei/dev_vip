API 详情

# API1401
获取当前用户的设备信息(包括channel_id/user_id/device_type)

## METHOD: POST

## URL
/notifications/device/

## REQUEST

### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|
|channel_id|string|yes|通道id|data-form|5194127824291972987|
|user_id|string|yes|用户id|data-form|801235190707786080|
|device_type|unicode|yes|设备类型|data-form|3:Android,4:iOS|

### EXAMPLE
~~~curl
curl --request POST \
  --url http://localhost:8000/api/v1/notifications/device/ \
  --header 'cache-control: no-cache' \
~~~

## RESPONSE

### STATUS
| value | description |
| ----- | ----------- |
|  200  | 成功获取设备相关参数  |
|400|参数错误|

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |

### EXAMPLE


# API1402
分页获取消息列表

## METHOD: GET

## URL
/notifications/

## REQUEST
### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|
|  p  |Integer| false | 页码数, 缺省默认为1 | query string |1|

### EXAMPLE
~~~curl
curl --request GET \
  --url 'http://localhost:8000/api/v1/notifications' \
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
|id|Integer|true|该条消息记录id|
|text|String|true|消息文本|
|banner|URLString|true|消息内容图片URL|
|date|String|true|发布时间|
|action|String|true|动作 Comment:评论了 Register:注册成功 Like:收藏了 Dislike:取消收藏了|
|is_read|bool|true|是否已读|
|triggering_user|Object|true|触发者|
|name|String|true|触发者昵称|
|avatar|URLString|true|触发者头像|
|content_type|String|true|消息类型 explore:发现 aerospace:宇航套餐 concert:演唱会 moments:圈子 disney:迪士尼|
|content_id|Integer|true|消息id|
|push_to_self|Boolean|true|接收人和触发者是否是同一用户|

### EXAMPLE
~~~javascript
{
    "triggering_user": {
      "name": "Ethan",
      "avatar": ""
    },
    "is_read": false,
    "date": "17:28",
    "action": "评论了",
    "push_to_self": false,
    "id": 78,
    "push_content": {
      "text": "1234567890",
      "content_id": 9,
      "banner": "/assets/moments/posts/9/image.jpg",
      "content_type": "moments"
    }
}
~~~

# API1403
具体某条消息记录标为已读

## METHOD: GET
## URL
/notifications/notification/{id}/read/

## REQUEST
### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|
|id|Integer|true|消息id|URL|

### EXAMPLE
~~~curl
curl --request GET \
  --url http://localhost:8000/api/v1/notifications/notification/60/read/ \
  --header 'cache-control: no-cache' \
~~~
git

## RESPONSE
### STATUS
| value | description |
| ----- | ----------- |
|200|成功获取指定消息|
|404|找不到对应id消息|

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |

### EXAMPLE

# API1404
获取未读消息数

## METHOD: GET
## URL
/notifications/unread/

## REQUEST
### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|

### EXAMPLE
~~~curl
curl --request GET \
  --url http://localhost:8000/api/v1/notifications/unread/ \
  --header 'cache-control: no-cache' \
~~~
git

## RESPONSE
### STATUS
| value | description |
| ----- | ----------- |
|200|成功获取未读消息数|
|400|参数错误|

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |

### EXAMPLE

# API1405
发送分享类消息推送

## METHOD: GET
## URL
/notifications/share/

## REQUEST
### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|
|shared_type|String|true|分享类型|url|'Explore':发现,'Disney':迪士尼,'Concert':音乐会,'Aerospace':宇航|
|shared_id|Integer|true|分享的某条记录的id|url|8|

### EXAMPLE
~~~curl
curl --request GET \
  --url http://localhost:8000/api/v1/notifications/share/Explore/8/ \
  --header 'cache-control: no-cache' \
~~~
git

## RESPONSE
### STATUS
| value | description |
| ----- | ----------- |
|200|成功获取推送分享类消息|
|400|参数错误|

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |

### EXAMPLE


# API1406
删除当前用户推送设备信息(包括channel_id/user_id/device_type)

## METHOD: GET

## URL
/notifications/device/delete/

## REQUEST

### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|

### EXAMPLE
~~~curl
curl --request POST \
  --url http://localhost:8000/api/v1/notifications/device/delete/ \
  --header 'cache-control: no-cache' \
~~~

## RESPONSE

### STATUS
| value | description |
| ----- | ----------- |
|  200  | 成功删除用户推送设备信息  |
|400|参数错误|

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |

### EXAMPLE


# API1407
删除当前用户推送设备信息(包括channel_id/user_id/device_type)

## METHOD: GET

## URL
/notifications/notification/read/

## REQUEST

### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|

### EXAMPLE
~~~curl
curl --request POST \
  --url http://localhost:8000/api/v1/notifications/notification/read/ \
  --header 'cache-control: no-cache' \
~~~

## RESPONSE

### STATUS
| value | description |
| ----- | ----------- |
|  200  | 成功将相应消息标为已读  |
|400|参数错误|

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