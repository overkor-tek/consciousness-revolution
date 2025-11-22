"""
DEPLOYMENT PACKAGER - Deployment Configuration Generator
=========================================================
Generates deployment configurations for various platforms.

Supports: Railway, Netlify, Vercel, Docker, AWS

Created: 2025-11-22
Trinity Build: Phase 2
"""

from datetime import datetime
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class DeploymentConfig:
    """Deployment configuration"""
    platform: str
    files: Dict[str, str]  # filename -> content
    commands: List[str]
    environment_vars: List[str]

class DeploymentPackager:
    """
    Generates deployment configurations for multiple platforms.
    """

    def __init__(self):
        self.package_count = 0

    def package_for_railway(self, spec: Dict[str, Any]) -> DeploymentConfig:
        """Generate Railway deployment config."""
        app_name = spec.get("name", "app")

        files = {
            "railway.toml": f'''[build]
builder = "nixpacks"

[deploy]
startCommand = "python app.py"
healthcheckPath = "/health"
healthcheckTimeout = 100
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 10
''',
            "Procfile": "web: python app.py"
        }

        commands = [
            "railway login",
            f"railway init --name {app_name}",
            "railway up --detach"
        ]

        env_vars = [
            "FLASK_ENV=production",
            "PORT=${{PORT}}"
        ]

        return DeploymentConfig(
            platform="railway",
            files=files,
            commands=commands,
            environment_vars=env_vars
        )

    def package_for_netlify(self, spec: Dict[str, Any]) -> DeploymentConfig:
        """Generate Netlify deployment config."""
        app_name = spec.get("name", "app")

        files = {
            "netlify.toml": f'''[build]
  command = "npm run build"
  publish = "build"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
''',
            "_redirects": "/*    /index.html   200"
        }

        commands = [
            "npm run build",
            f"netlify deploy --prod --site {app_name}"
        ]

        env_vars = [
            "NODE_ENV=production",
            "REACT_APP_API_URL=/.netlify/functions"
        ]

        return DeploymentConfig(
            platform="netlify",
            files=files,
            commands=commands,
            environment_vars=env_vars
        )

    def package_for_vercel(self, spec: Dict[str, Any]) -> DeploymentConfig:
        """Generate Vercel deployment config."""
        app_name = spec.get("name", "app")

        files = {
            "vercel.json": f'''{{
  "version": 2,
  "name": "{app_name}",
  "builds": [
    {{
      "src": "app.py",
      "use": "@vercel/python"
    }}
  ],
  "routes": [
    {{
      "src": "/(.*)",
      "dest": "app.py"
    }}
  ]
}}'''
        }

        commands = [
            "vercel login",
            "vercel --prod"
        ]

        env_vars = [
            "VERCEL_ENV=production"
        ]

        return DeploymentConfig(
            platform="vercel",
            files=files,
            commands=commands,
            environment_vars=env_vars
        )

    def package_for_docker(self, spec: Dict[str, Any]) -> DeploymentConfig:
        """Generate Docker deployment config."""
        app_name = spec.get("name", "app")
        features = spec.get("features", [])

        # Determine base image and port
        port = 5000 if "rest_api" in features or "database" in features else 3000

        dockerfile = f'''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE {port}

CMD ["python", "app.py"]
'''

        compose = f'''version: '3.8'

services:
  {app_name}:
    build: .
    ports:
      - "{port}:{port}"
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
'''

        files = {
            "Dockerfile": dockerfile,
            "docker-compose.yml": compose,
            ".dockerignore": '''__pycache__
*.pyc
.git
.env
node_modules
'''
        }

        commands = [
            f"docker build -t {app_name} .",
            f"docker run -p {port}:{port} {app_name}",
            "# Or use: docker-compose up -d"
        ]

        env_vars = [
            f"PORT={port}",
            "FLASK_ENV=production"
        ]

        return DeploymentConfig(
            platform="docker",
            files=files,
            commands=commands,
            environment_vars=env_vars
        )

    def package_all(self, spec: Dict[str, Any]) -> Dict[str, DeploymentConfig]:
        """
        Generate deployment configs for all platforms.

        Args:
            spec: App specification

        Returns:
            Dictionary of platform -> DeploymentConfig
        """
        self.package_count += 1

        return {
            "railway": self.package_for_railway(spec),
            "netlify": self.package_for_netlify(spec),
            "vercel": self.package_for_vercel(spec),
            "docker": self.package_for_docker(spec)
        }

    def to_dict(self, config: DeploymentConfig) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "platform": config.platform,
            "files": list(config.files.keys()),
            "commands": config.commands,
            "environment_vars": config.environment_vars
        }


# Testing
if __name__ == "__main__":
    packager = DeploymentPackager()

    print("=" * 60)
    print("DEPLOYMENT PACKAGER - TEST")
    print("=" * 60)

    spec = {
        "name": "test_app",
        "features": ["user_authentication", "database", "rest_api"]
    }

    configs = packager.package_all(spec)

    for platform, config in configs.items():
        print(f"\n{platform.upper()}:")
        print(f"  Files: {list(config.files.keys())}")
        print(f"  Commands: {len(config.commands)}")
        print(f"  Env vars: {len(config.environment_vars)}")

    print("\n" + "=" * 60)
    print("DEPLOYMENT PACKAGER OPERATIONAL")
    print("=" * 60)
