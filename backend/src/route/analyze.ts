import express from "express";

import { getAnalyzeData, removeData } from "@/controller/analyze";
import { authenticate } from "@/middlewares/auth";

const router = express.Router();

router
  .route("/")
  .get(authenticate, getAnalyzeData)
  .delete(authenticate, removeData);

export default router;
