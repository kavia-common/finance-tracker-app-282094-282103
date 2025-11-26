from src.core.db import Base  # re-export Base for model modules

# Ensure model modules are importable when package is imported
# These imports are not strictly necessary here but documented for clarity:
# from .user import User
# from .transaction import Transaction

__all__ = ["Base"]
