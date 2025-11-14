from flask import jsonify

def success_response(message:str, data=None):
    """
    Generic success response GET, PUT/PATCH and DELETE.
    """
    return jsonify ({
        "success": True,
        "message": message,
        "data": data
    }), 200

def not_found(entity:str = "Resource"):
    """
    Generate a standard 404 JSON response
    """
    return jsonify({
        "success": False,
        "message": f"{entity} not found"
    }), 404