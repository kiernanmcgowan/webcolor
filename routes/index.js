var config = require('../config/config.json');
var pg = require('pg');

var client = new pg.Client(config.db);
client.connect(function(err) {
  if (err) {
    console.log(err);
  } else {
    console.log('postgres started');
   }
});

exports.index = function(req, res){
  client.query('SELECT * FROM site LIMIT 200', function(err, rs) {
    if (err) {
      res.render('index', {title: 'Internet color', data: []]});
    } else {
      res.render('index', {title: 'Internet color', data: rs.rows});
    }
  });
};