const express = require('express');
const bodyParser = require('body-parser');
const MongoClient = require('mongodb').MongoClient;
const app = express();

app.use(express.static(__dirname + "/public"));
app.use(bodyParser.urlencoded({extended: true}));

MongoClient.connect('mongodb://forage:forage@ds031741.mlab.com:31741/forage', (err, database) => {
  if (err) return console.log(err)
  db = database
  app.listen(3000, function() {
    console.log('Listening on port 3000');
  })
})

app.post('/query', (req, res) => {
  res.redirect('/');
})
