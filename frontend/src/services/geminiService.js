import axios from 'axios';

const GEMINI_API_KEY = process.env.REACT_APP_GEMINI_API_KEY;
const GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent';

// API key kontrolü ekleyelim
if (!GEMINI_API_KEY) {
  console.error('Gemini API anahtarı bulunamadı. Lütfen .env dosyasını kontrol edin.');
}

const geminiService = {
  /**
   * Generate a roadmap using Gemini Vision API
   * @param {File} imageFile - The image file to analyze
   * @param {string} projectName - Name of the project
   * @param {string} description - Description of the project
   */
  generateRoadmap: async (imageFile, projectName, description) => {
    try {
      // Convert image to base64
      const imageBase64 = await new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
          // Get base64 string without data URL prefix
          const base64String = reader.result.split(',')[1];
          resolve(base64String);
        };
        reader.onerror = reject;
        reader.readAsDataURL(imageFile);
      });

      const prompt = `Analyze this image and create a step-by-step roadmap for the project: ${projectName} - ${description}.

IMPORTANT: Your response must be ONLY a JSON array in the following format, with NO additional text or formatting:

[{
    "step_number": 1,
    "title": "First step title",
    "description": "Detailed description of what needs to be done",
    "estimated_time": "30 minutes",
    "materials_needed": ["item1", "item2"]
}]

Each step MUST have these fields:
- step_number (number)
- title (text)
- description (text)
- estimated_time (text)
- materials_needed (array of strings)

Provide 3-7 detailed steps that clearly explain how to complete this upcycling project.
Be specific about materials and time estimates.
Ensure the steps are in logical order.

Return ONLY the JSON array with NO additional text.`;

      const response = await axios.post(
        `${GEMINI_API_URL}?key=${GEMINI_API_KEY}`,
        {
          contents: [
            {
              parts: [
                { text: prompt },
                {
                  inlineData: {
                    mimeType: 'image/jpeg',
                    data: imageBase64
                  }
                }
              ]
            }
          ]
        }
      );

      // Parse and validate the response
      const candidates = response.data.candidates;
      if (!candidates || candidates.length === 0) {
        throw new Error('No response from Gemini API');
      }

      const content = candidates[0].content;
      if (!content || !content.parts || content.parts.length === 0) {
        throw new Error('Invalid response format from Gemini API');
      }

      const text = content.parts[0].text;
      if (!text) {
        throw new Error('Empty response from Gemini API');
      }

      // Clean up the response text to get just the JSON array
      let jsonText = text;
      if (text.includes('[') && text.includes(']')) {
        jsonText = text.substring(text.indexOf('['), text.lastIndexOf(']') + 1);
      }

      // Parse the JSON
      const steps = JSON.parse(jsonText);
      if (!Array.isArray(steps)) {
        throw new Error('Invalid roadmap format');
      }

      // Validate and clean up each step
      return steps.map((step, index) => ({
        step_number: index + 1,
        title: step.title || `Step ${index + 1}`,
        description: step.description || 'No description available',
        estimated_time: step.estimated_time || 'Time not specified',
        materials_needed: Array.isArray(step.materials_needed) ? step.materials_needed : []
      }));

    } catch (error) {
      console.error('Error generating roadmap:', error);
      throw new Error(error.response?.data?.error?.message || error.message || 'Failed to generate roadmap');
    }
  }
};

export default geminiService; 