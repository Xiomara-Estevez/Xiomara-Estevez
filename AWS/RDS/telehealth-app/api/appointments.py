from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from config.database import db

# Create the blueprint - THIS LINE WAS MISSING
appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/book', methods=['POST'])
@jwt_required()
def book_appointment():
    """Book a new appointment"""
    from flask import Blueprint, request, jsonify

    # Guard the optional dependency on flask_jwt_extended so importing this
    # module doesn't fail in environments where it's not installed.
    try:
        from flask_jwt_extended import jwt_required, get_jwt_identity  # type: ignore
    except Exception:
        # Provide no-op fallbacks so the blueprint remains importable during dev.
        def jwt_required(*_args, **_kwargs):
            def _decorator(f):
                return f

            return _decorator

        def get_jwt_identity():
            return None

    from config.database import db

    # Create the blueprint
    appointments_bp = Blueprint("appointments", __name__)


    @appointments_bp.route("/book", methods=["POST"])
    @jwt_required()
    def book_appointment():
        """Simple appointment booking endpoint (stub)."""
        try:
            user_id = get_jwt_identity()
            data = request.get_json(silent=True) or {}

            # In the current app this blueprint is a lightweight stub.
            # It intentionally does not depend on the app's demo token store.
            return jsonify({"success": True, "message": "Booking works!", "user_id": user_id, "payload": data}), 200

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500