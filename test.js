const express = require('express');
const cheerio = require('cheerio');
const fs = require('fs');
const {spawn} = require('child_process');
const app = express()
const port = 3000
var html = fs.readFileSync('C:/Users/students/Desktop/LABASLIETAS' + '/index.html', 'utf8');
var $ = cheerio.load(html);

app.get('/', (req, res) => {
  var dataToSend;
  // spawn new child process to call the python script
  const python = spawn('python', ['codev2.py']);
  // collect data from script
  python.stdout.on('data', function (data) {
  console.log('Pipe data from python script ...');
  dataToSend = data.toString();
  var scriptAnswer = `<p>${dataToSend}</p>`;
  $('body').append(scriptAnswer);

})
python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);
    // send data to browser
    res.send($.html());
    });
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})