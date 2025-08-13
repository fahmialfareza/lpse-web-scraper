import bcrypt from "bcrypt";
import { Request, Response, NextFunction } from "express";
import jwt, { JsonWebTokenError } from "jsonwebtoken";
import { CustomError, error } from "./errorHandler";
import { getUserById, getUserByUsername } from "@/repository/user";

export const signIn = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  const { username, password } = req.body;

  if (!username || !password) {
    throw error("Missing username or password", 400);
  }

  const user = await getUserByUsername(username);
  if (!user) {
    throw error("Invalid username or password", 401);
  }

  const isMatch = await bcrypt.compare(password, user.password || "");
  if (!isMatch) {
    throw error("Invalid username or password", 401);
  }

  const token = jwt.sign(
    { id: user.id },
    process.env.JWT_SECRET || "family-tree-secret"
  );

  req.user = user;
  req.token = token;

  next();
};

export const authenticate = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  try {
    const token = req.headers["authorization"]?.split(" ")[1];
    if (!token) {
      throw error("No token provided", 401);
    }

    const decoded = jwt.verify(
      token,
      process.env.JWT_SECRET || "family-tree-secret"
    );
    if (!decoded || typeof decoded !== "object" || !("id" in decoded)) {
      throw error("Invalid token", 401);
    }

    const user = await getUserById((decoded as jwt.JwtPayload).id);
    if (!user) {
      throw error("User not found", 401);
    }

    req.user = user;

    next();
  } catch (error) {
    let err: CustomError =
      error instanceof JsonWebTokenError
        ? (error as CustomError)
        : Object.assign(new Error("Unknown error"), { statusCode: 401 });
    err.statusCode = 401;

    next(err);
  }
};
