API 详情

# API1001
获取手机验证码, 用于登录或注册. 验证码格式为6位数字, 5分钟内有效

## METHOD: GET

## URL
/api/v1/pin/{phone_number}

## REQUEST

### PARAMS
| name | type | required | description | example |
|----- | -----| ----- | ----- | -----|

### EXAMPLE
/api/v1/pin/13911012345


## RESPONSE

### STATUS
| value | description |
| ----- | -----|
| 200 | OK |
| 403 | 操作过于频繁 |

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
|status| String| true | 请求状态|
|message| String | true | 状态信息描述|
|PIN| String | false | 验证码返回(仅在开发阶段有效)|

### EXAMPLE
~~~javascript
{
  "status": "200",
  "message": "验证码已发送成功",
  "PIN": "319522"
}
~~~

# API1002
用户通过推荐码注册账号

## METHOD: POST

## URL
/api/v1/signup

## REQUEST

### PARAMS
| name | type | required | description | example |
|----- | -----| ----- | ----- | -----|
|phone_number|String|true|注册手机号|13912312345|
|PIN|String|true|手机验证码, 5分钟内有效, 参数名区分大小写| 123321|
|promotion|String|邀请码, 8位字母| CUTBCUWN|

### EXAMPLE
/api/v1/signup/

phone_number=13912312345,

PIN=123321,

promotion=CUTBCUWN


## RESPONSE

### STATUS
| value | description |
| ----- | -----|
| 200 | OK |
| 4xx | Error |

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |


### EXAMPLE
注册成功

# API1003
用户登录

## METHOD: POST

## URL
/api/v1/login

## REQUEST

### PARAMS
| name | type | required | description | example |
|----- | -----| ----- | ----- | -----|
|phone_number|String|true|注册手机号|13912312345|
|PIN|String|true|手机验证码, 5分钟内有效, 参数名区分大小写| 123321|

### EXAMPLE
/api/v1/login/

phone_number=13912312345,

PIN=123321


## RESPONSE

### STATUS
| value | description |
| ----- | -----|
| 200 | OK |
| 4xx | Error |

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |


### EXAMPLE
缺少参数或参数名不匹配: 参数不正确

用户登陆成功: 登陆成功

参数值错误: 账号不存在/验证码错误, 登录失败

# API1004
用户退出登录

## METHOD: GET

## URL
/api/v1/logout

## REQUEST

### PARAMS
| name | type | required | description | example |
|----- | -----| ----- | ----- | -----|

### EXAMPLE
/api/v1/logout/

## RESPONSE

### STATUS
| value | description |
| ----- | -----|
| 200 | OK |
| 4xx | Error |

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |


### EXAMPLE
用户注销成功: 注销成功

# API1005
获取用户信息

## METHOD: GET

## URL
/api/v1/profiles

## REQUEST

### PARAMS
| name | type | required | description | example |
|----- | -----| ----- | ----- | -----|
|nickname|-|false|获取用户昵称|-|
|gender|-|false|获取用户性别|-|
|phone_number|-|false|获取用户手机号|-|
|avatar|-|false|获取用户头像图片URL|-|
|promoter|-|false|获取用户推荐人信息|-|
|promotion|-|false|获取用户剩余邀请码或邀请URL|-|
|labels|-|false|获取用户标签|-|
|promotable|-|false|获取用户是否能升级成为代理|-|
|agent|-|false|获取用户代理状态|-|

### EXAMPLE
/api/v1/profiles?nickname&phone_number&gender&promoter&promotion&avatar&labels

## RESPONSE

### STATUS
| value | description |
| ----- | -----|
| 200 | OK |
| 4xx | Error |

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
|id|Integer|true|用户id|
|nickname|String|false|获取用户昵称|
|gender|String|false|获取用户性别|
|phone_number|String|false|获取用户手机号|
|avatar|String|false|获取用户头像图片URL|
|promoter|Object|false|获取用户推荐人信息|
|promotion|List|false|获取用户剩余邀请码|
|labels|List|false|获取用户标签|
|agent|String|true|获取该用户是否为代理商/代理人, 有三种状态: "是", "正在审核", 和"否"|
|promotable|Boolean|true|获取用户是否能升级成为代理|
|emchatuser|String|true|获取用户环信账号名|
|emchatpd|String|true|获取用户环信账户密码|


### EXAMPLE
~~~javascript
{
  "phone_number": "13111111111",
  "gender": "女",
  "labels": [
    {
      "category": {
        "text": "性格",
        "id": 5,
        "name": "character"
      },
      "text": "坚强自信",
      "id": 3,
      "name": "confident"
    },
    {
      "category": {
        "text": "音乐偏好",
        "id": 6,
        "name": "music_preference"
      },
      "text": "歌剧",
      "id": 4,
      "name": "opera"
    }
  ],
  "promoter": {
    "phone_number": "13888800001",
    "gender": "男",
    "nickname": "李富豪"
  },
  "avatar": "/assets/registrar/user_profile/13111111111/avatar.png",
  "promotion": [],
  "nickname": "李慧媛"
  "emchatuser": "caymen3111111111",
  "emchatpd": "hdfkjdhj",
}
~~~

