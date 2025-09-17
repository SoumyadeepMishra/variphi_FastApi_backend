#!/usr/bin/env python3

try:
    print("Testing imports...")
    
    from app.main import app
    print("✓ Successfully imported app.main")
    
    from app.routes import auth_route, user_route, post_route
    print("✓ Successfully imported all routes")
    
    from app.services.auth_service import AuthService
    print("✓ Successfully imported AuthService")
    
    from app.core.auth import get_current_user
    print("✓ Successfully imported get_current_user")
    
    from app.core.roles import role_required
    print("✓ Successfully imported role_required")
    
    print("All imports successful!")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()