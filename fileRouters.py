from fastapi.responses import StreamingResponse
import io
from bson import ObjectId
from fastapi import HTTPException

async def download_file(file_id: str, fs):
    """Download a file from MongoDB GridFS"""
    try:
        file_id_obj = ObjectId(file_id)

        # Open the file stream for downloading
        file_stream = await fs.open_download_stream(file_id_obj)
        
        # Read the file data
        file_data = await file_stream.read()
        
        # Get the file metadata
        filename = file_stream.filename if hasattr(file_stream, "filename") else "downloaded_file"

        return StreamingResponse(io.BytesIO(file_data), 
                                 media_type="application/octet-stream",
                                 headers={"Content-Disposition": f"attachment; filename={filename}"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def delete_file(file_id: str, fs, db):
    """Delete a file from MongoDB GridFS"""
    try:
        file_id_obj = ObjectId(file_id)

        # Check if file exists in fs.files before deletion
        file_exists = await db["fs.files"].find_one({"_id": file_id_obj})
        if not file_exists:
            raise HTTPException(status_code=404, detail="File not found")

        # Delete the file from GridFS
        await fs.delete(file_id_obj)
        return {"message": "File deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))