const path = require('path');
const express = require('express');
const app = express();
const port = 7071;

app.use(express.static(path.join(__dirname, '/src')));
app.get('*', (req,res) =>{
  res.sendFile(path.join(__dirname + '/src/index.html'));
});
app.listen(port, () => console.log(`Listening on port ${port}`));
