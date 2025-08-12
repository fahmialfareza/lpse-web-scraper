import { NextFunction, Request, Response } from "express";
import newrelic from "newrelic";
import { z } from "zod";
import { responseSuccess } from "@/utils/response";
import { error } from "@/middlewares/errorHandler";
import { getData, clearData } from "@/service/analyze";

const getDataQuerySchema = z
  .object({
    data_type: z.enum(["tender"]).optional(),
    tender_type: z
      .enum([
        "Pengadaan Barang",
        "Pekerjaan Konstruksi",
        "Jasa Konsultansi Badan Usaha Non Konstruksi",
        "Jasa Konsultansi Badan Usaha Konstruksi",
        "Jasa Konsultansi Perorangan Non Konstruksi",
        "Jasa Konsultansi Perorangan Konstruksi",
        "Jasa Lainnya",
        "Pekerjaan Konstruksi Terintegrasi",
      ])
      .optional(),
    phase: z
      .enum([
        "Tender Gagal",
        "Tender Sudah Selesai",
        "Seleksi Gagal",
        "Masa Sanggah",
      ])
      .optional(),
    start_year: z.coerce.number().min(2000).max(2100).optional(),
    end_year: z.coerce.number().min(2000).max(2100).optional(),
    visualize_tender_type: z
      .enum(["Jumlah Tender", "Total Harga Penawaran"])
      .optional(),
    top: z.coerce.number().min(1).optional(),
  })
  .optional();

export const getAnalyzeData = async (
  req: Request<{}, {}, {}, z.infer<typeof getDataQuerySchema>>,
  res: Response,
  next: NextFunction
) => {
  return newrelic.startSegment(
    "controller.analyze.getAnalyzeData",
    true,
    async () => {
      const parsedQuery = getDataQuerySchema.safeParse(req.query);
      if (!parsedQuery.success) {
        throw error(parsedQuery.error.message, 400);
      }

      const data = await getData(parsedQuery.data ?? {});
      return responseSuccess(res, data);
    }
  );
};

export const removeData = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  return newrelic.startSegment(
    "controller.analyze.removeData",
    true,
    async () => {
      const data = await clearData();
      return responseSuccess(res, data);
    }
  );
};
