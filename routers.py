from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Service is running"}


@router.get("/search")
async def search(query: str):
    return {"results": f"Search results for: {query}"}


@router.get("/health")
async def health_check():
    return {"status": "healthy"}
