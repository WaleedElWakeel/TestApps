const express = require("express");
const app = express();
const router = express.Router();

const port = 8080;

router.use(function (req, res, next) {
  console.log("/" + req.method);
  next();
});

router.get("/usecase", function (req, res) {
  res.send({
    Id: 1,
    Name: "Customer Churn",
  });
});

app.use("/", router);

app.listen(port, function () {
  console.log("Example app listening on port 8080!");
});
