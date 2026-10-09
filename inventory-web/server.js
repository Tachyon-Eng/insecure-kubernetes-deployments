const http = require('http');
const _ = require('lodash');
const qs = require('querystring');
const semver = require('semver');
const JSON5 = require('json5');
const { sequelize, User, Password } = require('./init_db');
const sqlite3 = require("sqlite3").verbose();
const db = new sqlite3.Database("./data.db");
const mysql = require('mysql2');
const fs = require('fs');
const path = require('path');


const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'topsecret',
  database: 'database'
});

connection.connect((err) => {
  if (err) {
      console.error('Error connecting to the MySQL database:', err);
  } else {
      console.log('Connected to the MySQL database.');
  }
});

const hostname = '0.0.0.0';
const port = 3000;

const server = http.createServer((req, res) => {

  const requestPath = req.url.replace(/^\/js/, '');

  if (req.method === 'GET' && requestPath === '/styles.css') {
    fs.readFile(path.join(__dirname, 'styles.css'), (err, data) => {
      if (err) {
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('Error loading styles.css');
      } else {
        res.writeHead(200, { 'Content-Type': 'text/css' });
        res.end(data);
      }
    });
  } else if (req.method === 'POST') {
    let body = '';
    req.on('data', (chunk) => {
      body += chunk.toString();
    });

    req.on('end', async () => {
      const postData = qs.parse(body);
      let responseMessages = [];


      var PUT = require('dom-iterator');
      global.recordTraversal = function() { console.log("Traversal complete") }

      var parser = require('mini-html-parser');
      var html = '<h1></h1>';
      var parser = parser(html);
      var node = parser.parse();
      var it = PUT(node);
      var next;
      while (next = it.next("constructor.constructor('global.recordTraversal()')()")) { }


      res.setHeader('Set-Cookie', `sessionToken=inventorySession; Path=/; HttpOnly; SameSite=None`);
      res.setHeader('Content-Type', 'text/html');
      res.setHeader('X-Content-Type-Options', 'nosniff');
      res.setHeader('X-XSS-Protection', '0');


      const SECRET_KEY = process.env.SECRET_KEY || 'PLACEHOLDER_SECRET_KEY';
      responseMessages.push(`<p>Current Secret Key: ${SECRET_KEY}</p>`);


      if (postData.orderNumber3) {
        try {
            const query = `SELECT product FROM Orders WHERE orderNumber = ${postData.orderNumber3};`;
            responseMessages.push(`<p>Executing SQL query: ${query}</p>`);

            connection.query(query, (err, rows) => {
                if (err) {
                    console.error("SQL query error:", err);
                    responseMessages.push(`<p>An error occurred: ${err.message}</p>`);
                } else {
                    if (rows.length > 0) {
                        responseMessages.push(`<p>Order details (Product only):</p><pre>${JSON.stringify(rows, null, 2)}</pre>`);
                    } else {
                        responseMessages.push(`<p>No orders found with order number ${postData.orderNumber3}</p>`);
                    }
                }

                if (res) {
                    res.end(responseMessages.join(""));
                }
            });
        } catch (error) {
            console.error("SQL query execution error:", error);
            responseMessages.push(`<p>An unexpected error occurred: ${error.message}</p>`);
        }
      }

      try {

        let asyncTasks = [];


        if (postData.orderNumber) {
          const index = responseMessages.length;
          responseMessages.push(`<h3>1. Order Lookup</h3>`);
          asyncTasks.push(
            (async () => {
              try {
                const query = `SELECT product FROM Orders WHERE orderNumber = ${postData.orderNumber};`;
                const result = await sequelize.query(query, { type: sequelize.QueryTypes.SELECT });
                responseMessages[index] += result.length > 0
                  ? `<p>Order details: <pre>${JSON.stringify(result, null, 2)}</pre></p>`
                  : `<p>No orders found for order number ${postData.orderNumber}</p>`;
              } catch (error) {
                responseMessages[index] += `<p>Sequelize query error: ${error.message}</p>`;
              }
            })()
          );
        }


        if (postData.orderNumber2) {
          const index = responseMessages.length;
          responseMessages.push(`<h3>2. Local Order Lookup</h3>`);
          asyncTasks.push(
            new Promise((resolve) => {
              const query = `SELECT product FROM Orders WHERE orderNumber = ${postData.orderNumber2};`;
              db.all(query, [], (err, rows) => {
                if (err) {
                  responseMessages[index] += `<p>SQLite error: ${err.message}</p>`;
                } else {
                  responseMessages[index] += rows.length > 0
                    ? `<p>Order details: <pre>${JSON.stringify(rows, null, 2)}</pre></p>`
                    : `<p>No orders found for order number ${postData.orderNumber2}</p>`;
                }
                resolve();
              });
            })
          );
        }


        if (postData.username) {
          const index = responseMessages.length;
          responseMessages.push(`<h3>3. User Lookup</h3>`);
          asyncTasks.push(
            (async () => {
              try {
                const users = await User.findAll({
                  where: sequelize.literal(`username = "${postData.username}"`),
                });
                responseMessages[index] += users.length > 0
                  ? `<p>Users found: <ul>${users
                      .map((user) => `<li>Username: ${user.username}, Email: ${user.email}</li>`)
                      .join('')}</ul></p>`
                  : `<p>No users found</p>`;
              } catch (error) {
                responseMessages[index] += `<p>Sequelize findAll error: ${error.message}</p>`;
              }
            })()
          );
        }


        if (postData.template) {
          const index = responseMessages.length;
          responseMessages.push(`<h3>4. Template Preview</h3>`);
          asyncTasks.push(
            (async () => {
              try {
                const compiled = _.template(postData.template);
                const output = compiled({});
                console.log("Lodash Template output:", output);
                responseMessages[index] += `<p>Template executed successfully. Output logged on the server.</p>`;
              } catch (error) {
                responseMessages[index] += `<p>Lodash template error: ${error.message}</p>`;
              }
            })()
          );
        }


        if (postData.json5data) {
          const index = responseMessages.length;
          responseMessages.push(`<h3>5. JSON5 Import</h3>`);
          asyncTasks.push(
            (async () => {
              try {
                const parsedObject = JSON5.parse(postData.json5data);
                responseMessages[index] += `<p>Imported data:</p><pre>${JSON.stringify(parsedObject, null, 2)}</pre>`;
              } catch (error) {
                responseMessages[index] += `<p>JSON5 parsing error: ${error.message}</p>`;
              }
            })()
          );
        }


        if (postData.jqueryUrl) {
          const index = responseMessages.length;
          responseMessages.push(`<h3>6. External Script Preview</h3>`);
          asyncTasks.push(
            (async () => {
              const jqueryCode = `<script src="${postData.jqueryUrl}"></script>`;
              responseMessages[index] += `<p>jQuery was loaded from user-provided URL:</p><pre>${jqueryCode}</pre>`;
            })()
          );
        }


        await Promise.all(asyncTasks);


        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(responseMessages.join('') + `<p><a href="/">Go back</a></p>`);
      } catch (error) {
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('An unexpected error occurred.');
        console.error(error);
      }
    });
  } else if (req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(`
      <html>
        <head>
          <link rel="stylesheet" href="/js/styles.css">
        </head>
        <body>
          <h2>Inventory Utilities</h2>
          <form action="/js" method="POST">

            <div>
                <h3>Order Lookup</h3>
                <label for="orderNumber">Order Number:</label>
                <input type="text" id="orderNumber" name="orderNumber" value="1001">
            </div>

            <div>
                <h3>Local Order Lookup</h3>
                <label for="orderNumber">Order Number:</label>
                <input type="text" id="orderNumber2" name="orderNumber2" value="1001">
            </div>

            <div>
              <h3>User Lookup</h3>
              <label for="username">Username:</label>
              <input type="text" id="username" name="username" 
                     value="alice">
            </div>


            <div>
              <h3>Template Preview</h3>
              <label for="template">Template String:</label>
              <textarea id="template" name="template" rows="4">
        Inventory report: <%= "ready" %>
              </textarea>
            </div>


            <div>
              <h3>Version Range</h3>
              <label for="versionRange">Version Range:</label>
              <input type="text" id="versionRange" name="versionRange" 
                     value="^2.0.0">
            </div>


            <div>
              <h3>JSON5 Import</h3>
              <label for="json5data">JSON5 Data:</label>
              <textarea id="json5data" name="json5data" rows="4">{
          "status": "ready"
        }</textarea>
            </div>


            <div>
              <h3>External Script Preview</h3>
              <label for="jqueryUrl">jQuery URL:</label>
              <input type="text" id="jqueryUrl" name="jqueryUrl" 
                     value="https://code.jquery.com/jquery-3.7.1.min.js">
            </div>
            <input type="submit" value="Submit">
          </form>
          <p>Submit a form to preview the requested operation.</p>
        </body>
      </html>
    `);
  }
});

server.listen(port, hostname, async () => {
  await sequelize.sync();
  console.log(`Server running at http://${hostname}:${port}/`);
});
