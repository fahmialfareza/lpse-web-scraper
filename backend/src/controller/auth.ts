import { NextFunction, Request, Response } from "express";
import newrelic from "newrelic";
import { z } from "zod";
import { responseSuccess } from "@/utils/response";

export const profile = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  return newrelic.startSegment("controller.user.profile", true, async () => {
    const { user, token } = req;
    if (user && "password" in user) {
      delete user.password;
    }

    responseSuccess(res, { user, token }, 200);
  });
};
