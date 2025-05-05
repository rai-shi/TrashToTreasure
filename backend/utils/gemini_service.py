"""Gemini API service for generating project roadmaps."""
import json
import base64
import asyncio
from typing import List, Dict, Optional
from utils.geminiConnection import get_gemini_model
import google.generativeai as genai

class GeminiService:
    def __init__(self):
        self.model = get_gemini_model()

    async def _call_gemini_with_retry(self, prompt: str, image_part: Dict, max_retries: int = 3, delay: float = 1.0) -> Optional[str]:
        """Call Gemini API with retry logic."""
        for attempt in range(max_retries):
            try:
                response = await self.model.generate_content(
                    [prompt, image_part],
                    generation_config={
                        "temperature": 0.2,
                        "max_output_tokens": 4096
                    }
                )
                if response and response.text:
                    return response.text.strip()
                print(f"[WARN] Empty response from Gemini API on attempt {attempt + 1}")
            except Exception as e:
                print(f"[ERROR] Gemini API call failed on attempt {attempt + 1}: {str(e)}")
            if attempt < max_retries - 1:
                await asyncio.sleep(delay * (2 ** attempt))  # Exponential backoff
        return None

    def _clean_json_text(self, text: str) -> str:
        """Clean and prepare text for JSON parsing."""
        # Remove markdown code blocks
        if '```' in text:
            parts = text.split('```')
            if len(parts) > 1:
                # Take the content between first ``` pair
                text = parts[1].strip()
                if text.startswith('json'):
                    text = text[4:].strip()

        # Basic cleanup
        text = text.strip('`').strip()
        text = text.replace('\'', '"')
        text = text.replace('None', 'null')
        text = text.replace('True', 'true')
        text = text.replace('False', 'false')

        # Ensure we have a JSON array
        if '[' in text and ']' in text:
            start = text.find('[')
            end = text.rfind(']') + 1
            text = text[start:end]

        return text

    async def generate_roadmap(self, image_data: bytes, project_name: str, description: str) -> List[Dict]:
        """Generate a step-by-step roadmap for the upcycling project."""
        print(f"[DEBUG] Starting roadmap generation for project: {project_name}")
        
        try:
            # Convert binary image to base64 for Gemini API
            image_b64 = base64.b64encode(image_data).decode('utf-8')
            
            # Create the image part for the Gemini API
            image_part = {
                "mime_type": "image/jpeg",
                "data": image_b64
            }
            
            prompt = f"""Analyze this image and create a step-by-step roadmap for the project: {project_name} - {description}.

IMPORTANT: Your response must be ONLY a JSON array in the following format, with NO additional text or formatting:

[{{
    "step_number": 1,
    "title": "First step title",
    "description": "Detailed description of what needs to be done",
    "estimated_time": "30 minutes",
    "materials_needed": ["item1", "item2"]
}}]

Each step MUST have these fields:
- step_number (number)
- title (text)
- description (text)
- estimated_time (text)
- materials_needed (array of strings)

Provide 3-7 detailed steps that clearly explain how to complete this upcycling project.
Be specific about materials and time estimates.
Ensure the steps are in logical order.

Return ONLY the JSON array with NO additional text.

            ÖNEMLİ: Yanıtını SADECE aşağıdaki formatta JSON dizisi olarak ver, başka hiçbir metin veya biçimlendirme ekleme:

            [
                {{
                    "step_number": 1,
                    "title": "Malzemeleri Hazırla",
                    "description": "Projenin tüm malzemelerini topla",
                    "estimated_time": "30 dakika",
                    "materials_needed": ["makas", "tutkal", "boya"]
                }},
                {{
                    "step_number": 2,
                    "title": "İkinci Adım",
                    "description": "İkinci adımın açıklaması",
                    "estimated_time": "45 dakika",
                    "materials_needed": ["malzeme1", "malzeme2"]
                }}
            ]

            Her adımda şu alanlar MUTLAKA olmalı:
            - step_number (sayı)
            - title (metin)
            - description (metin)
            - estimated_time (metin)
            - materials_needed (metin dizisi)

            Lütfen SADECE JSON dizisini döndür, başka hiçbir şey ekleme.
            """

            print("[DEBUG] Generated prompt:")
            print(prompt)

            print("[DEBUG] Sending request to Gemini API...")
            # Create the Gemini API request with the image and prompt
            print("[DEBUG] Calling Gemini API with retry logic...")
            response_text = await self._call_gemini_with_retry(prompt, image_part)
            
            if not response_text:
                print("[ERROR] Failed to get valid response from Gemini API after retries")
                raise ValueError("Failed to get valid response from Gemini API")
                
            print("[DEBUG] Raw response from Gemini API:")
            print("----------------------------------------")
            print(response_text)
            print("----------------------------------------")
            
            # Function to validate step format
            def validate_step(step: Dict) -> Dict:
                required_fields = {
                    "step_number": int,
                    "title": str,
                    "description": str,
                    "estimated_time": str,
                    "materials_needed": list
                }
                
                for field, field_type in required_fields.items():
                    if field not in step:
                        print(f"[ERROR] Missing required field: {field}")
                        raise ValueError(f"Missing required field: {field}")
                    if not isinstance(step[field], field_type):
                        print(f"[ERROR] Invalid type for {field}: expected {field_type}, got {type(step[field])}")
                        raise ValueError(f"Invalid type for {field}")
                
                # Ensure materials_needed contains only strings
                if not all(isinstance(m, str) for m in step["materials_needed"]):
                    print("[ERROR] materials_needed must contain only strings")
                    raise ValueError("materials_needed must contain only strings")
                    
                return step
            
            try:
                # Clean and parse the response
                clean_text = self._clean_json_text(response_text)
                print("[DEBUG] Cleaned response text:")
                print(clean_text)
                
                # JSON parse etmeyi dene
                try:
                    steps = json.loads(clean_text)
                except json.JSONDecodeError as je:
                    print(f"[ERROR] JSON parse error: {str(je)}")
                    # Alternatif temizleme dene
                    if '[' in clean_text and ']' in clean_text:
                        clean_text = clean_text[clean_text.find('['):clean_text.rfind(']')+1]
                        steps = json.loads(clean_text)
                    else:
                        raise
                
                if not isinstance(steps, list):
                    raise ValueError("Yanıt bir liste değil")
                    
                print("[DEBUG] Successfully parsed JSON response")
                print(f"[DEBUG] Number of steps: {len(steps)}")
                
            except Exception as e:
                print(f"[ERROR] Gemini yanıtı işlenemedi: {str(e)}")
                print(f"[DEBUG] Ham yanıt: {response_text}")
                # Basit bir yol haritası döndür
                return [
                    {
                        "step_number": 1,
                        "title": "Projeyi Planla",
                        "description": "Detaylı yol haritası oluşturulamadı. Lütfen projenizi planlamaya başlayın.",
                        "estimated_time": "1 saat",
                        "materials_needed": ["kağıt", "kalem"]
                    }
                ]
            
            # Validate and clean up each step
            print("[DEBUG] Validating and cleaning up steps...")
            validated_steps = []
            for i, step in enumerate(steps):
                try:
                    # Ensure step_number is correct
                    step["step_number"] = i + 1
                    validated_step = validate_step(step)
                    validated_steps.append(validated_step)
                except Exception as e:
                    print(f"[ERROR] Invalid step format at index {i}: {str(e)}")
                    raise ValueError(f"Invalid step format at index {i}: {str(e)}")
            
            print(f"[DEBUG] Successfully generated roadmap with {len(validated_steps)} steps")
            return validated_steps
            
        except Exception as e:
            print(f"[ERROR] Failed to generate roadmap: {str(e)}")
            # Return a simple fallback roadmap in case of error
            return [
                {
                    "step_number": 1,
                    "title": "Plan Your Project",
                    "description": f"Error generating detailed roadmap: {str(e)}. Start by planning your approach.",
                    "estimated_time": "1 hour",
                    "materials_needed": ["paper", "pencil"]
                },
                {
                    "step_number": 2,
                    "title": "Gather Materials",
                    "description": "Collect all needed materials based on your plan.",
                    "estimated_time": "varies",
                    "materials_needed": []
                }
            ]
