from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from fastapi.encoders import jsonable_encoder

async def add_user(db, user_data):
    """Add a new user to the database"""
    user_data["ispaid"] = False  # Default value
    result = await db.users.insert_one(user_data)
    return {"success": True, "user_id": str(result.inserted_id)}

async def edit_user(db, user_id, update_data):
    """Edit user details"""
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    return {"success": True, "message": "User updated successfully"}

async def delete_user(db, user_id):
    """Delete a user from the database"""
    result = await db.users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"success": True, "message": "User deleted successfully"}

async def payment_completed(db, user_id):
    """Mark a user’s payment as completed"""
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"ispaid": True}})
    return {"success": True, "message": "Payment status updated to paid"}

async def get_all_users(db):
    """Fetch all users along with their order details"""
    users = await db.users.find().to_list(None)
    
    for user in users:
        # Convert ObjectId to string
        user["_id"] = str(user["_id"])
        user["orderId"] = str(user["orderId"]) if "orderId" in user and user["orderId"] else None
        
        # Handle order retrieval
        order_id = user.get("orderId")
        order_object_id = ObjectId(order_id) if order_id and ObjectId.is_valid(order_id) else None
        
        # Fetch the order if valid orderId exists
        if order_object_id:
            order = await db.orders.find_one({"_id": order_object_id})
            if order:
                # Convert ObjectId fields in order to strings
                order["_id"] = str(order["_id"])
                order["file_id"] = str(order["file_id"]) if "file_id" in order else None
                user["order"] = order
            else:
                user["order"] = {}
        else:
            user["order"] = {}

    return jsonable_encoder({"success": True, "users": users})



async def get_one_user(db, user_id):
    """Fetch a single user along with their order details"""
    # Fetch the user from the database
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Convert ObjectId fields in user to strings
    user["_id"] = str(user["_id"])
    user["orderId"] = str(user["orderId"]) if "orderId" in user else None

    # Extract and validate orderId
    order_id = user.get("orderId")
    order_object_id = ObjectId(order_id) if order_id and ObjectId.is_valid(order_id) else None

    # Fetch the order if a valid order ID exists
    order = await db.orders.find_one({"_id": order_object_id}) if order_object_id else None

    # Convert all ObjectId fields in the order to strings
    if order:
        order["_id"] = str(order["_id"])
        order["file_id"] = str(order["file_id"]) if "file_id" in order else None

    user["order"] = order if order else {}

    return jsonable_encoder({"success": True, "user": user})