# API1006
更新用户信息

## METHOD: POST

## URL
/api/v1/profiles

## REQUEST

### PARAMS
| name | type | required | description | example |
|----- | -----| ----- | ----- | -----|
|nickname|String|false|修改用户昵称, 最长不超过20个字|-|
|gender|String|false|修改用户性别, 取值范围为字母'M'(男)或'F'(女)|-|
|avatar|File|false|修改用户头像图片|-|
|label|Int|false|更新用户标签, 重复调用为选中或取消该标签|-|

### EXAMPLE
/api/v1/profiles

label=7

nickname=李慧媛

gender=F

## RESPONSE

### STATUS
| value | description |
| ----- | -----|
| 200 | OK |
| 4xx | Error |

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
|status|String|true|返回状态|
|profile|Object|true|返回修改后的用户信息|
|nickname|String|false|修改后的昵称|
|gender|String|false|修改后的用户性别|
|avatar|String|false|修改后的用户头像图片URL|
|labels|List|false|修改后的用户标签|


### EXAMPLE
~~~javascript
{
  "status": "success",
  "profile": {
    "gender": "女",
    "labels": [
      {
        "category": {
          "text": "年龄段",
          "id": 3,
          "name": "generation"
        },
        "text": "60后",
        "id": 1,
        "name": "60s"
      },
      {
        "category": {
          "text": "性格",
          "id": 5,
          "name": "character"
        },
        "text": "坚强自信",
        "id": 3,
        "name": "confident"
      },
      {
        "category": {
          "text": "音乐偏好",
          "id": 6,
          "name": "music_preference"
        },
        "text": "歌剧",
        "id": 4,
        "name": "opera"
      }
    ],
    "nickname": "李慧媛",
    "avatar": "/assets/registrar/user_profile/13111111111/avatar.png"
  }
}
~~~

# API1007
获取所有标签, 若有参数则返回满足参数条件的所有标签

## METHOD: GET

## URL
/api/v1/labels

## REQUEST

### PARAMS
| name | type | required | description | example |
|----- | -----| ----- | ----- | -----|
|id|Int|false|获取指定id的标签数据|-|
|name|String|false|获取指定名称的标签数据|-|

### EXAMPLE
/api/v1/labels

name=confident

## RESPONSE

### STATUS
| value | description |
| ----- | -----|
| 200 | OK |
| 4xx | Error |

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
|category|Object|true|标签所属种类|
|text|String|true|标签全称|
|id|Int|true|标签id|
|name|String|true|标签简称|
|category.text|String|true|标签种类全称|
|category.id|Int|true|标签种类id|
|category.name|String|true|标签种类简称|


### EXAMPLE
~~~javascript
{
  "category": {
    "text": "性格",
    "id": 5,
    "name": "character"
  },
  "text": "坚强自信",
  "id": 3,
  "name": "confident"
}
~~~

# API1008
获取指定标签

## METHOD: GET

## URL
/api/v1/labels/{id or name}

## REQUEST

### PARAMS
| name | type | required | description | example |
|----- | -----| ----- | ----- | -----|

### EXAMPLE
/api/v1/labels/confident

or

/api/v1/labels/1


## RESPONSE

### STATUS
| value | description |
| ----- | -----|
| 200 | OK |
| 4xx | Not Found |

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
|category|Object|true|标签所属种类|
|text|String|true|标签全称|
|id|Int|true|标签id|
|name|String|true|标签简称|
|category.text|String|true|标签种类全称|
|category.id|Int|true|标签种类id|
|category.name|String|true|标签种类简称|


### EXAMPLE
~~~javascript
{
  "category": {
    "text": "性格",
    "id": 5,
    "name": "character"
  },
  "text": "坚强自信",
  "id": 3,
  "name": "confident"
}

{
  "category": {
    "text": "年龄段",
    "id": 3,
    "name": "generation"
  },
  "text": "60后",
  "id": 1,
  "name": "60s"
}
~~~

# API1009
获取所有标签种类

## METHOD: GET

## URL
/api/v1/label_categories/

## REQUEST

### PARAMS
| name | type | required | description | example |
|----- | -----| ----- | ----- | -----|


### EXAMPLE
/api/v1/label_categories

## RESPONSE

### STATUS
| value | description |
| ----- | -----|
| 200 | OK |

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
|text|String|true|标签种类全称|
|labels|List|true|该种类所含所有标签|
|labels.id|Int|true|标签id|
|labels.name|String|true|标签简称|
|labels.text|String|true|标签全称|


