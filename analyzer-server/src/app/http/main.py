from fastapi import APIRouter
from analyzer.main import run_analyzer
from fastapi import Query

router = APIRouter()


@router.get("/analyze")
async def analyze(
    data_type: str = Query("tender"),
    tender_type: str = Query(None),
    phase: str = Query(None),
    start_year: int = Query(None),
    end_year: int = Query(None),
    visualize_tender_type: str = Query("Jumlah Tender"),
    top: int = Query(10),
):
    analyzer = run_analyzer(
        data_type=data_type,
        tender_type=tender_type,
        phase=phase,
        start_year=start_year,
        end_year=end_year,
        visualize_tender_type=visualize_tender_type,
        top=top,
    )
    if isinstance(analyzer, str) and analyzer.startswith(
        "/Users/fahmialfareza/Code/mas-arif-project/lpse-web-scraper/tmp/"
    ):
        filename = analyzer.split("/")[-1]
        analyzer = f"/public/{filename}"

    return {"data": analyzer, "status": "ok"}
