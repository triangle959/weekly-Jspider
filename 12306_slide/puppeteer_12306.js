/*
  12306抢票脚本，附带阿里云滑块验证
  需要手动填写12306验证码，保存cookie后在点击购买事件内循环刷新即可实现抢票功能
*/
const puppeteer = require('puppeteer');
const information = {
  username: '', //12306账号名
  password: '',  //12306密码
  year:'2020',
  month: '一月',   
  day: '22',
  start: "福州",
  arrive: "重庆",
  checi: 'D2226',  //车次信息（已知这一趟列车一定会有滑块验证码）
  passenger: '', //乘客信息
};
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
(async () => {
  const browser = await puppeteer.launch({
    headless: false, slowMo: 150, ignoreDefaultArgs: ["--enable-automation"], defaultViewport: {
      width: 1280,
      height: 1080
    },
  });
  const page = await browser.newPage();
  await page.setJavaScriptEnabled(true);
  // page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  await page.goto('https://kyfw.12306.cn/otn/login/init')
  await page.type('#username', information.username)
  await page.type('#password', information.password)
  await page.waitForNavigation({
    waitUntil: 'domcontentloaded'
  })
  console.log(page.url())
  console.log('自行填写验证码后登录')
  await page.waitForNavigation({
    waitUntil: 'load'
  })
  await page.waitForSelector('.welcome-name')
  await page.goto('https://kyfw.12306.cn/otn/leftTicket/init')
  await page.waitForSelector('#fromStationText');  // 等待输入框加载完成

  console.log("选中出发地输入框");
  const start_input = await page.$('#fromStationText')  // 出发地输入框
  await start_input.click()
  console.log("输入出发地");
  await start_input.type(information.start) // 输入出发地
  await start_input.type(" ")  // 激活对应城市下拉选择框 添加一个空格
  await page.keyboard.press('Backspace');  // 删除一个空格
  await page.waitForSelector('#panel_cities>div')  // 等待下拉选择框加载
  let cityList = await page.$$eval('#panel_cities>div .ralign', res=>res.map(ele=>ele.innerText))  // 获取激活选择框中的城市列表
  let listIndex = cityList.map((res,index) => {  // 遍历城市列表获取城市下标
    if(res === information.start){
      return index
    }
  })
  let startIndex = parseInt(String(listIndex).replace(/[^0-9]/ig,""))  // 处理下标
  if(startIndex < 1){  // 增加判断，因为找不到nth-child(0)的元素，当下标小于1时，选择第一个元素
    await page.click("#panel_cities>div:first-child")  // 选中对应城市
  }else {
    await page.click("#panel_cities>div:nth-child("+startIndex+")")  // 选中对应城市
  }

  console.log("选中到达地输入框");
  const end_input = await page.$('#toStationText')
  await end_input.click()
  console.log("输入到达地");
  await end_input.type(information.arrive)
  await end_input.type(" ")  // 激活对应城市下拉选择框 添加一个空格
  await page.keyboard.press('Backspace');  // 删除一个空格
  await page.waitForSelector('#panel_cities>div')  // 等待下拉选择框加载
  cityList = await page.$$eval('#panel_cities>div .ralign',res=>res.map(ele=>ele.innerText))  // 获取激活选择框中的城市列表
  listIndex = cityList.map((res,index) => {  // 遍历城市列表获取城市下标
    if(res ===information.arrive){
      return index
    }
  })
  let endIndex = parseInt(String(listIndex).replace(/[^0-9]/ig,""))  // 处理下标
  if(endIndex < 1){
    await page.click("#panel_cities>div:first-child")  // 选中对应城市
  }else {
    await page.click("#panel_cities>div:nth-child("+endIndex+")")  // 选中对应城市
  }
  await page.tap('#date_icon_1');

  console.log('开始填写日期');
  let date= new Date;
  let month= date.getMonth()+1;
  month= (month<10 ? "0"+month:month);
  let thisMonth= (month.toString());  // 当前月份
  let dataMonth = information.month
  let dataDay = information.day
  await page.waitForSelector("#train_date")  // 等待日期选择框加载完成
  await sleep(100)
  await page.click("#train_date")  // 点击日期选择框
  if(thisMonth === dataMonth){
    await page.click("body > div.cal-wrap > div:nth-child(1) > div.cal-cm > div:nth-child("+dataDay+")")
  }else {
    await page.click("body > div.cal-wrap > div.cal.cal-right > div.cal-cm > div:nth-child("+dataDay+")")
  }

  //点击查询
  await page.click("#query_ticket") 

  // 车次选择以及点击购买
  await page.waitForSelector("#queryLeftTable > tr")
  await sleep(100)
  const ticketTable = await page.$$eval('#queryLeftTable > tr',res=>res.map(ele=>ele.innerText)) // 获取路线车次表格
  let ticketIndex = ticketTable.map((res, index) =>{
    if(res.indexOf(information.checi)!== -1){
      return index
    }
  })
  ticketIndex = parseInt(String(ticketIndex).replace(/[^0-9]/ig,""))
  // console.log(page.$$eval('#queryLeftTable > tr:nth-child(' + ticketIndex + ') > td:last-child > a').innerText);
  if(ticketIndex < 1){
    await page.click("#queryLeftTable > tr:first-child > td:last-child > a")
  }else {
    await page.click('#queryLeftTable > tr:nth-child('+ (ticketIndex + 1) +') > td:last-child > a')
  }

  // 乘客信息选择
  await page.waitForSelector("#normal_passenger_id")
  await sleep(1000)
  console.log("获取联系人信息");
  const contactList = await page.$$eval('#normal_passenger_id > li > label', res=>res.map(ele=>ele.innerText))  // 获取联系人列表数据
  for (let index = 0; index < contactList.length; index ++) {
    console.log(index + "：" +contactList[index]);
    if(contactList[index].toString() === information.passenger){
      if(index < 1){
        await page.click("#normal_passenger_id > li:first-child > label")
      }else {
        await page.click("#normal_passenger_id > li:nth-child("+ (index+1) +") > label")
      }
      console.log('找到啦！' + contactList[index].toString() + " === " + information.passenger)
    }
  }

  // 等待滑块出现
  var slide_btn = await page.waitForSelector('#nc_1_n1t', {timeout: 30000})
  // 计算滑块距离
  const rect = await page.evaluate((slide_btn) => {
      const {top, left, bottom, right} = slide_btn.getBoundingClientRect();
      return {top, left, bottom, right}
  }, slide_btn)
  console.log(rect)
  rect.left = rect.left + 10
  rect.top = rect.top + 10
  const mouse = page.mouse
  await mouse.move(rect.left, rect.top)
  await page.touchscreen.tap(rect.left, rect.top)
  await mouse.down()
  var start_time = new Date().getTime()
  await mouse.move(rect.left + 800, rect.top, {steps: 25})
  await page.touchscreen.tap(rect.left + 800, rect.top,)
  console.log(new Date().getTime() - start_time)
  await mouse.up()
  console.log(await page.evaluate('navigator.webdriver'))
  console.log('end')
  await sleep(500)
  await  page.click('#qr_submit_id')
  // await browser.close();
})();