from bson import ObjectId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from helpers.converters import convert_objectid

def serialize_order(order):
    """Convert ObjectId to string in an order document"""
    if order:
        order["_id"] = str(order["_id"])
    return order


async def fetch_orders(db):
    orders_collection = db["orders"]
    orders = []
    async for order in orders_collection.find():
        orders.append(order)
    return orders

async def get_order_by_id(db, order_id):
    orders_collection = db["orders"]
    order = await orders_collection.find_one({"_id": ObjectId(order_id)})
    if order:
        return {"success": True, "data": convert_objectid(order)}
    return {"success": False, "message": "Order not found"}

async def delete_order(db, order_id):
    orders_collection = db["orders"]
    result = await orders_collection.delete_one({"_id": ObjectId(order_id)})
    if result.deleted_count:
        return {"success": True, "message": "Order deleted successfully"}
    return {"success": False, "message": "Order not found"}
