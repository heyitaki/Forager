const express = require('express');
const compression = require('compression');
const helmet = require('helmet');
const url = require('url');
const querystring = require('querystring');
const bodyParser = require('body-parser');
const path = require('path');
const pug = require('pug');
const PythonShell = require('python-shell');
const app = express();
const PORT = process.env.PORT || 5000;

app.use(compression());
app.use(helmet());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.static(path.join(__dirname, "public")));
app.set('view engine', 'pug');

app.listen(PORT, function() {
  console.log(`Listening on port ${ PORT }`);
});

app.get('/', (req, res) => {
  res.render('index');
});

app.get('/query', (req, res) => {
  res.status(303).send('303: Use /search.');
});

app.post('/query', (req, res) => {
  res.redirect(url.format({
    pathname: '/search/' + req.body.searchQuery,
  }));
});

app.get('/search/:id', (req, res) => {
  var options = {
    mode: 'json',
    args: [req.params.id],
    scriptPath: './elasticsearch',
  };

  PythonShell.run('search_by_query.py', options, function (err, results) {
      if (err) throw err;
      res.render('results', {query: req.params.id, results: results[0]});
  });
});

app.get('/search/', (req, res) => {
  res.redirect(url.format({
    pathname: '/'
  }));
});

app.get('/question/:id', (req, res) => {
  var options = {
    mode: 'json',
    args: [req.params.id],
    scriptPath: './elasticsearch',
  };

  PythonShell.run('search_by_id.py', options, function (err, results) {
      if (err) throw err; 
      res.render('question', {question: results[0], require: require});
  });
});

app.get('*', (req, res) => {
  res.redirect(url.format({
    pathname: '/'
  }));
});

app.post('*', (req, res) => {
  res.status(404).send('404: Page not found.')
});
