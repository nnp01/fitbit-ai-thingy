const express = require('express');
const cheerio = require('cheerio');
const fs = require('fs');
const {spawn} = require('child_process');
const app = express()
app.use(express.static('public'));
const port = 3000
var html
var $

app.get('/', (req, res) => {
  html = fs.readFileSync('index.html', 'utf8');
  $ = cheerio.load(html);
  var dataToSend;
  // spawn new child process to call the python script
  const python = spawn('python', ['codeAI.py']);
  // collect data from script
  python.stdout.on('data', function (data) {
  console.log('Pipe data from python script ...');
  dataToSend = data.toString();
  var scriptAnswer = $(`<p class='python'>${dataToSend}</p>`);
  $('.python').replaceWith(scriptAnswer);

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