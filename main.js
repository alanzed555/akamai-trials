const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());
const express = require('express');
const bodyParser = require('body-parser');
const url = require('url');
const ghostCursor = require("ghost-cursor");
const adyenEncrypt = require('node-adyen-encrypt')(18);
var util = require('util');
var page;
const page_list = ['https://www.footlocker.com/product/model/starter-sweatshirt-womens/318828.html','https://www.footlocker.com/product/model/starter-sweatshirt-womens/318828.html','https://www.footlocker.com/product/model/nike-satin-hook-t-shirt-mens/323947.html','https://www.footlocker.com/product/model/reebok-vector-crew-mens/318979.html','https://www.footlocker.com/product/model/converse-all-star-ox-boys-grade-school/191450.htm','https://www.footlocker.com/product/model/converse-all-star-ox-womens/149982.html','https://www.footlocker.com/product/model/nike-air-force-1-low-boys-grade-school/100214.html','https://www.footlocker.com/product/nike-air-fear-of-god-moc-mens/M8086200.html', 'https://footlocker.com', 'https://www.footlocker.com/product/nike-lebron-17-low-mens/D5007101.html']

puppeteer.launch({ headless: true, args: [`--window-size=1366,768`] }).then(async browser => {
  page = await browser.newPage();
  page.setViewport({width: 1366, height:728})
  await page.goto('https://footlocker.com');
  await page.evaluate(()=>{
    bmak.fpcf.fpValstr = "1454252292;895908107;dis;,7,8;true;true;true;240;true;24;24;true;false;-1";
    window.innerHeight = 657;
    window.innerWidth = 1366;
//    window.screen.height = 768;
  })
  const cursor = ghostCursor.createCursor(page);
    setInterval(async function(){
    try{await cursor.move('body');
    if(Math.random() > 0.85){await cursor.click();}
    }catch(e){}}, 0.5)
})

async function check_cookies(){
    var tstart = 0;
    while(true){
        var cookies = await page.cookies();
        for(i = 0; i < cookies.length; i++){
            if(cookies[i].name == '_abck'){
                console.log(cookies[i].value);
                if ((cookies[i].value.slice(-12).includes('=~') || cookies[i].value.slice(-12).includes('||')) && !cookies[i].value.slice(-12).includes('==')){
                    return cookies[i].value;
                }
            }
        }
        tstart ++;
        if(tstart > 5){
            await page.goto(page_list[parseInt(Math.random()*11)])
            tstart = 0;
        }
        await new Promise(r => setTimeout(r, 2000));
    }
}

async function abck(abckcookie, link, indx){
    const cookie = {
          name: '_abck',
          value: abckcookie,
          domain: '.footlocker.com',
          url: 'https://www.footlocker.com/',
          path: '/',
          httpOnly: false,
          secure: true
        }
    await page.setCookie(cookie);
    await page.evaluate((link, indx) => {
        history.pushState({}, null, link);
        bmak.apicall_bm(bmak.cf_url, true, bmak.patp);
    }, link, indx);
    return await check_cookies()
}

async function sensor(abckcookie, link, indx){
    const cookie = {
          name: '_abck',
          value: abckcookie,
          domain: '.footlocker.com',
          url: 'https://www.footlocker.com/',
          path: '/',
          httpOnly: false,
          secure: true
        }

    await page.setCookie(cookie);
    return await page.evaluate((link, indx) => {
        history.pushState({}, null, link);
        bmak.cma(MouseEvent, 1);
        bmak.cdma(DeviceMotionEvent);
        bmak.aj_type = 1;
        bmak.aj_index = indx;
        bmak.bpd();
        return bmak.sensor_data;
    }, link, indx);
}

async function adyen_encrypt(adyenkey, card_num, card_month, card_year, card_cvv, card_name){
     const options = {};
     const cardData = {
         number : card_num,       // 'xxxx xxxx xxxx xxxx'
         cvc : card_cvv,                 //'xxx'
         holderName : card_name,   // 'John Doe'
         expiryMonth : card_month, //'MM'
         expiryYear : card_year,   // 'YYYY'
         generationtime : new Date().toISOString() // new Date().toISOString()
     };
     const cseInstance = adyenEncrypt.createEncryption(adyenkey, options);
     console.log(cseInstance.validate({number: card_num, generationtime : new Date().toISOString()}));
     console.log(cseInstance.validate({cvc : card_cvv, generationtime : new Date().toISOString()}));
     console.log(cseInstance.validate({expiryMonth : card_month, generationtime : new Date().toISOString()}));
     console.log(cseInstance.validate({expiryYear : card_year, generationtime : new Date().toISOString()}));
     var encrypteddata = {"encryptedCardNumber":cseInstance.encrypt({number: card_num, generationtime : new Date().toISOString()}),
        "encryptedExpiryMonth":cseInstance.encrypt({expiryMonth : card_month, generationtime : new Date().toISOString()}),
        "encryptedExpiryYear":cseInstance.encrypt({expiryYear : card_year, generationtime : new Date().toISOString()}),
        "encryptedSecurityCode":cseInstance.encrypt({cvc : card_cvv, generationtime : new Date().toISOString()})
     }
     console.log(encrypteddata);
     return encrypteddata;
}

function initBankServer() {
	bankExpressApp = express();

	let port = '7000';
	let address = '127.0.0.1';

	console.log('Bank server listening on port: ' + port);
	bankExpressApp.set('port', port);
	bankExpressApp.set('address', address);
	bankExpressApp.use(bodyParser.json());
	bankExpressApp.use(bodyParser.urlencoded({ extended: true }));

	bankExpressApp.get('/sensor', async function(req, res) {
	    var forminf = url.parse(req.url, true).query;
        res.send(await sensor(forminf.abck, forminf.url, forminf.indx));
        res.end();
    });

    bankExpressApp.get('/akamai', async function(req, res){
        var forminf = url.parse(req.url, true).query;
       res.send(await abck(forminf.abck, forminf.url, forminf.indx));
       res.end();
    });

    bankExpressApp.get('/alternatepage', async function(req, res){
       await page.goto(page_list[parseInt(Math.random()*11)])
       res.send('reloaded');
       res.end();
    });

    bankExpressApp.get('/adyen', async function(req, res){
        var forminf = url.parse(req.url, true).query;
        res.send(await adyen_encrypt(forminf.adyen_key, forminf.number, forminf.month, forminf.year, forminf.cvv, forminf.name));
        res.end();
    });

	bankServer = bankExpressApp.listen(bankExpressApp.get('port'), bankExpressApp.get('address'));
	}

initBankServer();