### EXAMPLE
~~~javascript
[
  {
    "text": "年龄段",
    "labels": [
      {
        "text": "60后",
        "id": 1,
        "name": "60s"
      },
      {
        "text": "90后",
        "id": 9,
        "name": "90s"
      },
      {
        "text": "00后",
        "id": 10,
        "name": "00s"
      },
      {
        "text": "70后",
        "id": 27,
        "name": "70s"
      },
      {
        "text": "80后",
        "id": 28,
        "name": "80s"
      }
    ],
    "id": 3,
    "name": "generation"
  }
]
~~~

# API1010
根据URL中给出的id或简称获取指定标签种类

## METHOD: GET

## URL
/api/v1/label_categories/{id or name}

## REQUEST

### PARAMS
| name | type | required | description | example |
|----- | -----| ----- | ----- | -----|


### EXAMPLE
/api/v1/label_categories/3

or

/api/v1/label_categories/generation

## RESPONSE

### STATUS
| value | description |
| ----- | -----|
| 200 | OK |

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
|text|String|true|标签种类全称|
|labels|List|true|该种类所含所有标签|
|labels.id|Int|true|标签id|
|labels.name|String|true|标签简称|
|labels.text|String|true|标签全称|


### EXAMPLE
~~~javascript
[
  {
    "text": "年龄段",
    "labels": [
      {
        "text": "60后",
        "id": 1,
        "name": "60s"
      },
      {
        "text": "90后",
        "id": 9,
        "name": "90s"
      },
      {
        "text": "00后",
        "id": 10,
        "name": "00s"
      },
      {
        "text": "70后",
        "id": 27,
        "name": "70s"
      },
      {
        "text": "80后",
        "id": 28,
        "name": "80s"
      }
    ],
    "id": 3,
    "name": "generation"
  }
]
~~~

# API1011
申请成为代理, 请求返回字符串, 描述请求结果

## METHOD: GET

## URL
/api/v1/apply/agent/

## REQUEST
### PARAMS
| name | type | required | description | in | example |
|-----|----|--------|-----------|---|-------|

### EXAMPLE
curl -X GET "http://120.76.126.214:8000/api/v1/apply/agent"

## RESPONSE

### STATUS
| value | description |
| ----- | ----------- |
|  200  |请求成功|
|403|请求用户无权成为代理|
|400|用户重复申请|

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |

### EXAMPLE
成功: OK
普通用户申请成为代理: User cannot be promoted to be an agent, error.
用户重复申请成为代理: Duplicated application, operation failed.

# API1012
根据URL中给出的id或环信账号获取用户信息

## METHOD: GET

## URL
/api/v1/userinfor/{id or emchatuser}

## REQUEST

### PARAMS
| name | type | required | description | example |
|----- | -----| ----- | ----- | -----|
|nickname|-|false|获取用户昵称|-|
|gender|-|false|获取用户性别|-|
|phone_number|-|false|获取用户手机号|-|
|avatar|-|false|获取用户头像图片URL|-|
|promoter|-|false|获取用户推荐人信息|-|
|promotion|-|false|获取用户剩余邀请码或邀请URL|-|
|labels|-|false|获取用户标签|-|
|promotable|-|false|获取用户是否能升级成为代理|-|
|agent|-|false|获取用户代理状态|-|

### EXAMPLE
/api/v1/profiles?nickname&phone_number&gender&promoter&promotion&avatar&labels

## RESPONSE

### STATUS
| value | description |
| ----- | -----|
| 200 | OK |
| 4xx | Error |

### BODY
| name | type  | not null | description |
| ----- | ----- | ----- | ----- |
|id|Integer|true|用户id|
|nickname|String|false|获取用户昵称|
|gender|String|false|获取用户性别|
|phone_number|String|false|获取用户手机号|
|avatar|String|false|获取用户头像图片URL|
|promoter|Object|false|获取用户推荐人信息|
|promotion|List|false|获取用户剩余邀请码|
|labels|List|false|获取用户标签|
|agent|String|true|获取该用户是否为代理商/代理人, 有三种状态: "是", "正在审核", 和"否"|
|promotable|Boolean|true|获取用户是否能升级成为代理|
|emchatuser|String|true|获取用户环信账号名|
|emchatpd|String|true|获取用户环信账户密码|


### EXAMPLE
~~~javascript
{
  "phone_number": "13111111111",
  "gender": "女",
  "labels": [
    {
      "category": {
        "text": "性格",
        "id": 5,
        "name": "character"
      },
      "text": "坚强自信",
      "id": 3,
      "name": "confident"
    },
    {
      "category": {
        "text": "音乐偏好",
        "id": 6,
        "name": "music_preference"
      },
      "text": "歌剧",
      "id": 4,
      "name": "opera"
    }
  ],
  "promoter": {
    "phone_number": "13888800001",
    "gender": "男",
    "nickname": "李富豪"
  },
  "avatar": "/assets/registrar/user_profile/13111111111/avatar.png",
  "promotion": [],
  "nickname": "李慧媛"
  "emchatuser": "caymen3111111111",
  "emchatpd": "hdfkjdhj",
}
~~~