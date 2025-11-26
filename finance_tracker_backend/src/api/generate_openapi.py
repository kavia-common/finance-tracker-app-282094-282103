import json
import os

from src.api.main import app

# Generate OpenAPI after all routers are included by importing app above
openapi_schema = app.openapi()

# Save schema to interfaces/openapi.json
output_dir = "interfaces"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "openapi.json")

with open(output_path, "w") as f:
    json.dump(openapi_schema, f, indent=2)
