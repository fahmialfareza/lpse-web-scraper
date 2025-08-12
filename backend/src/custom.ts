import { IUser } from "./db/schema";

declare global {
  namespace Express {
    interface Response {
      success: (data: any, status: number, message?: string) => this;
    }

    interface Request {
      user?: IUser;
      token?: string;
    }
  }
}
