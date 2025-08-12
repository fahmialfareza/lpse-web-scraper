import {
  AnalyzeParams,
  deleteAnalyzeDataImage,
  fetchAnalyzeData,
} from "@/repository/analyze";

export async function getData(params: AnalyzeParams) {
  return fetchAnalyzeData(params);
}

export async function clearData() {
  return deleteAnalyzeDataImage();
}
