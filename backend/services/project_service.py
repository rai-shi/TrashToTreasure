"""Service for handling project and roadmap operations."""
import json
import base64
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from utils.models import Project, RoadmapStep, User
from utils.gemini_service import GeminiService
import os
import uuid

class ProjectService:
    def __init__(self, db: Session):
        self.db = db
        self.gemini_service = GeminiService()
        
    def _save_image(self, image_data: bytes) -> str:
        """Save image to disk and return the filename."""
        print("[DEBUG] Starting image save process...")
        try:
            # Create uploads directory if it doesn't exist
            upload_dir = "static/uploads"
            os.makedirs(upload_dir, exist_ok=True)
            
            # Generate unique filename
            filename = f"{uuid.uuid4()}.jpg"
            filepath = f"{upload_dir}/{filename}"
            
            print(f"[DEBUG] Saving image to {filepath}")
            # Save file
            with open(filepath, "wb") as f:
                f.write(image_data)
                
            print("[DEBUG] Image saved successfully")
            return filepath  # Return path relative to the application root
            
        except Exception as e:
            print(f"[ERROR] Failed to save image: {str(e)}")
            raise ValueError(f"Failed to save image: {str(e)}")

    async def create_project_with_roadmap(
        self, 
        user_id: int,
        name: str,
        description: str,
        image_data: bytes
    ) -> Project:
        """Create a new project and generate its roadmap."""
        print(f"[DEBUG] Starting project creation for user {user_id}...")
        try:
            # Validate input parameters
            if not user_id or not isinstance(user_id, int):
                raise ValueError("Invalid user_id")
            if not name or not isinstance(name, str):
                raise ValueError("Invalid project name")
            if not description or not isinstance(description, str):
                raise ValueError("Invalid project description")
            if not image_data or not isinstance(image_data, bytes):
                raise ValueError("Invalid image data")
                
            # Save image to disk
            print("[DEBUG] Saving project image...")
            image_path = self._save_image(image_data)
            
            # Create project
            print("[DEBUG] Creating project record...")
            project = Project(
                name=name,
                description=description,
                image=image_path,
                user_id=user_id
            )
            self.db.add(project)
            self.db.flush()  # Get project ID without committing
            print(f"[DEBUG] Project record created with ID: {project.id}")

            # Generate roadmap using Gemini
            print("[DEBUG] Generating project roadmap...")
            roadmap_steps = await self.gemini_service.generate_roadmap(
                image_data=image_data,
                project_name=name,
                description=description
            )

            # Create roadmap steps
            print("[DEBUG] Creating roadmap steps...")
            for step in roadmap_steps:
                try:
                    db_step = RoadmapStep(
                        project_id=project.id,
                        step_number=step["step_number"],
                        title=step["title"],
                        description=step["description"],
                        estimated_time=step["estimated_time"],
                        materials_needed=step["materials_needed"]
                    )
                    self.db.add(db_step)
                except Exception as step_error:
                    print(f"[ERROR] Failed to create roadmap step: {str(step_error)}")
                    raise ValueError(f"Failed to create roadmap step: {str(step_error)}")

            print("[DEBUG] Committing transaction...")
            self.db.commit()
            print(f"[DEBUG] Project creation completed successfully. Project ID: {project.id}")
            return project

        except Exception as e:
            print(f"[ERROR] Project creation failed: {str(e)}")
            self.db.rollback()
            raise ValueError(f"Project creation failed: {str(e)}")

    def get_project_roadmap(self, project_id: int) -> List[Dict]:
        """Get the roadmap steps for a project."""
        steps = (
            self.db.query(RoadmapStep)
            .filter(RoadmapStep.project_id == project_id)
            .order_by(RoadmapStep.step_number)
            .all()
        )
        
        return [
            {
                "id": step.id,
                "step_number": step.step_number,
                "title": step.title,
                "description": step.description,
                "estimated_time": step.estimated_time,
                "materials_needed": step.materials_needed
            }
            for step in steps
        ]
    
    def get_user_projects(self, user_id: int) -> List[Dict]:
        """Get all projects for a user."""
        projects = (
            self.db.query(Project)
            .filter(Project.user_id == user_id)
            .order_by(Project.created_at.desc())
            .all()
        )
        
        return [
            {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "image": project.image
            }
            for project in projects
        ]
        
    def get_project_details(self, project_id: int) -> Optional[Dict]:
        """Get details for a specific project."""
        project = (
            self.db.query(Project)
            .filter(Project.id == project_id)
            .first()
        )
        
        if not project:
            return None
            
        # Get the roadmap steps
        steps = self.get_project_roadmap(project_id)
        
        # Get the user (owner)
        user = self.db.query(User).filter(User.id == project.user_id).first()
        
        return {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "image": project.image,
            "user_id": project.user_id,
            "created_at": project.created_at.isoformat(),
            "updated_at": project.updated_at.isoformat(),
            "done": project.done,
            "is_public": project.is_public,
            "roadmap": steps,
            "user": {
                "username": user.username if user else None,
                "id": user.id if user else None
            }
        }
