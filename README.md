# 学生综合信息平台（后端）

## 接口设计( /api )

### /login [POST]
* 登录
* 接口来源  
    http://cer.nju.edu.cn/amserver/UI/Login  
* 请求格式  
    name: 学号  
    key: 密码  
    code: 验证码  
* 返回格式  
    [ 认证结果字符串 ]  
    列表为空 —— 登录失败  
    cer_success —— 统一身份认证成功  
    
### /personInfo [GET]
* 获取个人信息
* 接口来源   
    http://imp.nju.edu.cn/imp/iss/myAccount.do?action=getMyAcount
* 返回格式  
    name: 姓名  
    id: 学号  
    identity: 身份证号  
    college: 所在学院  
    phone: 联系电话  
    email: 电子邮箱  
    
### /card/info [GET]
* 获取校园卡相关基础信息
* 接口来源  
    http://mapp.nju.edu.cn/mobile/getCardInfo.mo  
    https://cpay.nju.edu.cn/pay/ykt/cardstatus  
    https://cpay.nju.edu.cn/pay/bankcard/list
* 返回格式  
    name: 姓名  
    balance: 余额  
    bankCardNo: 绑定银行卡号  
    status: 状态  
    
### /card/record [GET]
* 查询一段时间内的消费明细记录
* 接口来源  
    https://oa.nju.edu.cn/ecard/web/学号/1  
    *http://mapp.nju.edu.cn/mobile/getTransList.mo*此接口未使用  
* 查询参数  
    from: [yyyy-MM-dd]开始时间  
    to: [yyyy-MM-dd]结束时间  
    区间均包含两侧端点   
* 返回参数  
    details: 条目细节  
        [  
        transTime: 消费时间  
        transName: 条目类别  
        amount: 消费金额  
        balance: 余额  
        termName: 条目名称  
        ]  
    daily: 按日计算的支出  
        [ 按序排列的支出金额 ]  
    income: 转入金额总和  
    expense: 支出金额总额  

### /card/payment [GET]
* 按月查询支出的组成情况
* 接口来源  
    http://mapp.nju.edu.cn/mobile/getTransList.mo  
* 查询参数  
    month: [yyyyMM]查询月份  
* 返回参数  
    [  
    value: 分类金额  
    name: 分类名  
    ]  
## 资源列表
记录使用的来自其他网站的资源  

|URL|用途|
|:---|:---|
|http://cer.nju.edu.cn/amserver/verify/image.jsp|登录认证用验证码|
