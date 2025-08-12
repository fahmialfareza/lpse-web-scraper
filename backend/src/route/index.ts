import express from "express";
import auth from "./auth";
import analyze from "./analyze";

const router = express.Router();

router.use("/auth", auth);
router.use("/analyze", analyze);

export default router;
