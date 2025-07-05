from flask import Flask, jsonify, request
from flask_cors import CORS
from cloudinary.utils import api_sign_request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import time
import os
import logging
import hashlib
import hmac

# Load environment variables
load_dotenv()

# Setup Flask app
app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiter (prevent spam/abuse)
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["20 per minute"],
    storage_uri="memory://"
)

# Allowed CORS origins
allowed_origins = [
    "https://astrakshaya.in",
    "https://tarqgaur.github.io",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:5000"
]

cors_config = {
    "origins": allowed_origins,
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}
CORS(app, resources={r"/*": cors_config})

# Load Cloudinary config from env
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
FRONTEND_SECRET = os.getenv("FRONTEND_SECRET", "skyhack_2024_secret")

# Validate required environment variables
if not all([CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET]):
    logger.error("Missing required Cloudinary environment variables")
    raise ValueError("Missing Cloudinary configuration")

@app.route("/generate-signature", methods=["POST", "OPTIONS"])
@limiter.limit("10 per minute")
def generate_signature():
    """Generate signed upload signature for Cloudinary"""
    if request.method == "OPTIONS":
        return "", 200

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Optional frontend auth check
        if data.get("frontend_secret") != FRONTEND_SECRET:
            logger.warning(f"Unauthorized signature request from {request.remote_addr}")
            return jsonify({"error": "Unauthorized"}), 403

        user_uid = data.get("user_uid", "").strip()
        user_name = data.get("user_name", "").strip()

        if not user_uid:
            return jsonify({"error": "user_uid is required"}), 400

        # Generate timestamp
        timestamp = int(time.time())
        
        # Create upload folder structure
        folder_path = f"skyhack_volunteers/{user_uid}"
        
        # Parameters to sign for volunteer portfolio uploads
        params_to_sign = {
            "timestamp": timestamp,
            "upload_preset": "signed_upload",
            "folder": folder_path,
            "context": f"user_uid={user_uid}|user_name={user_name}|type=volunteer_portfolio",
            "tags": f"skyhack,volunteer,portfolio,{user_uid}",
            "resource_type": "auto",  # Auto-detect file type (image/video/raw)
            "allowed_formats": "jpg,jpeg,png,gif,mp4,mov,pdf,doc,docx"
        }

        # Generate signature
        signature = api_sign_request(params_to_sign, CLOUDINARY_API_SECRET)

        logger.info(f"Generated signature for volunteer: {user_uid} ({user_name})")

        return jsonify({
            "signature": signature,
            "timestamp": timestamp,
            "cloud_name": CLOUDINARY_CLOUD_NAME,
            "api_key": CLOUDINARY_API_KEY,
            "upload_preset": "signed_upload",
            "folder": folder_path,
            "context": params_to_sign["context"],
            "tags": params_to_sign["tags"],
            "resource_type": "auto",
            "allowed_formats": params_to_sign["allowed_formats"]
        }), 200

    except Exception as e:
        logger.error(f"Error generating signature: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/webhook/upload-complete", methods=["POST"])
@limiter.limit("100 per minute")
def upload_complete_webhook():
    """Handle Cloudinary upload completion webhook"""
    try:
        # Verify webhook signature (optional but recommended)
        signature = request.headers.get('X-Cld-Signature')
        timestamp = request.headers.get('X-Cld-Timestamp')
        
        if signature and timestamp:
            # Verify the webhook is from Cloudinary
            expected_signature = hmac.new(
                CLOUDINARY_API_SECRET.encode('utf-8'),
                f"{timestamp}{request.get_data().decode('utf-8')}".encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            if signature != expected_signature:
                logger.warning("Invalid webhook signature")
                return jsonify({"error": "Invalid signature"}), 403

        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400

        # Log successful upload
        public_id = data.get('public_id')
        resource_type = data.get('resource_type')
        user_context = data.get('context', {})
        
        logger.info(f"Upload completed: {public_id} (type: {resource_type})")
        logger.info(f"User context: {user_context}")
        
        # Here you could:
        # 1. Update database with upload info
        # 2. Send notification to user
        # 3. Process the uploaded file
        # 4. Generate thumbnails for videos
        
        return jsonify({"status": "success"}), 200

    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return jsonify({"error": "Webhook processing failed"}), 500


@app.route("/volunteer/<user_uid>/uploads", methods=["GET"])
@limiter.limit("30 per minute")
def get_volunteer_uploads(user_uid):
    """Get all uploads for a specific volunteer"""
    try:
        # This would typically query your database
        # For now, returning a placeholder response
        
        # You could also query Cloudinary API to get files by tag
        # import cloudinary.api
        # files = cloudinary.api.resources(
        #     type="upload",
        #     prefix=f"skyhack_volunteers/{user_uid}",
        #     tags=f"skyhack,volunteer,{user_uid}"
        # )
        
        return jsonify({
            "user_uid": user_uid,
            "uploads": [],
            "message": "Upload history feature coming soon"
        }), 200

    except Exception as e:
        logger.error(f"Error fetching uploads for {user_uid}: {str(e)}")
        return jsonify({"error": "Failed to fetch uploads"}), 500


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "timestamp": int(time.time()),
        "cloudinary_configured": bool(CLOUDINARY_CLOUD_NAME)
    }), 200


@app.route("/", methods=["GET"])
def index():
    """Root endpoint"""
    return jsonify({
        "message": "SkyHack Volunteer Backend API",
        "version": "1.0.0",
        "endpoints": {
            "generate_signature": "/generate-signature",
            "webhook": "/webhook/upload-complete",
            "health": "/health"
        }
    }), 200


@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit exceeded"""
    return jsonify({
        "error": "Rate limit exceeded",
        "message": "Too many requests. Please try again later."
    }), 429


@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors"""
    logger.error(f"Internal server error: {str(e)}")
    return jsonify({
        "error": "Internal server error",
        "message": "Something went wrong. Please try again."
    }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"
    
    logger.info(f"Starting SkyHack Backend on port {port}")
    logger.info(f"Debug mode: {debug}")
    logger.info(f"Cloudinary Cloud: {CLOUDINARY_CLOUD_NAME}")
    
    app.run(host="0.0.0.0", port=port, debug=debug)