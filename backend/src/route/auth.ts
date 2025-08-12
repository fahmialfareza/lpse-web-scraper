import express from "express";

import { profile } from "@/controller/auth";
import { authenticate, signIn } from "@/middlewares/auth";

const router = express.Router();

router.route("/").get(authenticate, profile);
router.post("/signin", signIn, profile);

export default router;
